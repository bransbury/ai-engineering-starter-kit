# Current phase: Inspecting

## Understanding

Intended behaviour:
- Whitespace-only report names should be treated as empty and rejected using the existing validation pattern.

Current behaviour:
- A name like `"   "` is being accepted, which means validation is likely checking length before trimming.

Files/modules inspected:
- Validation logic for report names
- Existing report-name validation tests
- The create/save call site that sends the name into validation

Existing patterns to follow:
- Reuse the current validation schema/pattern rather than adding special-case form logic.
- Add a targeted test next to the existing validation tests.

Assumptions:
- There is already a validation rule for empty report names.
- The smallest safe fix is in shared validation, not the form component.

Risks:
- Trimming at the wrong layer could create inconsistent behaviour between create and edit flows.

| Area | File/module | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| Validation logic | `src/reports/validation.ts` | Confirmed | `reportNameSchema` rejects empty string but does not trim first | Most direct control point |
| Existing tests | `src/reports/validation.test.ts` | Confirmed | Covers empty string, not whitespace-only input | Closest proof target |
| Validation call site | `src/reports/create.ts` | Confirmed | Passes name straight into validation | No separate form-only guard |

Finding: `"   "` passes because the existing validation pattern applies the length check before trimming.

# Current phase: Planning

Smallest safe complete change:
- Trim the report name inside the shared validation pattern before the non-empty check.
- Add or update a targeted test covering whitespace-only input.

Proof before patch:
- Run the affected validation test file and confirm a whitespace-only name is rejected using the existing validation behaviour.

Choose an option:

1. Patch the shared validation and add the targeted test — recommended
2. Show the relevant validation code before patching
3. Stop here

# After patching: Current phase: Reviewing

Changes:
- `src/reports/validation.ts`: trim before the existing non-empty validation check
- `src/reports/validation.test.ts`: add a test proving whitespace-only names are rejected

Checks run:
- Targeted test for the affected validation behaviour

Review handoff:
- Small safe fix scoped to shared report-name validation
- No report form redesign
- No API or data-shape change expected

## PR

Title: `fix: reject whitespace-only report names`

Body:
> Whitespace-only report names were accepted because the existing validation pattern checked for non-empty input before trimming. This updates shared report-name validation to trim first and adds a targeted test covering the whitespace-only case.
>
> Proof: affected validation test updated to verify whitespace-only names are rejected.
