# Cloud agent usage

Use `ppp-cloud` for autonomous coding agents.

It is the non-interactive version of Plan. Patch. Prove.

```text
Inspect → Decide → Plan → Prove → Patch → Validate → Review → Draft PR
```

## Good cloud-agent tasks

- clear bug fixes
- test additions
- small validation rules
- small UI states
- docs updates
- small refactors with tests
- coverage around existing behaviour

## Avoid assigning directly

- broad features
- architecture-heavy work
- auth/security/permission changes
- database migrations
- public API decisions
- billing/tenancy changes
- unclear product behaviour

## Expected output

The cloud agent should either:

1. create one focused draft PR; or
2. stop with a useful blocker.

## Suggested issue/task format

```md
Use the `ppp-cloud` skill.

## Task

<clear bounded task>

## Expected behaviour

- ...

## Scope

Do:
- ...

Do not:
- ...

## Context

- Relevant files/modules:
- Existing pattern to follow:
- Related tests:

## Proof required

- Add/update:
- Run:

## Stop conditions

Stop and report if:
- product behaviour is unclear;
- auth/security/data/API changes are required;
- tests fail after two focused attempts;
- implementation requires broad refactoring;
- repo instructions conflict with this task.

## PR expectation

Create one focused draft PR.
Follow repo PR template and commit/title conventions.
```

This repo also includes a ready-to-copy issue template at `.github/ISSUE_TEMPLATE/ppp-cloud-task.md`.

## Review expectation

Cloud-created PRs should still be reviewed by a human.

Focus review on:

- assumptions
- tests/checks run
- checks not run
- scope creep
- security/privacy/auth/data/API risks
- whether the PR should remain draft
