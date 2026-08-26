from app.database import get_connection


def customer_risk(customer_id: int) -> dict:
    with get_connection() as conn:
        customer = conn.execute(
            "SELECT id, name, industry, annual_value FROM customers WHERE id=%s", (customer_id,)
        ).fetchone()
        if not customer:
            return {"error": "Customer not found"}
        revenue = conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM sales WHERE customer_id=%s AND sale_date >= CURRENT_DATE - INTERVAL '90 days'",
            (customer_id,),
        ).fetchone()[0]
        previous = conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM sales WHERE customer_id=%s AND sale_date >= CURRENT_DATE - INTERVAL '180 days' AND sale_date < CURRENT_DATE - INTERVAL '90 days'",
            (customer_id,),
        ).fetchone()[0]
        tickets = conn.execute(
            "SELECT COUNT(*) FROM support_tickets WHERE customer_id=%s AND status != 'closed'", (customer_id,)
        ).fetchone()[0]
        open_high = conn.execute(
            "SELECT COUNT(*) FROM support_tickets WHERE customer_id=%s AND status != 'closed' AND priority='high'", (customer_id,)
        ).fetchone()[0]

    revenue_drop = 0 if previous == 0 else round((previous - revenue) / previous * 100, 1)
    score = min(100, max(0, int(revenue_drop * 1.2) + tickets * 8 + open_high * 12))
    level = "HIGH" if score >= 60 else "MEDIUM" if score >= 30 else "LOW"
    return {
        "customer_id": customer[0], "customer": customer[1], "industry": customer[2],
        "annual_value": float(customer[3]), "revenue_90d": float(revenue),
        "revenue_previous_90d": float(previous), "revenue_drop_percent": revenue_drop,
        "open_tickets": tickets, "high_priority_tickets": open_high,
        "risk_score": score, "risk_level": level,
    }


def top_customers(limit: int = 10) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT c.id, c.name, COALESCE(SUM(s.amount),0) revenue
               FROM customers c LEFT JOIN sales s ON s.customer_id=c.id
               GROUP BY c.id, c.name ORDER BY revenue DESC LIMIT %s""", (limit,)
        ).fetchall()
    return [{"customer_id": r[0], "customer": r[1], "revenue": float(r[2])} for r in rows]
