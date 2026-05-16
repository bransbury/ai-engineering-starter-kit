---
name: ppp
version: 0.3.0
description: "Plan. Patch. Prove. A lightweight interactive workflow for normal engineering tasks: inspect code, clarify only blocking questions, plan the smallest safe complete change, prove it, patch in small loops, review production readiness, and prepare a PR."
---

# Plan. Patch. Prove.

Use this skill for normal engineering tickets, bugs, small features, tests, UI changes, and small refactors.

Core loop:

```text
Inspect → Clarify → Plan → Prove → Patch → Review → PR
```

The engineer remains responsible for intent, judgement, validation, architecture, and final approval. AI accelerates the work inside those boundaries.

<!-- Similar section in ppp-cloud — keep core rules consistent -->
## Token discipline

Be concise. Inspect only relevant files, summarise instead of pasting code/logs, and avoid restating large specs or prior outputs. Prefer file paths, decisions, risks, checks run, and next actions.

Do not create task artifact files by default. Keep state in the conversation and code changes unless the user explicitly asks for notes.

## Interaction rules

This skill is interactive. When a decision or next action is needed, show a short menu.

Rules:

- Put the recommended action as option 1.
- Keep menus to 3–5 options.
- Treat `yes`, `y`, `go`, `continue`, `proceed`, `next`, `do it`, `run it`, `1`, and `option 1` as selecting option 1.
- If the user gives free text, treat it as instructions.
- Always state the current phase: Inspecting, Clarifying, Planning, Proving, Patching, Reviewing, PR handoff, or Blocked.

Menu format:

```text
Current phase:
<phase>

Recommended next action:
<action>

Choose an option:

1. <recommended action> — recommended
2. <alternative>
3. <alternative>
4. Stop here
```

<!-- Similar section in ppp-cloud — keep core rules consistent -->
## Hard rules

- Inspect relevant code before planning or editing.
- Follow repo guidance and nearby code/test conventions.
- Do not invent requirements.
- Ask only blocking/high-impact questions.
- Do not silently make product, architecture, security, auth, data migration, permission, tenancy, billing, or public API decisions.
- Do not touch unrelated files.
- Do not weaken tests or remove validation to make checks pass.
- Do not claim checks passed unless they actually ran.
- Do not shortcut required changes just to keep the diff small.
- Do not leave related code paths half-updated when correctness requires consistency.
- Stop after two focused failed fix attempts and hand useful context back to the user.

<!-- Similar section in ppp-cloud — keep core rules consistent -->
## Repo guidance

Before planning or editing, inspect repo guidance if available:

- `.github/copilot-instructions.md`
- `.github/instructions/**/*.instructions.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `README.md`
- package-specific README files near the changed code
- `.github/PULL_REQUEST_TEMPLATE.md`

Follow repo guidance for architecture, style, tests, validation commands, PR format, forbidden areas, and security/privacy rules. If no guidance exists, infer conventions from nearby code and tests.

If repo guidance conflicts with this skill, follow repo guidance unless it weakens safety, validation, or production readiness.

## Task fit gate

Before implementation, decide whether the task fits PPP.

PPP is suitable when the selected work can be completed as one focused PR with clear proof.

If the task is broad or underspecified, do not implement it directly. Examples:

- “build a new analytics dashboard”
- “add reporting”
- “improve onboarding”
- “build the new permissions system”
- “migrate this service”

If too large, offer:

1. Identify the smallest PPP-ready task — recommended
2. Implement only the smallest useful first increment
3. Ask for a fuller spec
4. Stop here

If the user provides a large spec, summarise the goal briefly, identify the smallest PPP-ready task, ask the user to confirm, and proceed only with that task. For multi-PR or multi-slice work, recommend a feature-slicing workflow.

## 1. Inspect

Read the ticket and inspect relevant code before planning.

Return a concise understanding:

```md
## Understanding

Intended behaviour:
- ...

Current behaviour:
- ...

Files/modules inspected:
- ...

Existing patterns to follow:
- ...

Assumptions:
- ...

Open questions:
- ...

Risks:
- ...
```

Use a codebase inspection table when file paths or modules matter:

| Area | File/module | Status | Evidence | Notes |
|---|---|---|---|---|

Statuses:

- Confirmed — inspected and exists
- Inferred — likely, but not inspected
- Proposed new — does not exist yet and is proposed
- Missing — expected but not found

Do not present inferred paths as confirmed. If codebase inspection is unavailable, say so and provide an implementation pack that must be verified in the IDE before coding.

## 2. Clarify

Ask only questions that materially affect implementation, proof, risk, or acceptance.

Limits:

- Default maximum: 5 questions
- Complex task maximum: 10 questions
- Never exceed 10 unless the user asks for exhaustive discovery

If a question can be resolved by inspecting code or tests, inspect instead of asking.

Prefer a recommended default when the choice is low-risk, reversible, internal, or already implied by repo patterns.

Use this format:

```md
## Questions before implementation

Q1. <question>
Why it matters: <reason>
Recommended answer: <safe default>

Options:
1. Use recommended answer — recommended
2. Provide a different answer
3. Mark out of scope
4. Defer and inspect existing pattern
```

If the user accepts the recommended answer, document it as a decision and continue. If the answer affects architecture, security, data, auth, permissions, public APIs, or user-facing semantics, get clarity before proceeding.

## 3. Plan

Propose the smallest safe complete change that satisfies the selected task.

```md
## Plan

Smallest safe complete change:
- ...

Files to change:
- ...

Tests/checks to add or update:
- ...

Validation:
- ...

Risks:
- ...

Will not change:
- ...
```

The plan must follow repo conventions, components, styling, architecture, and design patterns.

Do not plan unrelated refactors. Do not avoid legitimate required files merely to keep the diff small. If the work becomes larger or riskier than expected, stop and re-plan or recommend splitting.

## 4. Prove

Define proof before implementation.

Choose exactly one primary proof and up to three supporting checks. The primary proof must directly validate the changed behaviour. Lint/typecheck alone is not sufficient for behavioural changes unless no behavioural proof is practical.

Use the lowest-cost proof that gives meaningful confidence:

- Static/local sanity: lint, typecheck, build affected package
- Targeted unit/component test: default for logic and UI behaviour
- Focused integration/API/contract test: for cross-module or API behaviour
- E2E/manual workflow: when a real workflow is needed
- Full suite/expensive checks: only when repo convention, risk, or user request requires it

Ask before running expensive integration/E2E/full-suite checks unless the repo explicitly requires them.

```md
## Proof plan

Primary proof:
- ...

Supporting checks:
- ...

Commands:
- ...

Manual verification, if needed:
- ...

Not running:
- ...
```

Prefer red-green testing where practical.

## Automated testing and coverage

Before patching, inspect whether the affected area has automated tests or CI coverage expectations.

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

If CI/CD enforces unit coverage, do not recommend a normal PR that is likely to fail coverage. Add tests or flag the blocker first.

## 5. Patch

Implement in small validated loops:

```text
small change → run proof/check → inspect result → fix → review diff → continue
```

Rules:

- stay within the agreed task and plan;
- update all related code paths required for correctness;
- preserve existing behaviour unless the ticket requires changing it;
- avoid unrelated refactors and opportunistic cleanup;
- validate after meaningful changes.

If the work becomes larger, riskier, or different from the plan, stop and re-plan.

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

After two failed attempts, stop and hand back:

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
Ask a peer/senior engineer to inspect, or debug manually with this evidence.

Choose an option:

1. Produce a debugging handoff — recommended
2. Try one more fix with your guidance
3. Revert last attempt
4. Stop here
```

## 7. Review

When implementation appears complete, review as QA and production reviewer.

### Blocking — must fix before normal PR

- Task is not satisfied
- Acceptance criteria not covered
- Required proof/tests missing or failing
- CI/PR checks likely to fail
- Unit/automated coverage requirement not met where applicable
- Security/privacy/auth/permission risk unresolved
- Related code paths left inconsistent
- Unrelated files changed
- Engineer cannot explain the change

### Should fix if safe and in scope

- Edge cases weakly handled
- Error/loading/empty states incomplete where relevant
- Existing patterns not followed
- Accessibility not considered for UI changes
- Performance risk not considered
- Tests assert implementation rather than behaviour
- Unnecessary complexity added

If three or more “Should fix” items apply, address them before PR unless the user explicitly chooses to defer them.

### Nice to have / follow-up

- Additional refactoring
- Extra docs/comments
- Broader E2E coverage
- Non-blocking polish

If a blocking item fails, do not finish. Fix it if safe and in scope, rerun proof, and review again. If not safe, report the blocker.

When review fails:

```text
Current phase:
hardening-needed

Recommended next action:
Fix failed review items.

Choose an option:

1. Fix failed review items — recommended
2. Show review details
3. Mark follow-ups and stop
4. Stop here
```

## 8. PR handoff

When production readiness is `Ready`, do not end without a PR next step.

Before preparing the PR, inspect repo PR guidance:

- `.github/PULL_REQUEST_TEMPLATE.md`
- `CONTRIBUTING.md`
- `AGENTS.md`
- repo/team-specific PR guidance

Follow repo PR and commit conventions if present.

## Ticket reference

Use “ticket reference” generically. Jira is one example.

Look for a ticket reference in:

1. branch name
2. user task/ticket text
3. recent commit messages if relevant
4. ask the user

Examples:

- Jira: `AEP-2714`, `MONE-61005`
- Linear: `ENG-123`
- GitHub issue: `#1234`

Do not invent a ticket reference.

If none is found:

```text
Current phase:
PR handoff

I could not find a ticket reference in the branch name or task context.

Recommended next action:
Enter the ticket reference so I can create the commit and PR title correctly.

Choose an option:

1. Enter ticket reference — recommended
2. Continue without a ticket reference
3. Prepare PR title/body only
4. Stop here
```

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

Do not commit until:

- production readiness is `Ready`, or user explicitly asks for draft/WIP;
- ticket reference has been found or user chose to continue without one;
- commit message and PR title have been shown.

## Git safety

Before staging or committing:

- inspect `git status`;
- stage only files relevant to this task;
- do not stage unrelated user changes;
- if unrelated modified files exist, list them and ask before proceeding;
- never force-push or amend commits unless explicitly asked.

## PR menu

```text
Current phase:
PR handoff

Recommended next action:
Stage changes, commit, and create PR.

Choose an option:

1. Stage changes, commit, and create PR — recommended
2. Explain changes before committing
3. Show commit message and PR body first
4. Prepare PR title/body only
5. Stop here
```

### Explain changes option

If the user selects “Explain changes before committing”, provide a concise two-minute walkthrough:

- what changed and why
- how the pieces fit together
- non-obvious decisions
- proof/checks used
- what to say if asked “walk me through this” in review

After the explanation, return to the PR handoff menu.

If option 1 is selected:

1. inspect `git status`;
2. stage only relevant files;
3. commit using the agreed message;
4. create a PR using repo template if available;
5. return the PR URL.

If the harness cannot run git or create PRs, say so and provide exact `git add`, `git commit`, and `gh pr create` commands.

## Default PR body

If no repo template exists:

```md
## Summary

- ...

## Changes

- ...

## Testing

- ...

## Risks / follow-ups

- ...

## Screenshots

<include if UI changed>
```

## Final response

When done, return:

```md
## Completed

What changed:
- ...

Files changed:
- ...

Checks run:
- ...

Validation result:
- ...

Production readiness:
- Ready / Not ready

Risks / follow-ups:
- ...

## Commit and PR handoff

Ticket reference:
- `<ticket reference or not found>`

Suggested commit message:
- ...

Suggested PR title:
- ...

Suggested PR body:
- ...

Current phase:
PR handoff

Recommended next action:
Stage changes, commit, and create PR.

Choose an option:

1. Stage changes, commit, and create PR — recommended
2. Explain changes before committing
3. Show commit message and PR body first
4. Prepare PR title/body only
5. Stop here
```

Do not say the work is complete if proof is missing or failing.

## Stop conditions

Stop and ask before continuing if:

- critical requirements are unclear
- work no longer fits the agreed task
- architecture/auth/security/permission/data migration/public API changes are required
- tests fail after two focused attempts
- failure cause is unknown
- unrelated files would need to be changed
- relevant code cannot be inspected
- validation cannot be performed
- CI/coverage requirements are likely to fail and cannot be addressed within scope

When blocked, hand useful context back to the user so they can investigate or get help from a peer.
