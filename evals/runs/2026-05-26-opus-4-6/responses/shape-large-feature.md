# Response for shape-large-feature

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 150

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#151-151), lines 151 to 300

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#301-301), lines 301 to 450

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#451-451), lines 451 to 550

Now I have a complete understanding of the Shape skill. Let me apply it to this large feature ticket.

---

## Understanding

**Goal:** Build a new analytics dashboard showing A/B test data, conversion rates, traffic split, confidence intervals, date range filters, and CSV export.

**Current problem:** No analytics dashboard exists for A/B test data.

**Likely users/systems affected:** Product/growth team consuming A/B test results; frontend (new dashboard UI); backend (data queries, export endpoint); possibly existing A/B test infrastructure.

**Relevant constraints:** None specified.

**Areas unclear:** Many — see below.

---

## Facts, assumptions, and open questions

### Known facts
- The work spans UI, data access, filtering, and export — multiple independent concerns.

### Assumptions
- An existing A/B test data source exists (database, analytics service, or API).
- The dashboard will be a new page/route in an existing application.
- Standard auth applies (no new permission model needed).

### Open questions

| # | Question | Why it matters | Recommended answer | Blocks shaping? |
|---|---|---|---|---|
| 1 | Where does A/B test data currently live (DB table, third-party API, event store)? | Determines data-access layer shape and whether we need an integration or just a query. | Assume existing DB/service. | No |
| 2 | Is there an existing component library / design system to use? | Affects UI task scope and proof strategy. | Assume yes — use existing system. | No |
| 3 | Who needs access — all users or only admins/growth team? | Could require new permissions. | Assume existing role-based access is sufficient. | No |
| 4 | Does "confidence" mean a statistical significance calculation performed server-side, or is it a stored value? | Determines whether we need new computation logic. | Assume stored/pre-computed. | No |
| 5 | Is there an existing CSV export pattern in the codebase? | Affects export task scope. | Assume yes or use standard pattern. | No |

### Non-goals
- Running or configuring A/B tests from this dashboard.
- Real-time streaming updates.
- Custom visualisations or charting beyond tabular data (unless explicitly requested later).

---

## Scope

**In scope:**
- Dashboard page shell and routing
- Table/list of A/B test experiments with key metrics
- Date range filter
- CSV export of filtered data

**Out of scope:**
- Creating/editing/stopping experiments
- New permissions model
- Real-time data
- Custom chart visualisations (can be a follow-on)

## Acceptance criteria

| ID | Acceptance criterion | Proof idea |
|---|---|---|
| AC1 | Dashboard page loads behind a feature flag and displays a list of A/B tests | Route exists, renders with test data, flag controls visibility |
| AC2 | Each row shows: experiment name, variants, traffic split, conversion rate, confidence | Rendered table matches fixture data |
| AC3 | Date range filter restricts displayed experiments by date | Filter applied → table updates correctly |
| AC4 | Export button downloads CSV of currently filtered data | Click export → file downloads with correct content |

---

## Slice

| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | PR-size score | Split? | Risk |
|---|---|---|---|---|---|---|---:|---|---|
| T1 | Dashboard shell + route behind feature flag | New route, empty page, feature flag wiring | No data, no table, no filters | AC1 | None | Route renders, flag gates access | 6 | No | Low |
| T2 | A/B test data table with metrics | Data-fetching hook/service, table component rendering test data | Filters, export | AC2 | T1 | Table renders fixture/seed data correctly | 8 | No | Low |
| T3 | Date range filter | Filter component, query parameter, data re-fetch | Export, other filters | AC3 | T2 | Filter changes → table updates | 7 | No | Low |
| T4 | CSV export of filtered data | Export endpoint or client-side generation, download trigger | Custom formats, scheduling | AC4 | T2 | Download contains expected rows/columns | 7 | No | Low |

---

## Delegation and parallel readiness

| Task ID | Clarity | Independence | Conflict risk | Risk | Verifiability | Recommendation | Evidence |
|---------|--------:|-------------:|--------------:|-----:|-------------:|----------------|----------|
| T1 | 5 | 5 | 1 | 1 | 5 | `/ppp-cloud` | Clear scope, one route + flag |
| T2 | 4 | 3 | 2 | 2 | 4 | `/ppp` | Needs data-access decisions |
| T3 | 4 | 3 | 2 | 1 | 5 | `/ppp` or `/ppp-cloud` | Depends on T2 patterns |
| T4 | 4 | 3 | 2 | 1 | 5 | `/ppp` or `/ppp-cloud` | Depends on T2 patterns |

T3 and T4 are parallel candidates after T2 merges (independent of each other, both depend on T2's data layer).

---

## Shape result

**Status:** `ready-for-ship`

**Recommended next action:** Pass shaped work to `/ship` for coordinated delivery of T1 → T2 → T3 + T4 (parallel).

**Reason:** This is clearly multi-PR work. T1 is a safe, minimal first PR that unblocks everything. T2 establishes patterns. T3 and T4 are independent follow-ons.

**Confidence:** Medium — no codebase inspection possible; based on task text and common patterns.

---

## First PR

**Task:** T1 — Dashboard shell + route behind feature flag

**Mode:** `/ppp-cloud`

**Why first:**
- Smallest safe useful increment
- Unblocks all subsequent work
- No product/data decisions required
- Clear, bounded, trivially provable

**Proof:**
- New route responds with empty dashboard shell
- Feature flag off → route inaccessible
- Feature flag on → route renders page

**PR-size assessment:** Score 6 (one behaviour, one module area, no contract change, one proof, low risk) — well within one focused PR.

---

## Confirm decision 1

**Decision:** Delivery strategy

**Options:**
1. **Recommended:** Pass to `/ship` — sequence T1 → T2 → (T3 ∥ T4), with T1 delegated to cloud agent.
2. Start with T1 only via `/ppp-cloud`, decide later.
3. Keep shaped output, route manually.

**Why option 1 is recommended:** The work is well-structured with clear dependencies. Ship can coordinate the sequence and parallelise T3/T4 after T2 lands.

Reply with `1`, `2`, or `3`.