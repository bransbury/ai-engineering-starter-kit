#!/usr/bin/env python3

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RUNS_DIR = ROOT / "evals" / "runs"
DEFAULT_OUTPUT = ROOT / "evals" / "scoreboard.md"


def relative_string(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    return str(path)


def load_results_files(runs_dir: Path) -> list[Path]:
    return sorted(runs_dir.glob("*/results.json"))


def load_result(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def percent_for_skill(result: dict[str, Any], skill: str) -> str:
    per_skill = result.get("per_skill", {})
    totals = per_skill.get(skill)
    if not totals:
        return "-"
    return f"{totals.get('percent', 0.0)}%"


def percent_for_dimension(result: dict[str, Any], dimension: str) -> str:
    dimensions = result.get("dimensions", {})
    totals = dimensions.get(dimension)
    if not totals:
        return "-"
    return f"{totals.get('percent', 0.0)}%"


def titleize_dimension(dimension: str) -> str:
    return dimension.replace("_", " ").replace("-", " ").title()


def titleize_skill(skill: str) -> str:
    mapping = {
        "ppp": "PPP",
        "ppp-cloud": "PPP Cloud",
        "shape": "Shape",
        "ship": "Ship",
    }
    return mapping.get(skill, skill.replace("-", " ").title())


def metric_label(kind: str, metric_id: str) -> str:
    if kind == "skill":
        return titleize_skill(metric_id)
    if kind == "dimension":
        return titleize_dimension(metric_id)
    if kind == "case":
        return metric_id
    return metric_id


def score_percent_map(result: dict[str, Any], key: str) -> dict[str, float]:
    if key == "dimensions":
        entries = result.get("dimensions") or {}
    elif key == "per_skill":
        entries = result.get("per_skill") or {}
    else:
        raise ValueError(f"Unsupported score map key: {key}")
    return {
        entry_id: float((totals or {}).get("percent", 0.0))
        for entry_id, totals in entries.items()
    }


def case_percent_map(result: dict[str, Any]) -> dict[str, float]:
    case_map: dict[str, float] = {}
    for case in result.get("cases", []) or []:
        case_id = case.get("id")
        max_score = float(case.get("max_score", 0) or 0)
        score = float(case.get("score", 0) or 0)
        if not case_id:
            continue
        case_map[case_id] = round((score / max_score) * 100, 1) if max_score else 0.0
    return case_map


def result_fingerprint(result: dict[str, Any]) -> str:
    fingerprints = result.get("fingerprints") or {}
    return fingerprints.get("combined_sha256") or "-"


def run_label(path: Path, result: dict[str, Any]) -> str:
    manifest = result.get("manifest") or {}
    return manifest.get("run_id", path.parent.name)


def model_label(result: dict[str, Any]) -> str:
    manifest = result.get("manifest") or {}
    model = manifest.get("model", {})
    agent = manifest.get("agent", {})
    model_name = model.get("name", "-")
    agent_name = agent.get("name", "-")
    return f"{model_name} ({agent_name})"


def format_delta(delta: float) -> str:
    if delta > 0:
        return f"+{delta:.1f} pts"
    if delta < 0:
        return f"{delta:.1f} pts"
    return "0.0 pts"


def compare_percent_maps(
    left: dict[str, float], right: dict[str, float]
) -> tuple[list[tuple[str, float]], list[tuple[str, float]], list[str]]:
    left_wins: list[tuple[str, float]] = []
    right_wins: list[tuple[str, float]] = []
    ties: list[str] = []
    for metric_id in sorted(set(left) | set(right)):
        left_value = left.get(metric_id)
        right_value = right.get(metric_id)
        if left_value is None or right_value is None:
            continue
        delta = round(left_value - right_value, 1)
        if delta > 0:
            left_wins.append((metric_id, delta))
        elif delta < 0:
            right_wins.append((metric_id, abs(delta)))
        else:
            ties.append(metric_id)
    left_wins.sort(key=lambda item: (-item[1], item[0]))
    right_wins.sort(key=lambda item: (-item[1], item[0]))
    ties.sort()
    return left_wins, right_wins, ties


def render_pairwise_section(results: list[tuple[Path, dict[str, Any]]]) -> list[str]:
    lines = ["## Pairwise Comparison", ""]
    if len(results) < 2:
        lines.append("Need at least two scored runs for pairwise comparison.")
        lines.append("")
        return lines

    for (left_path, left_result), (right_path, right_result) in itertools.combinations(
        results, 2
    ):
        left_run = run_label(left_path, left_result)
        right_run = run_label(right_path, right_result)
        left_model = model_label(left_result)
        right_model = model_label(right_result)
        left_overall = float((left_result.get("totals") or {}).get("percent", 0.0))
        right_overall = float((right_result.get("totals") or {}).get("percent", 0.0))
        overall_delta = round(left_overall - right_overall, 1)
        fingerprint_match = result_fingerprint(left_result) == result_fingerprint(
            right_result
        )

        lines.append(f"### {left_run} vs {right_run}")
        lines.append("")
        lines.append(f"- `{left_run}`: {left_model}")
        lines.append(f"- `{right_run}`: {right_model}")
        if fingerprint_match:
            lines.append("- Fingerprint match: yes")
        else:
            lines.append(
                "- Fingerprint match: no. Treat this as a directional comparison only."
            )
        if overall_delta > 0:
            lines.append(
                f"- Overall winner: `{left_run}` by {format_delta(overall_delta)}."
            )
        elif overall_delta < 0:
            lines.append(
                f"- Overall winner: `{right_run}` by {format_delta(abs(overall_delta))}."
            )
        else:
            lines.append("- Overall result: tie.")
        lines.append("")

        left_skills, right_skills, tied_skills = compare_percent_maps(
            score_percent_map(left_result, "per_skill"),
            score_percent_map(right_result, "per_skill"),
        )
        lines.append("#### Skill Edges")
        lines.append("")
        lines.append(
            f"- `{left_run}` leads on: "
            + (
                ", ".join(
                    f"`{titleize_skill(skill)}` ({format_delta(delta)})"
                    for skill, delta in left_skills
                )
                if left_skills
                else "none"
            )
            + "."
        )
        lines.append(
            f"- `{right_run}` leads on: "
            + (
                ", ".join(
                    f"`{titleize_skill(skill)}` ({format_delta(delta)})"
                    for skill, delta in right_skills
                )
                if right_skills
                else "none"
            )
            + "."
        )
        if tied_skills:
            lines.append(
                "- Tied skills: "
                + ", ".join(f"`{titleize_skill(skill)}`" for skill in tied_skills)
                + "."
            )
        lines.append("")

        left_dimensions = score_percent_map(left_result, "dimensions")
        right_dimensions = score_percent_map(right_result, "dimensions")
        lines.append("#### Dimension Edges")
        lines.append("")
        if left_dimensions and right_dimensions:
            left_dim_wins, right_dim_wins, tied_dims = compare_percent_maps(
                left_dimensions, right_dimensions
            )
            lines.append(
                f"- `{left_run}` leads on: "
                + (
                    ", ".join(
                        f"`{titleize_dimension(dimension)}` ({format_delta(delta)})"
                        for dimension, delta in left_dim_wins
                    )
                    if left_dim_wins
                    else "none"
                )
                + "."
            )
            lines.append(
                f"- `{right_run}` leads on: "
                + (
                    ", ".join(
                        f"`{titleize_dimension(dimension)}` ({format_delta(delta)})"
                        for dimension, delta in right_dim_wins
                    )
                    if right_dim_wins
                    else "none"
                )
                + "."
            )
            if tied_dims:
                lines.append(
                    "- Tied dimensions: "
                    + ", ".join(
                        f"`{titleize_dimension(dimension)}`" for dimension in tied_dims
                    )
                    + "."
                )
        else:
            lines.append(
                "- Dimension-level comparison unavailable. Rescore these runs with the newer eval harness to unlock dimension deltas."
            )
        lines.append("")

        left_cases, right_cases, tied_cases = compare_percent_maps(
            case_percent_map(left_result),
            case_percent_map(right_result),
        )
        lines.append("#### Top Separating Cases")
        lines.append("")
        lines.append(
            f"- `{left_run}` strongest cases: "
            + (
                ", ".join(
                    f"`{case_id}` ({format_delta(delta)})"
                    for case_id, delta in left_cases[:5]
                )
                if left_cases
                else "none"
            )
            + "."
        )
        lines.append(
            f"- `{right_run}` strongest cases: "
            + (
                ", ".join(
                    f"`{case_id}` ({format_delta(delta)})"
                    for case_id, delta in right_cases[:5]
                )
                if right_cases
                else "none"
            )
            + "."
        )
        if tied_cases:
            lines.append(
                f"- Tied cases: {len(tied_cases)} of {len(set(case_percent_map(left_result)) | set(case_percent_map(right_result)))}."
            )
        lines.append("")

    return lines


def criterion_percent_map(result: dict[str, Any]) -> dict[str, float]:
    metric_map: dict[str, float] = {}
    for case in result.get("cases", []) or []:
        case_id = case.get("id")
        if not case_id:
            continue
        criteria = case.get("criteria") or case.get("checks") or []
        for criterion in criteria:
            name = criterion.get("name")
            points = float(criterion.get("points", 0) or 0)
            if not name or points <= 0:
                continue
            earned = float(criterion.get("earned", 0) or 0)
            percent = round((earned / points) * 100, 1)
            metric_map[f"{case_id} / {name}"] = percent
    return metric_map


def group_results_by_fingerprint(
    results: list[tuple[Path, dict[str, Any]]]
) -> dict[str, list[tuple[Path, dict[str, Any]]]]:
    grouped: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for path, result in results:
        grouped.setdefault(result_fingerprint(result), []).append((path, result))
    return grouped


def classify_signal(
    values: list[float], full_credit_count: int
) -> tuple[str, str, float, int, float]:
    if not values:
        return ("unavailable", "No comparable scored values.", 0.0, 0, 0.0)
    spread = round(max(values) - min(values), 1)
    unique_count = len({round(value, 1) for value in values})
    full_credit_rate = round((full_credit_count / len(values)) * 100, 1)
    average = round(sum(values) / len(values), 1)

    if spread == 0:
        if full_credit_count == len(values):
            return (
                "saturated",
                "All comparable runs hit full credit.",
                spread,
                unique_count,
                full_credit_rate,
            )
        return (
            "saturated",
            f"No separating power. All comparable runs clustered at {average}%.",
            spread,
            unique_count,
            full_credit_rate,
        )
    if spread >= 20 or unique_count >= 3:
        return (
            "high-signal",
            f"Clear separation across runs with {spread:.1f} pts of spread.",
            spread,
            unique_count,
            full_credit_rate,
        )
    if spread >= 8:
        return (
            "medium-signal",
            f"Some separation across runs with {spread:.1f} pts of spread.",
            spread,
            unique_count,
            full_credit_rate,
        )
    return (
        "saturated",
        f"Low separation only ({spread:.1f} pts spread).",
        spread,
        unique_count,
        full_credit_rate,
    )


def build_saturation_rows(
    results: list[tuple[Path, dict[str, Any]]],
    metric_kind: str,
    extractor,
) -> list[dict[str, Any]]:
    per_run_maps = [extractor(result) for _, result in results]
    metric_ids: list[str] = []
    for metric_map in per_run_maps:
        for metric_id in metric_map:
            if metric_id not in metric_ids:
                metric_ids.append(metric_id)

    rows: list[dict[str, Any]] = []
    for metric_id in metric_ids:
        values = [metric_map[metric_id] for metric_map in per_run_maps if metric_id in metric_map]
        if len(values) < 2:
            continue
        full_credit_count = sum(1 for value in values if value >= 100.0)
        signal, note, spread, unique_count, full_credit_rate = classify_signal(
            values, full_credit_count
        )
        rows.append(
            {
                "id": metric_id,
                "label": metric_label(metric_kind, metric_id),
                "signal": signal,
                "spread": spread,
                "full_credit_count": full_credit_count,
                "run_count": len(values),
                "full_credit_rate": full_credit_rate,
                "unique_count": unique_count,
                "note": note,
                "average": round(sum(values) / len(values), 1),
            }
        )
    rows.sort(key=lambda row: (-row["spread"], row["label"]))
    return rows


def saturation_table(rows: list[dict[str, Any]], max_rows: int | None = None) -> str:
    headers = [
        "Metric",
        "Signal",
        "Spread",
        "Full Credit",
        "Avg",
        "Notes",
    ]
    table_rows: list[list[str]] = []
    for row in rows[:max_rows] if max_rows else rows:
        table_rows.append(
            [
                f"`{row['label']}`",
                row["signal"],
                f"{row['spread']:.1f} pts",
                f"{row['full_credit_count']}/{row['run_count']} ({row['full_credit_rate']:.1f}%)",
                f"{row['average']:.1f}%",
                row["note"],
            ]
        )
    return markdown_table(headers, table_rows)


def render_saturation_section(results: list[tuple[Path, dict[str, Any]]]) -> list[str]:
    lines = ["## Saturation Analysis", ""]
    if len(results) < 2:
        lines.append("Need at least two scored runs for saturation analysis.")
        lines.append("")
        return lines

    lines.append(
        "This section analyzes only comparable run cohorts that share the same fingerprint. "
        "A metric is `high-signal` when it clearly separates runs, `medium-signal` when it shows some spread, "
        "and `saturated` when it no longer provides meaningful separation."
    )
    lines.append("")

    for fingerprint, cohort in sorted(group_results_by_fingerprint(results).items()):
        lines.append(
            f"### Fingerprint Cohort `{fingerprint[:12] if fingerprint != '-' else '-'}` ({len(cohort)} runs)"
        )
        lines.append("")
        if len(cohort) < 2:
            lines.append("Need at least two runs in the same fingerprint cohort.")
            lines.append("")
            continue

        skill_rows = build_saturation_rows(cohort, "skill", lambda result: score_percent_map(result, "per_skill"))
        dimension_rows = build_saturation_rows(
            cohort, "dimension", lambda result: score_percent_map(result, "dimensions")
        )
        case_rows = build_saturation_rows(cohort, "case", case_percent_map)
        criterion_rows = build_saturation_rows(cohort, "criterion", criterion_percent_map)

        summary_counts = {
            "skills": skill_rows,
            "dimensions": dimension_rows,
            "cases": case_rows,
            "criteria": criterion_rows,
        }
        for section_name, rows in summary_counts.items():
            if not rows:
                lines.append(f"- `{section_name}`: unavailable until runs are rescored with the current harness." if section_name == "dimensions" else f"- `{section_name}`: no comparable rows found.")
                continue
            high_signal = sum(1 for row in rows if row["signal"] == "high-signal")
            medium_signal = sum(1 for row in rows if row["signal"] == "medium-signal")
            saturated = sum(1 for row in rows if row["signal"] == "saturated")
            lines.append(
                f"- `{section_name}`: {high_signal} high-signal, {medium_signal} medium-signal, {saturated} saturated."
            )
        lines.append("")

        lines.append("#### Skills")
        lines.append("")
        lines.append(saturation_table(skill_rows))
        lines.append("")

        lines.append("#### Dimensions")
        lines.append("")
        if dimension_rows:
            lines.append(saturation_table(dimension_rows))
        else:
            lines.append(
                "Dimension saturation is unavailable for this cohort. Rescore these runs with the newer eval harness first."
            )
        lines.append("")

        lines.append("#### Cases")
        lines.append("")
        lines.append(saturation_table(case_rows))
        lines.append("")

        lines.append("#### Criteria")
        lines.append("")
        if criterion_rows:
            top_signal = [row for row in criterion_rows if row["signal"] != "saturated"][:12]
            saturated = [row for row in criterion_rows if row["signal"] == "saturated"][:12]
            if top_signal:
                lines.append("- Top separating criteria:")
                lines.append("")
                lines.append(saturation_table(top_signal))
                lines.append("")
            if saturated:
                lines.append("- Saturated criteria:")
                lines.append("")
                lines.append(saturation_table(saturated))
                lines.append("")
        else:
            lines.append("No comparable criterion data found.")
            lines.append("")

    return lines


def run_summary_row(path: Path, result: dict[str, Any]) -> list[str]:
    manifest = result.get("manifest") or {}
    model = manifest.get("model", {})
    agent = manifest.get("agent", {})
    cases = result.get("cases", [])
    completed = sum(
        1
        for case in cases
        if not case.get("missing_response") and not case.get("placeholder_response")
    )
    total_cases = len(cases)
    return [
        manifest.get("run_id", path.parent.name),
        model.get("provider", "-"),
        model.get("name", "-"),
        agent.get("name", "-"),
        f"{completed}/{total_cases}",
        f"{result['totals']['percent']}%",
        percent_for_skill(result, "shape"),
        percent_for_skill(result, "ship"),
        percent_for_skill(result, "ppp"),
        percent_for_skill(result, "ppp-cloud"),
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_scoreboard(results: list[tuple[Path, dict[str, Any]]]) -> str:
    lines = ["# Skill Eval Scoreboard", ""]
    lines.append(
        "This table compares scored eval runs across models and agents. "
        "Use runs from the same case set and skill commit when you want a fair comparison."
    )
    lines.append("")
    if not results:
        lines.append("No scored runs found.")
        lines.append("")
        return "\n".join(lines)

    headers = [
        "Run ID",
        "Provider",
        "Model",
        "Agent",
        "Cases",
        "Overall",
        "Shape",
        "Ship",
        "PPP",
        "PPP Cloud",
    ]
    rows = [run_summary_row(path, result) for path, result in results]
    lines.append(markdown_table(headers, rows))
    lines.append("")
    lines.append("## Dimension Matrix")
    lines.append("")
    dimension_ids: list[str] = []
    for _, result in results:
        for dimension in result.get("dimensions", {}):
            if dimension not in dimension_ids:
                dimension_ids.append(dimension)
    if dimension_ids:
        dimension_headers = ["Run ID", "Model", "Agent"] + [
            titleize_dimension(dimension) for dimension in dimension_ids
        ]
        dimension_rows: list[list[str]] = []
        for path, result in results:
            manifest = result.get("manifest") or {}
            model = manifest.get("model", {})
            agent = manifest.get("agent", {})
            row = [
                manifest.get("run_id", path.parent.name),
                model.get("name", "-"),
                agent.get("name", "-"),
            ]
            for dimension in dimension_ids:
                row.append(percent_for_dimension(result, dimension))
            dimension_rows.append(row)
        lines.append(markdown_table(dimension_headers, dimension_rows))
        lines.append("")
    else:
        lines.append("No dimension data found in scored runs.")
        lines.append("")
    lines.extend(render_pairwise_section(results))
    lines.extend(render_saturation_section(results))
    lines.append("## Case Matrix")
    lines.append("")
    case_ids: list[str] = []
    for _, result in results:
        for case in result.get("cases", []):
            case_id = case.get("id")
            if case_id and case_id not in case_ids:
                case_ids.append(case_id)
    if not case_ids:
        lines.append("No cases found in scored runs.")
        lines.append("")
        lines.append("## Notes")
        lines.append("")
        lines.append("- Use a fresh session per case to reduce context leakage.")
        lines.append("- Keep model, tool environment, and exposed sampling settings fixed within a run.")
        lines.append("- Exact identical outputs are not guaranteed by most providers; compare scores and drift, not just raw text.")
        lines.append("- Compare runs only when the fingerprint matches, or treat differences as case-set/skill-set changes rather than pure model deltas.")
        lines.append("")
        return "\n".join(lines)
    matrix_headers = ["Run ID", "Model", "Agent"] + case_ids
    matrix_rows: list[list[str]] = []
    for path, result in results:
        manifest = result.get("manifest") or {}
        model = manifest.get("model", {})
        agent = manifest.get("agent", {})
        case_lookup = {case["id"]: case for case in result.get("cases", [])}
        row = [
            manifest.get("run_id", path.parent.name),
            model.get("name", "-"),
            agent.get("name", "-"),
        ]
        for case_id in case_ids:
            case = case_lookup.get(case_id)
            if not case:
                row.append("-")
                continue
            note = ""
            if case.get("missing_response"):
                note = " missing"
            elif case.get("placeholder_response"):
                note = " placeholder"
            row.append(f"{case['score']}/{case['max_score']}{note}")
        matrix_rows.append(row)
    lines.append(markdown_table(matrix_headers, matrix_rows))
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Use a fresh session per case to reduce context leakage.")
    lines.append("- Keep model, tool environment, and exposed sampling settings fixed within a run.")
    lines.append("- Exact identical outputs are not guaranteed by most providers; compare scores and drift, not just raw text.")
    lines.append("- Compare runs only when the fingerprint matches, or treat differences as case-set/skill-set changes rather than pure model deltas.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Markdown scoreboard from scored skill eval runs."
    )
    parser.add_argument(
        "--runs-dir",
        default=str(DEFAULT_RUNS_DIR),
        help="Directory containing eval run subdirectories.",
    )
    parser.add_argument(
        "--write-markdown",
        default=str(DEFAULT_OUTPUT),
        help="Where to write the scoreboard Markdown.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    runs_dir = Path(args.runs_dir).resolve()
    if not runs_dir.exists():
        print(f"Runs directory does not exist: {runs_dir}", file=sys.stderr)
        return 1

    results: list[tuple[Path, dict[str, Any]]] = []
    for result_path in load_results_files(runs_dir):
        try:
            results.append((result_path, load_result(result_path)))
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    output_path = Path(args.write_markdown).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_scoreboard(results), encoding="utf-8")
    print(f"Wrote scoreboard: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
