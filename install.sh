#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=0
FORCE=0
SKIP_PROMPTS=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [--dry-run] [--force] [--yes] [--help]

Options:
  --dry-run  Show what would be installed without writing files
  --force    Overwrite existing installs without prompting
  --yes      Non-interactive; skip overwrite prompts and leave existing files untouched
  --help     Show this help text
EOF
}

log() {
  echo "$*"
}

run_cmd() {
  if (( DRY_RUN )); then
    log "[dry-run] $*"
  else
    "$@"
  fi
}

action_word() {
  if (( DRY_RUN )); then
    echo "Would install"
  else
    echo "Installed"
  fi
}

skill_version() {
  local skill_name="$1"
  local src="$ROOT/skills/$skill_name/SKILL.md"
  grep -E '^version:' "$src" | head -n 1 | sed -E 's/^version:[[:space:]]*//'
}

backup_file() {
  local path="$1"
  local backup_path

  backup_path="${path}.bak.$(date +%Y%m%d%H%M%S)"

  run_cmd cp "$path" "$backup_path"
  if (( DRY_RUN )); then
    log "Would back up existing file to $backup_path"
  else
    log "Backed up existing file to $backup_path"
  fi
}

should_overwrite() {
  local path="$1"

  if [[ ! -e "$path" ]]; then
    return 0
  fi

  if (( FORCE )); then
    return 0
  fi

  if (( SKIP_PROMPTS )) || [[ ! -t 0 ]]; then
    log "Exists at $path — skipping (use --force to overwrite)"
    return 1
  fi

  printf 'Overwrite %s? [y/N] ' "$path" >&2
  read -r reply
  case "$reply" in
    y|Y|yes|YES)
      return 0
      ;;
    *)
      log "Skipping $path"
      return 1
      ;;
  esac
}

install_skill() {
  local skill_name="$1"
  local target_root="$2"
  local src="$ROOT/skills/$skill_name/SKILL.md"
  local dest="$target_root/$skill_name"
  local target_file="$dest/SKILL.md"
  local version

  version="$(skill_version "$skill_name")"

  if [[ ! -f "$src" ]]; then
    echo "Missing skill: $src"
    exit 1
  fi

  run_cmd mkdir -p "$dest"

  if should_overwrite "$target_file"; then
    if [[ -f "$target_file" ]]; then
      backup_file "$target_file"
    fi
    run_cmd cp "$src" "$target_file"
    log "$(action_word) $skill_name $version to $target_file"
  fi
}

install_cursor_rule() {
  local src="$ROOT/templates/cursor-ppp-rule.mdc"
  local dest_dir=".cursor/rules"
  local dest="$dest_dir/ppp.mdc"

  if [[ ! -f "$src" ]]; then
    echo "Missing Cursor rule template: $src"
    return 1
  fi

  run_cmd mkdir -p "$dest_dir"

  if should_overwrite "$dest"; then
    if [[ -f "$dest" ]]; then
      backup_file "$dest"
    fi
    run_cmd cp "$src" "$dest"
    log "$(action_word) Cursor rule to $dest"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    --force)
      FORCE=1
      ;;
    --yes)
      SKIP_PROMPTS=1
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

log "PPP installer"
log "Version: $(skill_version "ppp")"
if (( DRY_RUN )); then
  log "Mode: dry-run"
fi
if (( FORCE )); then
  log "Overwrite mode: force"
fi
echo

install_skill "ppp" "$HOME/.agents/skills"
install_skill "ppp" "$HOME/.claude/skills"
install_skill "ppp" "$HOME/.copilot/skills"
install_skill "ppp-cloud" "$HOME/.agents/skills"
install_skill "ppp-cloud" "$HOME/.claude/skills"
install_skill "ppp-cloud" "$HOME/.copilot/skills"

echo
if [[ -d ".cursor" ]]; then
  install_cursor_rule
else
  log "Cursor not detected in current directory — skipping Cursor rule install."
  log "To install manually: cp templates/cursor-ppp-rule.mdc .cursor/rules/ppp.mdc"
fi

echo
log "Done."
log "Important: /ppp works only where your tool loads skills as slash commands."
log "Fallback: Use the Plan. Patch. Prove workflow on this prompt:"
log "<paste prompt>"
