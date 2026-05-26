# Skill Eval Assets

- `cases/` contains rubric definitions.
- each case now also includes `reasoning_quality_notes` for weak / good / excellent human calibration
- `prompts/` contains shared prompt files used by cases.
- `runs/` contains scaffolded multi-model eval runs.
- `scoreboard.md` is the generated cross-run comparison table.
- each run can also include `manual-review.md`, a human-review companion sheet

Create a new run scaffold with:

```bash
python3 scripts/init_skill_eval_run.py \
  --run-id 2026-05-24-gpt-5-codex \
  --provider openai \
  --model gpt-5 \
  --agent codex
```

Then score it with:

```bash
python3 scripts/eval_skills.py --run-dir evals/runs/2026-05-24-gpt-5-codex
```

Refresh the human-review companion sheet with machine-score hotspots:

```bash
python3 scripts/render_skill_manual_review_sheet.py \
  --run-dir evals/runs/2026-05-24-gpt-5-codex
```

And regenerate the scoreboard with:

```bash
python3 scripts/render_skill_eval_scoreboard.py
```
