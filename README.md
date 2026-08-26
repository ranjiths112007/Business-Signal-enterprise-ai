# Business Signal

**Enterprise AI Decision Intelligence Platform**

Business Signal combines structured business data and company documents to produce explainable, evidence-first decisions.

## What it does

```text
Business question
      ↓
Question / prompt guard
      ↓
 ┌────┴────┐
 ▼         ▼
SQL       RAG
 ▼         ▼
Business evidence + document evidence
      ↓
Decision engine
      ↓
Answer + signals + recommendation + evidence
```

## Core capabilities

- FastAPI backend
- PostgreSQL + pgvector
- Customer, sales and support-ticket intelligence
- Deterministic customer risk scoring
- Revenue decline detection
- Natural-language → safe read-only SQL
- PDF ingestion and semantic retrieval
- Evidence-aware AI responses with Gemini
- Prompt-injection guard
- Basic RBAC foundation
- Executive analytics and revenue trends
- Browser dashboard
- Docker local environment
- Automated regression/evaluation checks
- CI workflow

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Liveness |
| GET | `/health/ready` | Database readiness |
| GET | `/metrics` | Lightweight app metrics |
| GET | `/api/v1/business/summary` | Executive KPIs |
| GET | `/api/v1/business/top-customers` | Revenue ranking |
| POST | `/api/v1/business/risk` | Customer risk |
| POST | `/api/v1/business/decision/{customer_id}` | Explainable intervention decision |
| POST | `/api/v1/business/sql` | Natural-language SQL |
| POST | `/api/v1/business/ask` | Evidence-first AI answer |
| POST | `/api/v1/documents/upload` | Index a PDF |
| POST | `/api/v1/documents/search` | Semantic document search |

## Run locally

```bash
docker compose up -d
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```

Then open `frontend/index.html`.

For AI features, set `LLM_API_KEY` in `.env`. The SQL agent also has deterministic offline fallback queries for the demo dataset.

## Engineering decisions

- The LLM does not directly mutate the database.
- Generated SQL is restricted to a single read-only SELECT.
- Suspicious prompt-injection patterns are rejected before AI execution.
- Deterministic business rules remain the source of truth for risk scoring.
- The LLM is used for synthesis and explanation rather than inventing business facts.
- No fake benchmark numbers are claimed; metrics must come from executed evaluations.

## Portfolio focus

Business Signal demonstrates applied AI engineering across RAG, LLM tool use, structured data reasoning, AI safety, backend engineering, evaluation, and product integration.
