from app.intelligence import build_business_context


def test_risk_context_returns_customer_risk_records():
    context = build_business_context("Which customers are at risk and why?")
    risks = context["risk_analysis"]
    assert len(risks) > 0
    assert all("customer_id" in item and "risk_level" in item for item in risks)


def test_revenue_context_returns_top_customers():
    context = build_business_context("Which customers generated the most revenue?")
    customers = context["top_customers"]
    assert len(customers) > 0
    assert customers[0]["revenue"] >= customers[-1]["revenue"]
