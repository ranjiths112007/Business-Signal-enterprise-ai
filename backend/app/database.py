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
