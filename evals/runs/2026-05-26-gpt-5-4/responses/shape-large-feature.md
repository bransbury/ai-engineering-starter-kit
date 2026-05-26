# Response for shape-large-feature

I’m pulling the shape skill guidance and existing memory notes first so I can answer this the way the workflow is intended, not improvise a different triage path.

Read memory

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 250

Read memory [](file:///Users/marcus/Library/Application%20Support/Code/User/workspaceStorage/132b72ca2af431e74a40f7948dacfa93/GitHub.copilot-chat/memory-tool/memories/repo/ai-engineering-starter-kit.md)

I’ve confirmed this repo’s eval pattern and the shape skill’s core constraints. One more targeted read will tell me the expected output structure so I can return a properly shaped first-PR recommendation instead of a generic refusal.

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#251-251), lines 251 to 520

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#521-521), lines 521 to 642

## Shape result

Status:
- `too-broad-shape-first`

Recommended next action:
- Start with one focused first PR: create an analytics dashboard shell behind a feature flag, with static layout regions for summary metrics, experiment table, filters, and export entry point.

Reason:
- The original ticket bundles multiple behaviours: data sourcing, metric computation, traffic split/confidence presentation, filtering, and CSV export.
- That is not one PPP-sized change. It needs sequencing and proof per slice.

Confidence:
- Medium

## Confirmed decisions
- No blocking product or security decision is required to shape a safe first PR.
- Recommended default: first PR is UI shell only, behind a feature flag, with no live analytics calculations and no CSV export.

## Shaped work

| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | Expected files/modules | PR-size score | Split? | Risk |
|---|---|---|---|---|---|---|---|---:|---|---|
| T1 | Dashboard shell behind feature flag | Add route/page/container, empty states, placeholders for KPI cards, results table, filters, export action; gate behind feature flag | No live data, no metric math, no export, no persistence | AC1, AC2 | None | Feature flag off hides entry; flag on renders shell and empty state | Dashboard page, routing, feature flag config, basic tests | 8 | No | Low |
| T2 | Read-only experiment results table | Populate table from existing A/B test result source if one already exists; show experiment, date range, conversion rate, traffic split, confidence | No new analytics pipeline, no editing, no export | AC3, AC4 | T1 | Table renders known fields from existing data source; empty/error states covered | Data adapter, table component, tests | 10 | No | Medium |
| T3 | Date range filtering | Add date range controls and filter query/state for the read-only data set | No custom reporting builder, no saved filters | AC5 | T2 | Filter changes visible rows correctly; invalid ranges handled | Filter UI, query/state handling, tests | 9 | No | Medium |
| T4 | CSV export | Export currently visible read-only table rows to CSV | No background jobs, no scheduled exports | AC6 | T2 or T3 | Export matches visible columns/rows | Export utility, UI action, tests | 8 | No | Low |

## Scope

In scope:
- A safe first delivery slice that establishes the dashboard entry point and rollout guardrail.
- Sequenced follow-on slices for read-only data display, filtering, and export.

Out of scope:
- New experimentation data models.
- Confidence-statistic redesign or analytics methodology changes.
- Editable dashboards, saved views, alerting, or drill-down workflows.

## Acceptance criteria

| ID | Acceptance criterion | Proof idea |
|---|---|---|
| AC1 | With the feature flag off, users do not see the analytics dashboard entry point. | Route/nav coverage test with flag off. |
| AC2 | With the feature flag on, users can open the dashboard shell and see structured empty placeholders for KPIs, experiment results, filters, and export action. | UI test or screenshot/assertion for shell render. |
| AC3 | The results table can render existing A/B test result records in read-only form. | Component/integration test with seeded records. |
| AC4 | Table handles empty and load-failure states predictably. | State-based tests. |
| AC5 | Date range filters constrain the displayed result set without breaking empty/error states. | Integration test across valid/invalid ranges. |
| AC6 | CSV export downloads exactly the rows and columns currently visible in the table. | Export content assertion test. |

## First PR

Task:
- T1: dashboard shell behind feature flag

Mode:
- `/ppp`

Why first:
- It is the smallest safe increment.
- It establishes routing, rollout control, and the UI/test pattern without forcing unresolved data or analytics decisions.
- It gives reviewers a concrete frame for later slices.

Proof:
- Flag-off hides the dashboard.
- Flag-on shows the shell and empty state.
- No existing navigation or pages regress.

PR-size assessment:
- Behaviour count: 2
- Module spread: 2
- Contract change: 1
- Proof complexity: 2
- Risk: 1
- Total: 8, suitable for one focused PR

## Follow-on tasks
- T2 after T1: read-only table for existing A/B test result data.
- T3 after T2: date range filtering.
- T4 after T2 or T3: CSV export for visible rows.

## Delegation assessment

| Task ID | Clarity | Independence | Conflict risk | Risk | Verifiability | Recommendation | Evidence |
| ------- | ------: | -----------: | ------------: | ---: | -----------: | -------------- | -------- |
| T1 | 5 | 4 | 2 | 2 | 5 | `/ppp` now | Clear UI-shell slice with obvious proof |
| T2 | 4 | 3 | 3 | 3 | 4 | sequence after T1 | Depends on actual existing data path |
| T3 | 4 | 3 | 2 | 3 | 4 | sequence after T2 | Depends on table/query wiring |
| T4 | 4 | 4 | 2 | 2 | 5 | possible later `/ppp-cloud` or `/ppp` | Clear once table contract exists |

## Human decisions needed
- None for T1.
- T2 may need a human decision only if no existing A/B result source exists and new data contracts would be required.

## Safe to proceed now
- Build T1 as a feature-flagged dashboard shell.
- Do not include live analytics logic in that first PR.

## Remaining ambiguity
- Whether an existing trusted source already provides conversion rate, traffic split, and confidence fields for T2.
- Exact CSV column contract for T4.

## Smallest next shaped task after answer
- If existing result data exists: T2 is the next safe task.
- If it does not: stop and shape a data-contract decision before implementation.

## Ready-to-ship prompt

1. Recommended: Pass T1 directly to `/ppp`.
2. Pass the full sequence to `/ship` for coordinated delivery planning.
3. Keep this shaped output only.

## Suggested next prompt

If starting the first PR now:

```text
/ppp Implement T1: add an analytics dashboard shell behind a feature flag. Include route/page wiring, placeholder KPI cards, empty table state, filter placeholders, and an inactive export entry point. Prove flag-off hides it and flag-on renders the shell without live data.
```