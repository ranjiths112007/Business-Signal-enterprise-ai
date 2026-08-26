# Business Signal

**Enterprise AI Decision Intelligence Platform**

Business Signal is a production-oriented AI system for answering business questions across unstructured documents and structured business data, while returning evidence and measurable confidence.

## Product vision

```text
Business data + Documents + Business rules
                 ↓
          AI reasoning layer
                 ↓
       Verified business signal
                 ↓
       Answer + evidence + confidence
```

## Planned capabilities

- Document-grounded RAG with source citations
- Natural-language-to-SQL business analysis
- Multi-step agentic reasoning and tool calling
- Evidence collection and answer verification
- Role-based data access controls
- Temporal and stale-data awareness
- Automated evaluation for accuracy, retrieval, citations, hallucination, latency and tool reliability
- Production API and web interface

## Repository structure

```text
backend/       FastAPI application
frontend/      Web application (coming next)
data/          Local development datasets and documents
evaluation/    Evaluation datasets and experiment results
```

## Current status

**Phase 1 — Foundation**

- [x] Repository initialized
- [x] FastAPI service
- [x] Local PostgreSQL + pgvector
- [x] Environment template
- [ ] Document ingestion
- [ ] Retrieval pipeline
- [ ] SQL reasoning
- [ ] Agent orchestration
- [ ] Verification and evaluation

## Local setup

### 1. Start PostgreSQL + pgvector

```bash
docker compose up -d
```

### 2. Create a Python environment

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and add a local LLM API key when we connect the model layer.

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

Health check: `GET /health`

## Engineering principle

Business Signal will not claim accuracy, performance or novelty without measuring it. Every meaningful capability will have tests and an evaluation dataset before it becomes a resume claim.
