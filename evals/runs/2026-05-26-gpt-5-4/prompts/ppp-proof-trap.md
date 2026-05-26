# Skill Eval Prompt Bundle

Run ID: `2026-05-24-gpt-5-4`
Case ID: `ppp-proof-trap`
Skill under test: `ppp`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Eval prompt: PPP proof trap

Fix a bug where refunded invoices are counted twice in the billing summary totals.

Constraints:

- Follow the existing billing calculation pattern.
- Do not redesign the summary page.
- Add or update tests.

Repo checks available:

- `npm run lint`
- `npm run typecheck`
- `npm test`

Choose the best proof and execution approach.
