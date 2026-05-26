# Response for shape-public-api-ambiguity

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#101-101), lines 101 to 300

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#301-301), lines 301 to 450

## Understanding

**Goal:**
- Add an endpoint that lets customers download their invoice history as a file or structured data export.

**Current problem:**
- Three open decisions block implementation: data inclusion (pending invoices), access control (admin-only vs billing viewers), and API contract type (public vs internal).

**Expected behaviour:**
- Authenticated users with the right permission can request an export of invoice records and receive a downloadable result.

**Likely users/systems affected:**
- Org admins (confirmed), possibly billing viewers (unresolved), downstream integrations if public API (unresolved).

**Relevant constraints:**
- Pending invoice inclusion, auth scope, and public contract status are all unresolved — all three are guardrail areas (security, billing, public API).

**Areas unclear:**
- All three open questions are blocking for different parts of scope.

---

## Facts, assumptions, and open questions

### Known facts
- The export covers invoice history (past invoices).
- Customers need to be able to download it.
- At least one role (org admin) will have access.

### Assumptions
- Export format is not decided; assume JSON or CSV for now — reversible.
- Pagination or size limits are out of scope for the first PR.

### Open questions

| # | Question | Why it matters | Recommended answer | Blocks shaping? |
|---|---|---|---|---|
| OQ1 | Should pending invoices appear in the export? | Determines data model scope and filtering logic | No — confirmed invoices only; pending is a follow-on | No (safe default exists) |
| OQ2 | Who can export: org admins only, or billing viewers too? | Auth middleware, permission check, and test scope | Org admins only — most restrictive; expand later | No (safe default exists) |
| OQ3 | Is this a new public API contract or internal-only? | Versioning, breaking-change guarantees, API gateway routing, docs | Internal-only behind app layer for now | No (safe default exists) |

### Non-goals
- Streaming or async export jobs (defer unless data volume demands it).
- Billing viewer access (defer pending Security sign-off).
- Pending invoice inclusion (defer pending Product sign-off).
- Public API contract/versioning/SDK (defer pending Platform decision).

---

## Scope

**In scope (first PR):**
- Internal-only endpoint (not a public API contract).
- Org admin permission check only.
- Confirmed/paid invoices only — no pending.
- Download response (JSON or CSV).
- Auth and permission tests.

**Out of scope:**
- Billing viewer role access.
- Pending invoice filtering.
- Public API contract, versioning, or gateway config.
- Async export jobs or large-file streaming.

## Acceptance criteria

| ID | Criterion | Proof idea |
|---|---|---|
| AC1 | Org admin can request invoice export and receive a downloadable file of confirmed invoices | Integration test: admin token → 200 + file body |
| AC2 | Non-admin authenticated user receives 403 | Integration test: billing viewer / member token → 403 |
| AC3 | Unauthenticated request receives 401 | Integration test: no token → 401 |
| AC4 | Pending invoices do not appear in export | Unit test: seed pending + confirmed; assert only confirmed in output |
| AC5 | Endpoint is not accessible via public API gateway (internal routing only) | Routing/config test or manual verification of gateway config |

---

## Slice

| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | PR-size score | Split? | Risk |
|---|---|---|---|---|---|---|---:|---|---|
| T1 | Internal invoice export endpoint (org admin, confirmed invoices) | Add route, auth check, query, response serialiser | Public contract, billing viewers, pending invoices, async jobs | AC1–AC5 | Existing auth middleware, invoice data model | AC1–AC5 integration + unit tests | 8 | No | Medium |

**T1 score breakdown:** behaviour count 1 (2), module spread 2–3 (3), contract change internal only (1), proof multiple checks (3), risk medium (3) → **total 12**. Borderline but acceptable as one PR given tight non-goals and safe defaults.

---

## Routing recommendation

**T1 → `/ppp`**

Reasoning:
- The safe-defaults approach (internal, admin-only, confirmed-only) is clear and bounded.
- The auth and data-model integration likely benefits from human steering given the security and billing context.
- Medium risk warrants IDE-led work.

**After T1 ships**, three follow-on decisions unlock follow-on tasks:

| Decision | Owner | Follow-on task |
|---|---|---|
| OQ1: pending invoices | Product | T2: add pending invoice flag/filter |
| OQ2: billing viewer access | Security | T3: expand permission to billing viewer role |
| OQ3: public API contract | Platform | T4: promote to public API with versioning and gateway config |

---

## Status: shaped with safe defaults applied

The three open questions do **not** block this first PR because the safest defaults (internal, admin-only, confirmed-only) are non-controversial and fully reversible. Each open question unlocks a follow-on task — none require rework of T1.

When you're ready, reply `/ppp` to start T1, or let me know if you want to adjust the defaults before proceeding.