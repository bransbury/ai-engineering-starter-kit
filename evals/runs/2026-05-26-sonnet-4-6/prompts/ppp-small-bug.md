# Skill Eval Prompt Bundle

Run ID: `2026-05-24-sonnet-4-6`
Case ID: `ppp-small-bug`
Skill under test: `ppp`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Example ticket: small bug fix

## Task

Users can save a report name that is only whitespace.

## Expected behaviour

Whitespace-only names should be treated as empty and rejected using the existing validation pattern.

## Notes

- Follow existing validation style.
- Add or update tests.
- Do not redesign the report form.
