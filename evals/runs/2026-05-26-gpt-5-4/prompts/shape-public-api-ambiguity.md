# Skill Eval Prompt Bundle

Run ID: `2026-05-24-gpt-5-4`
Case ID: `shape-public-api-ambiguity`
Skill under test: `shape`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Eval prompt: shape public API ambiguity

We need to add an invoice export API so customers can download invoice history.

Open questions:

- Product has not decided whether pending invoices should appear.
- Security has not decided whether only org admins can export or whether billing viewers can too.
- Platform has not decided whether this is a new public API contract or an internal-only endpoint behind the app.

Please shape this work into the safest next step.
