---
name: shape
description: "Shape rough work into clear, scoped, testable PR-sized tasks for PPP, PPP Cloud, or Ship orchestration."
---

# Shape

Use this skill to turn a rough ticket, bug, feature idea, or spec into clear, scoped, testable work.

Shape does not implement code. Shape makes the work ready to ship.

Core loop:

```text
Understand → Clarify → Scope → Slice → Route
```

Shape is for the work before building:

- clarify intent
- expose ambiguity
- define non-goals
- identify proof
- split into PR-sized tasks
- recommend whether work should go to `/ppp`, `/ppp-cloud`, `/ship`, or stop for a human decision

## Principle

Shape the work before working the change.

Prefer a small clear first PR over a large vague implementation.

Prefer “not ready” over confident guessing.

## Token discipline

Be concise.

- Do not restate long specs.
- Summarise large inputs.
- Preserve important constraints, assumptions, and risks.
- Prefer tables for task maps.
- Do not create artifacts unless the user asks or the work is multi-PR and needs coordination state.

## When to use Shape

Use Shape when:

- the ticket is vague
- the work seems bigger than one PR
- acceptance criteria are missing
- the engineer is not sure where to start
- cloud-agent delegation may be useful but scope is unclear
- multiple PRs may be needed
- the task may need architecture, security, data, migration, API, or product decisions

Do not use Shape for a tiny clear task that is already ready for PPP.

## Hard rules

- Do not write code.
- Do not create implementation tasks before understanding the goal.
- Do not invent requirements.
- Ask only blocking or high-impact questions.
- Use recommended defaults for low-risk ambiguity.
- Stop for critical product, security, auth, data, migration, tenancy, billing, or public API decisions.
- Always identify the smallest safe first PR when possible.
- Every proposed task must have scope, non-goals, proof, and dependencies.
- Do not mark tasks independent without evidence.
- Do not recommend parallel execution unless tasks are clear, low-risk, independently provable, and unlikely to conflict.

## Question policy

Ask as few questions as possible.

Limits:

- Default maximum: 5 questions
- Hard maximum: 10 questions

Only ask questions that materially affect:

- user-visible behaviour
- acceptance criteria
- data model or persistence
- permissions or security
- public API contract
- rollout/release risk
- proof/validation
- task boundaries

For each question, provide:

- why it matters
- a recommended answer if safe
- whether it blocks shaping

Use this format:

```md
## Questions

| # | Question | Why it matters | Recommended answer | Blocks shaping? |
|---|---|---|---|---|
| 1 | ... | ... | ... | Yes/No |
```

If high-impact ambiguity remains, still provide a partial shape, but mark status as `needs-human-decision`.

## 1. Understand

Summarise the work.

Return:

```md
## Understanding

Goal:
- ...

Current problem:
- ...

Expected behaviour:
- ...

Likely users/systems affected:
- ...

Relevant constraints:
- ...

Areas unclear:
- ...
```

If the input is a long spec, summarise it into the smallest useful delivery intent. Do not duplicate the full spec.

## 2. Clarify

Separate:

- known facts
- assumptions
- open questions
- non-goals

Use:

```md
## Facts, assumptions, and open questions

### Known facts
- ...

### Assumptions
- ...

### Open questions
- ...

### Non-goals
- ...
```

If an assumption is low-risk and reversible, continue with it and record it.

If an assumption affects product behaviour, security, auth, data, migrations, tenancy, billing, or public APIs, stop and ask.

## 3. Scope

Define what is in scope and out of scope.

Create acceptance criteria that are specific, testable, and behaviour-oriented.

Use stable IDs:

- `AC1`, `AC2`, `AC3` for acceptance criteria
- `R1`, `R2`, `R3` for requirements if needed

```md
## Scope

In scope:
- ...

Out of scope:
- ...

## Acceptance criteria

| ID | Acceptance criterion | Proof idea |
|---|---|---|
| AC1 | ... | ... |
```

Do not create acceptance criteria for invented requirements.

## 4. Slice

Split the work into PR-sized tasks.

Always identify the first PR.

The first PR should:

- be the smallest safe useful increment
- establish implementation/test pattern where needed
- reduce uncertainty early
- avoid broad refactoring
- be reviewable as one PR
- have clear proof

For each task include:

```md
| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | Expected files/modules | PR-size score | Split? | Risk |
|---|---|---|---|---|---|---|---|---:|---|---|
```

Task IDs should be stable:

```text
T1, T2, T3
```

## PR-size assessment

Before finalising each task, assess whether it is PR-sized.

A PR-sized task is not measured by file count alone.

A task is PR-sized when it has:

- one primary behaviour or one tightly related behaviour group
- clear acceptance criteria
- clear proof
- limited architectural decision-making
- no unresolved guardrail decisions
- a reviewable diff
- a coherent rollback story
- no dependency on unmerged work unless explicitly sequenced

A task is probably too large when it has:

- multiple independent behaviours
- several unrelated modules
- new API, data, auth, security, migration, tenancy, billing, or public contract decisions
- unclear proof
- mixed refactor and feature work
- multiple reviewers needed for different concerns
- high merge-conflict risk

Use structural signals rather than vague effort estimates.

Agents are better at judging:

- behaviour count
- module spread
- contract changes
- proof complexity
- guardrail risk
- dependency and conflict signals

Agents are worse at judging:

- elapsed time
- exact file count before inspection
- whether something is “easy”
- whether a task is “small” without evidence

Score each proposed task:

| Dimension | Score 1 | Score 3 | Score 5 |
| --- | --- | --- | --- |
| Behaviour count | one behaviour | 2–3 related behaviours | many behaviours/workflows |
| Module spread | one area | 2–3 related areas | many modules/services |
| Contract change | none | internal contract | public API/schema/data model |
| Proof complexity | one clear proof | multiple checks | unclear or expensive proof |
| Risk | low | medium | high/guardrailed |

Guidance:

- **5–8 total:** likely one focused PR
- **9–13 total:** possible one PR, but consider splitting
- **14+ total:** split before implementation
- **Any 5 in Contract change or Risk:** human-led, shape further, or stop for a decision

If the PR-size score suggests splitting, split the task before routing unless there is a strong reason to keep it together.

## Evidence and confidence

When codebase access is available, inspect relevant files before scoring module spread, expected files, proof, and conflict risk.

For each recommendation, mark confidence:

- **High** — based on inspected code or explicit spec
- **Medium** — based on clear task text and known patterns
- **Low** — based on inference; validate before execution

Do not use low-confidence analysis to recommend parallel execution.

## 5. Route

Recommend the safest execution path for each task.

Execution modes:

- `/ppp` — human-led IDE work for one focused task
- `/ppp-cloud` — autonomous single-task execution, draft PR or blocker
- `/ship` — coordinate delivery across one or more tasks
- `human decision` — stop and resolve before build
- `sequence` — do after another task/PR
- `parallel candidate` — can be considered by Ship for worktree delegation

Criteria:

### Recommend `/ppp` when

- the task is clear enough to build
- human steering is useful
- UI/product judgement may be needed
- risk is medium
- the engineer is already working in the IDE

### Recommend `/ppp-cloud` when

- the task is clear, bounded, low-risk, and testable
- existing patterns are obvious
- no critical human decision is needed
- the task can produce one focused draft PR or blocker

### Recommend `/ship` when

- there are multiple tasks
- dependency order matters
- parallel work may be possible
- worktree/cloud-agent coordination may be useful
- the engineer wants the system to decide how to deliver

### Recommend `human decision` when

- product behaviour is unclear
- auth/security/permission decisions are needed
- data migration/model decisions are needed
- public API contract changes are needed
- architecture direction is unclear
- proof cannot be defined

## Delegation and parallel readiness

For each task, classify:

| Task ID | Clarity | Independence | Conflict risk | Risk | Verifiability | Recommendation | Evidence |
| ------- | ------: | -----------: | ------------: | ---: | -----------: | -------------- | -------- |

Scores are 1–5.

Guidance:

- Clarity: 5 means expected behaviour is explicit.
- Independence: 5 means no dependency on unmerged work.
- Conflict risk: 1 is low, 5 is high.
- Risk: 1 is low, 5 is high.
- Verifiability: 5 means proof is obvious and automatable.

Parallel candidate only if:

- clarity >= 4
- independence >= 4
- conflict risk <= 2
- risk <= 3
- verifiability >= 4
- confidence is Medium or High

Do not mark a task as a parallel candidate if it touches shared coordination files unless it owns them exclusively.

Coordination files include:

- package files and lockfiles
- build/config files
- routing tables
- global exports/index files
- shared schemas/contracts
- database migrations
- feature flag configuration
- shared test fixtures
- API specs

## Output

Return one of:

- `ready-for-ppp`
- `ready-for-ppp-cloud`
- `ready-for-ship`
- `needs-human-decision`
- `too-broad-shape-first`
- `not-ready`

Use this final format:

```md
## Shape result

Status:
- ...

Recommended next action:
- ...

Reason:
- ...

Confidence:
- High / Medium / Low

## Shaped work
...

## First PR

Task:
- ...

Mode:
- `/ppp` / `/ppp-cloud` / `/ship` / human decision

Why first:
- ...

Proof:
- ...

PR-size assessment:
- ...

## Follow-on tasks
...

## Delegation assessment
...

## Human decisions needed
...

## Suggested next prompt

    /ship <summary of shaped work>
```

If there is only one clear task, suggest `/ppp` or `/ppp-cloud` directly instead of `/ship`.

If multiple tasks exist, suggest `/ship`.

## Stop conditions

Stop and ask for human input if:

- there are contradictory acceptance criteria
- the expected behaviour is undefined
- architecture direction is required
- auth/security/permissions are affected
- data migration/model changes are required
- public API contract changes are required
- tenancy/billing behaviour is affected
- proof cannot be defined
- the work cannot be split into safe PR-sized tasks

When stopped, return:

```md
## Stopped — human decision required

Reason:
- ...

Decision needed:
- ...

Recommended options:
1. ...
2. ...
3. ...

Recommended option:
- ...

What can be shaped now:
- ...
```
