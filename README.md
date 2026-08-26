# Business Signal

**Enterprise AI Decision Intelligence Platform**

Business Signal turns business data into explainable decisions. The first product slice combines customer revenue and support signals into a transparent risk score and recommended action. AI/RAG will sit on top of this reliable business layer.

## Current product flow

```text
Customer + Sales + Support
          ↓
     Signal Engine
          ↓
     Risk Scoring
          ↓
  Evidence + Decision
          ↓
 Lightweight Dashboard / API
```

## Implemented

- FastAPI backend
- PostgreSQL + pgvector-ready database
- Customer, sales and support-ticket schema
- Deterministic customer risk engine
- Revenue decline detection
- High-priority support detection
- Explainable business recommendations
- REST API for business signals and decisions
- Lightweight browser dashboard
- Seeded deterministic demo dataset
- Initial evaluation cases
- Docker PostgreSQL setup

## API

- `GET /health`
- `GET /api/v1/business/top-customers`
- `POST /api/v1/business/risk`
- `POST /api/v1/decision/customer`

Example request:

```json
{"customer_id": 3}
```

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

Open `frontend/index.html` in a browser after starting the API.

## Next engineering layer

1. Document ingestion and citations
2. Natural-language business questions
3. Retrieval + SQL tool routing
4. AI explanation and verification
5. RBAC and data freshness
6. Automated evaluation with real metrics
7. Deployment and observability

**Rule:** no fake performance numbers. Every resume metric must come from an actual experiment.
