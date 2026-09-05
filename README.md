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

The project includes a small, consistent demo dataset, so the dashboard has data immediately after the database is initialized.

Try:

```text
Which customers are at risk and why?
Which customers generated the most revenue?
What is the current support load?
```

The demo files are also available in `data/sample/`:

```text
data/sample/customers.csv
data/sample/sales.csv
data/sample/support_tickets.csv
```

The sales and support files use customer names to keep the example easy to read. The importer can also map common column-name variations from other CSV exports.

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

## Interview story

The useful part of Business Signal is the pipeline behind the answer:

**question → source/tool selection → evidence → deterministic checks → grounded AI response**.

That keeps the project small enough to explain end to end while still showing practical AI engineering skills.
