from fastapi import FastAPI

from app.business_api import router as business_router

app = FastAPI(
    title="Business Signal API",
    description="Enterprise AI decision intelligence platform",
    version="0.3.0",
)

app.include_router(business_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "business-signal-api", "version": "0.3.0"}
