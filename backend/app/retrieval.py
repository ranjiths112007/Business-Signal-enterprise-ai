from pathlib import Path
from typing import Any

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.database import get_connection

_MODEL: SentenceTransformer | None = None


def _model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(settings.embedding_model)
    return _MODEL


def _chunks(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    clean = " ".join(text.split())
    if not clean:
        return []
    out, start = [], 0
    while start < len(clean):
        end = min(start + size, len(clean))
        out.append(clean[start:end])
        if end == len(clean):
            break
        start = end - overlap
    return out


def ensure_documents_table() -> None:
    with get_connection() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("CREATE TABLE IF NOT EXISTS documents (id BIGSERIAL PRIMARY KEY, source TEXT NOT NULL, page INT, content TEXT NOT NULL, embedding vector(384), created_at TIMESTAMPTZ DEFAULT NOW())")
        conn.commit()


def ingest_pdf(path: str | Path) -> int:
    ensure_documents_table()
    reader = PdfReader(str(path))
    rows: list[tuple[str, int, str, list[float]]] = []
    model = _model()
    for page_no, page in enumerate(reader.pages, 1):
        for chunk in _chunks(page.extract_text() or ""):
            rows.append((Path(path).name, page_no, chunk, model.encode(chunk, normalize_embeddings=True).tolist()))
    with get_connection() as conn:
        conn.execute("DELETE FROM documents WHERE source=%s", (Path(path).name,))
        if rows:
            conn.executemany("INSERT INTO documents(source,page,content,embedding) VALUES (%s,%s,%s,%s)", rows)
        conn.commit()
    return len(rows)


def search_documents(query: str, top_k: int | None = None) -> list[dict[str, Any]]:
    ensure_documents_table()
    vector = _model().encode(query, normalize_embeddings=True).tolist()
    limit = top_k or settings.top_k
    with get_connection() as conn:
        rows = conn.execute("SELECT source,page,content,1-(embedding <=> %s::vector) AS score FROM documents WHERE embedding IS NOT NULL ORDER BY embedding <=> %s::vector LIMIT %s", (vector, vector, limit)).fetchall()
    return [{"source": r[0], "page": r[1], "content": r[2], "score": round(float(r[3]), 4)} for r in rows]
