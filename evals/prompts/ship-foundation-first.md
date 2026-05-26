# Eval prompt: foundation-first ship routing

We need to add a new `confidenceBand` field to experiment results and show it in the dashboard.

Likely work includes:

- updating the backend API response shape
- updating the shared TypeScript contract for experiment results
- updating validation/schema logic
- updating the results table UI
- updating CSV export
- updating any affected tests and docs

Choose the safest delivery path.

Important:

- do not assume everything can run in parallel
- the shared contract and validation base will be moving
- review burden matters, not just file overlap
