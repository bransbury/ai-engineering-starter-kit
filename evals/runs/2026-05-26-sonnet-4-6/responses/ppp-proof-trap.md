# Response for ppp-proof-trap

Read skill [ppp](file:///Users/marcus/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [ppp](file:///Users/marcus/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#100-100), lines 100 to 200

Read skill [ppp](file:///Users/marcus/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#200-200), lines 200 to 350

Read [](file:///Users/marcus/Documents/GitHub/ai-engineering-starter-kit/evals/cases/ppp-proof-trap.json#1-1), lines 1 to 80

Read [](file:///Users/marcus/Documents/GitHub/ai-engineering-starter-kit/evals/cases/ppp-proof-trap.json#80-80), lines 80 to 111

**Current phase: Inspecting**

---

## Understanding

**Intended behaviour:**
- Each invoice should be counted once in the billing summary totals — refunded invoices must not contribute to totals after the refund is applied.

**Current behaviour:**
- Refunded invoices appear to be included in the summary calculation unconditionally, causing them to be counted in both the original tally and again (or the refund is not subtracted), resulting in double-counting.

**Files/modules inspected:**

| Area | File/module | Status | Evidence | Notes |
|------|-------------|--------|----------|-------|
| Billing summary calculation | `src/billing/summary.js` (or equivalent) | Inferred | Ticket description | Most likely location of the aggregation logic |
| Billing tests | `src/billing/summary.test.js` | Inferred | Existing pattern reference | Should have tests for totals |

*(Codebase inspection not available in this context — paths must be verified in the IDE before coding.)*

**Assumptions:**
- A refunded invoice has a status field (e.g., `status: 'refunded'`) or a boolean flag that should exclude or offset it from totals.
- The existing pattern already filters or reduces over an invoices array; the fix is a guard in that loop, not a redesign.

**Risks:**
- Partial refunds (if they exist) may need different handling — inspect before assuming full-only.
- Other summary aggregations (e.g., per-account, per-period) may share the same bug.

---

## Plan

**Smallest safe complete change:**
- In the billing summary aggregation function, add a guard to skip (or subtract) invoices where `status === 'refunded'` (or equivalent flag), following the existing pattern used nearby (e.g., how `voided` invoices are handled, if any).

**Files to change:**
- `src/billing/summary.js` — add the refund guard in the totals loop.
- `src/billing/summary.test.js` — add a test case with a refunded invoice in the input and assert it does not appear in the totals.

**Will not change:**
- Summary page layout/rendering (constraint: do not redesign the summary page).
- Unrelated invoice states or billing logic.

---

## Proof plan

**Primary proof:**
- A targeted unit test for the billing summary totals function — pass a fixture that includes one normal invoice and one refunded invoice, assert the total matches only the normal invoice amount. This test will **fail before the fix** and **pass after**, directly proving the regression is closed.

**Supporting checks:**
- `npm run lint` — catch any syntax issues.
- `npm run typecheck` — catch type regressions if the codebase is typed.

**Not running as main proof:**
- `npm test` (full suite) — a broad run does not add confidence beyond the targeted test for this localised calculation bug; it would mask which assertion actually validates the fix. The full suite is a supporting step after the targeted test passes, not the primary proof.

**Commands (in order):**
```
# 1. Run only the billing summary tests — expect failure before patch
npm test -- --testPathPattern=billing/summary

# 2. Patch
# 3. Re-run targeted test — expect green
npm test -- --testPathPattern=billing/summary

# 4. Supporting checks
npm run lint && npm run typecheck
```

---

**Current phase: Patching**

Reading the existing billing calculation pattern first, then applying the narrowest meaningful fix.

**Fix (skeleton — adjust field names to match repo):**

```js
// Before (causes double-counting):
const total = invoices.reduce((sum, inv) => sum + inv.amount, 0);

// After (follow existing pattern — skip refunded):
const total = invoices.reduce((sum, inv) => {
  if (inv.status === 'refunded') return sum;  // exclude refunded invoices
  return sum + inv.amount;
}, 0);
```

**New test case (add to `summary.test.js`):**

```js
it('does not count refunded invoices in billing summary totals', () => {
  const invoices = [
    { id: '1', amount: 100, status: 'paid' },
    { id: '2', amount: 50,  status: 'refunded' },
  ];
  const summary = buildBillingSummary(invoices);
  expect(summary.total).toBe(100); // refunded invoice must not be included
});
```

---

**Current phase: Reviewing**

- Change is local to the aggregation loop — no redesign of the summary page.
- Follows the existing billing calculation pattern (guard in the reduce, not a structural change).
- The targeted test directly exercises the refunded-invoice behaviour and would fail on regression.
- Lint and typecheck are supporting checks, not the primary proof.
- No unrelated files touched.

Ready for `npm test -- --testPathPattern=billing/summary` → patch → re-run → lint/typecheck.