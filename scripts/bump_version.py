#!/usr/bin/env python3
"""Bump the release version across package.json, skill frontmatters, and CHANGELOG.md.

Usage:
    python3 scripts/bump_version.py 0.6.0
    python3 scripts/bump_version.py v0.6.0   # leading v is stripped
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
SKILL_FILES = [
    ROOT / "skills" / "ppp" / "SKILL.md",
    ROOT / "skills" / "ppp-cloud" / "SKILL.md",
    ROOT / "skills" / "shape" / "SKILL.md",
    ROOT / "skills" / "ship" / "SKILL.md",
]
PACKAGE_JSON = ROOT / "package.json"
CHANGELOG = ROOT / "CHANGELOG.md"


def parse_version(raw: str) -> str:
    version = raw.lstrip("v")
    if not SEMVER_RE.fullmatch(version):
        raise ValueError(
            f"Invalid version '{raw}'. Expected semver like 0.6.0 or v0.6.0."
        )
    return version


def bump_package_json(version: str) -> None:
    content = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    current = content.get("version", "")
    if current == version:
        raise ValueError(f"package.json already at version {version}.")
    content["version"] = version
    PACKAGE_JSON.write_text(
        json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"  package.json: {current} → {version}")


def bump_skill(path: Path, version: str) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^(version:\s*)([^\s]+)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"No version field found in {path}")
    current = match.group(2)
    if current == version:
        raise ValueError(f"{path.name} already at version {version}.")
    updated = text[: match.start(2)] + version + text[match.end(2) :]
    path.write_text(updated, encoding="utf-8")
    rel = path.relative_to(ROOT)
    print(f"  {rel}: {current} → {version}")


def bump_changelog(version: str) -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    heading = f"## {version}"
    if heading in text:
        raise ValueError(f"CHANGELOG already contains section '{heading}'.")
    # Insert new section after the first line (# Changelog)
    lines = text.splitlines(keepends=True)
    insert_at = 1
    # Skip blank lines after the title
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    stub = f"\n{heading}\n\n- TODO: add release notes\n\n"
    updated = "".join(lines[:insert_at]) + stub + "".join(lines[insert_at:])
    CHANGELOG.write_text(updated, encoding="utf-8")
    print(f"  CHANGELOG.md: added stub section '{heading}'")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="New version, e.g. 0.6.0 or v0.6.0")
    args = parser.parse_args()

    try:
        version = parse_version(args.version)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Bumping to {version}...")
    errors: list[str] = []

    for skill in SKILL_FILES:
        try:
            bump_skill(skill, version)
        except ValueError as exc:
            errors.append(str(exc))

    try:
        bump_package_json(version)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        bump_changelog(version)
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        print("\nwarnings:", file=sys.stderr)
        for msg in errors:
            print(f"  {msg}", file=sys.stderr)
        sys.exit(1)

    print(
        f"\nDone. Edit CHANGELOG.md to replace the TODO stub, then commit and tag v{version}."
    )


if __name__ == "__main__":
    main()
