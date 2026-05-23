---
name: ship
version: 0.8.0
description: "Choose and coordinate the safest delivery path for AI-assisted engineering work: shape if needed, run PPP, use PPP Cloud, or coordinate parallel worktree tasks."
---

# Ship

Use this skill when you want the system to decide how to deliver a task safely.

Ship is the coordination layer.

It decides whether to:

- shape the work first
- execute one local human-led task with PPP behaviour
- execute one autonomous task with PPP Cloud behaviour
- coordinate multiple autonomous tasks in isolated worktrees
- stop for a human decision

Ship solves the advanced problem:

> Coordinate multiple AI agents producing multiple PRs without branch chaos.

## Relationship to other skills

- `/shape` clarifies and splits rough work into PR-sized tasks.
- `/ppp` executes one human-led IDE task safely.
- `/ppp-cloud` executes one bounded autonomous task as a draft PR or blocker.
- `/ship` chooses and coordinates the safest delivery path.

Users should not need to choose between PPP, PPP Cloud, or parallel worktree mode. Ship should choose the safest viable path and proceed where the environment supports it.

## Core loop

```text
Assess → Shape if needed → Route → Execute → Coordinate → Report
```

## Principle

Autonomy should increase only when clarity, independence, proof, and safety increase.

Prefer:

- one good PR over many noisy PRs
- sequencing over unsafe parallelism
- the shortest safe delivery plan over a longer fully sequential plan
- stopping over guessing
- draft PRs over false confidence
- explicit contracts over implicit handoffs

## Token discipline

Be concise.

- Do not restate long specs.
- Summarise large inputs.
- Keep task contracts compact.
- Do not duplicate PPP or PPP Cloud instructions; reference them.
- Create coordination artifacts only for multi-PR or parallel work.

## Capability and permission handling

Ship should determine what the current environment supports as it works.

Useful capabilities include:

- read files
- edit files
- run commands
- inspect git status
- create branches
- create worktrees
- create commits
- create PRs
- launch subagents/background agents

If a capability is missing but can be requested, ask for permission at the point of need.

If permission is granted, proceed.

If permission is denied or unavailable, gracefully degrade:

- execute in the current session if safe
- produce a worktree/agent task plan
- output exact commands for the user
- stop with a blocker if safe execution is impossible

Do not repeatedly ask the user to choose execution modes. Ask only for missing permissions or critical decisions.

## Hard rules

- Inspect before routing.
- Shape unclear work before building.
- Do not invent requirements.
- Do not make critical product/security/data/API decisions.
- Do not parallelize tasks with unresolved dependencies.
- Do not parallelize tasks with likely shared-file conflicts.
- Do not create worktrees from an unknown or dirty base without handling it.
- Do not stage or commit unrelated user changes.
- Do not launch more parallel tasks than humans can review.
- When multiple safe routes exist, recommend the plan with the fewest serial execution waves.
- Always look for dependency-aware parallel waves before recommending a fully sequential plan.
- Default maximum parallel tasks: 2.
- Maximum parallel tasks without explicit approval: 3.
- Never run more than 4 parallel tasks.
- Stop after two focused fix attempts per autonomous task.
- All autonomous or worktree-generated PRs should be draft unless repo instructions say otherwise.

## 1. Assess

Read the user task/spec or shaped work.

Determine:

- Is it clear?
- Is it bounded?
- Is it testable?
- Is it one PR or multiple PRs?
- Does it require Shape?
- Does it require a human decision?
- Does it involve guardrailed areas?
- Are there independent parallelizable tasks?
- What is the shortest safe dependency-aware execution plan?

Guardrailed areas:

- product behaviour ambiguity
- architecture direction
- auth/security/permissions
- privacy/compliance
- data model or migration
- public API contract
- tenancy or billing
- destructive/irreversible changes
- new dependencies
- build/module enablement
- shared schemas/contracts

If guardrailed decisions are required, stop and ask.

## 2. Shape if needed

If the work is broad, vague, or multi-PR, apply Shape behaviour before routing.

Ship can perform lightweight shaping directly, but should preserve the Shape output fields:

- goal
- facts
- assumptions
- open questions
- non-goals
- acceptance criteria
- first PR
- follow-on tasks
- dependencies
- proof
- expected files/modules
- delegation assessment
- PR-size assessment
- confidence

If more than 10 questions would be needed, stop and recommend a dedicated Shape pass.

Ask at most 10 questions total.

Prefer 0–3 questions. Use recommended defaults for low-risk ambiguity.

## Routing scorecard

Before selecting the path, score the work from 1–5.

Use inspected code where possible. If a score is inferred from task text only, mark confidence as lower.

| Dimension | Meaning |
|---|---|
| Clarity | Expected behaviour is explicit |
| Boundedness | Scope fits one coherent PR |
| Verifiability | Proof is clear and runnable |
| Risk safety | No unresolved product/security/data/API guardrail decision |
| Independence | Does not depend on unmerged work |
| Conflict safety | Low expected file overlap/shared-file risk |

Confidence:

- **High** — based on inspected code or explicit shaped work
- **Medium** — based on clear task text and known repo patterns
- **Low** — based on inference; avoid autonomous or parallel execution

### Route thresholds

Route to local PPP when:

- clarity >= 3
- boundedness >= 3
- verifiability >= 3
- no guardrail blocker
- human judgement or steering is useful

Route to PPP Cloud when:

- clarity >= 4
- boundedness >= 4
- verifiability >= 4
- risk safety >= 4
- no guardrail blocker
- existing patterns are available
- confidence is Medium or High

Route to Shape when:

- clarity <= 2
- boundedness <= 2
- proof is unclear
- the work appears to contain multiple independent behaviours
- PR-size assessment says split
- confidence is Low and the work is not safe to execute

Route to parallel worktree coordination when:

- shaped work contains 2+ parallel candidates
- each candidate has independence >= 4
- each candidate has conflict safety >= 4
- each candidate has verifiability >= 4
- each candidate has Medium or High confidence
- no shared coordination-file conflict exists
- review capacity can handle the PR count

Stop for human decision when:

- risk safety <= 2
- product behaviour is unresolved
- auth/security/permissions are affected
- data model or migration decisions are needed
- public API contract is unclear
- architecture direction is unclear

Every Ship output must include the routing scorecard, selected route, and confidence.
Every multi-task Ship output must also include the recommended execution waves.

## 3. Route

Choose one path.

Do not ask the user to choose unless there is a critical decision or permission gap.

### Path A — Local PPP execution

Choose when:

- task is one focused PR
- user is in the IDE/current session
- human steering is useful
- risk is medium
- UI/product judgement may be needed

Apply PPP behaviour:

```text
Inspect → Clarify → Plan → Prove → Patch → Validate → Review → PR
```

### Path B — Autonomous PPP Cloud execution

Choose when:

- task is one focused PR
- expected behaviour is clear
- risk is low or medium-low
- proof is obvious
- existing patterns are available
- no critical decision is needed

Apply PPP Cloud behaviour:

```text
Inspect → Decide → Plan → Prove → Patch → Validate → Review → Draft PR
```

### Path C — Shape only

Choose when:

- work is broad
- expected behaviour is unclear
- multiple PRs are likely
- dependencies need mapping
- task cannot safely be routed yet

Return shaped work and recommended next action.

### Path D — Parallel worktree coordination

Choose when:

- Shape has produced multiple PR-sized tasks
- at least two tasks are independent
- tasks are clear and testable
- conflict risk is low
- proof is defined for each task
- review load is acceptable
- branch/worktree/agent capabilities are available or can be requested

Each parallel task uses PPP Cloud behaviour.
Recommend Path D when it materially shortens the safe delivery plan compared with fully sequential execution.

### Path E — Stop for human decision

Choose when:

- critical behaviour is undefined
- security/auth/data/API/migration decisions are required
- architecture direction is unclear
- proof cannot be defined
- safe routing is impossible

## 4. Parallel safety gate

Before parallel execution, pass this gate.

```md
## Parallel safety gate

Base:
- Branch:
- SHA:
- Working tree clean? Yes/No

Tasks:
- ...

Checks:
- [ ] Each task has clear scope
- [ ] Each task has explicit non-goals
- [ ] Each task has proof
- [ ] Dependencies are resolved
- [ ] File overlap is low
- [ ] Coordination files have one owner
- [ ] Max parallel task limit respected
- [ ] Branch names are deterministic
- [ ] Worktree paths are isolated
- [ ] Merge order is defined
- [ ] Stop conditions are included
```

If any check fails, sequence the work, shape again, or stop.

## 5. Branch and worktree rules

Use deterministic branch names:

```text
ai/<ticket-ref>/<task-number>-<task-slug>
```

If no ticket reference exists:

```text
ai/<feature-slug>/<task-number>-<task-slug>
```

Examples:

```text
ai/AEP-2714/01-empty-state
ai/saved-reports/02-validation-tests
```

Use isolated worktree paths outside the active working tree, for example:

```text
../worktrees/<repo-name>-<task-number>-<task-slug>
```

Each worktree task contract must include:

- base branch
- base SHA
- branch name
- worktree path
- task scope
- non-goals
- expected files/modules
- files/modules to avoid
- proof required
- stop conditions
- PR title/body expectation

Do not create worktrees if the current working tree has unrelated uncommitted changes that could be lost or confused. Ask permission or provide commands.

## 6. Dependency and conflict rules

Classify tasks as:

- foundation
- independent
- dependent
- integration/hardening

Rules:

- foundation runs first
- dependent tasks wait for dependencies
- independent tasks may run in parallel after dependencies are satisfied
- integration/hardening runs last
- tasks touching the same files should usually be sequenced
- coordination files may have only one owner
- unexpected need to edit a forbidden/shared file requires stop and report

Build an execution-wave plan:

- wave 1 contains the smallest required foundation work
- each later wave contains every safe task whose dependencies are already satisfied
- prefer broader safe waves over unnecessary serial execution
- do not delay an independent task to preserve task-number order
- if two plans are equally safe, recommend the one with fewer waves
- if a parallel wave would create review overload, reduce the wave size but still prefer the most efficient safe grouping

Use this format:

```md
## Recommended execution waves

1. Wave 1: T1
2. Wave 2: T2, T3, T4
3. Wave 3: T5, T6

Why this is the recommended plan:
- ...
```

Create a touch map:

```md
| Task | Expected files/modules | Shared with other task? | Conflict risk | Decision |
|---|---|---|---|---|
```

## 7. Worktree task contract

Every parallel task must receive a contract:

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

## 8. Execution

### Single-task execution

If Path A or B is selected, proceed using PPP or PPP Cloud behaviour.

If the current environment cannot perform required actions, ask permission at the point of need or degrade gracefully.

### Parallel execution

If Path D is selected:

1. inspect git status and base branch
2. record base branch and SHA
3. create or request permission to create worktrees
4. create deterministic branches
5. launch or prepare each PPP Cloud task
6. ensure each task creates a draft PR or blocker
7. produce a ship dashboard
8. define merge order and review focus

When Path D is not selected for safety reasons but some later waves can still run in parallel, return the most efficient safe mixed plan instead of a fully serial list.

If the environment cannot launch background agents, create worktrees and task contracts if possible, or provide exact commands and prompts.

Do not treat failure to launch agents as failure of Ship. Degrade to a manual parallel plan when needed.

## 9. Ship dashboard

For multi-task or parallel work, return:

```md
## Ship dashboard

Base:
- Branch:
- SHA:

Execution mode:
- local / autonomous / parallel worktree / shaped only / stopped

Recommended execution waves:
- ...

| Task | Branch | Worktree | Mode | Status | PR | Merge order | Review focus |
|---|---|---|---|---|---|---|---|

Not delegated:
| Task | Reason |
|---|---|

Routing scorecard:
- ...

Confidence:
- ...

Risks:
- ...

Next actions:
- ...
```

## 10. Stop formats

### Shape needed

```md
## Stopped — shape needed

Reason:
- ...

What is unclear:
- ...

Recommended next action:
- Run Shape on this work.

Suggested first questions:
1. ...
```

### Human decision required

```md
## Stopped — human decision required

Reason:
- ...

Decision needed:
- ...

Why it matters:
- ...

Recommended options:
1. ...
2. ...
3. ...

Recommended option:
- ...
```

### Capability unavailable

```md
## Stopped or degraded — capability unavailable

Needed capability:
- ...

What I can do instead:
- ...

Exact commands or task contracts:
- ...
```

## Output

Always return one of:

- `executed-local-ppp`
- `executed-autonomous-ppp-cloud`
- `shaped-only`
- `parallel-plan-created`
- `parallel-execution-started`
- `stopped-human-decision`
- `stopped-capability-unavailable`
- `stopped-unsafe`

For every output include:

- routing scorecard
- selected route
- confidence
- reason for route
- assumptions
- checks/proof
- risks
- next actions
- PR links if created
- blockers if any
