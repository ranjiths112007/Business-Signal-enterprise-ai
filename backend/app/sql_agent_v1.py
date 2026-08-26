import re
from typing import Any

from google import genai

from app.config import settings
from app.database import get_connection

BLOCKED = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|COPY|CALL|EXEC|EXECUTE)\b", re.I)
SCHEMA = "customers(id,name,industry,annual_value); sales(id,customer_id,amount,sale_date); support_tickets(id,customer_id,subject,priority,status,created_at)"

def validate_sql(sql: str) -> str:
    sql = sql.strip().rstrip(';')
    if not re.match(r'^SELECT\\b', sql, re.I) or BLOCKED.search(sql) or ';' in sql:
        raise ValueError('Only one read-only SELECT statement is allowed')
    return sql

def generate_sql(question: str) -> str:
    if not settings.llm_api_key:
        raise ValueError('LLM_API_KEY is required for natural-language SQL')
    client = genai.Client(api_key=settings.llm_api_key)
    response = client.models.generate_content(model=settings.llm_model, contents=f'Return ONE PostgreSQL SELECT query only. Schema: {SCHEMA}. Question: {question}')
    return validate_sql(response.text or '')

def execute_sql(sql: str, limit: int = 100) -> list[dict[str, Any]]:
    sql = validate_sql(sql)
    with get_connection() as conn:
        cur = conn.execute(f'SELECT * FROM ({sql}) AS q LIMIT {min(max(limit,1),1000)}')
        columns = [d.name for d in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def ask_sql(question: str) -> dict[str, Any]:
    sql = generate_sql(question)
    rows = execute_sql(sql)
    return {'question': question, 'sql': sql, 'rows': rows, 'row_count': len(rows)}
