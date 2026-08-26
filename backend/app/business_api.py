from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.business import customer_risk, top_customers

router = APIRouter(prefix="/api/v1/business", tags=["Business Intelligence"])


class RiskRequest(BaseModel):
    customer_id: int = Field(ge=1)


@router.get("/top-customers")
def get_top_customers(limit: int = 10):
    return {"customers": top_customers(min(limit, 50))}


@router.post("/risk")
def get_customer_risk(request: RiskRequest):
    result = customer_risk(request.customer_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
