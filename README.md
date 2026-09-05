# Business Signal

**Ask a business question. Find the signal.**

An AI engineering project that turns structured business data and documents into evidence-backed business answers.

> **Project showcase:** Business Signal is intentionally a portfolio / engineering showcase, not a production SaaS product.

**Author:** Ranjith

[![GitHub](https://img.shields.io/badge/GitHub-ranjiths112007-181717?style=flat-square&logo=github)](https://github.com/ranjiths112007)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ranjith-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ranjiths112007/)

---

## What this project demonstrates

Business Signal is built around an evidence-first AI engineering pipeline:

```text
Natural-language question
        ↓
Intent / source selection
        ↓
┌───────────────────────────────────┐
│ PostgreSQL analytics              │
│ Deterministic business rules      │
│ PDF retrieval + pgvector          │
│ Natural-language SQL              │
└───────────────────────────────────┘
        ↓
Evidence assembly
        ↓
Optional Gemini explanation
        ↓
Answer + evidence
```

The important idea is that the model is **not treated as the database or source of truth**. Structured calculations and retrieved evidence are assembled first, then the LLM is used to explain the result when configured.

## Core capabilities

| Capability | What it shows |
|---|---|
| Natural-language business analysis | Question → evidence → answer workflow |
| Natural-language SQL | Converting business questions into read-only PostgreSQL queries |
| Customer risk analysis | Explainable revenue + support risk heuristic |
| Revenue analytics | Aggregation, ranking, trends and industry summaries |
| Support analytics | Open backlog, priority and status analysis |
| RAG | PDF ingestion, chunking, embeddings and semantic retrieval |
| pgvector | Vector similarity search inside PostgreSQL |
| Gemini | Grounded natural-language explanation |
| Prompt / SQL safety | Guardrails around user input and generated SQL |
| CSV onboarding | Inspect → map → import workflow |
| FastAPI | Typed HTTP API layer |
| Next.js | Interactive project showcase UI |
| Docker | Reproducible local runtime |
| Pytest / CI | Regression testing and automation |

## Demo dataset

The database generates deterministic demo data automatically when the database is empty:

- **60 customers** across 10 industries
- **480 sales records** covering January–August 2026
- **Hundreds of support tickets** with varied priority and status patterns
- Several deliberately declining accounts to make risk analysis visible
- Reproducible seeding using `random.seed(42)`

The large fixture is generated in code instead of being checked into the repository as a huge CSV.

### Good demo questions

```text
Which customers are at risk and why?
Who generated the most revenue?
What is the current support load?
Which are the top 5 customers by revenue?
Which industry generated the most revenue?
How many customers do we have?
Which customers have declining revenue?
How many high-priority tickets are open?
Which customers have the most support tickets?
Give me a business snapshot.
What is the average sale amount?
Which industries contribute the most revenue?
Which customers have the highest annual value?
What is the revenue trend?
Which customers have unresolved high-priority issues?
Who are the highest-risk customers?
```

These examples describe the connected schema. Questions about fields that do not exist in the dataset cannot be answered reliably without adding that data source.

## Technology stack

### AI / ML

- **Google Gemini** — grounded answer generation and natural-language SQL generation
- **Sentence Transformers** — text embeddings for document retrieval
- **RAG** — retrieval of relevant PDF passages before explanation

### Data / backend

- **Python**
- **FastAPI**
- **PostgreSQL**
- **pgvector**
- **psycopg**
- **pypdf**
- **Pydantic Settings**

### Frontend

- **Next.js 14**
- **React 18**
- **TypeScript**
- Responsive CSS-based showcase UI

### Engineering

- Docker Compose
- Pytest
- GitHub Actions
- Read-only SQL validation
- Prompt sanitization / guardrails

## Repository structure

```text
Business-Signal-enterprise-ai/
│
├── backend/
│   ├── app/
│   │   ├── business.py          # revenue ranking + customer risk
│   │   ├── business_api.py      # FastAPI business endpoints
│   │   ├── database.py          # schema + deterministic demo seed
│   │   ├── decision.py           # decisions + grounded answer fallback
│   │   ├── intelligence.py       # question classification + evidence
│   │   ├── retrieval.py          # PDF / embedding / vector search
│   │   ├── sql_agent.py          # NL → SQL + validation
│   │   └── ...
│   ├── tests/                   # regression coverage
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # project showcase UI
│   │   └── globals.css          # visual system + responsive styles
│   └── package.json
│
├── data/sample/                 # small CSV examples
├── docs/
│   └── BUSINESS_SIGNAL_PROJECT_DOCUMENTATION.md
├── docker-compose.yml
└── README.md
```

## Data model

```text
customers
---------
id
name
industry
annual_value

sales
-----
id
customer_id → customers.id
amount
sale_date

support_tickets
---------------
id
customer_id → customers.id
priority
status
subject
created_at

documents
---------
id
source
page
content
embedding
created_at
```

The schema is intentionally compact. It is large enough to demonstrate joins, aggregation, operational analysis, risk signals and document retrieval without becoming an artificial enterprise ERP.

## Customer risk engine

Risk is deliberately **explainable rather than pretending to be a trained churn model**.

For a customer, the system examines:

1. Revenue during the trailing 90 days
2. Revenue in the previous 90-day period
3. Open support tickets
4. Open high-priority tickets

Conceptually:

```text
risk score
= revenue decline contribution
+ open ticket contribution
+ high-priority ticket contribution
```

The score is bounded to 0–100 and mapped to `LOW`, `MEDIUM`, or `HIGH`.

This makes an interview explanation straightforward: the system can show **why** an account is considered risky instead of returning an unexplained prediction.

## Natural-language SQL

With Gemini enabled, the SQL agent receives a constrained schema and is asked to produce **one PostgreSQL SELECT statement**.

Generated SQL then passes through a read-only validation layer.

Rejected operations include:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
COPY
CALL
multiple SQL statements
non-SELECT output
```

The runtime also adds a row limit when one is not already present.

> This is a portfolio-grade safety boundary, not a claim of production-grade SQL sandboxing. Production would use AST-based validation, a dedicated read-only database role and stronger isolation.

## RAG / document retrieval

PDF retrieval follows:

```text
PDF
 ↓
pypdf text extraction
 ↓
900-character chunks with overlap
 ↓
Sentence Transformer embeddings
 ↓
PostgreSQL vector(384)
 ↓
cosine-style vector similarity search
 ↓
top-k evidence passages
```

Keeping relational and vector data in PostgreSQL makes the local architecture easy to run and explain.

## CSV onboarding

Users do not have to learn the internal column names.

The workflow is:

```text
Upload CSV
   ↓
Inspect columns
   ↓
Detect common aliases
   ↓
Review mapping
   ↓
Import
```

Supported conceptual datasets:

- Customers: company/name, industry, annual value
- Sales: customer name/id, amount, date
- Support: customer name/id, priority, status, issue, date

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/business/summary` | Core business snapshot |
| GET | `/api/v1/business/revenue-trend` | Revenue trend data |
| GET | `/api/v1/business/top-customers` | Revenue-ranked customers |
| POST | `/api/v1/business/risk` | Customer risk analysis |
| POST | `/api/v1/business/decision/{customer_id}` | Intervention / monitoring decision |
| POST | `/api/v1/business/sql` | Natural-language SQL |
| POST | `/api/v1/business/ask` | Unified evidence-first analysis |
| POST | `/api/v1/data/analyze` | Inspect CSV columns |
| POST | `/api/v1/data/upload` | Import mapped CSV |

## Local setup

### Docker

```bash
docker compose up --build
```

The stack includes PostgreSQL + pgvector and the FastAPI service.

### Frontend development

```bash
cd frontend
npm install
npm run dev
```

The frontend development server uses port `3050`.

Open:

```text
http://localhost:3050
```

FastAPI runs on:

```text
http://localhost:8000
```

### Gemini

Set your API key in the environment:

```env
LLM_API_KEY=your_key_here
```

Without an LLM key, deterministic fallback logic is used for the core showcase questions.

### Reset the demo database

When an existing Docker volume contains older rows, rebuild the database from scratch with:

```bash
docker compose down -v
docker compose up --build
```

## Documentation

The full technical documentation is available here:

[`docs/BUSINESS_SIGNAL_PROJECT_DOCUMENTATION.md`](docs/BUSINESS_SIGNAL_PROJECT_DOCUMENTATION.md)

The accompanying portfolio documentation covers architecture, data model, AI engineering techniques, RAG, SQL generation, risk analysis, APIs, testing, Docker, lessons learned, limitations and production roadmap.

## What I would explain in an interview

> **Business Signal is an evidence-first AI business analysis system.** A user asks a question in natural language. The system decides what evidence it needs, pulls structured facts from PostgreSQL or relevant passages from documents, applies deterministic business logic where appropriate, and then optionally uses Gemini to explain the result. I built it this way because I wanted to demonstrate AI engineering as a complete system rather than just calling an LLM API.

The strongest walkthrough is the risk path:

```text
Which customers are at risk and why?
        ↓
Business intent
        ↓
PostgreSQL sales + support evidence
        ↓
Deterministic risk calculation
        ↓
Evidence assembly
        ↓
Grounded explanation
```

## Known boundaries

This project is a portfolio showcase, so it intentionally does **not** claim production readiness.

Current limitations include:

- heuristic risk scoring rather than a trained predictive model
- limited business schema compared with a real enterprise warehouse
- lightweight SQL validation rather than a full parser / sandbox
- RBAC foundation rather than full authorization enforcement
- no production multi-tenancy
- retrieval quality depends on the indexed documents
- latest CI status should be verified independently before presenting a build as production-stable

## License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

## Author

**Ranjith**

GitHub: [github.com/ranjiths112007](https://github.com/ranjiths112007)

LinkedIn: [linkedin.com/in/ranjiths112007](https://www.linkedin.com/in/ranjiths112007/)

---

### Business Signal

*Question → Evidence → Signal → Explanation.*
