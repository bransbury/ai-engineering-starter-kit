# Skill Eval Prompt Bundle

Run ID: `2026-05-26-opus-4-6`
Case ID: `ppp-failing-test`
Skill under test: `ppp`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

# Example ticket: failing test

## Task

Diagnose and fix a failing test without weakening the test.

## Input

Command:

```bash
<insert command>
```

Error:

```text
<insert error>
```

## Expected PPP behaviour

- reproduce or reason from the provided failure
- classify the failure
- attempt at most two focused fixes
- stop with a useful debugging handoff if still failing
