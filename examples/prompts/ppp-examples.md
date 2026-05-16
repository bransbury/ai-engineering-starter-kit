# PPP example prompts

## Small bug fix

```text
/ppp Fix whitespace-only report names being accepted. Follow existing validation patterns and add/update tests.
```

## UI empty state

```text
/ppp Add an empty state to the experiment results table when there are no rows. Use the existing empty-state component if one exists.
```

## Parser behaviour

```text
/ppp Update the token parser to preserve {{firstName|}} as an explicit empty fallback, while {{firstName}} remains no fallback. Add tests for both cases.
```

## Failing test

```text
/ppp This test is failing. Diagnose and fix it without weakening the test.

Command:
<command>

Error:
<error>
```

## Too-large task

```text
/ppp Build a new analytics dashboard to show A/B test data, conversion rates, traffic split, confidence, date range filters, and export to CSV.
```

Expected: PPP should recommend narrowing to the smallest first task.

---

## What good output looks like

The following is an example of a good PPP run for the whitespace-only bug fix prompt above.

---

### Current phase: Inspecting

| Area | File/module | Status | Evidence |
|---|---|---|---|
| Validation logic | `src/reports/validation.ts` | Confirmed | `reportNameSchema` validates `minLength(1)` but does not trim first |
| Existing tests | `src/reports/validation.test.ts` | Confirmed | Tests for empty string — no test for whitespace-only |
| Validation call site | `src/reports/create.ts` | Confirmed | Calls `reportNameSchema.parse(name)` directly with no pre-trim |

**Finding:** `"   "` passes the `minLength(1)` check because `.trim()` is not applied before validation.

---

### Current phase: Planning

Smallest safe change: trim before the length check in `reportNameSchema`, and add a test for whitespace-only input.

No migration needed. No other call sites pass names without trimming.

Proof: `validation.test.ts` passes with a new case for `"   "` returning a validation error.

Choose an option:

1. Patch `validation.ts` and add the test — recommended
2. Show the relevant code before patching
3. Stop here

---

### After patching — current phase: Reviewing

Changes:

- `src/reports/validation.ts`: added `.trim()` before `minLength` check
- `src/reports/validation.test.ts`: added test for whitespace-only name

Checks run: `pnpm test src/reports` — passed (14 tests, 1 new)

Production readiness:

- No migration needed
- No API contract change
- Existing valid names unaffected

### PR

Title: `fix: reject whitespace-only report names`

Body:
> Whitespace-only report names (e.g. `"   "`) were accepted because the length check ran before trimming. Added `.trim()` before the `minLength` check and a test covering the new case.
>
> Testing: unit tests pass. No migration needed.

---

Key things this run got right:

- inspected before editing
- no unnecessary questions
- defined proof before patching
- added a test rather than removing validation
- stated what checks actually ran
- kept the diff to the minimum required
