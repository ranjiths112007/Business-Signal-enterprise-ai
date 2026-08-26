from app.business import customer_risk


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
