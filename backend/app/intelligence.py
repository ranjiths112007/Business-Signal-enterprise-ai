from datetime import datetime
from typing import Any

from app.business import customer_risk, top_customers
from app.database import get_connection
from app.retrieval import search_documents


def classify_question(question: str) -> str:
    q = question.lower()
    if any(x in q for x in ["policy", "contract", "document", "refund", "leave", "pdf"]):
        return "document"
    if any(x in q for x in [
        "customer", "revenue", "sales", "sale", "ticket", "support", "risk",
        "churn", "business", "account", "industry", "company", "top", "highest",
        "lowest", "how many", "total", "average", "trend",
    ]):
        return "business"
    return "general"


def build_business_context(question: str) -> dict[str, Any]:
    q = question.lower()
    context: dict[str, Any] = {"generated_at": datetime.utcnow().isoformat() + "Z"}

    with get_connection() as conn:
        context["summary"] = {
            "customers": conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0],
            "total_revenue": float(conn.execute("SELECT COALESCE(SUM(amount), 0) FROM sales").fetchone()[0]),
            "open_tickets": conn.execute("SELECT COUNT(*) FROM support_tickets WHERE status <> 'closed'").fetchone()[0],
            "high_priority_tickets": conn.execute("SELECT COUNT(*) FROM support_tickets WHERE status <> 'closed' AND priority = 'high'").fetchone()[0],
        }

    customers = top_customers(limit=50)
    if any(x in q for x in [
        "top", "highest", "lowest", "revenue", "sales", "sale", "customer",
        "account", "company", "who",
    ]):
        context["top_customers"] = customers[:10]

    if any(x in q for x in ["risk", "churn", "danger", "at risk", "warning"]):
        risks = []
        for customer in customers:
            result = customer_risk(customer["customer_id"])
            if "error" not in result:
                risks.append(result)
        context["risk_analysis"] = risks

    return context


def gather_evidence(question: str) -> dict[str, Any]:
    intent = classify_question(question)
    result: dict[str, Any] = {"intent": intent, "documents": [], "business": {}}
    if intent in {"document", "general"}:
        result["documents"] = search_documents(question)
    if intent in {"business", "general"}:
        result["business"] = build_business_context(question)
    return result
