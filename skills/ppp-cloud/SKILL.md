---
name: ppp-cloud
version: 0.3.0
description: "Plan. Patch. Prove for autonomous cloud agents. Use for clear, bounded engineering tasks where the agent should inspect code, plan, prove, patch, validate, review, and open a draft PR or stop with a useful blocker."
---

# Plan. Patch. Prove — Cloud Agent Mode

Use this skill when running as an autonomous coding agent, such as GitHub Copilot Cloud Agent.

This is the non-interactive version of PPP.

Core loop:

```text
Inspect → Decide → Plan → Prove → Patch → Validate → Review → Draft PR
```

The goal is to produce one focused draft PR for a clear, bounded, verifiable task — or stop with a useful blocker when the task is unsafe or unclear.

## Cloud Agent principle

Autonomous agents may accelerate implementation, but they must not make high-risk product, architecture, security, auth, data, migration, tenancy, billing, or public API decisions without human input.

Prefer a safe stop over confident guessing.

<!-- Similar section in ppp — keep core rules consistent -->
## Token discipline

Be concise.

- Inspect only relevant files.
- Summarise instead of pasting large code/logs.
- Prefer file paths, decisions, risks, checks run, and next actions.
- Do not restate large specs or issue bodies.
- Do not create separate task artifacts unless repo instructions require them.
- Keep the PR body useful but not verbose.

## Suitable tasks

PPP Cloud is suitable when the task is:

- clear
- bounded
- expected to fit one focused PR
- low or medium risk
- testable or otherwise verifiable
- aligned with existing repo patterns
- not dependent on repeated human back-and-forth

Good examples:

- fix a clearly described bug
- add or update tests
- implement a small validation rule
- add an empty/loading/error state
- make a small UI behaviour change following existing patterns
- update docs
- make a small refactor with tests
- add coverage around existing behaviour

## Unsuitable tasks

Do not implement directly if the task is broad, ambiguous, high risk, or requires a significant decision.

Examples:

- “build a new analytics dashboard”
- “add reporting”
- “improve onboarding”
- “build the new permissions system”
- “migrate this service”
- “redesign this flow”
- “change how authentication works”
- “update billing behaviour”
- “change the public API contract”

For unsuitable tasks, stop and return a blocker or recommend splitting into a smaller task.

<!-- Similar section in ppp — keep core rules consistent -->
## Hard rules

- Inspect relevant code before planning or editing.
- Follow repo guidance and nearby code/test conventions.
- Do not invent requirements.
- Do not touch unrelated files.
- Do not weaken tests or remove validation to make checks pass.
- Do not claim checks passed unless they actually ran.
- Do not shortcut required related changes just to keep the diff small.
- Do not leave related code paths half-updated when correctness requires consistency.
- Stop after two focused failed fix attempts.
- Open a draft PR only when the work is coherent and reviewable.
- If validation is incomplete, the PR must be draft and must clearly state what was not run.

<!-- Similar section in ppp — keep core rules consistent -->
## Repo guidance

Before planning or editing, inspect repo guidance if available:

- `.github/copilot-instructions.md`
- `.github/instructions/**/*.instructions.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `README.md`
- package-specific README files near the changed code
- `.github/PULL_REQUEST_TEMPLATE.md`

Follow repo guidance for:

- architecture
- coding style
- testing
- validation commands
- PR format
- forbidden areas
- security/privacy rules

If repo guidance conflicts with this skill, follow repo guidance unless it weakens safety, validation, or production readiness.

If no repo guidance exists, infer conventions from nearby code and tests.

## 1. Inspect

Read the task and inspect relevant code before planning.

Identify:

- intended behaviour
- current behaviour, if known
- relevant files/modules
- existing patterns to follow
- test patterns
- assumptions
- risks
- potential blockers

Use a codebase inspection table when file paths or modules matter:

| Area | File/module | Status | Evidence | Notes |
|---|---|---|---|---|

Statuses:

- Confirmed — inspected and exists
- Inferred — likely, but not inspected
- Proposed new — does not exist yet and is proposed
- Missing — expected but not found

Do not present inferred paths as confirmed.

If relevant code cannot be inspected, stop and report a blocker.

## 2. Decide whether to proceed

Before implementation, decide whether to continue, narrow, or stop.

### Continue when

Continue without asking when:

- the expected behaviour is clear enough;
- the choice is low-risk;
- the repo has an existing pattern to follow;
- the decision is internal implementation detail;
- the decision is easy to reverse;
- the change does not affect product semantics, security, data, auth, permissions, migrations, billing, tenancy, or public APIs.

When continuing with an assumption, record it in the PR body under “Assumptions”.

### Stop when

Stop and report a blocker when the task requires a critical decision that is not answerable from repo context.

Critical decisions include:

- product behaviour or UX semantics
- acceptance criteria conflict
- public API contract
- data model or migration
- auth/security/permissions
- privacy or compliance behaviour
- tenancy or billing behaviour
- architecture or module boundary change
- destructive or irreversible changes
- high-risk production behaviour
- unclear test oracle

Use this blocker format:

```md
## Blocked — human decision required

I stopped because this task requires a decision I should not make autonomously.

Decision needed:
- ...

Why it matters:
- ...

Options:
1. ...
2. ...
3. ...

Recommended option:
- ...

Files inspected:
- ...

No implementation PR was created because proceeding would require guessing.
```

### Narrow when

If the task is too large but has an obvious first safe increment, implement only that increment if it is valuable and clearly within scope.

Examples:

- create a dashboard shell but not full analytics logic;
- add parser tests but not the full editor integration;
- add validation in one established path but not redesign validation globally.

If narrowing, state the narrowed scope in the PR body.

## 3. Plan

Create the smallest safe complete plan for the selected task or narrowed scope.

Include:

- objective
- files to change
- tests/checks to add or update
- validation commands
- risks
- explicit non-goals

The plan must follow repo conventions, components, styling, architecture, and design patterns.

Do not plan unrelated refactors.

Do not avoid legitimate required files just to keep the diff small.

If the plan reveals the task is not suitable for autonomous implementation, stop and report a blocker.

## 4. Prove

Define proof before implementation.

Choose exactly one primary proof and up to three supporting checks.

The primary proof must directly validate the changed behaviour. Lint/typecheck alone is not sufficient for behavioural changes unless no behavioural proof is practical.

Use the lowest-cost proof that gives meaningful confidence:

- Static/local sanity: lint, typecheck, build affected package
- Targeted unit/component test: default for logic and UI behaviour
- Focused integration/API/contract test: for cross-module or API behaviour
- E2E/manual workflow: when a real workflow is needed
- Full suite/expensive checks: only when repo convention or risk requires it

Prefer red-green testing where practical.

If expensive or environment-heavy checks are not practical, use targeted proof and document the skipped checks in the PR body.

## Automated testing and coverage

Inspect whether the affected area has automated tests or CI coverage expectations.

If unit tests exist for the affected area or new testable logic is added:

- add or update relevant unit tests;
- match or exceed the coverage standard of surrounding code;
- if no local standard exists, use 80% new-code unit coverage as a fallback target for testable logic;
- do not invent coverage numbers.

If unit tests are not practical or not applicable:

- update the next-best automated validation where appropriate;
- consider component, integration, API, E2E, snapshot, contract, build, or typecheck validation;
- explain why unit tests are not being added.

Do not write tests that only assert implementation details rather than behaviour.

If CI/CD enforces unit coverage, do not open a normal PR that is likely to fail coverage. Add tests, mark the PR as draft, or stop with a blocker if the issue cannot be addressed.

## 5. Patch

Implement in small validated loops:

```text
small change → run proof/check → inspect result → fix → review diff → continue
```

Rules:

- stay within the selected task or narrowed scope;
- update all related code paths required for correctness;
- preserve existing behaviour unless the task requires changing it;
- avoid unrelated refactors and opportunistic cleanup;
- validate after meaningful changes.

If the work becomes larger, riskier, or different from the plan, stop and reassess. If it now requires a critical decision, stop and report a blocker.

## 6. Validate failures

If validation fails, stop adding code and diagnose.

Classify the failure before fixing:

- Implementation bug
- Test expectation wrong
- Environment/setup issue
- Missing dependency
- Product ambiguity
- Architecture/design mismatch
- Unknown

Only attempt automatic fixes for implementation bugs or clearly incorrect tests.

Maximum automatic fix attempts: 2.

For each attempt:

1. reproduce the failure;
2. classify it;
3. identify the key error;
4. inspect the relevant code/test;
5. fix one confirmed cause;
6. rerun the targeted check.

After two failed attempts, stop. Open a draft PR only if the partial work is useful and reviewable; otherwise do not create a PR.

Use this failure summary:

```md
## Blocked after two focused fix attempts

What I tried:
1. ...
2. ...

Current evidence:
- failing command:
- key error:
- likely cause:
- files touched:

Recommended next action:
Human investigation required.
```

Do not weaken tests, delete validation, broaden scope, or keep retrying indefinitely.

## 7. Review

Before creating a draft PR, review as QA and production reviewer.

### Blocking — must fix or stop before PR

- Task is not satisfied
- Acceptance criteria not covered
- Required proof/tests missing or failing
- CI/PR checks likely to fail without explanation
- Unit/automated coverage requirement not met where applicable
- Security/privacy/auth/permission risk unresolved
- Related code paths left inconsistent
- Unrelated files changed
- Change cannot be explained clearly

### Should fix before PR if safe and in scope

- Edge cases weakly handled
- Error/loading/empty states incomplete where relevant
- Existing patterns not followed
- Accessibility not considered for UI changes
- Performance risk not considered
- Tests assert implementation rather than behaviour
- Unnecessary complexity added

If three or more “Should fix” items apply, address them before PR unless they are explicitly documented as follow-ups and the PR is draft.

### Nice to have / follow-up

- Additional refactoring
- Extra docs/comments
- Broader E2E coverage
- Non-blocking polish

If a blocking item cannot be fixed safely, stop or open a draft PR only if the partial result is valuable and clearly labelled.

## 8. Draft PR

Create a draft PR when:

- the task or narrowed scope is coherently implemented;
- the diff is reviewable;
- validation has been run or limitations are clearly documented;
- remaining risks are clearly stated.

Do not create a PR when:

- implementation is incoherent or half-applied;
- critical behaviour is unknown;
- auth/security/data/API decisions are unresolved;
- unrelated files would be included;
- tests fail and the cause is unknown;
- the change is likely harmful.

## Ticket reference

Use “ticket reference” generically. Jira is one example.

Look for a ticket reference in:

1. branch name
2. task/ticket text
3. recent commit messages if relevant

Examples:

- Jira: `AEP-2714`, `MONE-61005`
- Linear: `ENG-123`
- GitHub issue: `#1234`

Do not invent a ticket reference.

If none is found, continue without one and state that none was found in the PR body.

## Commit and PR conventions

Use repo conventions if present.

Fallback commit format with ticket reference:

```text
<TICKET-REF> <type>(<scope>): <short description>
```

Fallback PR title with ticket reference:

```text
[<TICKET-REF>] <type>(<scope>): <short description>
```

Without a ticket reference:

```text
<type>(<scope>): <short description>
```

Types: `feat`, `fix`, `test`, `refactor`, `chore`, `docs`.

## Git safety

Before staging or committing:

- inspect `git status`;
- stage only files relevant to this task;
- do not stage unrelated user changes;
- if unrelated modified files exist, exclude them and mention them in the PR body;
- never force-push or amend commits unless explicitly instructed by repo workflow.

## Draft PR body

Follow the repo PR template if present.

If no template exists, use:

```md
## Summary

- ...

## Scope

Implemented:
- ...

Not included:
- ...

## Assumptions

- ...

## Testing

Ran:
- ...

Not run:
- ...

## Risks / follow-ups

- ...

## Review notes

- ...

## Blockers, if any

- ...
```

The PR body must clearly state:

- what changed
- what was intentionally not changed
- assumptions made
- checks run and results
- checks not run and why
- any blockers or human decisions needed
- whether the PR is ready for review or draft/WIP

## Final response / PR outcome

Return one of:

### PR created

```md
## Draft PR created

PR:
- <url>

Summary:
- ...

Checks run:
- ...

Risks / follow-ups:
- ...

Human review focus:
- ...
```

### Stopped without PR

```md
## Stopped — no PR created

Reason:
- ...

Decision or help needed:
- ...

Files inspected:
- ...

Evidence:
- ...

Recommended next action:
- ...
```

### Blocked after partial work

```md
## Draft PR created with blockers

PR:
- <url>

What is complete:
- ...

What is blocked:
- ...

Checks run:
- ...

Human decision needed:
- ...
```

## Stop conditions

Stop without implementation or PR if:

- critical requirements are unclear
- work no longer fits the agreed task
- architecture/auth/security/permission/data migration/public API changes are required
- tests fail after two focused attempts and the result is not useful
- failure cause is unknown
- unrelated files would need to be changed
- relevant code cannot be inspected
- validation cannot be performed
- CI/coverage requirements are likely to fail and cannot be addressed or clearly documented
- proceeding would require guessing on high-impact behaviour

When blocked, return useful context so a human can continue efficiently.
