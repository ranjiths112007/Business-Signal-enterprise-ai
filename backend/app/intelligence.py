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
        "lowest", "how many", "total", "average", "trend", "backlog", "load",
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

        context["support_breakdown"] = [
            {"priority": row[0], "status": row[1], "count": row[2]}
            for row in conn.execute(
                "SELECT priority, status, COUNT(*) FROM support_tickets GROUP BY priority, status ORDER BY count DESC"
            ).fetchall()
        ]
        context["industry_summary"] = [
            {"industry": row[0], "customers": row[1], "revenue": float(row[2])}
            for row in conn.execute(
                """SELECT c.industry, COUNT(DISTINCT c.id), COALESCE(SUM(s.amount), 0)
                   FROM customers c
                   LEFT JOIN sales s ON s.customer_id = c.id
                   GROUP BY c.industry
                   ORDER BY revenue DESC"""
            ).fetchall()
        ]

    customers = top_customers(limit=50)
    if any(x in q for x in [
        "top", "highest", "lowest", "revenue", "sales", "sale", "customer",
        "account", "company", "who", "generated", "made",
    ]):
        context["top_customers"] = customers[:10]

    if any(x in q for x in ["risk", "churn", "danger", "at risk", "warning"]):
        risks = []
        for customer in customers:
            result = customer_risk(customer["customer_id"])
            if "error" not in result:
                risks.append(result)
        context["risk_analysis"] = sorted(
            risks,
            key=lambda item: (
                item.get("risk_level") != "HIGH",
                -float(item.get("revenue_drop_percent", 0)),
                -int(item.get("high_priority_tickets", 0)),
            ),
        )

    return context


def gather_evidence(question: str) -> dict[str, Any]:
    intent = classify_question(question)
    result: dict[str, Any] = {"intent": intent, "documents": [], "business": {}}
    if intent in {"document", "general"}:
        result["documents"] = search_documents(question)
    if intent in {"business", "general"}:
        result["business"] = build_business_context(question)
    return result
