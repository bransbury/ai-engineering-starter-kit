# Response for ship-foundation-first

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 120

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#121-121), lines 121 to 300

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#301-301), lines 301 to 450

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#451-451), lines 451 to 550

# Ship — Delivery routing for `confidenceBand`

## Assess

**Is it clear?** Yes — add a field to a known shape and propagate it through the stack.  
**Is it bounded?** Borderline — spans backend, shared contract, validation, UI, export, tests, docs.  
**Is it testable?** Yes — each layer has obvious proof.  
**Is it one PR or multiple?** Multiple PRs are safer here because the shared contract is moving.  
**Does it require Shape?** Lightweight shaping is sufficient inline.  
**Does it require a human decision?** No — the field semantics are given; no guardrailed areas are triggered.  
**Foundation-first?** Yes — the shared TypeScript contract and validation schema must stabilize before consumers build against them.

## Routing scorecard

| Dimension | Score | Confidence |
|---|---|---|
| Clarity | 4 | Medium — field name and consumers are stated |
| Boundedness | 3 | Medium — touches many layers |
| Verifiability | 4 | Medium — type checks, unit tests, integration tests |
| Risk safety | 5 | High — no auth/security/data/API guardrail |
| Independence | 2 | Medium — contract is unstable until wave 1 merges |
| Conflict safety | 3 | Medium — contract file is shared |
| Contract stability | 2 → 5 after wave 1 | Medium |
| Review burden | 4 if waved correctly | Medium |

## Route: Path D — Foundation-first parallel coordination

Confidence: **Medium-High**

A fully sequential plan is unnecessarily slow; a fully parallel plan is unsafe because the shared contract is moving. A two-wave foundation-first plan is the safest delivery path.

## Shaped tasks

| # | Task | Type |
|---|---|---|
| T1 | Add `confidenceBand` to the shared TypeScript contract + validation/schema | Foundation |
| T2 | Update backend API response to populate `confidenceBand` | Dependent (on T1) |
| T3 | Update results table UI to display `confidenceBand` | Dependent (on T1) |
| T4 | Update CSV export to include `confidenceBand` | Dependent (on T1) |
| T5 | Update affected tests and docs | Dependent (on T1; can absorb per-task test updates or run as integration/hardening) |

## Touch map

| Task | Expected files/modules | Shared contract/interface? | Conflict risk | Review burden | Decision |
|---|---|---|---|---|---|
| T1 | types/experiment.ts, schema/experiment.ts, validation/* | **Yes — defines it** | Low (sole owner) | Low | Wave 1 |
| T2 | api/experiments/handler.ts, tests | Consumes contract | Low after T1 | Low | Wave 2 |
| T3 | components/ResultsTable.tsx, tests | Consumes contract | Low after T1 | Low | Wave 2 |
| T4 | export/csv.ts, tests | Consumes contract | Low after T1 | Low | Wave 2 |
| T5 | docs/*, integration tests | Consumes contract | Low after T1 | Low | Wave 2 |

## Recommended execution waves

1. **Wave 1: T1** — Shared contract + validation/schema  
2. **Wave 2: T2, T3, T4, T5** (parallel, max 4 tasks)

### Why this is the recommended plan:

- **Foundation-first rationale:** The TypeScript contract and validation schema are consumed by every other task. If they move while consumers are being built, you get merge conflicts, type mismatches, or silent drift. Stabilizing them first in one small, easy-to-review PR eliminates that risk.
- **Review-burden rationale:** Wave 1 is a single small PR (types + schema + validation). Wave 2 PRs are independent leaf changes — reviewers never need to reason about the same contract across multiple PRs because it's already merged. Four concurrent PRs in wave 2 is acceptable because they touch disjoint files and distinct behaviours.
- **Why not fully sequential:** T2–T5 are independent of each other once the contract is stable. Sequencing them gains nothing and delays delivery.
- **Why not fully parallel:** T2–T5 would all be guessing at the contract shape or duplicating its definition, creating merge pain and review confusion.

## Next step

Merge T1, then launch T2–T5 in parallel (PPP Cloud per task, isolated worktree branches). Each wave-2 task bases off the commit where T1 merged.

Want me to produce the worktree agent contracts for each task, or execute T1 first?