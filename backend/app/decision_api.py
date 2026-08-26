from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.decision import customer_decision

router = APIRouter(prefix="/api/v1/decision", tags=["Decision Intelligence"])

class DecisionRequest(BaseModel):
    customer_id: int = Field(ge=1)

@router.post("/customer")
def analyze_customer(request: DecisionRequest):
    result = customer_decision(request.customer_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
