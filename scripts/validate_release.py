#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from extract_release_notes import extract_section, version_from_tag


ROOT = Path(__file__).resolve().parent.parent
SEMVER_TAG_RE = re.compile(r"^v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
SKILL_FILES = [
    ROOT / "skills" / "ppp" / "SKILL.md",
    ROOT / "skills" / "ppp-cloud" / "SKILL.md",
]


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def ensure_tag_format(tag: str) -> str:
    if not SEMVER_TAG_RE.fullmatch(tag):
        raise ValueError(
            f"Invalid release tag '{tag}'. Expected v<major>.<minor>.<patch> or prerelease variant."
        )
    return version_from_tag(tag)


def ensure_commit_on_default_branch(commit: str, default_branch: str) -> None:
    ref = f"origin/{default_branch}"
    fetch = git("fetch", "origin", default_branch, "--depth=1")
    if fetch.returncode != 0:
        raise ValueError(fetch.stderr.strip() or f"Failed to fetch {ref}")

    result = git("merge-base", "--is-ancestor", commit, ref)
    if result.returncode != 0:
        raise ValueError(f"Tagged commit {commit} is not reachable from {ref}")


def read_skill_version(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*([^\s]+)\s*$", content, re.MULTILINE)
    if not match:
        raise ValueError(f"Missing version field in {path}")
    return match.group(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True, help="Release tag, for example v0.3.0")
    parser.add_argument("--commit", required=True, help="Commit SHA for the release tag")
    parser.add_argument(
        "--default-branch",
        default="main",
        help="Default branch that release tags must point to",
    )
    parser.add_argument(
        "--skip-main-branch-check",
        action="store_true",
        help="Skip the commit-on-default-branch validation. Useful for local testing.",
    )
    args = parser.parse_args()

    try:
        version = ensure_tag_format(args.tag)
        extract_section(ROOT / "CHANGELOG.md", version)

        for skill_path in SKILL_FILES:
            skill_version = read_skill_version(skill_path)
            if skill_version != version:
                raise ValueError(
                    f"Skill version mismatch in {skill_path}: expected {version}, found {skill_version}"
                )

        if not args.skip_main_branch_check:
            ensure_commit_on_default_branch(args.commit, args.default_branch)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Release validation passed for {args.tag}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
