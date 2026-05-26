# Response for shape-clear-small-bug

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 80

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#80-80), lines 80 to 200

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#200-200), lines 200 to 350

Read skill [shape](file:///Users/marcus/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#350-350), lines 350 to 450

## Understanding

Goal:
- Prevent users from saving report names that consist entirely of whitespace characters.

Current problem:
- The report name field accepts whitespace-only strings, which pass validation and get persisted as meaningless names.

Expected behaviour:
- A whitespace-only name is normalised to empty and rejected by the existing empty-name validation — no new error message or validation path is needed.

Likely users/systems affected:
- Any user who can create or rename a report.
- The validation logic for the report name field (client or server, or both).

Relevant constraints:
- Must follow the existing validation style.
- Must not redesign the report form.
- Tests must be added or updated.

Areas unclear:
- None that block shaping. Validation layer (client/server) is an implementation detail the implementer resolves by inspecting the existing pattern.

---

## Facts, assumptions, and open questions

### Known facts
- A save path exists that accepts a report name.
- An empty-name validation already exists.

### Assumptions
- The fix is a `.trim()` (or equivalent) applied before the existing empty check — not a new validator.
- The validation lives in one place (one function or method); no cross-service schema change is needed.

### Non-goals
- Redesigning or refactoring the report form.
- Stripping leading/trailing whitespace from the saved value (only rejection is required, per spec).
- Changing the error message shown to users.

---

## Scope

In scope:
- Apply whitespace normalisation before the existing empty-name check.
- Add/update unit tests covering whitespace-only inputs (spaces, tabs, mixed).

Out of scope:
- New UX, error states, or form layout changes.
- Auto-trimming persisted names.
- Any other report field validations.

## Acceptance criteria

| ID | Acceptance criterion | Proof idea |
|---|---|---|
| AC1 | A name of `" "` (spaces only) is rejected with the same error as an empty name | Unit test: submit `"   "` → expect existing empty-name error |
| AC2 | A name of `"\t"` or `" \t "` is rejected | Unit test: submit tab/mixed whitespace → expect empty-name error |
| AC3 | A valid name with surrounding whitespace (e.g. `" Q4 Report "`) is handled per the existing trim policy (trimmed or accepted, matching current behaviour elsewhere) | Unit test: confirm behaviour is consistent with existing pattern |
| AC4 | No regression on valid non-empty names | Existing passing tests remain green |

---

## Slice

| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | Expected files/modules | PR-size score | Split? | Risk |
|---|---|---|---|---|---|---|---|---:|---|---|
| T1 | Add `.trim()` (or equivalent) before empty-name check; add/update tests | One guard in the existing validation function + test cases | Form redesign, new error messages, other field validations | AC1–AC4 | None | Unit tests green; whitespace-only names rejected; valid names unaffected | Report name validator + test file | 6 | No | Low |

**PR-size assessment for T1:**
- Behaviour count: 1 (whitespace = empty)
- Module spread: 1 (validator + its test)
- Contract change: none
- Proof complexity: one clear proof (unit tests)
- Risk: low

Total: **6** — one focused PR.

---

No meaningful decisions to confirm. The ticket is clear, the fix is a one-liner following existing patterns, and the test approach is unambiguous.

## Ready to ship

Options:
1. **Recommended:** Pass the shaped work to `/ppp` now — task is clear, bounded, and best built with human IDE context to locate the exact validator.
2. Pass to `/ppp-cloud` — if you prefer autonomous execution with a draft PR.
3. Stop here and keep the shaped output only.

Reply with `1`, `2`, or `3`.