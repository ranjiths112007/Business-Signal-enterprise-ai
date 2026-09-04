import random
from datetime import date, timedelta

from app.database import get_connection, init_db

NAMES = ["Nova Retail", "Vertex Systems", "Apex Logistics", "BluePeak Health", "Orbit Finance", "GreenGrid Energy", "Pulse Media", "NorthStar Manufacturing", "CloudNine Labs", "UrbanCart"]
INDUSTRIES = ["Retail", "SaaS", "Logistics", "Healthcare", "Finance", "Energy", "Media", "Manufacturing", "Technology", "E-commerce"]


def seed() -> None:
    init_db()
    with get_connection() as conn:
        if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] > 0:
            return
    random.seed(42)
    today = date.today()
    with get_connection() as conn:
        for i, name in enumerate(NAMES, 1):
            conn.execute("INSERT INTO customers (name, industry, annual_value) VALUES (%s,%s,%s)", (name, INDUSTRIES[i-1], 50000 + i * 25000))
            for days in range(15, 181, 15):
                # Some customers deliberately have a declining recent period for risk testing.
                multiplier = 0.55 if i in (3, 7) and days <= 90 else 1.0
                amount = round((8000 + i * 1100) * multiplier * random.uniform(.8, 1.2), 2)
                conn.execute("INSERT INTO sales (customer_id, amount, sale_date) VALUES (%s,%s,%s)", (i, amount, today - timedelta(days=days)))
            for t in range((i % 3) + (2 if i in (3, 7) else 0)):
                conn.execute("INSERT INTO support_tickets (customer_id, priority, status, subject, created_at) VALUES (%s,%s,%s,%s,%s)", (i, "high" if t == 0 and i in (3, 7) else "medium", "open", f"Customer issue {t+1}", today - timedelta(days=10+t)))
        conn.commit()

if __name__ == "__main__":
    seed()
    print("Business Signal sample data loaded.")
