from collections import defaultdict
from datetime import date, timedelta

from app.database import get_connection


def executive_summary() -> dict:
    with get_connection() as conn:
        customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        revenue = conn.execute("SELECT COALESCE(SUM(amount),0) FROM sales").fetchone()[0]
        open_tickets = conn.execute("SELECT COUNT(*) FROM support_tickets WHERE status <> 'closed'").fetchone()[0]
        high_priority = conn.execute("SELECT COUNT(*) FROM support_tickets WHERE status <> 'closed' AND priority = 'high'").fetchone()[0]
        industries = conn.execute("SELECT industry, COUNT(*) FROM customers GROUP BY industry ORDER BY COUNT(*) DESC").fetchall()
    return {"customers": customers, "total_revenue": float(revenue), "open_tickets": open_tickets, "high_priority_tickets": high_priority, "industries": [{"industry": x[0], "customers": x[1]} for x in industries]}


def revenue_trend() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT sale_date, SUM(amount) FROM sales GROUP BY sale_date ORDER BY sale_date").fetchall()
    return [{"date": row[0].isoformat() if hasattr(row[0], 'isoformat') else str(row[0]), "revenue": float(row[1])} for row in rows]
