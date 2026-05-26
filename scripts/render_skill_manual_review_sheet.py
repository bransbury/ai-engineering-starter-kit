#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CASES_DIR = ROOT / "evals" / "cases"


def relative_string(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    return str(path)


def relative_markdown_target(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, start=from_file.parent).replace("\\", "/")


def load_manifest(run_dir: Path) -> dict[str, Any]:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"Run manifest does not exist: {manifest_path}")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{manifest_path}: invalid JSON: {exc}") from exc


def load_case_records(cases_dir: Path) -> list[dict[str, Any]]:
    case_files = sorted(cases_dir.glob("*.json"))
    if not case_files:
        raise ValueError(f"No eval case files found under {cases_dir}")
    records: list[dict[str, Any]] = []
    for path in case_files:
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    return records


def load_results(run_dir: Path) -> dict[str, Any] | None:
    results_path = run_dir / "results.json"
    if not results_path.exists():
        return None
    try:
        return json.loads(results_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{results_path}: invalid JSON: {exc}") from exc


def case_review_prompts(case_id: str, skill: str) -> list[str]:
    specific: dict[str, list[str]] = {
        "ppp-failing-test": [
            "Did it preserve the failing test or failing proof target rather than weakening it?",
            "Did it work one focused debugging hypothesis at a time rather than proposing a bundle of speculative fixes?",
            "If it stopped, did it leave the proof gap and smallest safe resumable next task?",
        ],
        "ppp-proof-trap": [
            "Did it choose the smallest behaviourally meaningful proof rather than the smallest command or largest validation bundle?",
            "Did it clearly deprioritize broad fake-proof options like lint or full-suite checks as the primary proof?",
            "Did it tie the proof back to the changed behaviour rather than generic confidence language?",
        ],
        "shape-large-feature": [
            "Did it identify the best first PR slice instead of routing broad work straight into implementation?",
            "Did it preserve enough shape to make the next implementation step obvious and safe?",
            "Did it route to the right next workflow rather than over-shaping or under-shaping?",
        ],
        "shape-public-api-ambiguity": [
            "Did it stop on the right ambiguity rather than guessing through public API or permission decisions?",
            "Did it preserve safe shaped work that can still be trusted?",
            "Did it state the smallest next shaped task after the missing decision?",
        ],
        "ship-foundation-first": [
            "Did it detect that foundation work should stabilize first before follow-on delivery?",
            "Did it avoid unsafe parallelism around moving contracts, schemas, or validation rules?",
            "Did it produce a reviewable wave plan rather than just a parallel plan?",
        ],
        "ship-review-burden": [
            "Did it reason about review burden, not just file overlap or implementation independence?",
            "Did it choose the best route for human reviewability?",
            "Did it avoid splitting work into PRs that force reviewers to reconstruct one shared behaviour across diffs?",
        ],
        "ppp-cloud-auth-unclear": [
            "Did it stop rather than guessing through auth, permission, or public API uncertainty?",
            "Did it explain why the ambiguity blocks safe autonomous execution?",
            "Did it leave a strong human handoff with the decision needed and next safe step?",
        ],
    }
    if case_id in specific:
        return specific[case_id]

    defaults: dict[str, list[str]] = {
        "ppp": [
            "Did it choose the best proof and keep the changed behaviour as the primary validation target?",
            "Did it keep the work bounded and reviewable rather than widening scope unnecessarily?",
            "If blocked, did it leave a useful proof gap and smallest safe resumable next task?",
        ],
        "ppp-cloud": [
            "Did it stay within one bounded autonomous task and avoid unsafe guessing?",
            "Did it choose the right proof or the right stop point?",
            "If blocked, did it leave a strong handoff for the human or next agent?",
        ],
        "shape": [
            "Did it identify the best first slice rather than just a safe slice?",
            "Did it stop only on material ambiguity that really affects safe shaping?",
            "Did it preserve enough shaped work and the next resumable task?",
        ],
        "ship": [
            "Did it choose the best delivery route, not just an acceptable one?",
            "Did it handle sequencing, review burden, and unsafe overlap correctly?",
            "Did it produce a plan that a strong engineering lead would actually want to run?",
        ],
    }
    return defaults.get(
        skill,
        [
            "Did it choose the best route or decision for the case?",
            "Did it preserve the right amount of rigor without unnecessary ceremony?",
            "Did it minimize rediscovery work if a human had to take over?",
        ],
    )


def score_summary(case_result: dict[str, Any] | None) -> str:
    if not case_result:
        return "Not scored yet."
    score = case_result.get("score", 0)
    max_score = case_result.get("max_score", 0)
    if max_score:
        percent = round((float(score) / float(max_score)) * 100, 1)
        return f"{score}/{max_score} ({percent}%)"
    return f"{score}/{max_score}"


def rubric_hotspots(case_result: dict[str, Any] | None) -> tuple[list[str], list[str]]:
    if not case_result:
        return [], []
    criteria = case_result.get("criteria") or case_result.get("checks") or []
    missed: list[str] = []
    penalties: list[str] = []
    for criterion in criteria:
        name = criterion.get("name", "unknown")
        points = criterion.get("points", 0)
        earned = float(criterion.get("earned", 0) or 0)
        kind = criterion.get("kind")
        if kind == "penalty" or earned < 0:
            if earned < 0:
                penalties.append(f"`{name}` ({earned:.0f} pts)")
            continue
        if points and earned <= 0:
            missed.append(f"`{name}` ({points} pts)")
    return missed[:6], penalties[:6]


def render_case_section(
    case_data: dict[str, Any],
    run_dir: Path,
    output_path: Path,
    case_result: dict[str, Any] | None,
) -> str:
    case_id = case_data["id"]
    skill = case_data["skill"]
    prompt_file = ROOT / case_data["prompt_path"]
    response_file = run_dir / "responses" / f"{case_id}.md"
    prompt_path = relative_markdown_target(output_path, prompt_file)
    response_path = relative_markdown_target(output_path, response_file)
    prompts = case_review_prompts(case_id, skill)
    reasoning_notes = case_data.get("reasoning_quality_notes") or {}
    missed, penalties = rubric_hotspots(case_result)

    lines = [f"## {case_id}", ""]
    lines.append(f"- Skill: `{skill}`")
    lines.append(f"- Goal: {case_data['description']}")
    lines.append(f"- Prompt: [{case_data['prompt_path']}]({prompt_path})")
    lines.append(f"- Response: [{case_id}.md]({response_path})")
    lines.append(f"- Machine score: {score_summary(case_result)}")
    lines.append("")
    if missed:
        lines.append("- Machine-missed reward criteria: " + ", ".join(missed) + ".")
    if penalties:
        lines.append("- Triggered penalties: " + ", ".join(penalties) + ".")
    if missed or penalties:
        lines.append("")

    if reasoning_notes:
        lines.append("Reasoning quality notes:")
        lines.append("")
        for label in ("weak", "good", "excellent"):
            notes = reasoning_notes.get(label) or []
            if not notes:
                continue
            lines.append(f"- {label.title()} answers usually:")
            for note in notes:
                lines.append(f"  - {note}")
        lines.append("")

    lines.append("Review checklist:")
    lines.append("")
    for index, prompt in enumerate(prompts, start=1):
        lines.append(f"{index}. {prompt}")
    lines.append("")
    lines.append("- Best route chosen? [ ] yes [ ] mixed [ ] no [ ] n/a")
    lines.append("- Best proof chosen? [ ] yes [ ] mixed [ ] no [ ] n/a")
    lines.append("- Blocker / handoff quality? [ ] strong [ ] acceptable [ ] weak [ ] n/a")
    lines.append("- Too verbose? [ ] no [ ] slightly [ ] yes")
    lines.append("- Too generic? [ ] no [ ] slightly [ ] yes")
    lines.append("- Any rubric miss despite obvious good/bad behaviour? [ ] no [ ] false positive [ ] false negative")
    lines.append("- Notes:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def render_manual_review_sheet(
    run_dir: Path,
    manifest: dict[str, Any],
    case_records: list[dict[str, Any]],
    results: dict[str, Any] | None,
    output_path: Path,
) -> str:
    model = manifest.get("model", {})
    agent = manifest.get("agent", {})
    run_id = manifest.get("run_id", run_dir.name)
    result_case_lookup = {
        case["id"]: case for case in (results.get("cases", []) if results else [])
    }
    overall_score = "Not scored yet."
    if results:
        totals = results.get("totals") or {}
        overall_score = f"{totals.get('score', 0)}/{totals.get('max_score', 0)} ({totals.get('percent', 0.0)}%)"

    lines = [f"# Skill Eval Manual Review: {run_id}", ""]
    lines.append("- Reviewer: `TODO`")
    lines.append("- Review date: `TODO`")
    lines.append(f"- Model: `{model.get('provider', '-')}/{model.get('name', '-')}`")
    lines.append(f"- Model version: `{model.get('version', '-') or '-'}`")
    lines.append(f"- Agent: `{agent.get('name', '-')}`")
    lines.append(f"- Repo commit: `{manifest.get('repo_commit') or '-'}`")
    lines.append(f"- Machine overall: {overall_score}")
    lines.append("")
    lines.append("## How To Use This Sheet")
    lines.append("")
    lines.append("1. Read the prompt bundle and the model response for each case.")
    lines.append("2. Compare the machine score with your judgement, especially on low-scoring or high-signal cases.")
    lines.append("3. Record where the rubric missed obvious quality or obvious failure.")
    lines.append("4. Keep notes short and concrete so rubric updates can be justified later.")
    lines.append("")
    lines.append("## Overall Calibration")
    lines.append("")
    lines.append("- Best route choices overall? [ ] yes [ ] mixed [ ] no")
    lines.append("- Best proof choices overall? [ ] yes [ ] mixed [ ] no [ ] n/a")
    lines.append("- Blocker / handoff quality overall? [ ] strong [ ] acceptable [ ] weak [ ] n/a")
    lines.append("- Too verbose overall? [ ] no [ ] slightly [ ] yes")
    lines.append("- Too generic overall? [ ] no [ ] slightly [ ] yes")
    lines.append("- Any obvious rubric false positives? [ ] no [ ] yes")
    lines.append("- Any obvious rubric false negatives? [ ] no [ ] yes")
    lines.append("- Biggest quality gap you noticed:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    lines.append("- Best evidence that the skill is working as intended:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    lines.append("## Case Reviews")
    lines.append("")
    for case_data in case_records:
        lines.append(
            render_case_section(
                case_data,
                run_dir,
                output_path,
                result_case_lookup.get(case_data["id"]),
            )
        )
    lines.append("## Rubric Calibration Notes")
    lines.append("")
    lines.append("- Criteria that should probably be added, split, or removed:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    lines.append("- Cases that are saturating and may need tightening later:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    lines.append("- Cases that are valuable discriminators and should stay:")
    lines.append("")
    lines.append("```text")
    lines.append("")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a manual review companion sheet for a skill eval run."
    )
    parser.add_argument(
        "--run-dir",
        required=True,
        help="Scaffolded eval run directory, e.g. evals/runs/2026-05-24-gpt-5-codex",
    )
    parser.add_argument(
        "--cases-dir",
        default=str(DEFAULT_CASES_DIR),
        help="Directory containing eval case JSON files.",
    )
    parser.add_argument(
        "--write-markdown",
        default="",
        help="Optional output path. Defaults to <run-dir>/manual-review.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = Path(args.run_dir).resolve()
    cases_dir = Path(args.cases_dir).resolve()
    if not run_dir.exists():
        print(f"Run directory does not exist: {run_dir}", file=sys.stderr)
        return 1

    try:
        manifest = load_manifest(run_dir)
        case_records = load_case_records(cases_dir)
        results = load_results(run_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    output_path = (
        Path(args.write_markdown).resolve()
        if args.write_markdown
        else run_dir / "manual-review.md"
    )
    output_path.write_text(
        render_manual_review_sheet(run_dir, manifest, case_records, results, output_path),
        encoding="utf-8",
    )
    print(f"Wrote manual review sheet: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
