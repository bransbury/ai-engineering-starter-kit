#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from render_skill_manual_review_sheet import (
    load_case_records,
    render_manual_review_sheet,
)


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CASES_DIR = ROOT / "evals" / "cases"
DEFAULT_RUNS_DIR = ROOT / "evals" / "runs"


def git_commit() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return completed.stdout.strip() or None


def load_case_paths(cases_dir: Path) -> list[Path]:
    case_paths = sorted(cases_dir.glob("*.json"))
    if not case_paths:
        raise ValueError(f"No eval case files found under {cases_dir}")
    return case_paths


def relative_string(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    return str(path)


def render_prompt_bundle(case_data: dict, prompt_text: str, run_id: str) -> str:
    return f"""# Skill Eval Prompt Bundle

Run ID: `{run_id}`
Case ID: `{case_data['id']}`
Skill under test: `{case_data['skill']}`

## Execution rules

- Start a fresh session or thread for this case.
- Use the named skill naturally if the tool would normally trigger it.
- Do not reuse context from other eval cases.
- Do not mention the eval harness in the answer.
- Return the agent's normal user-facing output for this case.
- Keep the tool/model/settings fixed across the run if you want scores to be comparable.

## Prompt

{prompt_text.rstrip()}
"""


def response_placeholder(case_data: dict) -> str:
    return (
        f"# Response for {case_data['id']}\n\n"
        "<paste model output here>\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a scaffolded skill eval run directory."
    )
    parser.add_argument("--run-id", required=True, help="Run identifier, e.g. 2026-05-24-gpt-5-codex")
    parser.add_argument("--model", required=True, help="Model name, e.g. gpt-5")
    parser.add_argument("--provider", required=True, help="Model provider, e.g. openai")
    parser.add_argument("--agent", required=True, help="Agent/tool name, e.g. codex")
    parser.add_argument("--model-version", default="", help="Optional model snapshot/version string.")
    parser.add_argument("--temperature", default="", help="Temperature or equivalent setting if exposed.")
    parser.add_argument("--top-p", dest="top_p", default="", help="Top-p setting if exposed.")
    parser.add_argument("--reasoning-effort", default="", help="Reasoning effort setting if exposed.")
    parser.add_argument("--notes", default="", help="Optional notes for the run manifest.")
    parser.add_argument(
        "--cases-dir",
        default=str(DEFAULT_CASES_DIR),
        help="Directory containing eval case JSON files.",
    )
    parser.add_argument(
        "--runs-dir",
        default=str(DEFAULT_RUNS_DIR),
        help="Parent directory for scaffolded runs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases_dir = Path(args.cases_dir).resolve()
    runs_dir = Path(args.runs_dir).resolve()

    try:
        case_paths = load_case_paths(cases_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    run_dir = runs_dir / args.run_id
    if run_dir.exists():
        print(f"Run directory already exists: {run_dir}", file=sys.stderr)
        return 1

    prompts_dir = run_dir / "prompts"
    responses_dir = run_dir / "responses"
    prompts_dir.mkdir(parents=True)
    responses_dir.mkdir(parents=True)

    manifest = {
        "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo_commit": git_commit(),
        "cases_dir": relative_string(cases_dir),
        "model": {
            "provider": args.provider,
            "name": args.model,
            "version": args.model_version,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "reasoning_effort": args.reasoning_effort,
        },
        "agent": {
            "name": args.agent,
        },
        "notes": args.notes,
        "reproducibility": {
            "instructions": [
                "Use a fresh session/thread per case.",
                "Keep the same model, provider, tool environment, and exposed sampling settings for the whole run.",
                "Do not mix responses from different commits or different skill versions in one run.",
                "Exact output identity is not guaranteed by most LLM providers; compare scores and drift, not just byte-for-byte text.",
            ]
        },
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    for case_path in case_paths:
        case_data = json.loads(case_path.read_text(encoding="utf-8"))
        prompt_path = ROOT / case_data["prompt_path"]
        prompt_text = prompt_path.read_text(encoding="utf-8")
        prompt_bundle = render_prompt_bundle(case_data, prompt_text, args.run_id)
        (prompts_dir / f"{case_data['id']}.md").write_text(prompt_bundle, encoding="utf-8")
        (responses_dir / f"{case_data['id']}.md").write_text(
            response_placeholder(case_data),
            encoding="utf-8",
        )

    manual_review_path = run_dir / "manual-review.md"
    manual_review_path.write_text(
        render_manual_review_sheet(
            run_dir,
            manifest,
            load_case_records(cases_dir),
            results=None,
            output_path=manual_review_path,
        ),
        encoding="utf-8",
    )

    readme = f"""# Skill Eval Run: {args.run_id}

1. Open each file in `prompts/`.
2. Run that prompt against the target agent/model in a fresh session.
3. Replace the placeholder content in the matching file under `responses/`.
4. Complete `manual-review.md` as you review the run quality by hand.
5. Score the run:

```bash
python3 scripts/eval_skills.py --run-dir {relative_string(run_dir)}
```

6. Refresh the manual review sheet so it includes machine score hotspots:

```bash
python3 scripts/render_skill_manual_review_sheet.py --run-dir {relative_string(run_dir)}
```

7. Update the scoreboard:

```bash
python3 scripts/render_skill_eval_scoreboard.py
```
"""
    (run_dir / "README.md").write_text(readme, encoding="utf-8")

    print(f"Created skill eval run scaffold: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
