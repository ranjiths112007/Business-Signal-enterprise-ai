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
    return {"customer": risk["customer"], "risk": risk, "decision": "INTERVENE" if risk["risk_level"] == "HIGH" else "MONITOR", "reasons": reasons, "recommended_actions": actions, "evidence": ["sales: trailing 90-day revenue comparison", "support_tickets: open and high-priority ticket counts", "customers: annual customer value and industry"]}


def _fallback(evidence: dict[str, Any]) -> str:
    risks = evidence.get("business", {}).get("risk_analysis", [])
    high = [x for x in risks if x.get("risk_level") == "HIGH"]
    if high:
        return f"Business Signal identified {len(high)} high-risk customers. Review declining revenue and unresolved support activity first."
    docs = evidence.get("documents", [])
    if docs:
        return f"Found {len(docs)} relevant document passages. The evidence should be reviewed before acting."
    return "There is not enough evidence to make a reliable recommendation."


def answer(question: str) -> dict[str, Any]:
    evidence = gather_evidence(question)
    if not settings.llm_api_key:
        return {"answer": _fallback(evidence), "evidence": evidence, "confidence": 60}
    client = genai.Client(api_key=settings.llm_api_key)
    prompt = f"""You are Business Signal, an evidence-first enterprise decision assistant. Answer only from the supplied context. Never invent facts. Clearly separate evidence from recommendation. If evidence is insufficient, say so. Return a direct answer, key signals, recommended action when appropriate, evidence references, and confidence from 0-100.\n\nQUESTION:\n{question}\n\nCONTEXT:\n{evidence}"""
    response = client.models.generate_content(model=settings.llm_model, contents=prompt)
    return {"answer": response.text or "No answer generated.", "evidence": evidence}
