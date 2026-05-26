# Response for ship-review-burden

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#100-100), lines 100 to 300

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#300-300), lines 300 to 500

Read skill [ship](file:///Users/marcus/.agents/skills/ship/SKILL.md?vscodeLinkType%3Dskill#500-500), lines 500 to 700

## Ship assessment

**Task:** Rename `experimentStatus` enum values across backend enum/serializer, shared frontend contract, results table, filters, API docs, and tests.

---

### Routing scorecard

| Dimension | Score | Note |
|---|---|---|
| Clarity | 4 | Rename scope is explicit; target values not yet confirmed |
| Boundedness | 4 | One semantic operation, many files but no ambiguity of scope |
| Verifiability | 4 | Tests exist and will catch regressions |
| Risk safety | 3 | User-visible behaviour + shared API contract |
| Independence | 2 | All layers depend on the same value mapping — consumers cannot merge before the definition |
| Conflict safety | 4 | File overlap is low per task description |
| Contract stability | 2 | The shared frontend contract is the unstable foundation until it is defined and merged |
| Review burden | 2 | Task flags this explicitly: every PR touches the same mapping; reviewers must reason across them together |

**Confidence:** Medium (based on task description; no code inspection yet)

---

### Route: Path A — Single PR, local PPP

**Recommended path: one PR, not a parallel split.**

The rename is a single atomic semantic operation. Splitting it into parallel PRs would force reviewers to hold the mapping in their heads across multiple reviews simultaneously — the task description itself identifies this as the risk. That is the worst outcome for review burden, and there is no compensating benefit: the work is not independent, and the shared frontend contract is unstable until one owner defines the canonical new values.

A two-wave plan (wave 1: contract; wave 2: consumers) is structurally sound, but the wave-2 PRs still all describe the same user-visible change, so review burden remains high and merge order must be enforced anyway. The one-PR plan achieves the same result with less coordination overhead and a clearer diff.

**One PR makes the mapping obvious in a single review.**

---

### Before starting — one blocker

The target enum values are not specified. This is a public API contract decision; Ship must not invent them.

> **Confirm:** What are the new `experimentStatus` values, replacing the current ones?

Once confirmed, proceed with PPP execution:

```text
Inspect → Clarify (resolved above) → Plan → Prove → Patch → Validate → Review → Commit → PR
```

Expected files in scope: backend enum definition, serializer, shared frontend contract/type, results table component, filter component(s), API docs, tests. All in one branch, one PR.