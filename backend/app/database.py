import os
from contextlib import contextmanager
from typing import Iterator

import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://business_signal:business_signal@localhost:5432/business_signal")


@contextmanager
def get_connection() -> Iterator[psycopg.Connection]:
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


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
            conn.executemany(
                "INSERT INTO customers(name, industry, annual_value) VALUES (%s,%s,%s)",
                [
                    ("Northstar Foods", "Retail", 180000),
                    ("Vertex Mobility", "Logistics", 260000),
                    ("Cedar Health", "Healthcare", 220000),
                    ("Brightline Labs", "SaaS", 310000),
                    ("Harbor Hotels", "Hospitality", 145000),
                    ("Atlas Manufacturing", "Manufacturing", 275000),
                    ("Futura Energy", "Energy", 340000),
                    ("BluePeak Media", "Media", 120000),
                ],
            )
            conn.executemany(
                "INSERT INTO sales(customer_id, amount, sale_date) VALUES (%s,%s,%s)",
                [
                    (1, 42000, "2026-04-12"), (1, 38000, "2026-05-18"), (1, 45000, "2026-06-21"), (1, 41000, "2026-08-14"),
                    (2, 62000, "2026-04-08"), (2, 58000, "2026-05-16"), (2, 64000, "2026-06-19"), (2, 61000, "2026-08-09"),
                    (3, 42000, "2026-04-20"), (3, 39000, "2026-05-22"), (3, 22000, "2026-07-18"), (3, 12000, "2026-08-24"),
                    (4, 72000, "2026-04-05"), (4, 76000, "2026-05-14"), (4, 81000, "2026-06-16"), (4, 79000, "2026-08-12"),
                    (5, 33000, "2026-04-16"), (5, 31000, "2026-05-17"), (5, 35000, "2026-06-20"), (5, 34000, "2026-08-15"),
                    (6, 68000, "2026-04-11"), (6, 65000, "2026-05-20"), (6, 71000, "2026-06-24"), (6, 69000, "2026-08-11"),
                    (7, 54000, "2026-04-07"), (7, 49000, "2026-05-13"), (7, 21000, "2026-07-16"), (7, 9000, "2026-08-26"),
                    (8, 28000, "2026-04-19"), (8, 26000, "2026-05-21"), (8, 29000, "2026-06-23"), (8, 27000, "2026-08-17"),
                ],
            )
            conn.executemany(
                "INSERT INTO support_tickets(customer_id, priority, status, subject, created_at) VALUES (%s,%s,%s,%s,%s)",
                [
                    (1, "low", "closed", "Invoice question", "2026-07-03"),
                    (1, "medium", "closed", "Account reporting request", "2026-08-02"),
                    (2, "low", "closed", "Delivery update", "2026-07-11"),
                    (2, "medium", "open", "Integration setup", "2026-08-20"),
                    (3, "high", "open", "Repeated service outage", "2026-08-08"),
                    (3, "high", "open", "Escalated support case", "2026-08-22"),
                    (3, "medium", "pending", "Slow response time", "2026-08-28"),
                    (4, "low", "closed", "Billing clarification", "2026-07-15"),
                    (4, "low", "closed", "User access request", "2026-08-05"),
                    (5, "low", "closed", "Monthly report request", "2026-08-03"),
                    (6, "medium", "closed", "API configuration", "2026-07-21"),
                    (6, "low", "open", "Minor dashboard issue", "2026-08-30"),
                    (7, "high", "open", "Contract escalation", "2026-08-10"),
                    (7, "high", "open", "Service quality issue", "2026-08-25"),
                    (7, "medium", "pending", "Renewal concern", "2026-08-29"),
                    (8, "low", "closed", "Password reset", "2026-08-04"),
                ],
            )
            conn.commit()
