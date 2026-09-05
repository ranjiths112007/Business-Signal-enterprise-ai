from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.business import customer_risk, top_customers
from app.database import get_connection
from app.decision import answer, customer_decision
from app.prompt_guard import sanitize_question
from app.sql_agent import execute_sql

router = APIRouter(prefix="/api/v1/business", tags=["Business Intelligence"])


class RiskRequest(BaseModel):
    customer_id: int = Field(ge=1)


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


@router.get("/summary")
def summary() -> dict:
    with get_connection() as conn:
        customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        revenue = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM sales").fetchone()[0]
        open_tickets = conn.execute("SELECT COUNT(*) FROM support_tickets WHERE status <> 'closed'").fetchone()[0]
        high_priority = conn.execute("SELECT COUNT(*) FROM support_tickets WHERE status <> 'closed' AND priority = 'high'").fetchone()[0]
    return {
        "customers": customers,
        "total_revenue": float(revenue),
        "open_tickets": open_tickets,
        "high_priority_tickets": high_priority,
    }


@router.get("/revenue-trend")
def trend() -> dict:
    with get_connection() as conn:
        rows = conn.execute("SELECT sale_date, SUM(amount) FROM sales GROUP BY sale_date ORDER BY sale_date").fetchall()
    return {
        "trend": [
            {"date": row[0].isoformat(), "revenue": float(row[1])}
            for row in rows
        ]
    }


@router.get("/top-customers")
def get_top_customers(limit: int = 10) -> dict:
    return {"customers": top_customers(min(limit, 50))}


@router.post("/risk")
def get_customer_risk(request: RiskRequest) -> dict:
    result = customer_risk(request.customer_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/decision/{customer_id}")
def get_customer_decision(customer_id: int) -> dict:
    result = customer_decision(customer_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/sql")
def ask_sql_endpoint(request: AskRequest) -> dict:
    try:
        return execute_sql(sanitize_question(request.question))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/ask")
def ask_business(request: AskRequest) -> dict:
    try:
        return answer(sanitize_question(request.question))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
