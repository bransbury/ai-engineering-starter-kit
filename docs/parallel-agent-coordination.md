# Parallel Agent Coordination

This document explains how to coordinate multiple AI agents producing multiple PRs without branch chaos.

It supports the `ship` skill.

## The problem

As AI agents become more capable, engineers will increasingly run multiple agents at the same time.

That creates a new engineering problem:

> How do we safely coordinate multiple agents producing multiple PRs without creating chaos?

The risks are real:

- confusing branch names
- stale or inconsistent base branches
- hidden dependencies
- merge conflicts
- shared file ownership
- weak test isolation
- unclear PR ownership
- duplicate changes
- review fatigue
- agent drift from original intent

The answer is not “parallelize everything.”

The answer is:

> Parallelize only clear, bounded, independent, testable, low-risk work with explicit contracts.

## Core model

```text
Shape → Ship → PPP Cloud tasks → Draft PRs → Human review
```

- Shape clarifies and splits work.
- Ship chooses the safest execution path.
- PPP Cloud executes one bounded autonomous task.
- Parallel work happens only when Ship passes the safety gate.

## When parallel agent work is appropriate

Parallel work is appropriate when tasks are:

- clear
- bounded
- independently testable
- low or medium-low risk
- unlikely to touch the same files
- not dependent on unmerged work
- not making critical product/security/data/API decisions

Good examples:

- add tests for independent modules
- update docs in separate areas
- add empty states to independent pages
- apply a known validation pattern to separate components
- add coverage around existing behaviour

## When parallel agent work is not appropriate

Do not parallelize:

- new architecture decisions
- auth/security/permission changes
- database migrations
- public API contract changes
- shared data model changes
- shared component redesign
- feature flag or build/module enablement changes
- tasks touching the same coordination files
- tasks that depend on an unmerged foundation PR
- tasks with unclear proof

## First PR / foundation rule

For larger work, the first PR often establishes the pattern.

If a new implementation pattern is needed, do not parallelize implementation tasks until the first/foundation PR is complete and merged.

The foundation PR should establish:

- file locations
- naming conventions
- test style
- feature flag approach
- integration pattern
- validation method
- boundaries for follow-on tasks

After the foundation is merged, Ship can reassess follow-on tasks for parallel execution.

## Execution modes

Ship may choose:

| Mode | Use when |
|---|---|
| Local PPP | One focused task, human steering useful |
| PPP Cloud | One clear bounded autonomous task |
| Shape only | Work is not ready to build |
| Parallel worktree | Multiple independent tasks are safe to delegate |
| Stop | Critical human decision required |

## PR-size and route judgement

Do not ask agents to judge whether work is “small” in the abstract.

Use structural signals instead:

- behaviour count
- module spread
- contract changes
- proof complexity
- guardrail risk
- dependency order
- file overlap
- coordination-file ownership
- review capacity

Agents should mark confidence:

- **High** — inspected code or explicit shaped work
- **Medium** — clear task text and known patterns
- **Low** — inference only

Low-confidence tasks should not be parallelized.

## Route scorecard

Ship should score each task from 1–5:

| Dimension | Meaning |
|---|---|
| Clarity | Expected behaviour is explicit |
| Boundedness | Scope fits one coherent PR |
| Verifiability | Proof is clear and runnable |
| Risk safety | No unresolved guardrail decision |
| Independence | Does not depend on unmerged work |
| Conflict safety | Low expected file overlap/shared-file risk |

Route guidance:

- local PPP for clear work where human judgement is useful
- PPP Cloud for clear, bounded, low-risk, verifiable work
- Shape when clarity or boundedness is low
- parallel worktree mode when multiple tasks are independent, verifiable, and low conflict
- stop when guardrailed decisions are unresolved

## Parallel readiness scoring

Score each candidate task from 1–5.

| Dimension | Meaning |
|---|---|
| Clarity | Expected behaviour is explicit |
| Independence | Does not depend on unmerged work |
| Conflict risk | Likelihood of overlapping file changes; lower is better |
| Risk | Product/technical/security/release risk; lower is better |
| Verifiability | Proof is clear and runnable |

A task is a parallel candidate only if:

- clarity >= 4
- independence >= 4
- conflict risk <= 2
- risk <= 3
- verifiability >= 4

If a task fails this gate, sequence it or keep it human-led.

## Branch naming

Use deterministic branch names:

```text
ai/<ticket-ref>/<task-number>-<task-slug>
```

Examples:

```text
ai/AEP-2714/01-empty-state
ai/AEP-2714/02-validation-tests
```

If there is no ticket reference:

```text
ai/<feature-slug>/<task-number>-<task-slug>
```

Examples:

```text
ai/saved-reports/01-empty-state
ai/saved-reports/02-rename-report
```

## Base branch consistency

Every parallel task must record:

- base branch
- base SHA

Example:

```md
Base branch: main
Base SHA: abc123
```

If the base branch changes significantly before PRs merge, reassess affected worktrees.

## Worktree location

Worktrees should live outside the active working tree.

Example:

```text
../worktrees/<repo-name>-<task-number>-<task-slug>
```

This avoids polluting the engineer’s current branch.

## Touch map

Before parallelizing, create a touch map.

```md
| Task | Expected files/modules | Shared with other task? | Conflict risk | Decision |
|---|---|---|---|---|
```

Rules:

- same file usually means sequence
- shared coordination file means one owner
- unknown expected files means do not parallelize
- if an agent discovers it must edit a forbidden/shared file, it stops

## Coordination files

Coordination files require special handling.

Examples:

- package files and lockfiles
- build/config files
- routing tables
- global exports/index files
- shared schemas/contracts
- database migrations
- feature flag configuration
- shared test fixtures
- API specs

Only one task may own a coordination file.

If multiple tasks need the same coordination file, sequence them.

## Worktree task contract

Every parallel task needs a contract.

```md
# Worktree Agent Contract

## Original intent

...

## Task

...

## Scope

Do:
- ...

Do not:
- ...

## Base

Base branch:
- ...

Base SHA:
- ...

Branch:
- ...

Worktree:
- ...

## Expected files/modules

Allowed:
- ...

Avoid:
- ...

Stop if you need to edit:
- ...

## Dependencies

- ...

## Proof required

Primary:
- ...

Supporting:
- ...

## Stop conditions

Stop if:
- dependency missing
- file boundary needs to be crossed
- product/security/API/data decision needed
- tests fail after two focused attempts
- another task appears to overlap
- base branch/SHA is not available

## Output

Create a draft PR with:
- summary
- assumptions
- checks run
- checks not run
- risks
- human review focus
```

## PR ownership

All agent-generated parallel PRs should be draft PRs unless repo instructions say otherwise.

The engineer remains responsible for the PR.

Each PR body should include:

- generated by PPP Cloud
- owner/reviewer
- original intent
- scope
- assumptions
- checks run
- checks not run
- risks
- human review focus
- merge order

## Review fatigue

Do not create more parallel PRs than humans can review.

Defaults:

- default max parallel tasks: 2
- maximum without explicit approval: 3
- never more than 4

Prefer batches:

```text
Batch 1: foundation
Batch 2: two independent follow-ons
Batch 3: integration/hardening
```

## Merge order

Ship should always define merge order.

Example:

```md
1. Foundation PR
2. Independent follow-on PRs
3. Integration/hardening PR
4. Documentation/cleanup PR
```

Dependent PRs should not merge before their prerequisites.

## Ship dashboard

For multi-PR work, Ship should maintain or return a dashboard.

```md
## Ship dashboard

Base:
- Branch:
- SHA:

| Task | Branch | Worktree | Status | PR | Merge order | Review focus |
|---|---|---|---|---|---|---|

Not delegated:
| Task | Reason |
|---|---|

Risks:
- ...

Next actions:
- ...
```

## Capability fallback

Not every environment can create branches, worktrees, launch agents, or create PRs.

If capability is unavailable:

1. ask for permission if the tool can request it
2. degrade to a plan if permission is denied or unavailable
3. provide exact commands and task contracts
4. stop if safe execution is impossible

Parallel coordination should be useful even when it cannot execute everything automatically.

## Success criteria

Parallel agent coordination is working when:

- each PR has clear scope
- branch names are predictable
- base branch/SHA are recorded
- dependencies are explicit
- merge conflicts are rare
- draft PRs include proof and assumptions
- reviewers know what to review first
- agents stop instead of crossing unsafe boundaries
- the engineer’s local branch is not disturbed
