# Response for shape-clear-small-bug

## Understanding

Goal:
- Reject report names that become empty after trimming.

Current problem:
- The form currently allows a report name that is only whitespace to be saved.

Expected behaviour:
- Whitespace-only names should be treated as empty and rejected through the existing validation path.

Likely users/systems affected:
- Users creating or renaming reports.
- The report form validation logic and its tests.

Relevant constraints:
- Follow the existing validation style.
- Add or update tests.
- Do not redesign the report form.

Areas unclear:
- None that block shaping.

## Facts, assumptions, and open questions

### Known facts
- Whitespace-only report names are currently accepted.
- There is already an existing validation pattern for empty names.
- The fix should include test coverage.

### Assumptions
- The intended change is to trim for the emptiness check and reuse the existing empty-name validation outcome.
- Existing report form tests or nearby validation tests can be extended without broader refactoring.

### Open questions
- None blocking.

### Non-goals
- Redesigning the report form.
- Introducing new naming rules beyond whitespace-only rejection.
- Changing unrelated persistence or save flows.

## Scope

In scope:
- Reject whitespace-only names using the existing empty-name validation pattern.
- Add or update focused tests for whitespace-only rejection.

Out of scope:
- New validation rules for length, duplicates, or characters.
- UI redesign or new form interactions.

## Acceptance criteria

| ID | Acceptance criterion | Proof idea |
|---|---|---|
| AC1 | A report name composed only of whitespace is rejected the same way as an empty name. | Add or update a targeted test that submits whitespace-only input and asserts the existing validation result. |
| AC2 | A normal non-empty report name still passes validation under the current rules. | Keep or add a nearby positive-path test for a valid name. |
| AC3 | The fix reuses the existing validation pattern instead of introducing a new UX flow. | Review the implementation and confirm it routes through the current empty-name validation branch. |

## Task breakdown

| Task ID | Task | Scope | Non-goals | ACs | Dependencies | Proof | Expected files/modules | PR-size score | Split? | Risk |
|---|---|---|---|---|---|---|---|---:|---|---|
| T1 | Reject whitespace-only report names and cover the bug with tests | Update the report-name validation check so whitespace-only input is treated as empty, and extend tests for that path | Form redesign, unrelated validation changes, storage refactors | AC1, AC2, AC3 | None identified | Focused validation tests for whitespace-only rejection and a valid-name regression check | Report form validation code and its test file | 6 | No | Low |

No material decisions need confirmation. The task is already clear, bounded, and PR-sized.

## Delegation and parallel readiness

| Task ID | Clarity | Independence | Conflict risk | Risk | Verifiability | Recommendation | Evidence |
| ------- | ------: | -----------: | ------------: | ---: | -----------: | -------------- | -------- |
| T1 | 5 | 5 | 1 | 1 | 5 | /ppp | The ticket defines one local behaviour change, preserves the existing pattern, and has obvious focused proof through tests. |

## Shape result

Status:
- ready-for-ppp

Recommended next action:
- Pass T1 to /ppp and implement the validation fix plus focused tests in a single PR.

Why:
- This is a small, well-specified bug fix. Additional shaping would not reduce risk.

Confidence:
- High
