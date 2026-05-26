# Response for shape-clear-small-bug

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 150

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#151-151), lines 151 to 300

Read skill [shape](file:///Users/mabr/.agents/skills/shape/SKILL.md?vscodeLinkType%3Dskill#301-301), lines 301 to 450

## Understanding

**Goal:** Reject whitespace-only report names at save time.

**Current problem:** The report name field accepts strings containing only spaces/tabs/newlines, bypassing validation that already rejects empty strings.

**Expected behaviour:** Whitespace-only names are trimmed or treated as empty, triggering the existing "name required" rejection.

**Likely users/systems affected:** Any user saving or renaming a report.

**Relevant constraints:** Follow existing validation style; don't redesign the form.

**Areas unclear:** None material — the ticket is specific and bounded.

---

## Facts, assumptions, and open questions

### Known facts
- An existing validation pattern already rejects empty names.
- The gap is only for whitespace-only input.

### Assumptions
- Trimming before the existing check (or an equivalent `.trim().length === 0` guard) is sufficient — no new error message or UX change needed.
- Tests exist or can be co-located with existing validation tests.

### Open questions
None blocking.

### Non-goals
- Redesigning the report form.
- Changing error copy or UX for the empty-name case.
- Adding character-set or length validation beyond whitespace.

---

## Acceptance criteria

| ID | Acceptance criterion | Proof idea |
|---|---|---|
| AC1 | Submitting a report name of `"   "` (spaces only) is rejected with the same error as an empty name | Unit test: pass whitespace-only string to validation, assert rejection |
| AC2 | Submitting a report name of `"\t\n"` (tabs/newlines only) is rejected | Unit test: same as above with tab/newline variants |
| AC3 | Valid names with leading/trailing whitespace still succeed (trim for validation, not storage, unless existing pattern trims before save) | Unit test: `" My Report "` passes validation |

---

## Task map

| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | PR-size score | Risk |
|---|---|---|---|---|---|---|---:|---|
| T1 | Add whitespace-only guard to report-name validation + tests | Add `.trim()` or equivalent before existing empty check; add/update unit tests | New error messages, form redesign, length limits | AC1, AC2, AC3 | None | Unit tests pass; manual save of `"   "` shows existing error | **5** (1+1+1+1+1) | Low |

---

## Routing

This is a single, clear, low-risk, one-PR task.

**Recommended route: `/ppp`**

Rationale: the fix is a one-line guard plus a few test cases. Human-led IDE work is fastest and appropriate — no coordination, no ambiguity, no need for cloud-agent overhead.

---

## Ready to ship

Options:
1. **Recommended:** Hand this directly to `/ppp` — it's already shaped and ready to build.
2. Pass to `/ship` (unnecessary for a single task, but available).
3. Stop here and keep the shaped output only.

Reply with `1`, `2`, or `3`.