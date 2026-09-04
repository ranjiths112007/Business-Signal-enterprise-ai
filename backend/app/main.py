import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.business_api import router as business_router
from app.decision_api import router as decision_router
from app.document_api import router as document_router
from app.data_api import router as data_router
from app.database import init_db
from app.health import router as health_router

app = FastAPI(title="Business Signal API", description="Enterprise AI decision intelligence platform", version="1.1.0")

cors_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3100,http://127.0.0.1:3100").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

app.include_router(business_router)
app.include_router(decision_router)
app.include_router(document_router)
app.include_router(data_router)
app.include_router(health_router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "business-signal-api", "version": "1.1.0"}
