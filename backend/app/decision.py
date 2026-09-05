from typing import Any

from google import genai

from app.business import customer_risk
from app.config import settings
from app.intelligence import gather_evidence


def customer_decision(customer_id: int) -> dict:
    risk = customer_risk(customer_id)
    if "error" in risk:
        return risk
    reasons = []
    actions = []
    if risk["revenue_drop_percent"] >= 20:
        reasons.append(f"Revenue fell {risk['revenue_drop_percent']}% versus the previous 90-day period.")
        actions.append("Schedule an account review and investigate the revenue decline.")
    if risk["high_priority_tickets"]:
        reasons.append(f"{risk['high_priority_tickets']} high-priority support ticket(s) remain open.")
        actions.append("Escalate unresolved high-priority support issues.")
    if risk["open_tickets"]:
        reasons.append(f"There are {risk['open_tickets']} open support ticket(s).")
    if not reasons:
        reasons.append("No major revenue or support warning signal was detected.")
        actions.append("Continue normal account monitoring.")
    return {
        "customer": risk["customer"],
        "risk": risk,
        "decision": "INTERVENE" if risk["risk_level"] == "HIGH" else "MONITOR",
        "reasons": reasons,
        "recommended_actions": actions,
        "evidence": [
            "sales: trailing 90-day revenue comparison",
            "support_tickets: open and high-priority ticket counts",
            "customers: annual customer value and industry",
        ],
    }


def _fallback(evidence: dict[str, Any], question: str) -> str:
    business = evidence.get("business", {})
    summary = business.get("summary", {})
    risks = business.get("risk_analysis", [])
    customers = business.get("top_customers", [])
    q = question.lower()

    if risks:
        high = [x for x in risks if x.get("risk_level") == "HIGH"]
        if high:
            names = ", ".join(x["customer"] for x in high[:3])
            return f"I found {len(high)} high-risk customer(s): {names}. The strongest signals are declining recent revenue and unresolved support activity."
        return f"I checked {len(risks)} customers and found no HIGH-risk customers in the current dataset."

    if any(x in q for x in ["revenue", "sales", "sale", "highest", "top", "customer"]):
        if customers:
            top = customers[0]
            return f"{top['customer']} is the top customer by recorded revenue at ₹{top['revenue']:,.0f}. I found {len(customers)} ranked customer records in the current evidence."
        return "There are no recorded customer sales in the current dataset."

    if any(x in q for x in ["ticket", "support", "backlog"]):
        open_tickets = summary.get("open_tickets", 0)
        high_priority = summary.get("high_priority_tickets", 0)
        return f"The current support backlog is {open_tickets} open ticket(s), including {high_priority} high-priority ticket(s)."

    if any(x in q for x in ["how many customer", "number of customer", "customer count", "customers"]):
        return f"The database currently contains {summary.get('customers', 0)} customer record(s)."

    if any(x in q for x in ["business health", "overall", "summary", "snapshot"]):
        return (
            f"Current snapshot: {summary.get('customers', 0)} customers, "
            f"₹{summary.get('total_revenue', 0):,.0f} recorded revenue, and "
            f"{summary.get('open_tickets', 0)} open support ticket(s)."
        )

    docs = evidence.get("documents", [])
    if docs:
        return f"I found {len(docs)} relevant document passage(s). Review the evidence shown with the answer before acting."

    return "I can answer questions about the connected customer, sales, support, and indexed document data."


def answer(question: str) -> dict[str, Any]:
    evidence = gather_evidence(question)
    if not settings.llm_api_key:
        return {"answer": _fallback(evidence, question), "evidence": evidence, "confidence": 60}
    client = genai.Client(api_key=settings.llm_api_key)
    prompt = f"""You are Business Signal, an evidence-first business analysis assistant. Answer only from the supplied context. Never invent facts. Give a direct answer first, then key signals and a practical next step when useful. If the context truly cannot answer the question, say exactly what information is missing.

QUESTION:
{question}

CONTEXT:
{evidence}"""
    response = client.models.generate_content(model=settings.llm_model, contents=prompt)
    return {"answer": response.text or "No answer generated.", "evidence": evidence}
