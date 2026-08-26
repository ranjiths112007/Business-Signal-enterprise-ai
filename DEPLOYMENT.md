# Business Signal deployment

## Local

1. Copy `.env.example` to `.env` and set `LLM_API_KEY`.
2. Start PostgreSQL/pgvector with `docker compose up -d`.
3. Install backend dependencies: `pip install -r backend/requirements.txt`.
4. Start API: `uvicorn app.main:app --app-dir backend --reload`.
5. Start frontend from `frontend` with `npm install && npm run dev`.

## Production checklist

- Use managed PostgreSQL with pgvector.
- Store API keys in platform secrets.
- Restrict CORS to the deployed frontend origin.
- Put the API behind HTTPS and a reverse proxy.
- Add authentication provider and enforce roles on every protected route.
- Enable structured logs and external monitoring.
- Run evaluation and tests in CI before deployment.
- Use separate staging and production databases.

## Demo flow

1. Open the dashboard.
2. Inspect executive metrics.
3. Select a customer and inspect risk evidence.
4. Ask: `Which customers are at risk and why?`
5. Ask: `Which customers generated the most revenue?`
6. Upload a PDF policy and ask a policy question.
