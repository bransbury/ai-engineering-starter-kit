#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def version_from_tag(tag: str) -> str:
    if not tag.startswith("v") or len(tag) < 2:
        raise ValueError(f"Tag must start with 'v': {tag}")
    return tag[1:]


def extract_section(changelog_path: Path, version: str) -> str:
    lines = changelog_path.read_text(encoding="utf-8").splitlines()
    heading = f"## {version}"
    start_index = None

    for index, line in enumerate(lines):
        if line.strip() == heading:
            start_index = index + 1
            break

    if start_index is None:
        raise ValueError(
            f"Could not find changelog section '{heading}' in {changelog_path}"
        )

    end_index = len(lines)
    for index in range(start_index, len(lines)):
        if lines[index].startswith("## "):
            end_index = index
            break

    body_lines = lines[start_index:end_index]

    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()

    if not body_lines:
        raise ValueError(f"Changelog section '{heading}' is empty in {changelog_path}")

    return "\n".join(body_lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True, help="Release tag, for example v0.3.0")
    parser.add_argument(
        "--changelog",
        default=str(ROOT / "CHANGELOG.md"),
        help="Path to CHANGELOG.md",
    )
    parser.add_argument(
        "--output",
        help="Optional output file. Defaults to stdout when omitted.",
    )
    args = parser.parse_args()

    version = version_from_tag(args.tag)
    changelog_path = Path(args.changelog)
    section = extract_section(changelog_path, version)

    if args.output:
        Path(args.output).write_text(section, encoding="utf-8")
    else:
        sys.stdout.write(section)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
