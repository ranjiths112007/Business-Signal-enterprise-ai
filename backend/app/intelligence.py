from datetime import datetime
from typing import Any

from app.business import customer_risk, top_customers
from app.retrieval import search_documents


def classify_question(question: str) -> str:
    q = question.lower()
    if any(x in q for x in ["policy", "contract", "document", "refund", "leave"]):
        return "document"
    if any(x in q for x in ["customer", "revenue", "sales", "ticket", "risk", "churn"]):
        return "business"
    return "general"


def build_business_context(question: str) -> dict[str, Any]:
    q = question.lower()
    context: dict[str, Any] = {"generated_at": datetime.utcnow().isoformat() + "Z"}
    if any(x in q for x in ["top", "highest", "revenue", "customer"]):
        context["top_customers"] = top_customers(limit=10)
    if any(x in q for x in ["risk", "churn", "danger", "at risk"]):
        context["risk_analysis"] = customer_risk()
    return context


def gather_evidence(question: str) -> dict[str, Any]:
    intent = classify_question(question)
    result: dict[str, Any] = {"intent": intent, "documents": [], "business": {}}
    if intent in {"document", "general"}:
        result["documents"] = search_documents(question)
    if intent in {"business", "general"}:
        result["business"] = build_business_context(question)
    return result
