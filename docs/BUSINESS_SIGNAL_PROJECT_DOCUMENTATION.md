# Business Signal - Project Documentation

> **Ask a business question. Find the signal.**
>
> An AI engineering project that combines structured business data, SQL, document retrieval, deterministic analysis, and grounded AI responses.

## 1. Why I built it

I wanted a project that showed more than a model call. Business Signal treats the language model as one component in a larger evidence pipeline:

**question -> source/tool selection -> SQL / retrieval / business rules -> evidence -> AI explanation**

The project is intentionally a showcase rather than a production SaaS application. The codebase is small enough to explain end to end while still demonstrating practical AI engineering skills.

## 2. What the project demonstrates

- Natural-language business analysis
- Natural-language-to-SQL
- PostgreSQL analytics
- PostgreSQL + pgvector vector search
- PDF ingestion and semantic retrieval (RAG)
- Deterministic customer risk scoring
- Evidence-first answer generation
- Prompt-injection guard
- Read-only SQL validation
- FastAPI backend engineering
- Next.js frontend engineering
- CSV inspection and column mapping
- Pytest regression tests
- Docker Compose local runtime
- GitHub Actions CI foundation

## 3. Architecture

```text
User
  |
  v
Next.js UI
  |
  v
FastAPI API
  |
  +--> prompt guard
  +--> question classification
  |      |
  |      +--> business context --> PostgreSQL
  |      |                         deterministic rules
  |      |
  |      +--> document context --> PDF chunks
  |                                embeddings
  |                                pgvector
  |
  +--> optional Gemini explanation
  |
  v
answer + evidence
```

## 4. Repository structure

| Path | Responsibility |
|---|---|
| `backend/app/business.py` | Customer risk scoring and revenue ranking |
| `backend/app/intelligence.py` | Question classification and evidence assembly |
| `backend/app/decision.py` | Customer decisions and grounded answer fallback / generation |
| `backend/app/sql_agent.py` | Natural-language SQL generation and validation |
| `backend/app/retrieval.py` | PDF ingestion, chunking, embeddings, vector search |
| `backend/app/database.py` | Database schema and deterministic demo seed |
| `backend/app/business_api.py` | FastAPI business endpoints |
| `backend/tests/` | Regression tests |
| `frontend/app/page.tsx` | Showcase UI and data workflow |
| `frontend/app/globals.css` | Visual system and responsive layout |
| `data/sample/` | Small example CSVs |
| `docker-compose.yml` | Local PostgreSQL + API stack |

## 5. Data model

### Customers

`id, name, industry, annual_value`

### Sales

`id, customer_id, amount, sale_date`

### Support tickets

`id, customer_id, priority, status, subject, created_at`

### Documents

`id, source, page, content, embedding, created_at`

The model is intentionally compact: enough relationships to demonstrate joins, aggregation, trends, operational load, and risk without turning the project into a full ERP schema.

## 6. Deterministic demo data

The application generates a reproducible demo dataset in code instead of storing a huge fixture in the repository.

- **60 customers** across 10 industries
- **480 sales records** covering January-August 2026
- **Hundreds of support tickets** with varied priority/status patterns
- Several deliberately declining customer accounts to make risk analysis visible
- `random.seed(42)` for repeatability

To rebuild from scratch:

```bash
docker compose down -v
docker compose up --build
```

## 7. Business analytics layer

Core metrics are calculated from PostgreSQL instead of being invented by an LLM.

Examples:

- Total customer count
- Recorded revenue
- Top customers by revenue
- Revenue trend
- Revenue by industry
- Support backlog
- High-priority support load
- Customer support activity
- Customer risk indicators

## 8. Customer risk engine

For each customer the system compares the trailing 90-day revenue with the previous 90-day period and combines that signal with unresolved support activity.

A simplified view of the current heuristic:

```text
risk score = revenue decline contribution
           + open ticket contribution
           + high-priority ticket contribution
```

The score is bounded to 0-100 and mapped to `LOW`, `MEDIUM`, or `HIGH`.

This is an explainable heuristic, not a trained churn model.

## 9. Natural-language SQL

With Gemini enabled, the SQL path converts a user question into one PostgreSQL `SELECT` statement using a constrained schema.

Safety checks then reject:

- `INSERT`
- `UPDATE`
- `DELETE`
- DDL operations such as `DROP`, `ALTER`, `CREATE`
- Multiple statements
- Non-SELECT outputs

A result limit is also applied when the generated SQL does not include one.

## 10. RAG / document retrieval

The document path handles knowledge that lives in PDFs rather than relational rows.

Pipeline:

```text
PDF
 -> pypdf extraction
 -> text chunks (900 chars, 120 overlap)
 -> Sentence Transformer embeddings
 -> PostgreSQL vector(384)
 -> similarity search
 -> top-k evidence passages
```

Using PostgreSQL + pgvector keeps the local stack simple because the relational and vector data live in one database.

## 11. Evidence-first answer generation

The unified `/api/v1/business/ask` flow gathers evidence before generation.

Gemini is instructed to:

- answer only from supplied context
- never invent facts
- give the direct answer first
- distinguish signals from recommendations
- say what is missing when the evidence truly cannot answer the question

When no LLM key is configured, deterministic fallback answers handle core business questions.

## 12. Prompt and SQL safety

Two boundaries are treated separately:

1. User question -> prompt sanitization
2. LLM output -> SQL validation

This is intentionally a lightweight portfolio implementation. Production hardening would add a full SQL parser/AST validation layer, a dedicated read-only database role, stronger authentication, and monitoring.

## 13. CSV onboarding

CSV imports follow an inspect -> map -> import workflow.

Supported datasets:

- Customers: company/name, industry, annual value
- Sales: customer name/id, amount, date
- Support: customer name/id, priority, status, issue, date

The UI detects common column variations and lets the user confirm mappings before import. This avoids forcing users to learn the internal database schema.

## 14. FastAPI API surface

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/v1/business/summary` | Business summary |
| GET | `/api/v1/business/revenue-trend` | Revenue trend |
| GET | `/api/v1/business/top-customers` | Ranked customer revenue |
| POST | `/api/v1/business/risk` | Customer risk analysis |
| POST | `/api/v1/business/decision/{customer_id}` | Intervene / monitor decision |
| POST | `/api/v1/business/sql` | Natural-language SQL |
| POST | `/api/v1/business/ask` | Unified analysis |
| POST | `/api/v1/data/analyze` | Inspect CSV columns |
| POST | `/api/v1/data/upload` | Import mapped CSV |

## 15. Frontend

The frontend is a project showcase rather than a fake SaaS dashboard.

Main sections:

- Hero and project positioning
- Ask Business Signal
- Supported question guide
- Optional CSV upload and mapping
- Result metrics
- Top customer list
- Evidence trace
- Repository source link

The design uses the project's existing teal / deep-ink visual language with readable typography and responsive behavior.

## 16. Example questions

The current demo is designed for questions such as:

- Which customers are at risk and why?
- Who generated the most revenue?
- What is the current support load?
- Which are the top 5 customers by revenue?
- Which industry generated the most revenue?
- How many customers do we have?
- Which customers have declining revenue?
- How many high-priority tickets are open?
- Which customers have the most support tickets?
- Give me a business snapshot.
- What is the average sale amount?
- Which industries contribute the most revenue?
- Which customers have the highest annual value?
- What is the revenue trend?
- Which industry has the most customers?
- Which customers have unresolved high-priority issues?
- Who are the highest-risk customers?

The examples are a guide to the current connected data model, not a claim that arbitrary questions about nonexistent fields can be answered.

## 17. Docker runtime

The local Compose stack uses:

- `pgvector/pgvector:pg17` for PostgreSQL + vector support
- FastAPI on port 8000
- PostgreSQL on port 5432
- Next.js development server on port 3050

Run the stack:

```bash
docker compose up --build
```

Enable Gemini with `LLM_API_KEY` in the environment.

## 18. Dependencies

Backend:

- FastAPI 0.116.1
- Uvicorn 0.35.0
- psycopg 3.2.9
- pgvector 0.4.1
- pypdf 6.0.0
- sentence-transformers 5.1.0
- google-genai 1.30.0
- pytest 8.4.1

Frontend:

- Next.js 14.2.31
- React 18.3.1
- TypeScript 5.7.3

## 19. Testing

Regression coverage includes:

- risk context contains customer risk records
- revenue context returns ordered top customers
- support questions always receive core summary evidence
- SQL safety rejects non-read-only statements

The project is configured for GitHub Actions. The latest connector view did not expose a completed workflow run for the most recent changes, so a final CI pass is not claimed here without verification.

## 20. Real engineering lessons

### Evidence was too narrow

An earlier implementation returned a generic insufficient-evidence response for questions that the database could answer. The evidence builder was expanded so core business questions receive broader context instead of depending on one narrow keyword branch.

### Demo data needed to feel real

Rather than checking in a giant CSV, the application now generates a richer deterministic dataset at startup when the database is empty.

### Database volumes can hide code changes

A previously initialized PostgreSQL volume will keep old demo rows. That is why the reset command removes the volume when the new seed needs to be loaded.

### Users should not need internal schemas

The CSV mapping layer hides database naming details behind an inspect-and-confirm workflow.

### UI readability matters

A technically correct demo can still fail as a portfolio piece if the typography is too small. Readability is part of the product, not an afterthought.

## 21. AI engineering strengths

This project demonstrates practical work across multiple layers rather than only prompting:

- LLM API integration
- RAG architecture
- embeddings and vector search
- natural-language SQL
- prompt design
- grounding and evidence handling
- safety controls
- deterministic decision logic
- relational analytics
- API design
- frontend integration
- testing and CI
- Dockerized local environments

## 22. 90-second interview explanation

> Business Signal is an evidence-first AI business analysis project. A user asks a business question in natural language, and the system gathers the right evidence from PostgreSQL, deterministic business rules, or document retrieval. When an LLM is configured, Gemini explains the evidence rather than acting as the source of truth. I built it this way because I wanted to demonstrate AI engineering as system design, not just model calling.

The best concrete walkthrough is the risk question:

```text
Which customers are at risk and why?
 -> classify as business intent
 -> read sales + support data
 -> calculate deterministic risk signals
 -> assemble evidence
 -> optional grounded Gemini explanation
```

## 23. Known boundaries

This showcase does not claim to be production-ready.

Current boundaries include:

- no production multi-tenancy
- RBAC foundation rather than full authorization enforcement
- lightweight SQL validation rather than a full parser
- heuristic risk scoring rather than a trained ML model
- limited schema coverage compared with a real enterprise warehouse
- retrieval quality depends on the indexed documents

## 24. Production roadmap

A realistic next path would be:

1. Add a typed tool router for business vs document tasks.
2. Replace regex SQL checks with AST-based validation.
3. Enforce a read-only database role.
4. Add authentication and real RBAC.
5. Add tracing, observability, and evaluation datasets.
6. Make the model provider interface configurable.
7. Add production secrets handling, HTTPS, rate limiting, and monitoring.

## 25. Closing

Business Signal is deliberately small. The goal is clarity, not feature count.

The engineering story is the product:

**question -> evidence -> decision logic -> grounded explanation**

That is the behavior I want this project to communicate in an AI engineering portfolio.

---

**Repository:** `https://github.com/ranjiths112007/Business-Signal-enterprise-ai`
