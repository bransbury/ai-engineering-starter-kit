# Response for ship-foundation-first

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#100-100), lines 100 to 300

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#300-300), lines 300 to 450

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#450-450), lines 450 to 600

## Ship assessment

**Task**: Add `confidenceBand` field to experiment results and show in dashboard.

The prompt explicitly flags that the shared contract and validation base will be moving — this is a foundation-first constraint. I'll route after scoring.

---

## Routing scorecard

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 4 | Field name and affected layers are explicit |
| Boundedness | 2 | Multi-layer: API, contract, validation, UI, export, tests/docs |
| Verifiability | 4 | Type checks, unit tests, visual verification |
| Risk safety | 4 | No auth/security/data migration concerns |
| Independence | 2 | All consumer tasks depend on a contract that is still moving |
| Conflict safety | 3 | Layers touch different files, but all share the same contract |
| Contract stability | 1 | Explicitly flagged as unstable and moving |
| Review burden | 3 | Multiple PRs, but sequenceable into manageable waves |

**Confidence**: Medium — no codebase to inspect; scored from task text and standard patterns.

**Route: Path D — Parallel worktree coordination, foundation-first.**

Boundedness is low, but that is because the work spans layers — not because the scope is unclear. Each layer is a clear, bounded task. Shape is not needed. The contract stability score (1) and the explicit prompt constraint rule out starting parallel execution immediately. Wave 1 must land and stabilize before anything else runs.

---

## Shape (lightweight)

| | |
|---|---|
| **Goal** | Add `confidenceBand` to experiment result type, API response, validation, results table UI, and CSV export |
| **Facts** | Shared TypeScript contract and validation base are moving; review burden matters |
| **Non-goals** | Changing the meaning or derivation logic for `confidenceBand` (assumed to be computed upstream); no new backend computation needed beyond passing the field through |
| **Assumptions** | `confidenceBand` is a string or enum (e.g. `"low" \| "medium" \| "high"`); if it is a numeric range, T1 will need a decision before proceeding |
| **Open question** | What is the type of `confidenceBand`? If undefined, T1 should stop and report before merging |
| **Acceptance criteria** | Field appears in TypeScript type; validated at API boundary; shown in results table; included in CSV export; existing tests pass; new field is tested |

---

## Touch map

| Task | Expected files/modules | Shared contract? | Conflict risk | Review burden | Decision |
|---|---|---|---|---|---|
| T1 — Contract + validation | Shared experiment result type, schema/validation module, validation tests | **Owner** — defines it | Low | Low — one focused PR | Foundation; must merge first |
| T2 — Backend API | API response serializer/handler, API integration tests | Consumer of T1 | Low | Medium | Depends on T1 |
| T3 — Results table UI | Results table component, snapshot/unit tests | Consumer of T1 | Low | Medium | Depends on T1; independent from T2 |
| T4 — CSV export | Export module, export tests | Consumer of T1 | Low | Low | Depends on T1; can run after T2+T3 |
| T5 — Docs | Docs only | None | None | Low | Depends on confirmed behaviour |

---

## Recommended execution waves

```
Wave 1:  T1  —  Contract + validation (foundation)
Wave 2:  T2  +  T3  —  Backend API  |  Results table UI
Wave 3:  T4  +  T5  —  CSV export   |  Docs
```

**Why this plan:**
- Contract stability is 1. No consumer task can safely begin until T1 is merged and the type/schema is locked. Parallelizing before that point would cause every consumer branch to rebase against a moving interface.
- T2 and T3 are independent after T1 merges: they touch different files and neither consumes the other's output. Two PRs in Wave 2 is within the default parallel limit and produces two clean, reviewable PRs.
- T4 (CSV export) is light and data-layer only. Reviewers benefit from seeing T2 merged first to confirm the API shape is final before reviewing export. Wave 3 also absorbs docs at low review cost.
- Docs last: behaviour should be confirmed before docs are written.

**Foundation-first rationale:**
- T2, T3, and T4 all import the shared experiment result type. If that type changes after they branch, all three PRs require rebases and re-validation.
- The prompt explicitly states the validation base will be moving. T1 freezes it.

**Review-burden rationale:**
- 2-PR waves keep each review round coherent.
- Wave 2 reviewers need only understand one thing: "does this layer correctly consume the contract T1 defined?"
- Wave 3 is low-stakes and can be reviewed quickly.

---

## Parallel safety gate (Wave 2)

```md
## Parallel safety gate

Base:
- Branch: main (or current integration branch)
- SHA: confirmed at Wave 1 merge
- Working tree clean? Verify before creating worktrees

Tasks: T2 (backend API), T3 (results table UI)

Checks:
- [x] Each task has clear scope
- [x] Each task has explicit non-goals
- [x] Each task has proof
- [x] Foundation-first task (T1) is identified and sequenced first
- [ ] Dependencies resolved — T1 must be merged before Wave 2 begins
- [x] File overlap is low — API serializer vs. UI component
- [x] Shared contract stable at Wave 2 start — enforced by wave sequencing
- [x] Coordination files have one owner
- [x] Review burden acceptable — 2 PRs
- [x] Max parallel task limit respected (2 of 3 max)
- [x] Branch names deterministic
- [x] Worktree paths isolated
- [x] Merge order defined — T2 and T3 can merge in either order; T4 waits for both
- [x] Stop conditions included in each contract
```

---

## Worktree task contracts

### T1 — Shared TypeScript contract + validation

```md
# Worktree Agent Contract

## Task
Add `confidenceBand` to the shared experiment result TypeScript type and
update the validation/schema logic to require and validate the new field.

## Scope

Do:
- Add `confidenceBand` to the experiment result interface/type
- Update the schema or validation module to validate the field
- Add or update unit tests for the validation change
- Export the type so consumers can import it without circular references

Do not:
- Touch any API handler, UI component, or export module
- Change any other field on the experiment result type
- Merge until the type for `confidenceBand` is confirmed (stop if ambiguous)

## Base
Base branch: main
Base SHA: (confirm at task start)
Branch: ai/confidence-band/01-contract-validation
Worktree: ../worktrees/repo-01-contract-validation

## Expected files/modules
Allowed:
- experiment result type definition (e.g. types/experimentResult.ts or equivalent)
- validation/schema module
- unit tests for validation

Avoid:
- API handlers
- UI components
- CSV/export modules
- docs

Stop if you need to edit files outside this list.

## Proof required
- TypeScript compiles with no errors
- Validation unit tests pass
- `confidenceBand` is present in the exported type with correct type signature

## Stop conditions
Stop if:
- The type of `confidenceBand` is ambiguous (string, enum, numeric range?) — report and ask
- Validation logic is entangled with API handler code that other tasks will also touch
- Tests fail after two focused attempts
```

---

### T2 — Backend API response shape

```md
# Worktree Agent Contract

## Task
Update the backend API response serializer/handler to include `confidenceBand`
in the experiment result response shape.

## Scope

Do:
- Include `confidenceBand` in the API response object
- Update API integration/unit tests to assert the field is present
- Follow the type from T1 exactly

Do not:
- Change the experiment result TypeScript type (owned by T1)
- Touch the results table UI or CSV export
- Add computation logic for `confidenceBand` (assumed computed upstream)

## Base
Base branch: ai/confidence-band/01-contract-validation (after merge to main)
Base SHA: T1 merge SHA
Branch: ai/confidence-band/02-backend-api
Worktree: ../worktrees/repo-02-backend-api

## Expected files/modules
Allowed:
- API response serializer or handler for experiment results
- API tests

Avoid:
- Shared type definitions (T1 owns these)
- UI components
- Export/CSV modules

## Dependencies
- T1 merged

## Proof required
- API test asserts `confidenceBand` is present in response
- TypeScript compiles

## Stop conditions
Stop if:
- `confidenceBand` is not yet in the shared type (T1 not merged)
- API handler is shared with another module T3 or T4 also needs to edit
```

---

### T3 — Results table UI

```md
# Worktree Agent Contract

## Task
Add a `confidenceBand` column to the experiment results table in the dashboard UI.

## Scope

Do:
- Add `confidenceBand` column to the results table component
- Import and use the type from T1
- Add or update component snapshot/unit tests

Do not:
- Change the API response handler (owned by T2)
- Change the shared type definition (owned by T1)
- Touch CSV export

## Base
Base branch: ai/confidence-band/01-contract-validation (after merge to main)
Base SHA: T1 merge SHA
Branch: ai/confidence-band/03-results-table-ui
Worktree: ../worktrees/repo-03-results-table-ui

## Expected files/modules
Allowed:
- Results table component and its tests

Avoid:
- API handlers
- Shared types
- Export/CSV

## Dependencies
- T1 merged

## Proof required
- Component renders `confidenceBand` value
- TypeScript compiles
- Existing table tests still pass

## Stop conditions
Stop if:
- Results table component also owns API fetch logic that T2 is changing
- UI product decision needed (e.g. how to display null/missing `confidenceBand`)
```

---

### T4 — CSV export

```md
# Worktree Agent Contract

## Task
Add `confidenceBand` as a column in the experiment results CSV export.

## Scope

Do:
- Add `confidenceBand` to the CSV export column list
- Update export unit/integration tests

Do not:
- Change the shared type, API handler, or UI component

## Base
Base branch: main (after T1 and Wave 2 merge)
Branch: ai/confidence-band/04-csv-export
Worktree: ../worktrees/repo-04-csv-export

## Dependencies
- T1 merged
- T2 merged (confirm API shape is final before export tests run against it)

## Proof required
- Export test asserts column is present
- TypeScript compiles

## Stop conditions
Stop if:
- CSV export module directly imports from the API handler and T2 is not yet merged
```

---

**Next action**: Confirm the type of `confidenceBand` (string literal union, number, or other), then execute Wave 1 (T1). All other tasks are blocked until T1 merges.