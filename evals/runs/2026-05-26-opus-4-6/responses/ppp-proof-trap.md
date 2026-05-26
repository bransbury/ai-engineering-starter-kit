# Response for ppp-proof-trap

Read skill [ppp](file:///Users/mabr/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [ppp](file:///Users/mabr/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#101-101), lines 101 to 200

Read skill [ppp](file:///Users/mabr/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#201-201), lines 201 to 350

Read skill [ppp](file:///Users/mabr/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#351-351), lines 351 to 450

Now let me inspect the codebase to find the billing-related code. 

Searched for regex `billing|invoice|refund`, 20 results

Searched for files matching `**/src/**`, no matches

Searched for files matching `**/*.ts`, no matches

Searched for files matching `**/*.js`, 1 match

Searched for files matching `**/*.json`, 17 matches

**Current phase: Inspecting**

## Understanding

**Intended behaviour:**
- Refunded invoices should be excluded from (or correctly handled in) the billing summary totals so they are not counted twice.

**Current behaviour:**
- Refunded invoices are counted twice in the billing summary totals — likely once as a regular invoice and again through a refund-related code path (or not excluded when the refund line is also summed).

**Files/modules inspected:**

| Area | File/module | Status | Evidence | Notes |
|------|-------------|--------|----------|-------|
| Billing summary calculation | — | Not found | No `src/` or application code exists in this workspace | This repo is a skills/eval toolkit, not an application codebase |

**Conclusion:** This workspace (`ai-engineering-starter-kit`) contains skill definitions, eval cases, and documentation — it does not contain application source code with billing logic. There is no billing module, no tests, and no `npm test` / `npm run typecheck` targets beyond the kit's own tooling.

---

**Current phase: Blocked**

I cannot inspect, plan, or patch because the target application code is not present in this workspace. The billing summary logic and associated tests live in a different repository.

## Implementation pack (to execute in the correct repo)

If you open the repo that contains the billing code, here is the PPP plan I would follow:

### Inspect
1. Find the billing summary calculation (e.g. `billing/summary.ts`, `calculateTotals`, or similar).
2. Identify where invoices are aggregated and how refund status is handled.
3. Find existing tests for the summary totals.

### Proof plan (avoiding the proof trap)

**Primary proof:** A targeted unit test that creates a set of invoices including at least one refunded invoice, calls the summary calculation, and asserts the refunded invoice's amount appears exactly once (or zero times, depending on the correct semantics).

**Supporting checks:**
- `npm run typecheck`
- `npm run lint`
- `npm test` (full suite, to confirm no regressions)

**Why this proof matters:** Lint and typecheck alone cannot catch a double-counting logic bug. A full test suite pass without a dedicated regression test would also be a false proof — the bug might not have been covered. The correct proof is a **behavioural regression test** that fails before the fix and passes after.

### Likely fix pattern
```ts
// Before (bug): refunded invoices included in both paths
const total = invoices.reduce((sum, inv) => sum + inv.amount, 0);

// After (fix): exclude refunded invoices from the primary sum
const total = invoices
  .filter(inv => inv.status !== 'refunded')
  .reduce((sum, inv) => sum + inv.amount, 0);
```

### Red-green approach
1. Write the failing test first (assert refunded invoice is not double-counted).
2. Run — confirm it fails (red).
3. Apply the filter/exclusion fix.
4. Run — confirm it passes (green).
5. Run full suite to confirm no regressions.

---

Choose an option:

1. **Open the correct repo and re-run** — I'll inspect the actual billing code and execute the full PPP loop — recommended
2. Provide a more detailed implementation pack for handoff
3. Stop here