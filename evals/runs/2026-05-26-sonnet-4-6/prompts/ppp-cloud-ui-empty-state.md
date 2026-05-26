# Skill Eval Prompt Bundle

Run ID: `2026-05-24-sonnet-4-6`
Case ID: `ppp-cloud-ui-empty-state`
Skill under test: `ppp-cloud`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Example ticket: UI empty state

## Task

Show an empty state in the experiment results table when there are zero rows.

## Expected behaviour

- If there are no results, show the existing empty-state component if available.
- Do not create new styling unless no existing component/pattern exists.
- Preserve current loading and error behaviour.

## Proof

Add/update a component test if this area has component tests. Otherwise document manual verification.
