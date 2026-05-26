# Response for shape-public-api-ambiguity

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 150

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#151-151), lines 151 to 300

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#301-301), lines 301 to 450

## Understanding

**Goal:** Allow customers to download their invoice history via an API endpoint.

**Current problem:** No export mechanism exists for invoices today.

**Likely users/systems affected:** Billing viewers, org admins, external integrations (if public API), app frontend.

**Areas unclear:** Three critical open questions remain — all in guardrail domains.

---

## Facts, assumptions, and open questions

### Known facts
- Customers need to download invoice history
- Invoice data already exists (implied — there is a history to export)

### Assumptions
- Invoice records already exist in the data model (medium confidence — not inspected)
- Export format is likely CSV or JSON (reversible, low-risk assumption)

### Open questions

| # | Question | Why it matters | Recommended answer | Blocks shaping? |
|---|---|---|---|---|
| 1 | Should pending invoices appear in the export? | Changes data scope, acceptance criteria, and edge-case handling. A pending invoice exposed prematurely could mislead customers on amounts owed. | Exclude pending invoices in v1 (safest default — avoids exposing unstable data). | **Yes** — product decision |
| 2 | Who can export: org admins only, or billing viewers too? | Determines auth middleware, test matrix, and whether a new permission is needed. Getting this wrong is a security incident. | Cannot safely recommend — this is a security/access-control decision that must come from Security. | **Yes** — security decision |
| 3 | Public API contract or internal-only endpoint behind the app? | A public API requires versioning, rate-limiting, documentation, deprecation policy, and a stability contract. An internal endpoint has none of those costs. | Cannot safely recommend — this is a platform architecture decision. | **Yes** — platform/API-contract decision |

### Non-goals
- Changing invoice creation or payment flows
- Building a UI for export (separate concern)
- Supporting real-time streaming of invoice data

---

## Status: `needs-human-decision`

All three open questions fall into guardrail domains (product behaviour, security/auth, public API contract). Shaping cannot safely continue past scoping until these are answered.

---

## What is already safe and shaped

Regardless of the answers, the **smallest safe first PR** is the same:

> **T1 — Internal invoice export service (no endpoint)**
>
> A pure domain/service-layer function that takes a user/org context and returns completed invoices as structured data. No HTTP layer, no auth decisions, no public contract.

| Dimension | Score |
|---|---|
| Behaviour count | 1 (query + serialize) |
| Module spread | 1 (billing/invoices domain) |
| Contract change | 1 (no public surface) |
| Proof complexity | 1 (unit test: given org with invoices → returns expected list) |
| Risk | 1 (no auth, no public API) |
| **Total** | **5** — clearly one focused PR |

This task is safe because it:
- makes no auth decision (caller passes context; enforcement is the endpoint's job)
- excludes pending invoices by default (filter on status = completed)
- exposes no HTTP surface
- is independently provable with a unit test
- is useful regardless of how questions 2 and 3 are answered

---

## What remains intentionally unshaped

| Unshaped work | Blocked by |
|---|---|
| T2 — HTTP endpoint + auth middleware | Questions 2 and 3 |
| T3 — Include/exclude pending invoices logic | Question 1 |
| T4 — Public API versioning, rate-limiting, docs (if public) | Question 3 |

---

## Recommended next steps

1. **Now (no decisions needed):** Route T1 to `/ppp` or `/ppp-cloud` — it is clear, bounded, low-risk, and testable.
2. **Async:** Get answers to questions 1–3 from Product, Security, and Platform.
3. **After answers:** Re-invoke `/shape` to scope T2–T4.

---

## Route recommendation for T1

| Option | Route | Rationale |
|---|---|---|
| **1 (recommended)** | `/ppp-cloud` | Clear, bounded, low-risk, testable, no human judgement needed. |
| 2 | `/ppp` | If the engineer wants to explore the existing invoice data model hands-on. |

Reply with `1` or `2` to route T1, or answer any of the open questions to continue shaping the remaining work.