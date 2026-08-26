from dataclasses import dataclass

from app.business import customer_risk, top_customers


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def run_smoke_evaluation() -> list[Check]:
    checks: list[Check] = []
    top = top_customers(3)
    checks.append(Check("top_customers_returns_data", len(top) > 0, f"returned {len(top)} rows"))
    if top:
        risk = customer_risk(top[0]["customer_id"])
        checks.append(Check("risk_engine_returns_score", "risk_score" in risk, str(risk.get("risk_level", "missing"))))
        checks.append(Check("risk_score_bounds", 0 <= risk.get("risk_score", -1) <= 100, str(risk.get("risk_score"))))
    return checks
