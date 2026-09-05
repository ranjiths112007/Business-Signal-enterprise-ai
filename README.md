# Business Signal

**An AI engineering project that answers business questions with evidence.**

Business Signal combines structured business data, SQL, document retrieval, deterministic analysis, and Gemini to produce grounded answers.

## What the project demonstrates

```text
Question
  ↓
Choose the right source
  ↓
SQL / retrieval / business rules
  ↓
Evidence
  ↓
AI explanation
```

This is a **project showcase**, not a production SaaS product.

## Demo

The database creates a deterministic demo business dataset automatically when empty:

- **60 customers** across 10 industries
- **480 sales records** across Jan–Aug 2026
- **380 support tickets** with realistic priority/status patterns
- several deliberately declining accounts for risk analysis

Try:

```text
Which customers are at risk and why?
Which customers generated the most revenue?
What is the current support load?
What industry has the most revenue?
What is the average customer value?
Show the latest sales trend.
```

The small CSV examples are also available in `data/sample/` for demonstrating the import/mapping flow:

```text
data/sample/customers.csv
data/sample/sales.csv
data/sample/support_tickets.csv
```

## Bring your own CSV

CSV import is optional. Upload a file, inspect the detected columns, review the mapping, then import it.

Supported data:

| Dataset | Typical fields |
|---|---|
| Customers | company/name, industry, annual value |
| Sales | customer name/id, amount, date |
| Support | customer name/id, priority, status, issue, date |

## Stack

- Next.js frontend
- FastAPI backend
- PostgreSQL + pgvector
- Natural-language SQL
- RAG / document retrieval
- Gemini integration
- Prompt-injection guard
- Deterministic risk analysis
- Automated tests + GitHub Actions

## Run locally

```bash
docker compose up --build
```

Then:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

Set `LLM_API_KEY` in `.env` to enable Gemini-backed answers.

## Reset the demo database

To load the richer demo dataset from scratch:

```bash
docker compose down -v
docker compose up --build
```

## Documentation

A comprehensive project documentation source is available at:

`docs/BUSINESS_SIGNAL_PROJECT_DOCUMENTATION.md`

It covers the architecture, data model, AI engineering techniques, RAG flow, natural-language SQL, risk engine, API surface, testing, deployment, lessons learned, limitations, roadmap, and interview walkthrough.

## Interview story

The useful part of Business Signal is the pipeline behind the answer:

**question → source/tool selection → evidence → deterministic checks → grounded AI response**.

That keeps the project small enough to explain end to end while still showing practical AI engineering skills.
