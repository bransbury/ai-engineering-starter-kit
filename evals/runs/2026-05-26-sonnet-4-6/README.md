# Skill Eval Run: 2026-05-24-sonnet-4-6

1. Open each file in `prompts/`.
2. Run that prompt against the target agent/model in a fresh session.
3. Replace the placeholder content in the matching file under `responses/`.
4. Score the run:

```bash
python3 scripts/eval_skills.py --run-dir evals/runs/2026-05-24-sonnet-4-6
```

5. Update the scoreboard:

```bash
python3 scripts/render_skill_eval_scoreboard.py
```
