# Skill Eval Prompt Bundle

Run ID: `2026-05-24-sonnet-4-6`
Case ID: `shape-large-feature`
Skill under test: `shape`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Example ticket: too large for PPP

## Task

Build a new analytics dashboard to show A/B test data, conversion rates, traffic split, confidence, date range filters, and export to CSV.

## Expected PPP behaviour

PPP should not implement this directly.

It should recommend identifying the smallest first PPP-ready task, such as:

- create a dashboard shell behind a feature flag; or
- add a read-only table for existing A/B test result data; or
- create a proof plan and split the work.
