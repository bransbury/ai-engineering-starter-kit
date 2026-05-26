# Response for ship-foundation-first

Route: foundation-first two-wave delivery. Use local PPP for wave 1, then reassess for a small parallel wave 2 only after the shared base is stable.

Confidence: Medium.

Why this route:

- The shared TypeScript contract, backend response shape, and validation/schema logic are the foundation. Those are unstable until the first change lands, so do not parallelize work that depends on them.
- Splitting everything immediately would raise review burden: reviewers would need to track merge order, cross-PR contract drift, and duplicated fixes across API, UI, and export paths.
- This is clear enough to execute, but not safe enough to send straight into parallel autonomous work before the base is stabilized.

Wave 1:

- One PR that adds `confidenceBand` to the backend API response, shared experiment-result contract, and validation/schema logic.
- Update the narrow tests that prove the contract and validation base are correct.
- This PR establishes the merge point for everything else.

Wave 2:

- After wave 1 merges, handle the dependent surfaces: results table UI, CSV export, and any docs or follow-on tests.
- If inspection shows the UI and CSV paths are cleanly separated and review capacity exists, split wave 2 into at most two parallel tasks. Otherwise keep wave 2 as one follow-on PR.

What I would not do:

- Do not parallelize the backend, contract, validation, UI, and export changes from the start.
- Do not create multiple PRs that all touch the moving shared contract or validation base.

Routing scorecard:

- Clarity: 4/5
- Boundedness: 3/5
- Verifiability: 4/5
- Risk safety: 4/5
- Independence: 2/5 before foundation, 4/5 after foundation
- Conflict safety: 2/5 before foundation, 4/5 after foundation
- Contract stability: 2/5 before wave 1, 4/5 after wave 1
- Review burden: 3/5 with two waves, lower than immediate multi-PR parallelism

Recommended delivery path:

1. Wave 1 single PR: contract/schema/validation foundation.
2. Merge and validate.
3. Wave 2: UI, CSV export, docs, and remaining tests, with at most two parallel tasks if the post-foundation inspection shows clean independence.
