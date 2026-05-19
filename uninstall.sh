#!/usr/bin/env bash
set -euo pipefail

for root in "$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.copilot/skills"; do
  for skill in ppp ppp-cloud; do
    target="$root/$skill"
    if [[ -d "$target" ]]; then
      rm -rf "$target"
      echo "Removed $target"
    else
      echo "Not found, skipping: $target"
    fi
  done
done

cursor_rule=".cursor/rules/ppp.mdc"
if [[ -f "$cursor_rule" ]]; then
  rm "$cursor_rule"
  echo "Removed $cursor_rule"
else
  echo "Not found, skipping: $cursor_rule"
fi

echo "Done."
