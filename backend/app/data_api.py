import csv
import io
import json
from datetime import date
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from app.database import get_connection

router = APIRouter(prefix="/api/v1/data", tags=["Business Data"])

EXPECTED_COLUMNS = {
    "customers": {"name", "industry", "annual_value"},
    "sales": {"customer_id", "amount", "sale_date"},
    "support_tickets": {"customer_id", "priority", "status", "subject", "created_at"},
}

COLUMN_ALIASES: dict[str, dict[str, set[str]]] = {
    "customers": {
        "name": {"name", "customer", "customer_name", "company", "company_name", "account", "account_name", "client", "client_name"},
        "industry": {"industry", "sector", "vertical", "business_type", "category"},
        "annual_value": {"annual_value", "annual_revenue", "arr", "acv", "contract_value", "customer_value", "yearly_revenue"},
    },
    "sales": {
        "customer_id": {"customer_id", "customerid", "account_id", "accountid", "client_id", "clientid", "company_id"},
        "amount": {"amount", "sale_amount", "sales_amount", "revenue", "value", "deal_value", "order_value", "total"},
        "sale_date": {"sale_date", "sales_date", "date", "closed_at", "close_date", "transaction_date", "order_date"},
    },
    "support_tickets": {
        "customer_id": {"customer_id", "customerid", "account_id", "accountid", "client_id", "clientid", "company_id"},
        "priority": {"priority", "severity", "urgency", "ticket_priority"},
        "status": {"status", "ticket_status", "state", "case_status"},
        "subject": {"subject", "title", "issue", "summary", "description", "ticket_subject"},
        "created_at": {"created_at", "created_date", "opened_at", "opened_date", "date_created", "ticket_date", "created_on"},
    },
}


def _norm(value: str) -> str:
    return "".join(ch for ch in value.strip().lower() if ch.isalnum())


def _suggest_mapping(dataset: str, headers: list[str]) -> dict[str, str | None]:
    normalized = {_norm(header): header for header in headers}
    mapping: dict[str, str | None] = {}
    for target, aliases in COLUMN_ALIASES[dataset].items():
        match = None
        for alias in aliases:
            if _norm(alias) in normalized:
                match = normalized[_norm(alias)]
                break
        mapping[target] = match
    return mapping


def _read_csv(content: bytes) -> tuple[list[dict[str, str]], list[str]]:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded") from exc
    reader = csv.DictReader(io.StringIO(text))
    headers = [h.strip() for h in (reader.fieldnames or []) if h and h.strip()]
    rows = list(reader)
    if not headers or not rows:
        raise HTTPException(status_code=400, detail="CSV must contain a header row and at least one data row")
    return rows, headers


def _resolve_mapping(dataset: str, headers: list[str], mapping: dict[str, Any]) -> dict[str, str]:
    suggested = _suggest_mapping(dataset, headers)
    resolved: dict[str, str] = {}
    for target in EXPECTED_COLUMNS[dataset]:
        source = mapping.get(target) or suggested.get(target)
        if not source or source not in headers:
            raise HTTPException(
                status_code=400,
                detail=f"Map '{target}' to one of your CSV columns. Missing mapping for {target}.",
            )
        resolved[target] = source
    return resolved


@router.post("/analyze")
async def analyze_csv(
    file: UploadFile = File(...),
    dataset: str = Query(..., pattern="^(customers|sales|support_tickets)$"),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")
    rows, headers = _read_csv(await file.read())
    mapping = _suggest_mapping(dataset, headers)
    missing = [column for column, source in mapping.items() if source is None]
    return {
        "dataset": dataset,
        "columns": headers,
        "sample": rows[:5],
        "mapping": mapping,
        "missing": missing,
        "ready": not missing,
        "requirements": sorted(EXPECTED_COLUMNS[dataset]),
    }


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    dataset: str = Query(..., pattern="^(customers|sales|support_tickets)$"),
    replace: bool = Query(False),
    mapping: str = Form("{}"),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")
    try:
        requested_mapping = json.loads(mapping or "{}")
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Column mapping must be valid JSON") from exc

    rows, headers = _read_csv(await file.read())
    resolved = _resolve_mapping(dataset, headers, requested_mapping)

    try:
        with get_connection() as conn:
            if replace:
                conn.execute(f"TRUNCATE {dataset} RESTART IDENTITY CASCADE")
            if dataset == "customers":
                conn.cursor().executemany(
                    "INSERT INTO customers(name, industry, annual_value) VALUES (%s,%s,%s)",
                    [(r[resolved["name"]], r[resolved["industry"]], float(r[resolved["annual_value"]])) for r in rows],
                )
            elif dataset == "sales":
                conn.cursor().executemany(
                    "INSERT INTO sales(customer_id, amount, sale_date) VALUES (%s,%s,%s)",
                    [(int(r[resolved["customer_id"]]), float(r[resolved["amount"]]), date.fromisoformat(r[resolved["sale_date"]])) for r in rows],
                )
            else:
                conn.cursor().executemany(
                    "INSERT INTO support_tickets(customer_id, priority, status, subject, created_at) VALUES (%s,%s,%s,%s,%s)",
                    [
                        (
                            int(r[resolved["customer_id"]]),
                            r[resolved["priority"]],
                            r[resolved["status"]],
                            r[resolved["subject"]],
                            date.fromisoformat(r[resolved["created_at"]]),
                        )
                        for r in rows
                    ],
                )
            conn.commit()
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid {dataset} data: {exc}") from exc
    return {"dataset": dataset, "rows_imported": len(rows), "replaced": replace, "mapping": resolved}
