# Business Signal Architecture

## Product goal

Business Signal is an evidence-first decision intelligence application. It combines business data and company documents to produce explainable recommendations rather than unsupported chatbot answers.

## Flow

```text
User -> Next.js UI -> FastAPI
                    |
             Question Router
              /           \
         Documents       Business Data
            |                 |
       pgvector RAG       PostgreSQL
              \             /
               Evidence Context
                      |
               Decision Engine
                      |
            Answer + Evidence
```

## Design principles

1. Evidence before generation.
2. Read-only data access for analytics.
3. Simple deterministic risk logic before LLM judgment.
4. LLM is used for explanation and synthesis, not as the source of truth.
5. Evaluation is part of the product.
6. Keep infrastructure simple until scale requires more.

## Security roadmap

- Role-based access control
- Read-only SQL execution
- Prompt-injection resistant retrieval
- Audit logging
- Secret management

## Production roadmap

- Container deployment
- Managed PostgreSQL
- Observability
- Background ingestion
- Model/provider fallback
- Automated evaluation in CI
