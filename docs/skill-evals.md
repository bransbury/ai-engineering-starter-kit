# Skill Evals

This repo includes a repo-local skill eval harness so skill updates can be scored for regressions and improvements across repeated runs, models, and agents.

The harness is intentionally pragmatic:

- it scores generated skill outputs against repo-local rubric cases
- it uses granular weighted criteria rather than one coarse pass/fail check per behaviour
- it supports both reward criteria and penalty criteria
- it rolls scores up by dimension so you can see where a model is strong or weak
- it writes scored results to run-local files
- it supports scaffolded multi-model runs
- it renders a scoreboard table so runs can be compared across models and agents
- it is good for catching drift and obvious regressions
- it is not a substitute for blind human review on real tasks

Use it as a repeatable regression check, not as ground truth.

## Reproducibility expectations

You should aim for stable scoring, not byte-identical text.

Most LLM providers do not guarantee perfectly identical output even when the model name is the same. The harness helps by recording:

- model/provider/agent metadata
- repo commit
- case, prompt, and skill file fingerprints
- one scored result file per run

For best repeatability:

- use a fresh session or thread per case
- keep the same model, provider, tool environment, and exposed sampling settings for the whole run
- do not mix responses from different commits in one run
- compare runs using the same case set and skill fingerprints

## What it evaluates

The eval harness checks outputs for the behaviour this repo cares about most:

- `shape` identifies a safe first PR and avoids premature coding
- `ship` chooses safe delivery waves and avoids unsafe parallelism
- `ppp` defines proof before patching and prefers behaviourally direct validation
- `ppp-cloud` stays bounded, proves the right thing, and stops cleanly when needed

The current case set includes both normal and adversarial cases:

- clear small-task routing
- broad work that must be split
- public API / auth ambiguity that should stop
- unsafe parallelism around moving contracts
- review-burden traps
- fake-proof traps where lint/typecheck/full-suite runs are weaker than targeted proof

## Case files

Eval assets live in:

- [evals/cases](/Users/marcus/Documents/GitHub/ai-engineering-starter-kit/evals/cases)
- [evals/prompts](/Users/marcus/Documents/GitHub/ai-engineering-starter-kit/evals/prompts)
- [evals/runs](/Users/marcus/Documents/GitHub/ai-engineering-starter-kit/evals/runs)
- [evals/README.md](/Users/marcus/Documents/GitHub/ai-engineering-starter-kit/evals/README.md)

Each case defines:

- the skill under test
- the prompt file
- weighted rubric criteria
- `reasoning_quality_notes` for human reviewers

Each criterion includes:

- a `dimension` such as `proof`, `routing`, `scope`, `blocker_handoff`, or `reviewability`
- a positive `reward` score or a negative `penalty`
- regex rules that decide whether the criterion matched

Each case's `reasoning_quality_notes` block includes:

- `weak`: what a weak answer tends to do
- `good`: what a good answer should do
- `excellent`: what an excellent answer should do

This lets one case distinguish:

- acceptable vs strong answers
- presence of the best choice vs merely a safe choice
- good behaviour vs explicit bad behaviour

For key discriminator cases, the harness also includes explicit `preferred_choice` criteria.

These encode the benchmark's view of the strongest answer for that case, for example:

- the preferred route
- the preferred proof
- the preferred first slice
- the preferred blocker structure

That means the benchmark now scores not just "was this safe enough?" but also "did it choose well?"

## Validate the harness

First validate the eval case files:

```bash
python3 scripts/eval_skills.py --validate-only
```

## Create a run scaffold

Create a scaffolded run directory for a specific model/agent:

```bash
python3 scripts/init_skill_eval_run.py \
  --run-id 2026-05-24-gpt-5-codex \
  --provider openai \
  --model gpt-5 \
  --agent codex
```

This creates:

```text
evals/runs/2026-05-24-gpt-5-codex/
  manifest.json
  manual-review.md
  prompts/
  responses/
  README.md
```

Each prompt bundle in `prompts/` is ready to paste into a fresh session for the named skill case.

## Run the cases manually

For each prompt bundle:

- open the matching file in `prompts/`
- run it against the target model/agent in a fresh session
- paste the final user-facing output into the matching file under `responses/`

The response filename must match the case ID:

```text
<case-id>.md
```

Each run also includes a manual-review companion sheet:

```text
manual-review.md
```

Use it to record:

- whether the best route was chosen
- whether the best proof was chosen
- blocker and handoff quality
- verbosity or genericness problems
- rubric false positives or false negatives

## Score a run

Score the run directly from its scaffold directory:

```bash
python3 scripts/eval_skills.py --run-dir evals/runs/2026-05-24-gpt-5-codex
```

This writes:

```text
evals/runs/2026-05-24-gpt-5-codex/results.json
evals/runs/2026-05-24-gpt-5-codex/results.md
```

After scoring, refresh the manual-review sheet so it includes machine-score hotspots:

```bash
python3 scripts/render_skill_manual_review_sheet.py \
  --run-dir evals/runs/2026-05-24-gpt-5-codex
```

It can also fail if any response is still missing or placeholder content:

```bash
python3 scripts/eval_skills.py \
  --run-dir evals/runs/2026-05-24-gpt-5-codex \
  --fail-on-missing
```

To compare against a previous run:

```bash
python3 scripts/eval_skills.py \
  --run-dir evals/runs/2026-05-24-gpt-5-codex \
  --baseline evals/runs/2026-05-10-gpt-5-codex/results.json \
  --fail-on-regression
```

## Build a cross-model scoreboard

After scoring one or more runs:

```bash
python3 scripts/render_skill_eval_scoreboard.py
```

This writes:

```text
evals/scoreboard.md
```

The scoreboard includes:

- run ID
- provider
- model
- model version if recorded
- agent
- completed case count
- overall score
- per-skill scores
- per-dimension scores
- pairwise comparisons across runs, including which run leads by skill, dimension, and case
- saturation analysis for skills, dimensions, cases, and rubric criteria
- a per-case matrix for comparing models on the same prompts

## Recommended workflow

1. Pick a stable model + tool environment for the run.
2. Scaffold one run directory per model/agent combination.
3. Generate responses for all cases, one fresh session per case.
4. Fill out `manual-review.md` while reading the responses.
5. Score each run with `eval_skills.py`.
6. Refresh `manual-review.md` so it includes machine-score hotspots.
7. Regenerate `evals/scoreboard.md`.
8. Compare against the previous baseline and inspect every regression manually before changing the skills again.

When comparing models:

- first check that the scoreboard fingerprint matches
- then compare overall score
- then compare per-skill scores
- then compare the pairwise section to see where one run actually leads
- then compare per-dimension scores
- then inspect the per-case matrix to see where one model is actually stronger or weaker

If an older run was scored before dimension-level analysis was added, the pairwise section will still compare:

- overall score
- per-skill scores
- top separating cases

Rescore older runs with the current harness to unlock dimension-level pairwise deltas.

The saturation section analyzes only comparable runs that share the same fingerprint. It labels each metric as:

- `high-signal` when it clearly separates models or agents
- `medium-signal` when it shows some useful spread
- `saturated` when it no longer separates runs in a meaningful way

Use that section to decide whether:

- a skill or case is still useful for model comparison
- a criterion is doing real discriminator work
- a case is becoming too easy and should be tightened later

The manual-review sheet complements this by capturing the judgement the regex harness cannot:

- best-vs-acceptable route choices
- best-vs-acceptable proof choices
- blocker quality and resumability
- verbosity or genericness problems
- obvious rubric misses despite the machine score

It also embeds each case's `reasoning_quality_notes` so the reviewer can calibrate against the intended weak / good / excellent answer patterns while reading the response.

## Limits

This harness is regex- and rubric-based. It will not perfectly capture nuanced reasoning quality or guarantee deterministic text.

Use it to catch:

- missing proof planning
- unsafe routing drift
- weaker blocker handoffs
- loss of reviewability signals
- partial quality differences between strong and very strong outputs

Do not use it alone to decide that a skill is good enough to ship.
