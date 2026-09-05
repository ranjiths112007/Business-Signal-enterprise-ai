# Business Signal - Project Documentation

> **Ask a business question. Find the signal.**
>
> A technical project showcase for an end-to-end AI engineering pipeline that combines structured business data, SQL, deterministic analysis, document retrieval, vector search, and grounded LLM responses.

## 1. Project thesis

Business Signal is intentionally a project showcase, not a production SaaS product. The point is to demonstrate the engineering system behind an AI answer:

```text
Question
  -> source / intent selection
  -> SQL / retrieval / business rules
  -> evidence
  -> optional LLM explanation
  -> answer + evidence
```

The language model is not treated as the source of truth. Facts should come from the underlying data or retrieved documents; the model is used to translate, synthesize, and explain those facts.

## 2. What the project demonstrates

- Natural-language business analysis
- Natural-language-to-SQL
- PostgreSQL analytics and joins
- PostgreSQL + pgvector vector search
- PDF ingestion and semantic retrieval (RAG)
- Sentence-transformer embeddings
- Deterministic customer risk scoring
- Evidence-first answer generation
- Prompt-injection guard
- Read-only SQL validation
- FastAPI backend engineering
- Next.js / React frontend engineering
- CSV inspection and column mapping
- Pytest regression tests
- Docker Compose local runtime
- GitHub Actions CI foundation

## 3. System architecture

```text
User
  |
  v
Next.js showcase UI
  |
  v
FastAPI API
  |
  +--> input sanitation
  +--> question classification
  |      |
  |      +--> business context --> PostgreSQL
  |      |                         deterministic analytics
  |      |                         customer risk rules
  |      |
  |      +--> document context --> PDF chunks
  |                                embeddings
  |                                pgvector
  |
  +--> optional Gemini synthesis
  |
  v
answer + evidence
```

### Architectural principle

Structured questions should be computed from structured data. Document questions should retrieve document evidence. Mixed or general questions may combine both. The LLM sits downstream of evidence gathering rather than upstream of factual computation.

## 4. Repository structure

| Path | Responsibility |
|---|---|
| `backend/app/business.py` | Customer risk scoring and revenue ranking |
| `backend/app/intelligence.py` | Question classification and evidence assembly |
| `backend/app/decision.py` | Customer decisions and grounded answer generation/fallback |
| `backend/app/sql_agent.py` | Natural-language SQL generation and validation |
| `backend/app/retrieval.py` | PDF ingestion, chunking, embeddings, vector search |
| `backend/app/database.py` | Database schema and deterministic demo seed |
| `backend/app/business_api.py` | FastAPI business endpoints |
| `backend/tests/` | Regression tests |
| `frontend/app/page.tsx` | Showcase UI and data workflow |
| `frontend/app/globals.css` | Visual system and responsive layout |
| `data/sample/` | Small example CSVs |
| `docker-compose.yml` | PostgreSQL + pgvector and API runtime |
| `README.md` | Setup, project positioning and demo story |

## 5. Data model

### Customers

`id, name, industry, annual_value`

### Sales

`id, customer_id, amount, sale_date`

### Support tickets

`id, customer_id, priority, status, subject, created_at`

### Documents

`id, source, page, content, embedding, created_at`

Relationships are centered on `customers.id`. Sales and support tickets reference the customer so that one question can combine commercial behavior and operational friction.

The document table is intentionally separate because vector retrieval has a different access pattern from transactional analytics.

## 6. Deterministic demo dataset

The application generates a reproducible demo dataset in code rather than checking a huge fixture into the repository.

- **60 customers** across 10 industries
- **480 sales records** covering January-August 2026
- **448 support tickets** with varied priority/status patterns
- **5 deliberately declining customer accounts** for risk scenarios
- Additional upward-trending accounts to avoid a uniform dataset
- `random.seed(42)` for repeatability

The demo seed only runs when the database is empty and `DEMO_DATA=true`.

To force a clean dataset reset:

```bash
docker compose down -v
docker compose up --build
```

### Why procedural demo data?

The seed stays version-controlled as code, takes little repository space, and creates a controlled environment where specific behaviors can be reproduced. The goal is not maximum row count; the goal is enough variation for useful questions and a believable demonstration.

## 7. Business analytics layer

Core facts are calculated directly from PostgreSQL and deterministic Python logic.

Examples:

- Customer count
- Total recorded revenue
- Top customers by revenue
- Revenue trend
- Revenue by industry
- Support backlog
- High-priority support load
- Customer ticket load
- Customer risk signals

Typical examples:

```text
Who generated the most revenue?
Which industry generated the most revenue?
How many customers do we have?
What is the current support load?
```

## 8. Customer risk engine

For a customer, the system compares recent revenue with the previous comparison window and combines that signal with unresolved support activity.

Simplified heuristic:

```text
risk score = revenue decline contribution
           + open ticket contribution
           + high-priority ticket contribution
```

Current implementation uses these weighted components:

```text
revenue decline % * 1.2
open tickets       * 8
high-priority      * 12
```

The final score is bounded from 0-100 and mapped to:

- `LOW`
- `MEDIUM`
- `HIGH`

This is deliberately an explainable heuristic, not a trained churn model. The project does not claim predictive ML capability where no trained model or labeled historical outcome exists.

## 9. Natural-language SQL

With Gemini enabled, a user question can be translated into one PostgreSQL `SELECT` query using a constrained schema.

The generated SQL passes through validation before execution.

### Current validation contract

- query must begin with `SELECT`
- write operations are rejected
- DDL operations are rejected
- multiple statements are rejected
- a row limit is added when one is not present

Rejected examples include:

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
```

The current validation is application-level protection. Production hardening should add a read-only database role and parser/AST-based policy.

## 10. RAG / document retrieval

The document path handles knowledge that lives in PDFs instead of relational tables.

```text
PDF
 -> pypdf extraction
 -> normalized text
 -> ~900 character chunks
 -> ~120 character overlap
 -> Sentence Transformer embedding
 -> PostgreSQL vector(384)
 -> similarity search
 -> top-k passages
 -> evidence context
```

Each stored chunk keeps source and page metadata so the final evidence can be traced back to the original document location.

Using PostgreSQL + pgvector keeps the local architecture compact by storing relational and vector data in the same database technology.

## 11. Evidence orchestration

The unified analysis flow first gathers evidence, then produces an explanation.

```text
question
  -> classify intent
  -> build evidence
  -> business analytics and/or document retrieval
  -> deterministic checks
  -> grounded response
```

The evidence object can contain:

```text
business.summary
business.top_customers
business.risk_analysis
business.support_breakdown
business.industry_summary
documents[]
```

This separation makes it possible to inspect what the model was given rather than treating the final prose as the only artifact.

## 12. Gemini usage

Gemini is used in two bounded places:

1. Natural-language question -> SQL translation
2. Evidence -> human-readable business explanation

The answer prompt is explicitly evidence-first. It instructs the model to answer from the supplied context, avoid invented facts, and state what information is missing when the context truly cannot answer the question.

When no API key is configured, deterministic fallbacks provide useful responses for the common business questions supported by the demo schema.

## 13. CSV onboarding

The CSV flow is designed as:

```text
upload
  -> inspect columns
  -> detect likely mappings
  -> user reviews / edits mapping
  -> import
```

Supported datasets:

| Dataset | Typical fields |
|---|---|
| Customers | company/name, industry, annual value |
| Sales | customer name/id, amount, date |
| Support | customer name/id, priority, status, issue, date |

This matters because users should not have to know the internal database column names before they can try the system.

## 14. FastAPI API surface

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/v1/business/summary` | Business summary |
| GET | `/api/v1/business/revenue-trend` | Revenue trend |
| GET | `/api/v1/business/top-customers` | Ranked customer revenue |
| POST | `/api/v1/business/risk` | Customer risk analysis |
| POST | `/api/v1/business/decision/{customer_id}` | Intervene / monitor decision |
| POST | `/api/v1/business/sql` | Natural-language SQL execution |
| POST | `/api/v1/business/ask` | Unified analysis and evidence |
| POST | `/api/v1/data/analyze` | Inspect CSV columns |
| POST | `/api/v1/data/upload` | Import mapped CSV |

The route layer remains thin: validate the request, call domain logic, return structured JSON.

## 15. Frontend showcase

The UI is deliberately positioned as a technical project showcase rather than a production SaaS dashboard.

Main areas:

- Project hero and thesis
- Natural-language question runner
- Supported-question guide
- Optional CSV upload and mapping
- Results and summary metrics
- Top customer list
- Evidence trace
- Repository source link

The UI's job is to make the engineering pipeline understandable within a few seconds of opening the project.

## 16. Demo question catalog

The current dataset is designed for questions such as:

### Revenue

- Who generated the most revenue?
- Which are the top 5 customers by revenue?
- What is the total revenue?
- What is the average sale amount?
- Which industry generated the most revenue?
- Which industries contribute the most revenue?
- Show the revenue trend.

### Customers

- How many customers do we have?
- Which customers have the highest annual value?
- Which industries have the most customers?
- Which company is our biggest customer?

### Risk

- Which customers are at risk and why?
- Which customers have declining revenue?
- Which customers need intervention?
- Who are the highest-risk customers?
- Which customers have unresolved high-priority issues?

### Support

- What is the current support load?
- How many support tickets are open?
- How many high-priority tickets are open?
- Which customers have the most support tickets?
- What is the support breakdown by status?

These examples describe the current evidence model. They are not a claim that questions about nonexistent fields can be answered.

## 17. Docker runtime

The local stack uses:

- `pgvector/pgvector:pg17`
- PostgreSQL on port `5432`
- FastAPI on port `8000`
- Next.js development server on port `3050` when run separately

Primary command:

```bash
docker compose up --build
```

Gemini can be enabled through environment configuration such as:

```text
LLM_API_KEY=<your-key>
LLM_MODEL=gemini-3.6-flash
```

## 18. Dependencies

### Backend

- FastAPI 0.116.1
- Uvicorn 0.35.0
- pydantic-settings 2.10.1
- psycopg 3.2.9
- pgvector 0.4.1
- pypdf 6.0.0
- sentence-transformers 5.1.0
- google-genai 1.30.0
- python-multipart 0.20.0
- pytest 8.4.1

### Frontend

- Next.js 14.2.31
- React 18.3.1
- TypeScript 5.7.3

## 19. Testing and quality

Regression coverage protects the most important intelligence behaviors:

- risk context returns customer risk records
- revenue context returns an ordered customer ranking
- support questions receive summary evidence
- SQL security rejects non-read-only statements
- frontend build catches TypeScript and UI integration issues

GitHub Actions provides a CI foundation. Recent connector access did not expose a completed workflow result for the newest documentation commits, so this document does not claim a fresh CI pass without verification.

## 20. Engineering lessons

### Evidence coverage matters more than dataset size

A larger database does not help if the evidence layer cannot retrieve the right aggregates. The project therefore expanded the business context with support breakdowns, industry summaries, customer rankings and risk analysis.

### The fallback path matters

A demo that only works when an external LLM credential exists is fragile. Deterministic fallbacks make common business questions demonstrable locally.

### Demo state must be reproducible

Procedural seeding with a fixed seed gives a fresh developer the same intended scenario after a volume reset.

### UI is part of the engineering story

A portfolio project can have correct backend logic and still feel broken if the interface is hard to read. Typography, spacing, question examples and evidence visibility are part of the showcase quality.

### Be honest about model boundaries

The project uses a deterministic heuristic for risk, not a trained ML model. It uses RAG for documents, not magical “knowledge.” It translates language to constrained SQL rather than giving an LLM unrestricted database access.

## 21. AI engineering skill map

Business Signal demonstrates work across several AI engineering layers:

| Skill | Where it appears |
|---|---|
| LLM API integration | Gemini answer generation + NL-to-SQL |
| RAG | PDF chunking, embeddings, vector retrieval |
| Embeddings | Sentence Transformers |
| Vector search | pgvector similarity queries |
| Natural-language SQL | `sql_agent.py` |
| Grounding | Evidence object + evidence-first prompt |
| Safety | Prompt guard + SQL validation |
| Data engineering | PostgreSQL schema + deterministic seed |
| Business analytics | Revenue, support and risk logic |
| Backend engineering | FastAPI + Pydantic |
| Frontend engineering | Next.js / React |
| Testing | pytest regression suite |
| Delivery | Docker Compose + GitHub Actions |

## 22. Interview walkthrough

The cleanest live demo is the risk question:

```text
Which customers are at risk and why?
        |
        v
classify_question()
        |
        v
business evidence
  - revenue summary
  - customer ranking
  - risk calculations
  - support activity
        |
        v
optional Gemini explanation
        |
        v
answer + evidence
```

### 90-second explanation

> I built Business Signal as an evidence-first AI engineering project. A user asks a business question in natural language, and the system gathers the right evidence from PostgreSQL, deterministic business rules, or document retrieval. When Gemini is enabled, the model explains the supplied evidence rather than acting as the source of truth. I added natural-language SQL, RAG with pgvector, customer risk scoring, prompt and SQL safety checks, CSV mapping, Docker setup and regression tests because I wanted the project to demonstrate the complete AI application pipeline instead of just a model call.

## 23. Known boundaries

This is a portfolio showcase and should be described accurately.

Current limitations include:

- no production multi-tenancy
- RBAC foundation rather than full authorization enforcement
- lightweight SQL validation rather than a full parser
- heuristic risk scoring rather than a trained churn model
- limited schema coverage versus a real enterprise warehouse
- retrieval quality depends on the indexed documents
- no claim of production-grade security or reliability

## 24. Production roadmap

A realistic hardening path is:

1. Add a stronger typed tool/router boundary.
2. Replace regex SQL checks with parser/AST-based validation.
3. Execute generated queries through a dedicated read-only database role.
4. Enforce authentication, RBAC and tenant isolation.
5. Add tracing, observability and structured evaluation datasets.
6. Add document ACLs and tenant-aware retrieval.
7. Expand business analytics only when the underlying schema supports it.
8. Add production secrets management, rate limiting, HTTPS and monitoring.

## 25. Documentation artifact

The accompanying high-fidelity project documentation is designed as a technical dossier covering the architecture, implementation, data model, analytics, RAG, LLM integration, safety, API surface, UI, testing, runbook, interview story, skill map, limitations and roadmap.

The source for the dossier lives in this directory so the written explanation can stay versioned with the codebase.

## 26. Closing

Business Signal is deliberately small in surface area and focused in its engineering story.

The core message is:

**question -> evidence -> decision logic -> grounded explanation**

That is the part worth showing in an AI engineering portfolio.
