#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CASES_DIR = ROOT / "evals" / "cases"
DEFAULT_RUNS_DIR = ROOT / "evals" / "runs"
SKILL_FILES = [
    ROOT / "skills" / "ppp" / "SKILL.md",
    ROOT / "skills" / "ppp-cloud" / "SKILL.md",
    ROOT / "skills" / "shape" / "SKILL.md",
    ROOT / "skills" / "ship" / "SKILL.md",
]
PLACEHOLDER_MARKERS = [
    "<paste model output here>",
    "todo: paste model output here",
]
DIMENSION_RE = re.compile(r"[a-z][a-z0-9_-]*")


@dataclass
class Criterion:
    name: str
    dimension: str
    points: int
    description: str
    kind: str
    all_patterns: list[str]
    any_patterns: list[str]
    none_patterns: list[str]


@dataclass
class Case:
    case_id: str
    skill: str
    description: str
    prompt_path: str
    criteria: list[Criterion]
    reasoning_quality_notes: dict[str, list[str]]
    case_path: Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_string(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    return str(path)


def current_git_commit() -> str | None:
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


def require_pattern_list(
    path: Path, raw: dict[str, Any], key: str, index: int
) -> list[str]:
    value = raw.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{path}: criterion {index} field '{key}' must be a list")
    patterns: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{path}: criterion {index} field '{key}' must contain non-empty strings"
            )
        patterns.append(item)
    return patterns


def require_reasoning_quality_notes(
    path: Path, data: dict[str, Any]
) -> dict[str, list[str]]:
    raw = data.get("reasoning_quality_notes")
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: reasoning_quality_notes must be an object")

    required_keys = ("weak", "good", "excellent")
    notes: dict[str, list[str]] = {}
    for key in required_keys:
        value = raw.get(key)
        if not isinstance(value, list) or not value:
            raise ValueError(
                f"{path}: reasoning_quality_notes.{key} must be a non-empty list"
            )
        cleaned: list[str] = []
        for index, item in enumerate(value, start=1):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(
                    f"{path}: reasoning_quality_notes.{key}[{index}] must be a non-empty string"
                )
            cleaned.append(item.strip())
        notes[key] = cleaned

    extra_keys = sorted(set(raw.keys()) - set(required_keys))
    if extra_keys:
        raise ValueError(
            f"{path}: reasoning_quality_notes has unsupported keys: {', '.join(extra_keys)}"
        )
    return notes


def compile_case(path: Path) -> Case:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "id",
        "skill",
        "description",
        "prompt_path",
        "criteria",
        "reasoning_quality_notes",
    }
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"{path}: missing required keys: {', '.join(missing)}")

    criteria_raw = data["criteria"]
    if not isinstance(criteria_raw, list) or not criteria_raw:
        raise ValueError(f"{path}: criteria must be a non-empty list")

    reasoning_quality_notes = require_reasoning_quality_notes(path, data)

    criteria: list[Criterion] = []
    for index, raw in enumerate(criteria_raw, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"{path}: criterion {index} must be an object")
        for key in ("name", "dimension", "points"):
            if key not in raw:
                raise ValueError(f"{path}: criterion {index} missing required key '{key}'")

        name = raw["name"]
        dimension = raw["dimension"]
        points = raw["points"]
        description = raw.get("description", "")
        kind = raw.get("kind", "reward")

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{path}: criterion {index} name must be a non-empty string")
        if not isinstance(dimension, str) or not DIMENSION_RE.fullmatch(dimension):
            raise ValueError(
                f"{path}: criterion {index} dimension must match {DIMENSION_RE.pattern}"
            )
        if not isinstance(points, int) or points <= 0:
            raise ValueError(f"{path}: criterion {index} points must be a positive integer")
        if not isinstance(description, str):
            raise ValueError(f"{path}: criterion {index} description must be a string")
        if kind not in {"reward", "penalty"}:
            raise ValueError(f"{path}: criterion {index} kind must be 'reward' or 'penalty'")

        all_patterns = require_pattern_list(path, raw, "all", index)
        any_patterns = require_pattern_list(path, raw, "any", index)
        none_patterns = require_pattern_list(path, raw, "none", index)
        if not all_patterns and not any_patterns and not none_patterns:
            raise ValueError(
                f"{path}: criterion {index} must define at least one of all/any/none"
            )

        for pattern in all_patterns + any_patterns + none_patterns:
            try:
                re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            except re.error as exc:
                raise ValueError(
                    f"{path}: invalid regex in criterion {index}: {exc}"
                ) from exc

        criteria.append(
            Criterion(
                name=name.strip(),
                dimension=dimension,
                points=points,
                description=description.strip(),
                kind=kind,
                all_patterns=all_patterns,
                any_patterns=any_patterns,
                none_patterns=none_patterns,
            )
        )

    prompt_path = data["prompt_path"]
    prompt_full_path = ROOT / prompt_path
    if not isinstance(prompt_path, str) or not prompt_path.strip():
        raise ValueError(f"{path}: prompt_path must be a non-empty string")
    if not prompt_full_path.exists():
        raise ValueError(f"{path}: prompt_path does not exist: {prompt_path}")

    case_id = data["id"]
    skill = data["skill"]
    description = data["description"]
    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError(f"{path}: id must be a non-empty string")
    if not isinstance(skill, str) or not skill.strip():
        raise ValueError(f"{path}: skill must be a non-empty string")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{path}: description must be a non-empty string")

    return Case(
        case_id=case_id.strip(),
        skill=skill.strip(),
        description=description.strip(),
        prompt_path=prompt_path.strip(),
        criteria=criteria,
        reasoning_quality_notes=reasoning_quality_notes,
        case_path=path,
    )


def load_cases(cases_dir: Path) -> list[Case]:
    case_files = sorted(cases_dir.glob("*.json"))
    if not case_files:
        raise ValueError(f"No eval case files found under {cases_dir}")

    seen_ids: set[str] = set()
    cases: list[Case] = []
    for path in case_files:
        case = compile_case(path)
        if case.case_id in seen_ids:
            raise ValueError(f"{path}: duplicate case id '{case.case_id}'")
        seen_ids.add(case.case_id)
        cases.append(case)
    return cases


def load_manifest(run_dir: Path) -> dict[str, Any]:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"Run manifest does not exist: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{manifest_path}: invalid JSON: {exc}") from exc

    required = {"run_id", "model", "agent"}
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(
            f"{manifest_path}: missing required keys: {', '.join(missing)}"
        )
    if not isinstance(data["model"], dict):
        raise ValueError(f"{manifest_path}: model must be an object")
    if not isinstance(data["agent"], dict):
        raise ValueError(f"{manifest_path}: agent must be an object")
    return data


def find_response_file(responses_dir: Path, case_id: str) -> Path | None:
    candidates = [
        responses_dir / f"{case_id}.md",
        responses_dir / f"{case_id}.txt",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def is_placeholder_response(text: str) -> bool:
    normalized = text.strip().lower()
    if not normalized:
        return True
    return any(marker in normalized for marker in PLACEHOLDER_MARKERS)


def matches(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE | re.MULTILINE) is not None


def criterion_matches(criterion: Criterion, text: str) -> bool:
    passed_all = all(matches(pattern, text) for pattern in criterion.all_patterns)
    passed_any = True
    if criterion.any_patterns:
        passed_any = any(matches(pattern, text) for pattern in criterion.any_patterns)
    passed_none = all(not matches(pattern, text) for pattern in criterion.none_patterns)
    return passed_all and passed_any and passed_none


def blank_dimension_totals() -> dict[str, float]:
    return {
        "reward_score": 0.0,
        "max_score": 0.0,
        "penalty_score": 0.0,
        "raw_net_score": 0.0,
        "score": 0.0,
        "percent": 0.0,
        "criteria_count": 0.0,
        "matched_count": 0.0,
    }


def finalize_dimension_totals(dimensions: dict[str, dict[str, float]]) -> None:
    for totals in dimensions.values():
        totals["raw_net_score"] = totals["reward_score"] + totals["penalty_score"]
        totals["score"] = max(0.0, totals["raw_net_score"])
        totals["percent"] = (
            round(totals["score"] / totals["max_score"] * 100, 1)
            if totals["max_score"]
            else 0.0
        )


def score_case(case: Case, text: str) -> dict[str, Any]:
    reward_score = 0.0
    max_score = 0.0
    penalty_score = 0.0
    criteria_details: list[dict[str, Any]] = []
    dimensions: dict[str, dict[str, float]] = {}

    for criterion in case.criteria:
        matched = criterion_matches(criterion, text)
        dimension = dimensions.setdefault(criterion.dimension, blank_dimension_totals())
        dimension["criteria_count"] += 1

        if criterion.kind == "reward":
            max_score += criterion.points
            dimension["max_score"] += criterion.points
            earned = float(criterion.points if matched else 0)
            reward_score += earned
            dimension["reward_score"] += earned
        else:
            earned = float(-criterion.points if matched else 0)
            penalty_score += earned
            dimension["penalty_score"] += earned

        if matched:
            dimension["matched_count"] += 1

        criteria_details.append(
            {
                "name": criterion.name,
                "dimension": criterion.dimension,
                "description": criterion.description,
                "kind": criterion.kind,
                "points": criterion.points,
                "earned": earned,
                "matched": matched,
                "all": criterion.all_patterns,
                "any": criterion.any_patterns,
                "none": criterion.none_patterns,
            }
        )

    finalize_dimension_totals(dimensions)

    raw_net_score = reward_score + penalty_score
    score = max(0.0, raw_net_score)
    percent = round(score / max_score * 100, 1) if max_score else 0.0

    return {
        "reward_score": reward_score,
        "max_score": max_score,
        "penalty_score": penalty_score,
        "raw_net_score": raw_net_score,
        "score": score,
        "percent": percent,
        "criteria": criteria_details,
        "dimensions": dimensions,
    }


def build_fingerprints(cases: list[Case]) -> dict[str, Any]:
    case_files = {
        case.case_id: {
            "case_file": relative_string(case.case_path),
            "case_sha256": sha256_file(case.case_path),
            "prompt_file": case.prompt_path,
            "prompt_sha256": sha256_file(ROOT / case.prompt_path),
        }
        for case in cases
    }
    skills = {
        path.parent.name: {
            "path": relative_string(path),
            "sha256": sha256_file(path),
        }
        for path in SKILL_FILES
    }
    return {
        "cases": case_files,
        "skills": skills,
        "combined_sha256": sha256_text(
            json.dumps({"cases": case_files, "skills": skills}, sort_keys=True)
        ),
    }


def finalize_scoring_totals(totals: dict[str, Any]) -> None:
    totals["raw_net_score"] = totals["reward_score"] + totals["penalty_score"]
    totals["score"] = max(0.0, totals["raw_net_score"])
    totals["percent"] = (
        round(totals["score"] / totals["max_score"] * 100, 1)
        if totals["max_score"]
        else 0.0
        )


def zeroed_dimensions_for_case(case: Case) -> dict[str, dict[str, float]]:
    dimensions: dict[str, dict[str, float]] = {}
    for criterion in case.criteria:
        dimension = dimensions.setdefault(criterion.dimension, blank_dimension_totals())
        dimension["criteria_count"] += 1
        if criterion.kind == "reward":
            dimension["max_score"] += criterion.points
    finalize_dimension_totals(dimensions)
    return dimensions


def build_run_analysis(
    cases: list[dict[str, Any]], dimensions: dict[str, dict[str, float]]
) -> dict[str, Any]:
    completed_cases = [
        case
        for case in cases
        if not case["missing_response"] and not case["placeholder_response"]
    ]

    weakest_cases = sorted(
        (
            {
                "id": case["id"],
                "skill": case["skill"],
                "score": case["score"],
                "max_score": case["max_score"],
                "percent": case["percent"],
            }
            for case in completed_cases
        ),
        key=lambda item: (item["percent"], item["score"]),
    )[:5]

    weakest_dimensions = sorted(
        (
            {
                "dimension": dimension,
                "score": totals["score"],
                "max_score": totals["max_score"],
                "percent": totals["percent"],
                "penalty_score": totals["penalty_score"],
            }
            for dimension, totals in dimensions.items()
            if totals["max_score"] > 0
        ),
        key=lambda item: (item["percent"], item["score"]),
    )[:5]

    missed_criteria_counts: dict[str, dict[str, Any]] = {}
    triggered_penalty_counts: dict[str, dict[str, Any]] = {}
    for case in completed_cases:
        for criterion in case.get("criteria", []):
            name = criterion["name"]
            bucket = (
                triggered_penalty_counts
                if criterion.get("kind") == "penalty" and criterion.get("matched")
                else missed_criteria_counts
            )
            should_count_miss = (
                criterion.get("kind") == "reward" and not criterion.get("matched")
            )
            should_count_penalty = (
                criterion.get("kind") == "penalty" and criterion.get("matched")
            )
            if not should_count_miss and not should_count_penalty:
                continue
            entry = bucket.setdefault(
                name,
                {
                    "name": name,
                    "dimension": criterion["dimension"],
                    "description": criterion.get("description", ""),
                    "count": 0,
                    "points": criterion["points"],
                },
            )
            entry["count"] += 1

    most_missed_criteria = sorted(
        missed_criteria_counts.values(),
        key=lambda item: (-item["count"], -item["points"], item["name"]),
    )[:10]
    most_triggered_penalties = sorted(
        triggered_penalty_counts.values(),
        key=lambda item: (-item["count"], -item["points"], item["name"]),
    )[:10]

    return {
        "weakest_cases": weakest_cases,
        "weakest_dimensions": weakest_dimensions,
        "most_missed_criteria": most_missed_criteria,
        "most_triggered_penalties": most_triggered_penalties,
    }


def build_results(
    cases: list[Case],
    responses_dir: Path,
    manifest: dict[str, Any] | None,
    run_dir: Path | None,
) -> dict[str, Any]:
    per_case: list[dict[str, Any]] = []
    skill_totals: dict[str, dict[str, Any]] = {}
    overall_dimensions: dict[str, dict[str, float]] = {}
    totals = {
        "reward_score": 0.0,
        "max_score": 0.0,
        "penalty_score": 0.0,
        "raw_net_score": 0.0,
        "score": 0.0,
        "percent": 0.0,
    }

    for case in cases:
        response_file = find_response_file(responses_dir, case.case_id)
        empty_dimensions = zeroed_dimensions_for_case(case)
        case_max_score = float(
            sum(criterion.points for criterion in case.criteria if criterion.kind == "reward")
        )

        skill_entry = skill_totals.setdefault(
            case.skill,
            {
                "reward_score": 0.0,
                "max_score": 0.0,
                "penalty_score": 0.0,
                "raw_net_score": 0.0,
                "score": 0.0,
                "percent": 0.0,
                "dimensions": {},
            },
        )
        skill_entry["max_score"] += case_max_score
        totals["max_score"] += case_max_score

        if response_file is None:
            per_case.append(
                {
                    "id": case.case_id,
                    "skill": case.skill,
                    "description": case.description,
                    "prompt_path": case.prompt_path,
                    "response_path": None,
                    "response_sha256": None,
                    "reward_score": 0.0,
                    "max_score": case_max_score,
                    "penalty_score": 0.0,
                    "raw_net_score": 0.0,
                    "score": 0.0,
                    "percent": 0.0,
                    "missing_response": True,
                    "placeholder_response": False,
                    "criteria": [],
                    "dimensions": empty_dimensions,
                }
            )
            continue

        text = response_file.read_text(encoding="utf-8")
        placeholder_response = is_placeholder_response(text)
        if placeholder_response:
            case_results = {
                "reward_score": 0.0,
                "max_score": case_max_score,
                "penalty_score": 0.0,
                "raw_net_score": 0.0,
                "score": 0.0,
                "percent": 0.0,
                "criteria": [],
                "dimensions": empty_dimensions,
            }
        else:
            case_results = score_case(case, text)

        totals["reward_score"] += case_results["reward_score"]
        totals["penalty_score"] += case_results["penalty_score"]
        skill_entry["reward_score"] += case_results["reward_score"]
        skill_entry["penalty_score"] += case_results["penalty_score"]

        for dimension, dimension_totals in case_results["dimensions"].items():
            overall_dimension = overall_dimensions.setdefault(dimension, blank_dimension_totals())
            skill_dimension = skill_entry["dimensions"].setdefault(
                dimension, blank_dimension_totals()
            )
            for key, value in dimension_totals.items():
                overall_dimension[key] += value
                skill_dimension[key] += value

        per_case.append(
            {
                "id": case.case_id,
                "skill": case.skill,
                "description": case.description,
                "prompt_path": case.prompt_path,
                "response_path": relative_string(response_file),
                "response_sha256": sha256_file(response_file),
                "reward_score": case_results["reward_score"],
                "max_score": case_results["max_score"],
                "penalty_score": case_results["penalty_score"],
                "raw_net_score": case_results["raw_net_score"],
                "score": case_results["score"],
                "percent": case_results["percent"],
                "missing_response": False,
                "placeholder_response": placeholder_response,
                "criteria": case_results["criteria"],
                "dimensions": case_results["dimensions"],
            }
        )

    finalize_dimension_totals(overall_dimensions)
    for skill_entry in skill_totals.values():
        finalize_scoring_totals(skill_entry)
        finalize_dimension_totals(skill_entry["dimensions"])
    finalize_scoring_totals(totals)

    fingerprints = build_fingerprints(cases)
    analysis = build_run_analysis(per_case, overall_dimensions)

    return {
        "schema_version": 3,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_commit": current_git_commit(),
        "run_dir": relative_string(run_dir) if run_dir else None,
        "responses_dir": relative_string(responses_dir),
        "manifest": manifest,
        "fingerprints": fingerprints,
        "totals": totals,
        "dimensions": overall_dimensions,
        "per_skill": skill_totals,
        "analysis": analysis,
        "cases": per_case,
    }


def compare_results(baseline: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    baseline_cases = {case["id"]: case for case in baseline.get("cases", [])}
    current_cases = {case["id"]: case for case in current.get("cases", [])}

    regressions: list[dict[str, Any]] = []
    improvements: list[dict[str, Any]] = []

    for case_id, current_case in current_cases.items():
        baseline_case = baseline_cases.get(case_id)
        if baseline_case is None:
            improvements.append(
                {
                    "id": case_id,
                    "type": "new-case",
                    "message": "new case in current results",
                }
            )
            continue

        delta = current_case["score"] - baseline_case.get("score", 0)
        if delta < 0:
            regressions.append(
                {
                    "id": case_id,
                    "type": "score-drop",
                    "baseline": baseline_case.get("score", 0),
                    "current": current_case["score"],
                    "delta": delta,
                }
            )
        elif delta > 0:
            improvements.append(
                {
                    "id": case_id,
                    "type": "score-gain",
                    "baseline": baseline_case.get("score", 0),
                    "current": current_case["score"],
                    "delta": delta,
                }
            )

    total_delta = current["totals"]["score"] - baseline["totals"].get("score", 0)
    return {
        "total_delta": total_delta,
        "baseline_total": baseline["totals"].get("score", 0),
        "current_total": current["totals"]["score"],
        "regressions": regressions,
        "improvements": improvements,
        "same_fingerprint": baseline.get("fingerprints", {}).get("combined_sha256")
        == current.get("fingerprints", {}).get("combined_sha256"),
    }


def titleize_dimension(dimension: str) -> str:
    return dimension.replace("_", " ").replace("-", " ").title()


def print_validation_summary(cases: list[Case]) -> None:
    total_criteria = sum(len(case.criteria) for case in cases)
    print(f"Validated {len(cases)} eval cases and {total_criteria} rubric criteria.")


def print_results(results: dict[str, Any], comparison: dict[str, Any] | None) -> None:
    manifest = results.get("manifest") or {}
    model = manifest.get("model", {})
    agent = manifest.get("agent", {})
    run_id = manifest.get("run_id") or "ad-hoc"
    if model or agent:
        print(f"Run: {run_id}")
        if model:
            print(f"Model: {model.get('name', 'unknown')} ({model.get('provider', 'unknown')})")
        if agent:
            print(f"Agent: {agent.get('name', 'unknown')}")
        print("")

    totals = results["totals"]
    print(
        f"Total score: {totals['score']}/{totals['max_score']} ({totals['percent']}%) "
        f"[reward {totals['reward_score']}, penalties {totals['penalty_score']}]"
    )
    print("")
    print("Per-skill totals:")
    for skill, skill_totals in sorted(results["per_skill"].items()):
        print(
            f"- {skill}: {skill_totals['score']}/{skill_totals['max_score']} "
            f"({skill_totals['percent']}%)"
        )

    print("")
    print("Dimension totals:")
    for dimension, dimension_totals in sorted(
        results["dimensions"].items(), key=lambda item: (item[1]["percent"], item[0])
    ):
        print(
            f"- {dimension}: {dimension_totals['score']}/{dimension_totals['max_score']} "
            f"({dimension_totals['percent']}%)"
        )

    print("")
    print("Cases:")
    for case in results["cases"]:
        suffix = ""
        if case["missing_response"]:
            suffix = " (missing response)"
        elif case["placeholder_response"]:
            suffix = " (placeholder response)"
        print(f"- {case['id']}: {case['score']}/{case['max_score']}{suffix}")

    analysis = results.get("analysis", {})
    weakest_dimensions = analysis.get("weakest_dimensions", [])
    weakest_cases = analysis.get("weakest_cases", [])
    if weakest_dimensions:
        print("")
        print("Weakest dimensions:")
        for item in weakest_dimensions:
            print(
                f"- {item['dimension']}: {item['score']}/{item['max_score']} "
                f"({item['percent']}%)"
            )
    if weakest_cases:
        print("")
        print("Weakest cases:")
        for item in weakest_cases:
            print(
                f"- {item['id']} ({item['skill']}): {item['score']}/{item['max_score']} "
                f"({item['percent']}%)"
            )
    if analysis.get("most_missed_criteria"):
        print("")
        print("Most missed criteria:")
        for item in analysis["most_missed_criteria"]:
            print(
                f"- {item['name']} [{item['dimension']}] missed in {item['count']} case(s)"
            )
    if analysis.get("most_triggered_penalties"):
        print("")
        print("Most triggered penalties:")
        for item in analysis["most_triggered_penalties"]:
            print(
                f"- {item['name']} [{item['dimension']}] triggered in {item['count']} case(s)"
            )

    if comparison is None:
        return

    print("")
    print(
        f"Comparison: {comparison['current_total']} vs {comparison['baseline_total']} "
        f"(delta {comparison['total_delta']:+g})"
    )
    print(
        "Case/skill fingerprint match: "
        + ("yes" if comparison["same_fingerprint"] else "no")
    )

    if comparison["regressions"]:
        print("Regressions:")
        for regression in comparison["regressions"]:
            print(
                f"- {regression['id']}: {regression['baseline']} -> "
                f"{regression['current']} ({regression['delta']:+g})"
            )
    else:
        print("Regressions: none")

    if comparison["improvements"]:
        print("Improvements:")
        for improvement in comparison["improvements"]:
            if improvement["type"] == "new-case":
                print(f"- {improvement['id']}: new case in current results")
            else:
                print(
                    f"- {improvement['id']}: {improvement['baseline']} -> "
                    f"{improvement['current']} ({improvement['delta']:+g})"
                )


def markdown_summary(results: dict[str, Any], comparison: dict[str, Any] | None) -> str:
    manifest = results.get("manifest") or {}
    model = manifest.get("model", {})
    agent = manifest.get("agent", {})
    lines = ["# Skill Eval Result", ""]
    lines.append(f"- Run ID: `{manifest.get('run_id', 'ad-hoc')}`")
    if model:
        lines.append(
            f"- Model: `{model.get('provider', 'unknown')}/{model.get('name', 'unknown')}`"
        )
    if agent:
        lines.append(f"- Agent: `{agent.get('name', 'unknown')}`")
    if results.get("repo_commit"):
        lines.append(f"- Commit: `{results['repo_commit']}`")
    lines.append(
        f"- Total: **{results['totals']['score']}/{results['totals']['max_score']} "
        f"({results['totals']['percent']}%)**"
    )
    lines.append(
        f"- Reward score: `{results['totals']['reward_score']}`; penalties: "
        f"`{results['totals']['penalty_score']}`"
    )
    lines.append("")
    lines.append("## Per Skill")
    lines.append("")
    lines.append("| Skill | Score | Max | Percent | Penalties |")
    lines.append("|---|---:|---:|---:|---:|")
    for skill, totals in sorted(results["per_skill"].items()):
        lines.append(
            f"| {skill} | {totals['score']} | {totals['max_score']} | "
            f"{totals['percent']}% | {totals['penalty_score']} |"
        )
    lines.append("")
    lines.append("## Dimension Breakdown")
    lines.append("")
    lines.append("| Dimension | Score | Max | Percent | Penalties |")
    lines.append("|---|---:|---:|---:|---:|")
    for dimension, totals in sorted(
        results["dimensions"].items(), key=lambda item: (item[1]["percent"], item[0])
    ):
        lines.append(
            f"| {titleize_dimension(dimension)} | {totals['score']} | {totals['max_score']} | "
            f"{totals['percent']}% | {totals['penalty_score']} |"
        )
    lines.append("")
    lines.append("## Cases")
    lines.append("")
    lines.append("| Case | Skill | Score | Max | Percent | Penalties | Notes |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for case in results["cases"]:
        notes = []
        if case["missing_response"]:
            notes.append("missing response")
        if case["placeholder_response"]:
            notes.append("placeholder response")
        lines.append(
            f"| {case['id']} | {case['skill']} | {case['score']} | {case['max_score']} | "
            f"{case['percent']}% | {case['penalty_score']} | {'; '.join(notes)} |"
        )
    analysis = results.get("analysis", {})
    if analysis.get("weakest_dimensions"):
        lines.append("")
        lines.append("## Weakest Dimensions")
        lines.append("")
        for item in analysis["weakest_dimensions"]:
            lines.append(
                f"- `{titleize_dimension(item['dimension'])}`: {item['score']}/{item['max_score']} "
                f"({item['percent']}%)"
            )
    if analysis.get("weakest_cases"):
        lines.append("")
        lines.append("## Weakest Cases")
        lines.append("")
        for item in analysis["weakest_cases"]:
            lines.append(
                f"- `{item['id']}` ({item['skill']}): {item['score']}/{item['max_score']} "
                f"({item['percent']}%)"
            )
    if analysis.get("most_missed_criteria"):
        lines.append("")
        lines.append("## Most Missed Criteria")
        lines.append("")
        for item in analysis["most_missed_criteria"]:
            lines.append(
                f"- `{item['name']}` ({titleize_dimension(item['dimension'])}): "
                f"missed in {item['count']} case(s)"
            )
    if analysis.get("most_triggered_penalties"):
        lines.append("")
        lines.append("## Most Triggered Penalties")
        lines.append("")
        for item in analysis["most_triggered_penalties"]:
            lines.append(
                f"- `{item['name']}` ({titleize_dimension(item['dimension'])}): "
                f"triggered in {item['count']} case(s)"
            )
    if comparison:
        lines.append("")
        lines.append("## Comparison")
        lines.append("")
        lines.append(
            f"- Total delta: `{comparison['total_delta']:+g}` "
            f"({comparison['baseline_total']} -> {comparison['current_total']})"
        )
        lines.append(
            "- Case/skill fingerprint match: "
            + ("yes" if comparison["same_fingerprint"] else "no")
        )
        if comparison["regressions"]:
            lines.append("- Regressions:")
            for regression in comparison["regressions"]:
                lines.append(
                    f"  - `{regression['id']}`: {regression['baseline']} -> "
                    f"{regression['current']} ({regression['delta']:+g})"
                )
        else:
            lines.append("- Regressions: none")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score skill outputs against repo-local eval rubrics."
    )
    parser.add_argument(
        "--cases-dir",
        default=str(DEFAULT_CASES_DIR),
        help="Directory containing eval case JSON files.",
    )
    parser.add_argument(
        "--run-dir",
        help="Run directory containing manifest.json and responses/.",
    )
    parser.add_argument(
        "--responses-dir",
        help="Directory containing one response file per case (<case-id>.md).",
    )
    parser.add_argument(
        "--write-json",
        help="Write scored results to this JSON file.",
    )
    parser.add_argument(
        "--write-markdown",
        help="Write a Markdown summary to this file.",
    )
    parser.add_argument(
        "--baseline",
        help="Existing results JSON to compare against.",
    )
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit non-zero if any case score regresses versus the baseline.",
    )
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Exit non-zero if any response file is missing or still a placeholder.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate case files only; do not score responses.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases_dir = Path(args.cases_dir).resolve()

    try:
        cases = load_cases(cases_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.validate_only:
        print_validation_summary(cases)
        return 0

    run_dir = Path(args.run_dir).resolve() if args.run_dir else None
    manifest = None
    responses_dir: Path | None = None
    if run_dir:
        if args.responses_dir:
            print("Use either --run-dir or --responses-dir, not both.", file=sys.stderr)
            return 1
        try:
            manifest = load_manifest(run_dir)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        responses_dir = run_dir / "responses"
        if not responses_dir.exists():
            print(f"Responses directory does not exist: {responses_dir}", file=sys.stderr)
            return 1
    else:
        if not args.responses_dir:
            print(
                "--run-dir or --responses-dir is required unless --validate-only is used.",
                file=sys.stderr,
            )
            return 1
        responses_dir = Path(args.responses_dir).resolve()
        if not responses_dir.exists():
            print(f"Responses directory does not exist: {responses_dir}", file=sys.stderr)
            return 1

    results = build_results(cases, responses_dir, manifest, run_dir)
    comparison = None
    if args.baseline:
        baseline_path = Path(args.baseline).resolve()
        if not baseline_path.exists():
            print(f"Baseline JSON does not exist: {baseline_path}", file=sys.stderr)
            return 1
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        comparison = compare_results(baseline, results)

    write_json_path = Path(args.write_json).resolve() if args.write_json else None
    if write_json_path is None and run_dir:
        write_json_path = run_dir / "results.json"
    if write_json_path:
        write_json_path.parent.mkdir(parents=True, exist_ok=True)
        write_json_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    write_markdown_path = Path(args.write_markdown).resolve() if args.write_markdown else None
    if write_markdown_path is None and run_dir:
        write_markdown_path = run_dir / "results.md"
    if write_markdown_path:
        write_markdown_path.parent.mkdir(parents=True, exist_ok=True)
        write_markdown_path.write_text(markdown_summary(results, comparison), encoding="utf-8")

    print_results(results, comparison)

    if args.fail_on_missing:
        missing_or_placeholder = any(
            case["missing_response"] or case["placeholder_response"]
            for case in results["cases"]
        )
        if missing_or_placeholder:
            return 1

    if args.fail_on_regression and comparison and comparison["regressions"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
