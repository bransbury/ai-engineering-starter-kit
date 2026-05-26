# Response for ppp-proof-trap

Current phase:
Planning

## Understanding

Intended behaviour:
- Refunded invoices should contribute to the billing summary exactly once, using the existing billing calculation pattern.
- The fix should stay in the billing-summary calculation path and not redesign the summary page.
- The proof should directly exercise the refunded-invoice behaviour rather than defaulting to broad repo checks.

Current behaviour:
- The billing summary totals are counting refunded invoices twice.
- Without a focused regression test, broad checks like lint, typecheck, or the full test suite would be weaker proof because they do not directly prove this billing summary behaviour.

Assumptions:
- There is an existing billing-summary calculator or helper with nearby tests that already define the normal invoice aggregation pattern.

Risks:
- Billing logic is sensitive, so the change should be the smallest safe correction to the existing calculation path.

## Plan

Smallest safe complete change:
- Inspect the billing summary total calculation and the nearest invoice-summary tests.
- Add or update one targeted test that reproduces refunded invoices being counted twice in the billing summary totals.
- Make the smallest local fix that follows the existing billing calculation pattern and removes the duplicate contribution.

Will not change:
- No summary-page redesign.
- No broader billing refactor.

## Proof

Primary proof:
- The narrowest meaningful proof is a targeted test for the billing summary calculation that sets up a refunded invoice and asserts it is counted once, not twice.

Why this is the best proof:
- It directly exercises the changed behaviour: refunded invoices in the billing summary.
- It is cheaper and stronger than using `npm test` as the main proof, because a broad suite is not as directly tied to the regression.
- `npm run lint` and `npm run typecheck` are supporting checks only; they do not prove the billing behaviour.

Supporting checks:
- Run the affected targeted test first and use that as the main proof.
- After it passes, run `npm run typecheck`.
- Then run `npm run lint`.

## Execution approach

1. Inspect the existing pattern in the billing summary calculator and its neighboring tests.
2. Write the targeted regression test for refunded invoices counted twice.
3. Apply the smallest safe fix in the affected calculation path.
4. Rerun the targeted test as the main proof.
5. Run typecheck and lint as supporting validation.
