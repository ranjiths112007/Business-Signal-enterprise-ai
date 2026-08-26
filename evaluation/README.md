# Business Signal Evaluation

The evaluation set starts small on purpose. It is used to verify deterministic business decisions before adding an LLM layer.

## Metrics

- Risk classification accuracy
- Decision consistency
- Evidence completeness
- API response latency

Run the API, seed the database, then evaluate the cases in `questions.json` manually or with an automated runner as the test set grows.
