# Response for shape-public-api-ambiguity

## Shape result

Status:
- needs-human-decision

Recommended next action:
- Resolve the product, permission, and API-surface decision in one short decision pass before shaping implementation work.

## Understanding

Goal:
- Let customers download invoice history through an export capability.

Current problem:
- The feature intent is clear, but three guardrail decisions that define behavior and risk are still open.

Expected behaviour:
- Authorized users can export invoice history, but the exact dataset, allowed roles, and API exposure are not yet decided.

Likely users/systems affected:
- Customers using billing/invoice workflows.
- App/backend teams owning billing data and export delivery.
- Security/platform owners if this becomes a public contract.

Relevant constraints:
- Pending-invoice inclusion changes user-visible behavior.
- Export permissions are a security decision.
- Internal endpoint vs public API changes contract, review burden, and rollout path.

Areas unclear:
- Whether pending invoices appear.
- Whether export is limited to org admins or also allowed for billing viewers.
- Whether this is internal-only behind the app or a supported public API.

## Facts, assumptions, and open questions

### Known facts
- The requested capability is invoice-history export.
- Customers are the intended consumers.
- Product, Security, and Platform each own a still-open decision.

### Assumptions
- None of the open decisions are safe to default, because each changes scope, proof, and risk.

### Open questions
- Should pending invoices be included in exports?
- Which roles may export: org admins only, or billing viewers too?
- Is the first delivery target an internal app-backed endpoint or a public API contract?

### Non-goals
- Designing the export file format.
- Picking delivery mechanics such as sync download vs async job.
- Shaping implementation tasks that depend on unresolved contract or permission choices.

## Why this blocks safe shaping

- Pending-invoice inclusion is a product behavior decision, so acceptance criteria are not stable yet.
- Export permissions are a security/auth decision, so access-control requirements and proof are not stable yet.
- Public API vs internal endpoint is a contract decision, so task boundaries, review path, and rollout risk are not stable yet.

## Questions

| # | Question | Why it matters | Recommended answer | Blocks shaping? |
|---|---|---|---|---|
| 1 | Should pending invoices appear in exported history? | Defines user-visible export contents and acceptance criteria. | Exclude pending invoices in the first release unless Product explicitly needs them. | Yes |
| 2 | Who may export invoices? | Defines authorization, audit expectations, and negative test coverage. | Restrict to org admins for the first release unless Security explicitly approves billing viewers. | Yes |
| 3 | Is this first release an internal endpoint behind the app or a public API contract? | Public API status changes versioning, docs, compatibility, and review burden. | Start with an internal-only endpoint behind the app unless Platform explicitly wants a public contract now. | Yes |

## What is already safe and shaped

- The work should be split into a decision step first, then implementation shaping.
- The first implementation slice should be one focused PR for a single export path with explicit permissions and explicit invoice-status filtering.
- Public API work, if chosen, should not be bundled with the first ambiguity-resolution step.

## What remains intentionally unshaped

- Final acceptance criteria for export contents.
- Final authorization matrix and proof plan.
- Whether the work is app-internal delivery or a public API contract.
- Any downstream tasks that depend on those choices, including docs, versioning, and external support obligations.

## Smallest next shaped task after answer

- Create one short decision record that locks these three choices:
	- export dataset: pending included or excluded
	- allowed roles: org admins only or billing viewers too
	- surface: internal endpoint or public API
- Once that record is confirmed, shape exactly one first PR:
	- one export entry point
	- one permission model
	- one clearly defined invoice-status filter
	- proof covering positive authorization, negative authorization, and exported data contents

## Safest next route after answer

- If the choices are internal endpoint + org-admin-only + explicit invoice-status rule, this becomes ready-for-ppp as one focused, reviewable implementation task.
- If Platform chooses a public API contract, continue shaping first; do not hand off to implementation until API contract, versioning, and compatibility expectations are explicit.
- If multiple follow-on tasks appear after the decision lands, route through /ship rather than sending partially defined work directly to build.

## Confirm decision 1

Decision:
- Resolve the three blocking choices as a single product/security/platform decision before implementation shaping.

Options:
1. Recommended: Confirm internal-only first release, org-admin-only export, and exclude pending invoices unless a stakeholder objects.
2. Keep all three questions open and stop here.
3. Provide edited answers for one or more of the three decisions.

Why this is recommended:
- It creates the smallest safe first release and avoids locking in a public contract or broader permissions without an explicit decision.

Reply with `1`, `2`, `3`, or provide an edited answer.
