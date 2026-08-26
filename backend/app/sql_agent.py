import re
from typing import Any

from google import genai

from app.config import settings
from app.database import get_connection

SCHEMA = """
customers(id, name, industry, annual_value)
sales(id, customer_id, amount, sale_date)
support_tickets(id, customer_id, priority, status, created_at, subject)
"""

FORBIDDEN = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|COPY|CALL)\b", re.I)

def validate_sql(sql: str) -> str:
    sql = sql.strip().rstrip(";")
    if not re.match(r"^SELECT\b", sql, re.I) or FORBIDDEN.search(sql):
        raise ValueError("Only safe read-only SELECT queries are allowed")
    if ";" in sql:
        raise ValueError("Multiple SQL statements are not allowed")
    return sql

def generate_sql(question: str) -> str:
    if not settings.llm_api_key:
        q = question.lower()
        if "top" in q and "customer" in q:
            return "SELECT c.name, SUM(s.amount) AS revenue FROM customers c JOIN sales s ON s.customer_id=c.id GROUP BY c.id,c.name ORDER BY revenue DESC LIMIT 10"
        if "ticket" in q:
            return "SELECT priority, status, COUNT(*) AS count FROM support_tickets GROUP BY priority,status ORDER BY count DESC"
        return "SELECT c.name, c.industry, c.annual_value FROM customers c ORDER BY c.annual_value DESC LIMIT 10"
    client = genai.Client(api_key=settings.llm_api_key)
    prompt = f"Convert the question into ONE PostgreSQL SELECT query. Use only this schema: {SCHEMA}. Never use writes, DDL, comments, multiple statements, or unknown tables. Return SQL only. Question: {question}"
    response = client.models.generate_content(model=settings.llm_model, contents=prompt)
    return validate_sql(response.text or "")

def execute_sql(question: str, limit: int = 100) -> dict[str, Any]:
    sql = validate_sql(generate_sql(question))
    if not re.search(r"\bLIMIT\b", sql, re.I):
        sql += f" LIMIT {min(limit, 100)}"
    with get_connection() as conn:
        cur = conn.execute(sql)
        columns = [d.name for d in cur.description]
        rows = cur.fetchmany(min(limit, 100))
    return {"question": question, "sql": sql, "columns": columns, "rows": [dict(zip(columns, row)) for row in rows]}
