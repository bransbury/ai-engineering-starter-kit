# Changelog

## 0.4.0

- Added a native `npx` installer via `bin/ai-engineering-starter-kit.js`.
- Added `package.json` for npm distribution and CLI aliases.
- Added support for `install`, `uninstall`, `--dry-run`, `--force`, `--yes`, and `--repo-local` in the Node CLI.
- Updated README install guidance to prefer `npx ai-engineering-starter-kit install`.

## 0.3.0

- Added README badges for CI, license, and GitHub releases.
- Added top-level "How it works" diagrams for `/ppp` and `ppp-cloud`.
- Added a README setup decision table covering personal install, repo rollout, Cursor, and cloud-agent usage.
- Added README positioning on how PPP differs from Matt Pocock's skills and `gstack`.
- Clarified slash-command support and promoted the always-works fallback invocation.
- Added explicit repo-local skill install commands for `.github/skills`.
- Added a concrete README bug-fix example that links to the full PPP transcript.
- Added `scripts/validate_skills.py` and a CI check for skill frontmatter and unclosed code fences.
- Added installer safety features: `--dry-run`, `--force`, backups, version output, and overwrite prompts.
- Added a `.github/ISSUE_TEMPLATE/ppp-cloud-task.md` template for assigning bounded cloud-agent tasks.
- Added a release automation spec recommending tag-driven GitHub Releases.
- Implemented tag-driven GitHub release automation from `v*` tags.

## 0.2.0

- Added Cursor rule install to `install.sh` — auto-installs to `.cursor/rules/ppp.mdc` when `.cursor/` is detected.
- Added `version` field to both skill frontmatters.
- Added similarity comments to shared sections in both skills.
- Improved `uninstall.sh` to check paths before removing and handle Cursor rule removal.
- Added `CONTRIBUTING.md`.
- Added GitHub Actions CI workflow (shellcheck + markdownlint).
- Added `.markdownlint.json` config.
- Expanded README templates section with copy-to destinations and purpose descriptions.
- Updated README "What gets installed?" to document Cursor rule install.
- Expanded `ide-setup.md` VS Code section with skill discovery explanation and fallback invocation.
- Updated `ide-setup.md` Cursor section to reflect auto-install.
- Added "What good output looks like" example to `ppp-examples.md`.
- Added "What a blocker output looks like" example to `ppp-cloud-examples.md`.

## 0.1.0

- Added `/ppp` skill for interactive IDE usage.
- Added `ppp-cloud` skill for autonomous cloud coding agents.
- Added install and uninstall scripts.
- Added repo templates for agent guidance, Copilot instructions, PR templates, and Cursor rules.
- Added adoption docs and example prompts.
