import re
from typing import Any

from google import genai

from app.config import settings
from app.database import get_connection

BLOCKED = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|COPY|CALL|EXEC|EXECUTE)\b", re.I)
SCHEMA = "customers(id,name,industry,annual_value); sales(id,customer_id,amount,sale_date); support_tickets(id,customer_id,subject,priority,status,created_at)"


def validate_sql(sql: str) -> str:
    sql = sql.strip().strip('`').rstrip(';')
    if not re.match(r'^SELECT\b', sql, re.I) or BLOCKED.search(sql) or ';' in sql or '--' in sql or '/*' in sql:
        raise ValueError('Only one safe read-only SELECT statement is allowed')
    return sql


def generate_sql(question: str) -> str:
    if not settings.llm_api_key:
        q = question.lower()
        if 'ticket' in q:
            return 'SELECT priority, status, COUNT(*) AS count FROM support_tickets GROUP BY priority,status ORDER BY count DESC LIMIT 10'
        if 'revenue' in q or 'top' in q or 'customer' in q:
            return 'SELECT c.name, SUM(s.amount) AS revenue FROM customers c JOIN sales s ON s.customer_id=c.id GROUP BY c.id,c.name ORDER BY revenue DESC LIMIT 10'
        return 'SELECT id,name,industry,annual_value FROM customers ORDER BY annual_value DESC LIMIT 10'
    client = genai.Client(api_key=settings.llm_api_key)
    prompt = f'Return ONE PostgreSQL SELECT query only. Schema: {SCHEMA}. Never use writes, DDL, comments, multiple statements, or unknown tables. Question: {question}'
    response = client.models.generate_content(model=settings.llm_model, contents=prompt)
    return validate_sql(response.text or '')


def execute_sql(sql: str, limit: int = 100) -> list[dict[str, Any]]:
    sql = validate_sql(sql)
    with get_connection() as conn:
        cur = conn.execute(f'SELECT * FROM ({sql}) AS business_signal_query LIMIT {min(max(limit, 1), 1000)}')
        columns = [d.name for d in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]


def ask_sql(question: str) -> dict[str, Any]:
    sql = generate_sql(question)
    rows = execute_sql(sql)
    return {'question': question, 'sql': sql, 'rows': rows, 'row_count': len(rows)}
