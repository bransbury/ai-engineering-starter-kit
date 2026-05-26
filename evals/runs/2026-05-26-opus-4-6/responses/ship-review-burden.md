# Response for ship-review-burden

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#101-101), lines 101 to 250

Read skill [ship](file:///Users/mabr/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#251-251), lines 251 to 400

## Ship — Routing Decision

### Assessment

This is a **mechanical rename** of `experimentStatus` values across 6 areas of the stack. The work is:

- **Clear** — rename mapping is fully defined once you choose the new values
- **Bounded** — touches multiple files but all serve one coherent behaviour change
- **Testable** — grep for old values returns zero, tests pass
- **Tightly coupled** — every layer references the same enum values; splitting creates intermediate inconsistency

The critical observation: all changes share the **same rename mapping** and affect the **same user-visible behaviour**. Splitting into multiple PRs would *increase* review burden — each reviewer must hold the same mapping in mind and reason about partial completion states.

### Routing Scorecard

| Dimension | Score | Confidence |
|---|---|---|
| Clarity | 5 | High — mechanical rename |
| Boundedness | 4 | High — one coherent change across files |
| Verifiability | 5 | High — grep + test suite |
| Risk safety | 4 | High — no product/security/API design decision |
| Independence | 5 | High — no unmerged dependencies |
| Conflict safety | 5 | High — single PR, no branches to coordinate |
| Contract stability | 4 | High — the rename *is* the contract change |
| Review burden | 4 | High — one PR with consistent mechanical rename is easy to review |

### Route: Path A — Local PPP (single PR)

**Why one PR, not many:**

1. **Atomicity** — a rename is either done or not. Intermediate states (backend renamed, frontend not) break the system.
2. **Review coherence** — one PR with "old value → new value" across all layers is faster to review than 3–4 PRs that each require the reviewer to verify the same mapping.
3. **No independent parallelism** — the tasks share the same contract change. Parallelizing would violate the hard rule: *do not parallelize tasks that depend on an unmerged shared contract.*
4. **Small total diff** — a rename across 6 areas is typically < 200 lines changed, well within single-PR review capacity.

**Why PPP (human-led) over PPP Cloud:**

- The new enum values haven't been specified yet — one clarifying question is needed before execution.
- Human can verify the mapping looks right before committing.

### Recommended Plan

```
Wave 1 (single PR):
  1. Define the rename mapping (old → new values)
  2. Update backend enum + serializer
  3. Update shared frontend contract
  4. Update results table rendering + filters
  5. Update API docs
  6. Update tests
  7. Prove: grep for old values = 0, full test suite green
  8. One commit, one PR
```

### Open question (blocking)

**What are the new `experimentStatus` values?** Once you provide the mapping (e.g. `draft → pending`, `active → running`, etc.), I can execute the rename immediately as a single PPP pass.