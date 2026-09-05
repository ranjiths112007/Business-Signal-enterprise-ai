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


def _fallback(evidence: dict[str, Any], question: str) -> str:  # noqa: C901
    """Answer from structured evidence when no LLM key is configured."""
    business = evidence.get("business", {})
    summary = business.get("summary", {})
    risks = business.get("risk_analysis", [])
    customers = business.get("top_customers", [])
    support = business.get("support_breakdown", [])
    industry = business.get("industry_summary", [])
    q = question.lower()

    total_customers = summary.get("customers", 0)
    total_revenue = summary.get("total_revenue", 0.0)
    open_tickets = summary.get("open_tickets", 0)
    high_priority = summary.get("high_priority_tickets", 0)

    # ── Risk questions ────────────────────────────────────────────────────────
    if risks and any(x in q for x in ["risk", "churn", "danger", "at risk", "warning", "declining", "intervention", "warning signal"]):
        high_risk = [x for x in risks if x.get("risk_level") == "HIGH"]
        medium_risk = [x for x in risks if x.get("risk_level") == "MEDIUM"]
        if any(x in q for x in ["why", "reason", "signal"]) and high_risk:
            top = high_risk[0]
            return (
                f"{top['customer']} is the highest-risk customer (score {top['risk_score']}/100). "
                f"Revenue dropped {top['revenue_drop_percent']}% vs the prior 90 days, with "
                f"{top['open_tickets']} open support ticket(s) including {top['high_priority_tickets']} high-priority. "
                f"Total high-risk accounts: {len(high_risk)}."
            )
        if high_risk:
            names = ", ".join(x["customer"] for x in high_risk[:5])
            parts = [f"Found {len(high_risk)} HIGH-risk customer(s): {names}."]
            if medium_risk:
                parts.append(f"Also {len(medium_risk)} MEDIUM-risk account(s).")
            parts.append("Key signals: revenue decline vs prior 90 days and unresolved high-priority support tickets.")
            return " ".join(parts)
        return f"Checked {len(risks)} customer(s) — no HIGH-risk accounts detected in the current dataset."

    # ── Total revenue ─────────────────────────────────────────────────────────
    if any(x in q for x in ["total revenue", "total sales", "overall revenue"]):
        return f"Total recorded revenue across all customers is ₹{total_revenue:,.0f}."

    # ── Average sale amount ────────────────────────────────────────────────────
    if any(x in q for x in ["average sale", "avg sale", "mean sale", "average amount"]):
        return (
            f"The total recorded revenue is ₹{total_revenue:,.0f} across {total_customers} customer(s). "
            "Average sale amount is not directly stored; connect an LLM API key for a precise per-transaction average."
        )

    # ── Revenue trend ─────────────────────────────────────────────────────────
    if any(x in q for x in ["trend", "over time", "month", "period"]):
        return (
            f"Total revenue is ₹{total_revenue:,.0f}. "
            "Detailed revenue trends require an LLM API key for time-series analysis. "
            "Risk scores already reflect 90-day vs prior-90-day revenue movement per customer."
        )

    # ── Industry revenue (MUST be before generic 'top'/'most' check) ────────────
    if any(x in q for x in ["industry", "sector", "vertical", "segment"]) and any(x in q for x in ["revenue", "most", "generated", "contribute"]):
        if industry:
            top = industry[0]
            lines = [f"{i+1}. {ind['industry']} — ₹{ind['revenue']:,.0f} ({ind['customers']} customers)" for i, ind in enumerate(industry[:5])]
            return f"Top industry by revenue: {top['industry']} at ₹{top['revenue']:,.0f}.\n\nFull breakdown:\n" + "\n".join(lines)
        return "No industry revenue data found."

    # ── Industry customer count (MUST be before generic customer check) ────────
    if any(x in q for x in ["industry", "industries", "sector", "segment"]) and any(x in q for x in ["customer", "how many", "count", "most customer", "industries"]):
        if industry:
            by_count = sorted(industry, key=lambda x: x["customers"], reverse=True)
            lines = [f"{i+1}. {ind['industry']} — {ind['customers']} customer(s)" for i, ind in enumerate(by_count[:5])]
            return "Industries by customer count:\n" + "\n".join(lines)
        return "No industry data found."

    # ── Top customers by revenue ───────────────────────────────────────────────
    if any(x in q for x in ["top", "highest revenue", "most revenue", "generated the most", "biggest customer", "largest"]):
        if customers:
            lines = [f"{i+1}. {c['customer']} ({c['industry']}) — ₹{c['revenue']:,.0f}" for i, c in enumerate(customers[:5])]
            return f"Top customers by recorded revenue:\n" + "\n".join(lines)
        return "No sales data found."

    # ── Least / lowest revenue ─────────────────────────────────────────────────
    if any(x in q for x in ["least revenue", "lowest revenue", "least", "bottom", "smallest"]):
        if customers:
            bottom = customers[-1]
            return f"{bottom['customer']} ({bottom['industry']}) has the lowest recorded revenue at ₹{bottom['revenue']:,.0f} among ranked customers."
        return "No sales data found."

    # ── Annual value ───────────────────────────────────────────────────────────
    if any(x in q for x in ["annual value", "highest annual", "annual_value"]):
        if customers:
            lines = [f"{i+1}. {c['customer']} ({c['industry']}) — ₹{c['revenue']:,.0f}" for i, c in enumerate(customers[:5])]
            return "Customers ranked by revenue (use annual value field for contract value):\n" + "\n".join(lines)
        return "No customer data found."


    # ── Customer count ─────────────────────────────────────────────────────────
    if any(x in q for x in ["how many customer", "number of customer", "customer count", "many customer", "count of customer"]):
        return f"The database currently contains {total_customers:,} customer record(s)."

    # ── Show / list customers ──────────────────────────────────────────────────
    if any(x in q for x in ["show", "list", "all customer", "customer"]) and any(x in q for x in ["show", "list", "top", "display"]):
        if customers:
            lines = [f"{i+1}. {c['customer']} ({c['industry']}) — ₹{c['revenue']:,.0f}" for i, c in enumerate(customers[:10])]
            return f"Top customers by revenue:\n" + "\n".join(lines)
        return "No customer data found."

    # ── Support: tickets / backlog / load ─────────────────────────────────────
    if any(x in q for x in ["ticket", "support", "backlog", "load", "open"]):
        if any(x in q for x in ["breakdown", "by priority", "by status", "split"]) and support:
            lines = [f"  {s['priority'].capitalize()} / {s['status']} — {s['count']}" for s in support]
            return f"Support ticket breakdown:\n" + "\n".join(lines) + f"\n\nTotal open: {open_tickets}, High-priority: {high_priority}."
        if any(x in q for x in ["high priority", "high-priority", "unresolved"]):
            return f"There are currently {high_priority} high-priority open support ticket(s) out of {open_tickets} total open tickets."
        return f"Current support backlog: {open_tickets} open ticket(s), including {high_priority} high-priority."

    # ── General summary / snapshot ────────────────────────────────────────────
    if any(x in q for x in ["overall", "summary", "snapshot", "business health", "overview"]):
        return (
            f"Business Signal snapshot:\n"
            f"  • Customers: {total_customers:,}\n"
            f"  • Total recorded revenue: ₹{total_revenue:,.0f}\n"
            f"  • Open support tickets: {open_tickets} ({high_priority} high-priority)\n"
            f"  • Top customer: {customers[0]['customer'] if customers else 'N/A'}"
        )

    # ── Generic revenue / sales fallback ─────────────────────────────────────
    if any(x in q for x in ["revenue", "sales", "sale"]):
        if customers:
            top = customers[0]
            return (
                f"Total revenue: ₹{total_revenue:,.0f} across {total_customers:,} customer(s). "
                f"Top earner: {top['customer']} at ₹{top['revenue']:,.0f}."
            )
        return f"Total recorded revenue: ₹{total_revenue:,.0f}."

    # ── Generic customers fallback ────────────────────────────────────────────
    if "customer" in q:
        if customers:
            top = customers[0]
            return f"There are {total_customers:,} customers. Top by revenue: {top['customer']} (₹{top['revenue']:,.0f})."
        return f"There are {total_customers:,} customer records in the database."

    # ── Document / general fallback ────────────────────────────────────────────
    docs = evidence.get("documents", [])
    if docs:
        return f"I found {len(docs)} relevant document passage(s). Review the evidence shown with the answer before acting."

    return (
        f"I have access to {total_customers:,} customers, ₹{total_revenue:,.0f} revenue, "
        f"and {open_tickets} open support tickets. "
        "Ask about customers, revenue, risk, support tickets, or industries."
    )


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
