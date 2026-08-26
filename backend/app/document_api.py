from pathlib import Path
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.retrieval import ingest_pdf, search_documents

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    try:
        count = ingest_pdf(path)
        return {"source": Path(file.filename).name, "chunks_indexed": count}
    finally:
        Path(path).unlink(missing_ok=True)


@router.post("/search")
def search(request: SearchRequest):
    return {"query": request.query, "results": search_documents(request.query, request.top_k)}
