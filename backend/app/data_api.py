import csv
import io
from datetime import date

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.database import get_connection

router = APIRouter(prefix="/api/v1/data", tags=["Business Data"])

EXPECTED_COLUMNS = {
    "customers": {"name", "industry", "annual_value"},
    "sales": {"customer_id", "amount", "sale_date"},
    "support_tickets": {"customer_id", "priority", "status", "subject", "created_at"},
}


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    dataset: str = Query(..., pattern="^(customers|sales|support_tickets)$"),
    replace: bool = Query(False),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")
    try:
        rows = list(csv.DictReader(io.StringIO((await file.read()).decode("utf-8-sig"))))
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded") from exc
    if not rows:
        raise HTTPException(status_code=400, detail="CSV has no data rows")
    columns = set(rows[0])
    missing = EXPECTED_COLUMNS[dataset] - columns
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(sorted(missing))}")

    try:
        with get_connection() as conn:
            if replace:
                conn.execute(f"TRUNCATE {dataset} RESTART IDENTITY CASCADE")
            if dataset == "customers":
                conn.cursor().executemany("INSERT INTO customers(name, industry, annual_value) VALUES (%s,%s,%s)", [(r["name"], r["industry"], float(r["annual_value"])) for r in rows])
            elif dataset == "sales":
                conn.cursor().executemany("INSERT INTO sales(customer_id, amount, sale_date) VALUES (%s,%s,%s)", [(int(r["customer_id"]), float(r["amount"]), date.fromisoformat(r["sale_date"])) for r in rows])
            else:
                conn.cursor().executemany("INSERT INTO support_tickets(customer_id, priority, status, subject, created_at) VALUES (%s,%s,%s,%s,%s)", [(int(r["customer_id"]), r["priority"], r["status"], r["subject"], date.fromisoformat(r["created_at"])) for r in rows])
            conn.commit()
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid {dataset} data: {exc}") from exc
    return {"dataset": dataset, "rows_imported": len(rows), "replaced": replace}