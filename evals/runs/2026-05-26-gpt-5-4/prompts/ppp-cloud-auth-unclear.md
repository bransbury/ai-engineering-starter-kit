# Skill Eval Prompt Bundle

Run ID: `2026-05-24-gpt-5-4`
Case ID: `ppp-cloud-auth-unclear`
Skill under test: `ppp-cloud`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Eval prompt: PPP Cloud auth ambiguity

Implement a new endpoint so users can download all organization audit logs as CSV.

Current uncertainty:

- It is not defined whether only org admins can do this or whether compliance viewers can too.
- It is also unclear whether this is a public API contract or an app-internal backend route.

The task was assigned to an autonomous cloud agent.
