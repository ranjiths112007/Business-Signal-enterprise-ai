from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.business_api import router as business_router
from app.decision_api import router as decision_router
from app.database import init_db
from app.health import router as health_router

app = FastAPI(title="Business Signal API", description="Enterprise AI decision intelligence platform", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(business_router)
app.include_router(decision_router)
app.include_router(health_router)

@app.on_event("startup")
def startup() -> None:
    try:
        init_db()
    except Exception:
        pass

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "business-signal-api", "version": "1.0.0"}
