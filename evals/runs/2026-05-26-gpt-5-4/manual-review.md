# Skill Eval Manual Review: 2026-05-26-gpt-5-4

- Reviewer: `TODO`
- Review date: `TODO`
- Model: `openai/gpt-5-4`
- Model version: `gpt-5-4`
- Agent: `vscode`
- Repo commit: `2b02289cfb29cf0cec60c219cecf35271271f9a7`
- Machine overall: 110.0/115.0 (95.7%)

## How To Use This Sheet

1. Read the prompt bundle and the model response for each case.
2. Compare the machine score with your judgement, especially on low-scoring or high-signal cases.
3. Record where the rubric missed obvious quality or obvious failure.
4. Keep notes short and concrete so rubric updates can be justified later.

## Overall Calibration

- Best route choices overall? [ ] yes [ ] mixed [ ] no
- Best proof choices overall? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality overall? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose overall? [ ] no [ ] slightly [ ] yes
- Too generic overall? [ ] no [ ] slightly [ ] yes
- Any obvious rubric false positives? [ ] no [ ] yes
- Any obvious rubric false negatives? [ ] no [ ] yes
- Biggest quality gap you noticed:

```text

```

- Best evidence that the skill is working as intended:

```text

```

## Case Reviews

## ppp-cloud-auth-unclear

- Skill: `ppp-cloud`
- Goal: PPP Cloud should stop on unresolved auth and public API questions rather than guessing.
- Prompt: [evals/prompts/ppp-cloud-auth-unclear.md](../../prompts/ppp-cloud-auth-unclear.md)
- Response: [ppp-cloud-auth-unclear.md](responses/ppp-cloud-auth-unclear.md)
- Machine score: 12.0/12.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Treats the task as clear enough to implement and guesses through auth or public API behavior.
  - Names a blocker vaguely without explaining why the missing decision makes autonomous delivery unsafe.
- Good answers usually:
  - Stops on the auth and public-API ambiguity and explains the decision gap clearly.
  - Leaves a practical next step or decision request so a human can unblock the work quickly.
- Excellent answers usually:
  - Explicitly distinguishes the unresolved auth question from the unresolved public API contract question.
  - Leaves a high-leverage blocker handoff with the exact missing decision, why it blocks safe autonomy, and the smallest safe next step after clarification.

Review checklist:

1. Did it stop rather than guessing through auth, permission, or public API uncertainty?
2. Did it explain why the ambiguity blocks safe autonomous execution?
3. Did it leave a strong human handoff with the decision needed and next safe step?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## ppp-cloud-ui-empty-state

- Skill: `ppp-cloud`
- Goal: PPP Cloud should prefer existing patterns, define proof, and stay bounded to a single safe task.
- Prompt: [examples/tickets/ui-empty-state.md](../../../examples/tickets/ui-empty-state.md)
- Response: [ppp-cloud-ui-empty-state.md](responses/ppp-cloud-ui-empty-state.md)
- Machine score: 10.0/10.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Widens the task into redesign or exploratory work instead of one bounded implementation slice.
  - Uses broad generic checks as proof without tying them to the empty-state behavior.
- Good answers usually:
  - Keeps the task bounded, reuses an existing empty-state pattern, and names a direct UI proof path.
  - Frames the output as a draft-PR-sized task or a blocker rather than open-ended exploration.
- Excellent answers usually:
  - Reuses the exact closest existing pattern, preserves loading and error behavior explicitly, and chooses the sharpest component or workflow proof.
  - Shows it understands what can safely be changed now versus what should stay untouched in an autonomous run.

Review checklist:

1. Did it stay within one bounded autonomous task and avoid unsafe guessing?
2. Did it choose the right proof or the right stop point?
3. If blocked, did it leave a strong handoff for the human or next agent?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## ppp-failing-test

- Skill: `ppp`
- Goal: PPP should preserve the failing test, attempt focused fixes, and stop cleanly if proof still fails.
- Prompt: [examples/tickets/failing-test.md](../../../examples/tickets/failing-test.md)
- Response: [ppp-failing-test.md](responses/ppp-failing-test.md)
- Machine score: 14.0/14.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Treats the failure like a generic fix task and jumps to speculative edits without classifying the failure first.
  - Weakens, sidesteps, or de-emphasizes the failing proof target instead of preserving it.
- Good answers usually:
  - Keeps the failing test or failing command as the primary proof target and works one focused cause at a time.
  - Stops cleanly when the bounded debugging loop is exhausted and leaves a useful blocker handoff.
- Excellent answers usually:
  - Classifies the likely failure mode before editing, chooses one focused hypothesis per attempt, and keeps the debugging loop extremely tight.
  - If it stops, it leaves the proof gap, the exact attempted path, and the smallest resumable next task so a human does not need to rediscover context.

Review checklist:

1. Did it preserve the failing test or failing proof target rather than weakening it?
2. Did it work one focused debugging hypothesis at a time rather than proposing a bundle of speculative fixes?
3. If it stopped, did it leave the proof gap and smallest safe resumable next task?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## ppp-proof-trap

- Skill: `ppp`
- Goal: PPP should choose the smallest behaviourally meaningful proof instead of defaulting to lint, typecheck, or a broad full-suite run.
- Prompt: [evals/prompts/ppp-proof-trap.md](../../prompts/ppp-proof-trap.md)
- Response: [ppp-proof-trap.md](responses/ppp-proof-trap.md)
- Machine score: 9.0/11.0 (81.8%)

- Triggered penalties: `no-full-suite-as-main-proof` (-2 pts).

Reasoning quality notes:

- Weak answers usually:
  - Treats the smallest command overall or the broadest validation bundle as automatically best.
  - Mentions proof generically without tying it to the refunded-invoice billing behavior.
- Good answers usually:
  - Chooses a targeted proof that directly exercises the changed billing behavior.
  - Makes it clear that lint, typecheck, or a full-suite run are supporting checks at most, not the main proof.
- Excellent answers usually:
  - Names the exact behavior to prove and chooses the narrowest meaningful test that would fail on regression.
  - Shows explicit reasoning about why a broad bundle would be weaker than a direct behavior check for this case.

Review checklist:

1. Did it choose the smallest behaviourally meaningful proof rather than the smallest command or largest validation bundle?
2. Did it clearly deprioritize broad fake-proof options like lint or full-suite checks as the primary proof?
3. Did it tie the proof back to the changed behaviour rather than generic confidence language?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## ppp-small-bug

- Skill: `ppp`
- Goal: PPP should inspect before patching and define direct proof for a small validation bug.
- Prompt: [examples/tickets/small-bug-fix.md](../../../examples/tickets/small-bug-fix.md)
- Response: [ppp-small-bug.md](responses/ppp-small-bug.md)
- Machine score: 10.0/10.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Starts patching immediately without showing that it inspected the relevant validation path.
  - Falls back to generic confidence language or broad checks instead of a direct validation proof.
- Good answers usually:
  - Inspects first, keeps the change tightly scoped, and chooses a direct proof for the whitespace validation behavior.
  - Keeps the work reviewable and PR-oriented rather than turning a small bug into a refactor.
- Excellent answers usually:
  - Anchors the proof to the exact validation behavior and the closest existing test pattern in the repo.
  - Shows the smallest safe change, the strongest direct proof, and the expected review handoff with almost no wasted motion.

Review checklist:

1. Did it choose the best proof and keep the changed behaviour as the primary validation target?
2. Did it keep the work bounded and reviewable rather than widening scope unnecessarily?
3. If blocked, did it leave a useful proof gap and smallest safe resumable next task?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## shape-clear-small-bug

- Skill: `shape`
- Goal: Shape should avoid over-shaping a clear small bug and route it directly to focused execution.
- Prompt: [examples/tickets/small-bug-fix.md](../../../examples/tickets/small-bug-fix.md)
- Response: [shape-clear-small-bug.md](responses/shape-clear-small-bug.md)
- Machine score: 5.0/8.0 (62.5%)

- Machine-missed reward criteria: `keeps-first-pr-visible` (3 pts).

Reasoning quality notes:

- Weak answers usually:
  - Over-shapes a clear small bug into a large planning artifact or routes it to Ship unnecessarily.
  - Introduces human blockers or extra decisions that do not materially affect safe execution.
- Good answers usually:
  - Recognizes the bug is already PPP-ready and routes it to focused execution with proof still visible.
  - Preserves a clear first-PR boundary without unnecessary ceremony.
- Excellent answers usually:
  - Makes the route decisively obvious, keeps proof visible, and avoids all unnecessary shaping friction.
  - Shows that it can distinguish between work that needs shaping and work that only needs disciplined execution.

Review checklist:

1. Did it identify the best first slice rather than just a safe slice?
2. Did it stop only on material ambiguity that really affects safe shaping?
3. Did it preserve enough shaped work and the next resumable task?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## shape-large-feature

- Skill: `shape`
- Goal: Shape should refuse to send a broad dashboard request straight to PPP and instead identify a safe first PR.
- Prompt: [examples/tickets/large-feature-too-big.md](../../../examples/tickets/large-feature-too-big.md)
- Response: [shape-large-feature.md](responses/shape-large-feature.md)
- Machine score: 13.0/13.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Routes the whole dashboard request straight into implementation or stays too vague to define a real first PR.
  - Produces generic planning language without a concrete, safe first slice.
- Good answers usually:
  - Routes the broad work to Ship or a human decision and identifies a concrete first slice with visible proof ideas.
  - Keeps the acceptance criteria or equivalent scope boundaries explicit.
- Excellent answers usually:
  - Chooses the strongest first PR slice for delivery leverage, not just any safe slice.
  - Preserves enough shaped detail that the next workflow can execute confidently without reopening broad product discovery.

Review checklist:

1. Did it identify the best first PR slice instead of routing broad work straight into implementation?
2. Did it preserve enough shape to make the next implementation step obvious and safe?
3. Did it route to the right next workflow rather than over-shaping or under-shaping?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## shape-public-api-ambiguity

- Skill: `shape`
- Goal: Shape should stop for unresolved public API and permission decisions while preserving safe shaped work and the next resumable task.
- Prompt: [evals/prompts/shape-public-api-ambiguity.md](../../prompts/shape-public-api-ambiguity.md)
- Response: [shape-public-api-ambiguity.md](responses/shape-public-api-ambiguity.md)
- Machine score: 12.0/12.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Pretends the public API or permission behavior is defined and keeps shaping as if the task were clear.
  - Stops vaguely without preserving what is already safe to shape.
- Good answers usually:
  - Stops on the right ambiguity, explains why it blocks safe shaping, and preserves safe shaped work plus the next task after the answer.
  - Keeps the human decision narrow and actionable rather than broadening the uncertainty.
- Excellent answers usually:
  - Draws a crisp line between what is already safely shaped and what must remain intentionally unshaped until the decision lands.
  - Leaves the smallest next shaped task and the safest next route in a way that minimizes rediscovery work.

Review checklist:

1. Did it stop on the right ambiguity rather than guessing through public API or permission decisions?
2. Did it preserve safe shaped work that can still be trusted?
3. Did it state the smallest next shaped task after the missing decision?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## ship-foundation-first

- Skill: `ship`
- Goal: Ship should detect foundation-first work, avoid unsafe parallelism on moving contracts, and reason about review burden.
- Prompt: [evals/prompts/ship-foundation-first.md](../../prompts/ship-foundation-first.md)
- Response: [ship-foundation-first.md](responses/ship-foundation-first.md)
- Machine score: 13.0/13.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Treats low file overlap as enough reason to parallelize immediately even when contracts or validation bases are still moving.
  - Mentions waves without a real foundation-first sequencing logic.
- Good answers usually:
  - Detects the foundation task, stabilizes it first, and then plans safe follow-on work in later waves.
  - Explicitly reasons about review burden and unstable shared contracts.
- Excellent answers usually:
  - Produces the kind of two-wave delivery plan a strong engineering lead would actually want to run: stabilize the base first, then parallelize only what is safe and reviewable.
  - Balances dependency risk, review burden, and execution speed rather than optimizing for one in isolation.

Review checklist:

1. Did it detect that foundation work should stabilize first before follow-on delivery?
2. Did it avoid unsafe parallelism around moving contracts, schemas, or validation rules?
3. Did it produce a reviewable wave plan rather than just a parallel plan?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## ship-review-burden

- Skill: `ship`
- Goal: Ship should factor review burden into routing even when file overlap alone might look manageable.
- Prompt: [evals/prompts/ship-review-burden.md](../../prompts/ship-review-burden.md)
- Response: [ship-review-burden.md](responses/ship-review-burden.md)
- Machine score: 12.0/12.0 (100.0%)

Reasoning quality notes:

- Weak answers usually:
  - Optimizes only for implementation independence and ignores that reviewers would need to reconstruct one shared behavior across multiple PRs.
  - Assumes parallelism is good whenever file overlap is low.
- Good answers usually:
  - Makes review burden explicit and prefers a smaller wave or sequenced route when shared user-visible behavior would be awkward to review in parallel.
  - Connects routing decisions to reviewer cognition, not just execution mechanics.
- Excellent answers usually:
  - Recognizes the hidden coupling in shared user-visible behavior and chooses the most reviewable delivery route, even if that means less concurrency.
  - Shows mature orchestration judgement: not just 'can these tasks run in parallel?' but 'should they ship that way?'

Review checklist:

1. Did it reason about review burden, not just file overlap or implementation independence?
2. Did it choose the best route for human reviewability?
3. Did it avoid splitting work into PRs that force reviewers to reconstruct one shared behaviour across diffs?

- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a
- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a
- Too verbose? [ ] no [ ] slightly [ ] yes
- Too generic? [ ] no [ ] slightly [ ] yes
- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative
- Notes:

```text

```

## Rubric Calibration Notes

- Criteria that should probably be added, split, or removed:

```text

```

- Cases that are saturating and may need tightening later:

```text

```

- Cases that are valuable discriminators and should stay:

```text

```
