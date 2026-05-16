# Changelog

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
