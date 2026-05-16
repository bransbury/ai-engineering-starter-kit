#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_skill() {
  local skill_name="$1"
  local target_root="$2"
  local src="$ROOT/skills/$skill_name/SKILL.md"
  local dest="$target_root/$skill_name"

  if [[ ! -f "$src" ]]; then
    echo "Missing skill: $src"
    exit 1
  fi

  mkdir -p "$dest"
  cp "$src" "$dest/SKILL.md"
  echo "Installed $skill_name to $dest/SKILL.md"
}

install_cursor_rule() {
  local src="$ROOT/templates/cursor-ppp-rule.mdc"
  local dest_dir=".cursor/rules"
  local dest="$dest_dir/ppp.mdc"

  if [[ ! -f "$src" ]]; then
    echo "Missing Cursor rule template: $src"
    return 1
  fi

  if [[ -f "$dest" ]]; then
    echo "Cursor rule already exists at $dest — skipping (remove it manually to reinstall)"
    return 0
  fi

  mkdir -p "$dest_dir"
  cp "$src" "$dest"
  echo "Installed Cursor rule to $dest"
}

install_skill "ppp" "$HOME/.agents/skills"
install_skill "ppp" "$HOME/.copilot/skills"
install_skill "ppp-cloud" "$HOME/.agents/skills"
install_skill "ppp-cloud" "$HOME/.copilot/skills"

echo
if [[ -d ".cursor" ]]; then
  install_cursor_rule
else
  echo "Cursor not detected in current directory — skipping Cursor rule install."
  echo "To install manually: cp templates/cursor-ppp-rule.mdc .cursor/rules/ppp.mdc"
fi

echo
echo "Done."
echo "Try: /ppp <your ticket or task>"
