# Skill Eval Prompt Bundle

Run ID: `2026-05-26-opus-4-6`
Case ID: `ship-review-burden`
Skill under test: `ship`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Eval prompt: ship review burden

We need to rename the `experimentStatus` values used across the stack:

- backend enum and serializer
- shared frontend contract
- results table rendering
- filters
- API docs
- tests

The file overlap is not huge, but all of the PRs would affect the same user-visible behaviour and reviewers would need to reason about the same mapping.

Choose the safest delivery path.
