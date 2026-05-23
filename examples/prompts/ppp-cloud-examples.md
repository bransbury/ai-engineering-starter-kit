# PPP Cloud example prompts

## Simple bug fix

```md
Use the `/ppp-cloud` skill.

## Task

Fix whitespace-only report names being accepted.

## Expected behaviour

- Whitespace-only report names are treated as empty.
- Existing validation style is preserved.

## Proof required

- Add or update relevant tests.
- Run the smallest meaningful validation.

## PR expectation

Create one focused draft PR.
```

## Test-only task

```md
Use the `/ppp-cloud` skill.

## Task

Add unit tests for the existing report name validation logic.

## Scope

Do:
- Add tests for empty, whitespace-only, valid, and long names.

Do not:
- Change production behaviour unless a bug is discovered and clearly documented.
```

## Guardrail task

```md
Use the `/ppp-cloud` skill.

## Task

Change how project admin permissions work for saved reports.

Expected:
The agent should stop unless the permission decision is already clearly specified and safe.
```

---

## What a blocker output looks like

When the cloud agent stops, it should return something like this:

---

### Status: Stopped — blocker

I cannot complete this task safely without human input.

### Why I stopped

This task requires product and permission decisions that are not specified and cannot be inferred safely:

- Which roles should gain or lose access to saved reports?
- Should existing saved reports be migrated to the new model, and if so, how?
- Is this a breaking change for any existing integrations?

These fall under guardrailed decisions (permissions, data migration, tenancy). Proceeding without answers would require inventing product behaviour.

### What I found

| Area | File/module | Status | Notes |
| --- | --- | --- | --- |
| Permission policy | `src/permissions/reportPolicy.ts` | Confirmed | Three roles: `owner`, `admin`, `viewer` |
| Policy call sites | `src/reports/create.ts`, `src/reports/read.ts` | Confirmed | Both call `reportPolicy.can(user, action)` |
| Migration tooling | — | Missing | No migration scripts found for this area |

### What's needed before I can proceed

1. A clear spec of the new permission rules per role
2. Confirmation of whether existing saved reports need migrating
3. Sign-off from the appropriate owner

Once those are clear, this task is a good fit for `/ppp-cloud`.

---

Key things this stop got right:

- did not guess at permission rules
- clearly stated what was and was not inspected
- returned actionable next steps rather than a vague error
- left the door open for a follow-up once the blocker is resolved
