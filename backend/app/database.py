import os
import random
from contextlib import contextmanager
from typing import Iterator

import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://business_signal:business_signal@localhost:5432/business_signal")

@contextmanager
def get_connection() -> Iterator[psycopg.Connection]:
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


def _seed_demo(conn) -> None:
    random.seed(42)
    industries = ["SaaS", "Retail", "Healthcare", "Finance", "Logistics", "Manufacturing", "Energy", "Media", "Hospitality", "Education"]
    prefixes = ["North", "Bright", "Cedar", "Vertex", "Atlas", "Harbor", "Futura", "Summit", "Blue", "Prime", "Oak", "Silver", "Red", "Green", "Metro", "Apex", "Nova", "Peak", "River", "Cloud"]
    nouns = ["Labs", "Foods", "Health", "Mobility", "Manufacturing", "Energy", "Media", "Hotels", "Systems", "Works", "Group", "Partners", "Commerce", "Logistics", "Solutions", "Analytics", "Networks", "Industries", "Services", "Holdings"]
    customers = []
    for i in range(1, 61):
        name = f"{prefixes[(i - 1) % len(prefixes)]} {nouns[(i * 3 - 1) % len(nouns)]} {i:02d}"
        industry = industries[(i - 1) % len(industries)]
        annual_value = round(random.randint(90, 480) / 10) * 10000
        customers.append((name, industry, annual_value))
    conn.cursor().executemany(
        "INSERT INTO customers(name, industry, annual_value) VALUES (%s,%s,%s)", customers
    )

    decliners = {7, 18, 29, 41, 52}
    sales = []
    for customer_id in range(1, 61):
        annual_value = customers[customer_id - 1][2]
        monthly_base = annual_value / 12 * random.uniform(0.75, 1.15)
        for month in range(1, 9):
            if customer_id in decliners:
                factor = [1.15, 1.12, 1.05, 0.95, 0.80, 0.65, 0.52, 0.40][month - 1]
            elif customer_id % 11 == 0:
                factor = [0.85, 0.90, 0.92, 1.00, 1.08, 1.16, 1.20, 1.25][month - 1]
            else:
                factor = random.uniform(0.85, 1.15)
            amount = max(3500, monthly_base * factor * random.uniform(0.88, 1.12))
            day = random.randint(3, 27)
            sales.append((customer_id, round(amount, 2), f"2026-{month:02d}-{day:02d}"))
    conn.cursor().executemany(
        "INSERT INTO sales(customer_id, amount, sale_date) VALUES (%s,%s,%s)", sales
    )

    priorities = ["low", "medium", "high"]
    statuses = ["open", "pending", "closed"]
    subjects = [
        "Invoice question", "Integration setup", "Account reporting request", "Delivery update",
        "API configuration", "Service outage", "Billing clarification", "User access request",
        "Renewal concern", "Performance issue", "Data export request", "Contract question",
        "Feature request", "Login issue", "Dashboard issue", "Security review",
    ]
    tickets = []
    for customer_id in range(1, 61):
        count = random.randint(3, 10) + (4 if customer_id in decliners else 0)
        for _ in range(count):
            if customer_id in decliners:
                priority = random.choices(priorities, [0.15, 0.35, 0.50])[0]
                status = random.choices(statuses, [0.50, 0.25, 0.25])[0]
            else:
                priority = random.choices(priorities, [0.50, 0.40, 0.10])[0]
                status = random.choices(statuses, [0.18, 0.14, 0.68])[0]
            month = random.randint(1, 8)
            day = random.randint(1, 28)
            tickets.append((customer_id, priority, status, random.choice(subjects), f"2026-{month:02d}-{day:02d}"))
    conn.cursor().executemany(
        "INSERT INTO support_tickets(customer_id, priority, status, subject, created_at) VALUES (%s,%s,%s,%s,%s)",
        tickets,
    )
    conn.commit()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name TEXT NOT NULL, industry TEXT NOT NULL, annual_value NUMERIC NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS sales (id SERIAL PRIMARY KEY, customer_id INT REFERENCES customers(id), amount NUMERIC NOT NULL, sale_date DATE NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS support_tickets (id SERIAL PRIMARY KEY, customer_id INT REFERENCES customers(id), priority TEXT NOT NULL, status TEXT NOT NULL, subject TEXT NOT NULL, created_at DATE NOT NULL)")
        conn.commit()

        demo_enabled = os.getenv("DEMO_DATA", "true").lower() == "true"
        customer_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if demo_enabled and customer_count == 0:
            _seed_demo(conn)
