from fastapi import APIRouter

from app.database import get_connection
from app.metrics import snapshot

router = APIRouter(tags=["System"])


@router.get("/health/ready")
def readiness():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return {"status": "ready", "database": "ok"}
    except Exception as exc:
        return {"status": "degraded", "database": "error", "detail": str(exc)}


@router.get("/metrics")
def metrics():
    return snapshot()
