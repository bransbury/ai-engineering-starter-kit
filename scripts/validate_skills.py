#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_FILES = sorted((ROOT / "skills").glob("*/SKILL.md"))
DESCRIPTION_LIMIT = 320
SEMVER_RE = re.compile(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?")


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"{path}: file does not exist"]

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        errors.append(f"{path}: must start with YAML frontmatter delimiter '---'")
        return errors

    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError:
        errors.append(f"{path}: missing closing YAML frontmatter delimiter '---'")
        closing_index = -1

    frontmatter_lines = lines[1:closing_index] if closing_index != -1 else []
    name = None
    version = None
    description = None

    for raw_line in frontmatter_lines:
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "name":
            name = value
        elif key == "version":
            version = value
        elif key == "description":
            description = value

    if not name:
        errors.append(f"{path}: frontmatter must include a non-empty name")
    elif not name.strip():
        errors.append(f"{path}: frontmatter name must not be empty")

    if version is None:
        errors.append(f"{path}: frontmatter must include version")
    elif not SEMVER_RE.fullmatch(version):
        errors.append(f"{path}: version must be a semver string")

    if description is None:
        errors.append(f"{path}: frontmatter must include description")
    else:
        if not re.fullmatch(r'"[^"]+"', description):
            errors.append(f"{path}: description must be a quoted single-line string")
        else:
            inner = description[1:-1]
            if not inner.strip():
                errors.append(f"{path}: description must not be empty")
            if len(inner) > DESCRIPTION_LIMIT:
                errors.append(
                    f"{path}: description must be at most {DESCRIPTION_LIMIT} characters"
                )

    fence_count = sum(1 for line in lines if line.strip().startswith("```"))
    if fence_count % 2 != 0:
        errors.append(f"{path}: contains an unclosed code fence")

    return errors


def main() -> int:
    if not SKILL_FILES:
        print("No skill files found under skills/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in SKILL_FILES:
        errors.extend(validate_skill(path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(SKILL_FILES)} skill files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
