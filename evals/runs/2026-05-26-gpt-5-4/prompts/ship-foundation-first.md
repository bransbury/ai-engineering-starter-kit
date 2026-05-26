# Skill Eval Prompt Bundle

Run ID: `2026-05-24-gpt-5-4`
Case ID: `ship-foundation-first`
Skill under test: `ship`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

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
