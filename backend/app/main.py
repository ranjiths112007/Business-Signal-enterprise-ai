from fastapi import FastAPI

app = FastAPI(
    title="Business Signal API",
    description="Enterprise AI decision intelligence platform",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "business-signal-api"}
