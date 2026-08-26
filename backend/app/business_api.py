from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.analytics import executive_summary, revenue_trend
from app.business import customer_risk, top_customers
from app.decision import answer, customer_decision
from app.sql_agent_v1 import ask_sql

router = APIRouter(prefix="/api/v1/business", tags=["Business Intelligence"])

class RiskRequest(BaseModel):
    customer_id: int = Field(ge=1)

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)

@router.get("/summary")
def summary(): return executive_summary()

@router.get("/revenue-trend")
def trend(): return {"trend": revenue_trend()}

@router.get("/top-customers")
def get_top_customers(limit: int = 10): return {"customers": top_customers(min(limit, 50))}

@router.post("/risk")
def get_customer_risk(request: RiskRequest):
    result = customer_risk(request.customer_id)
    if "error" in result: raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/decision/{customer_id}")
def get_customer_decision(customer_id: int):
    result = customer_decision(customer_id)
    if "error" in result: raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/sql")
def ask_sql_endpoint(request: AskRequest):
    try: return ask_sql(request.question)
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc))

@router.post("/ask")
def ask_business(request: AskRequest): return answer(request.question)
