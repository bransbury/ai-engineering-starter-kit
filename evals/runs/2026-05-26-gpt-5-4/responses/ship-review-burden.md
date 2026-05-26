# Response for ship-review-burden

Route: single PR with local PPP execution.

Confidence: High.

Why this route:

- This is one user-visible behaviour change: renaming `experimentStatus` values across backend, shared contract, UI rendering, filters, docs, and tests.
- Even if file overlap is limited, the semantic overlap is high. Reviewers would need to validate the same old-to-new status mapping across every PR.
- Splitting this into multiple PRs would increase review burden, create temporary contract drift risk, and make proof less clear because each PR would only validate part of the rename.
- The task is clear, bounded, and testable enough for one coherent change set. It does not need Shape, and it is not a good candidate for parallel work.

Recommended path:

1. Make the rename in one PR across backend enum/serializer, shared frontend contract, table rendering, filters, API docs, and tests.
2. Run the narrow proof for the full slice: backend serialization tests, frontend contract/type checks, affected UI/filter tests, and any API doc snapshot or schema checks.
3. Submit as a single review unit so reviewers can reason about the mapping once, end to end.

What I would not do:

- Do not split backend and frontend contract work into separate PRs.
- Do not parallelize docs/tests from the rename, because they are part of proving the same behaviour change.
- Do not use multi-PR worktree coordination here; it adds handoff and review cost without reducing risk.

Routing scorecard:

- Clarity: 5/5
- Boundedness: 4/5
- Verifiability: 5/5
- Risk safety: 4/5
- Independence: 2/5 across split PRs
- Conflict safety: 3/5 at file level, but 2/5 at behaviour/review level
- Contract stability: 2/5 until the rename lands everywhere together
- Review burden: 2/5 for split PRs, 5/5 for one PR
