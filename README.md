# Business Signal

**An AI engineering project for answering business questions with evidence.**

Business Signal combines structured business data, SQL, document retrieval, deterministic analysis, and Gemini to answer questions without presenting invented business facts.

## Demo flow

```text
Business question
       ↓
Prompt guard
       ↓
SQL / RAG / business rules
       ↓
Evidence
       ↓
AI explanation
```

The frontend is intentionally a small project showcase rather than a full SaaS product.

## What to try

1. Start the API and frontend.
2. Open the project and go to **Bring in data**.
3. Use the demo CSV files in `data/sample/` or drop in your own CSV.
4. Business Signal inspects your columns and lets you map them before import.
5. Ask a question such as:

```text
Which customers are at risk and why?
Which customers generated the most revenue?
What is the current support load?
```

## Demo data

The repository includes three small, consistent datasets:

- `data/sample/customers.csv`
- `data/sample/sales.csv`
- `data/sample/support_tickets.csv`

Import **customers first**, then sales and support. These are clearly labeled sample data for the portfolio demo, not real company data.

## Key engineering ideas

- Natural-language business questions
- Safe read-only SQL generation and execution
- PDF semantic search with PostgreSQL + pgvector
- Deterministic customer-risk scoring
- Evidence-first AI answers
- Prompt-injection guard
- Flexible CSV column mapping
- FastAPI backend + Next.js frontend
- Automated tests and CI

## Run locally

```bash
docker compose up --build
```

Then, in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

Set `LLM_API_KEY` in `.env` to enable Gemini-backed answers. The application still has deterministic fallback behavior when no LLM key is configured.

## Useful API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health |
| GET | `/health/ready` | Database readiness |
| GET | `/api/v1/business/summary` | Live business totals |
| GET | `/api/v1/business/top-customers` | Customer revenue ranking |
| POST | `/api/v1/business/risk` | Customer risk analysis |
| POST | `/api/v1/business/sql` | Natural-language SQL |
| POST | `/api/v1/business/ask` | Evidence-backed AI answer |
| POST | `/api/v1/data/analyze` | Inspect and map CSV columns |
| POST | `/api/v1/data/upload` | Import mapped CSV data |
| POST | `/api/v1/documents/upload` | Index a PDF |
| POST | `/api/v1/documents/search` | Search indexed documents |

## Portfolio story

The interesting part of Business Signal is not the dashboard. It is the pipeline behind the answer:

**question → tool selection → structured/document evidence → deterministic checks → grounded AI explanation.**

That makes the project easy to demonstrate in an AI engineering interview while keeping the codebase small enough to explain end to end.
