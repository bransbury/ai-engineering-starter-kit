# Response for shape-large-feature

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#101-101), lines 101 to 250

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#251-251), lines 251 to 400

Now I have enough context to respond as the Shape skill would for this large feature ticket.

---

## Understanding

**Goal:** Build an analytics dashboard for A/B test monitoring with data visualisation, filtering, and export.

**Likely users:** Internal product/growth teams reviewing experiment results.

**Relevant constraints:** None stated — no existing stack, data model, auth, or deployment context provided.

**Areas unclear:** Everything foundational — data source, existing API surface, auth model, frontend stack, how A/B test results are currently stored or exposed.

---

## Facts, assumptions, and open questions

### Known facts
- Desired outputs: A/B test data, conversion rates, traffic split, confidence intervals, date range filters, CSV export.

### Assumptions
- No existing dashboard shell or analytics module exists.
- A/B test result data is available from some backend source (API or DB).
- This is a web UI feature in an existing app.

### Open questions
- Where does the A/B test data come from? (internal DB, third-party service, analytics pipeline?)
- Is there an existing frontend framework and component library to use?
- Is auth/permissions required on the dashboard? (e.g. internal-only, role-gated?)
- Does "confidence" mean statistical significance calculation server-side or client-side?

These questions materially affect the data model, API contract, and proof strategy. However, shaping can still proceed to identify the first safe PR.

---

## Scope

This ticket as written is **not ready for PPP**. It describes a multi-PR feature spanning:
- Data access / API layer
- UI shell and routing
- Multiple visualisation components (traffic split, conversion rates, confidence)
- Filtering (date range)
- Export (CSV)

**PR-size assessment for the full ticket:**

| Dimension | Score |
|---|---|
| Behaviour count | 5+ independent behaviours | **5** |
| Module spread | API, UI components, routing, export | **5** |
| Contract change | Likely new API endpoints or data model | **5** |
| Proof complexity | Multiple independent checks | **4** |
| Risk | Data access + auth decisions unresolved | **4** |

**Total: 23 — split required before any implementation.**

---

## Slice

Recommended sequence of PR-sized tasks:

| Task | Scope | Non-goals | Proof | Risk | Split? |
|---|---|---|---|---|---|
| **T1** — Dashboard shell behind feature flag | Route + empty page + flag guard | No data, no charts | Flag off → page 404; flag on → blank page renders | Low | No |
| **T2** — Read-only A/B results table | Fetch + display raw results (name, variant, n, conversions) | No charts, no filters, no export | Table renders with fixture/real data; columns match spec | Medium | No |
| **T3** — Date range filter | Filter state + API param + re-fetch | No chart updates yet | Changing range re-fetches; empty state on no results | Low | No |
| **T4** — Conversion rate + confidence display | Calculated columns or server-derived metrics in table | No chart yet | Values match known test data; confidence shown correctly | Medium — depends on where calc lives | No |
| **T5** — Traffic split visualisation | Chart component for variant split | Full dashboard, other charts | Chart renders correct proportions from fixture | Low | No |
| **T6** — CSV export | Download button → client or server export | Streaming, async jobs | Downloaded file matches table state | Low | No |

**Recommended first PR: T1**

Smallest safe increment: establishes the route, page shell, and feature flag pattern. Zero data risk. Unblocks all other tasks. Reviewable in isolation.

---

## Confirm decision 1

**Decision:** Which task should go first?

**Options:**
1. **Recommended:** T1 — Dashboard shell behind a feature flag. Zero data risk, establishes pattern, unblocks everything.
2. T2 — Read-only results table first (skip shell/flag, go straight to data). Faster to something visible, but couples routing + data in one PR.
3. Stop here, resolve the open questions (data source, auth, stack), then re-shape.

**Why option 1 is recommended:** It is the smallest provable increment. It does not require resolving the open questions about data source or auth. It reduces integration risk for all subsequent tasks.

Reply with `1`, `2`, `3`, or provide an edited answer.