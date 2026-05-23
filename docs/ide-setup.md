# IDE setup

This starter kit is intended to work across IDEs and AI coding tools.

## Quick matrix

| Tool | Recommended setup | Notes |
| --- | --- | --- |
| VS Code + GitHub Copilot | Install personal skills to `~/.agents/skills`, `~/.claude/skills`, and `~/.copilot/skills` | Use Agent Mode where available |
| IntelliJ + GitHub Copilot | Use `/shape`, `/ship`, or `/ppp` if skills are picked up; otherwise paste the fallback prompt | Skill support may vary by environment |
| Cursor | Add PPP as a rule and keep canonical skills under `.agents/skills` | Use project/team/user rules |
| Claude Code | Use repo-local skills where supported | Keep shipped skills canonical in `skills/*/SKILL.md` |

## GitHub Copilot / VS Code

Install the skills:

```bash
npx ai-engineering-starter-kit install
```

Shell alternative:

```bash
./install.sh
```

Open your repo in VS Code, open Copilot Chat in Agent Mode, then run:

```text
/shape <prompt>
/ship <prompt>
/ppp <prompt>
```

**How skill discovery works:**
These slash-command skills become available when your Copilot environment supports loading personal skills from `~/.copilot/skills/` or `~/.agents/skills/`. If they do not autocomplete in the chat input, your setup may not load skills from those paths — use the fallback invocation instead.

**Fallback invocation (always works):**

```text
Use the Plan. Patch. Prove workflow on this prompt:
<paste prompt>
```

**Most reliable approach — repo-level guidance:**
Copy `templates/AGENTS.md` to `AGENTS.md` and `templates/copilot-instructions.md` to `.github/copilot-instructions.md` in your repo. These are picked up automatically by Copilot in VS Code and instruct it to follow the PPP loop regardless of whether the skill is installed.

## IntelliJ / JetBrains

Use:

```text
/shape <prompt>
/ship <prompt>
/ppp <prompt>
```

If the skill is not picked up, paste:

```text
Use the Plan. Patch. Prove workflow on this prompt:
<paste prompt>
```

Repo-local `AGENTS.md` and `.github/copilot-instructions.md` should also tell the assistant to follow the PPP loop.

## Cursor

If you run `npx ai-engineering-starter-kit install` or `./install.sh` from a project directory that already has a `.cursor/` folder, the rule is installed automatically to `.cursor/rules/ppp.mdc`.

To install manually into a project:

```bash
cp path/to/ai-engineering-starter-kit/templates/cursor-ppp-rule.mdc .cursor/rules/ppp.mdc
```

## Claude Code

Run the installer to install the shipped skills to `~/.claude/skills/`:

```bash
npx ai-engineering-starter-kit install
```

For repo-local skills (committed into the project), copy manually:

```bash
mkdir -p .claude/skills/ppp .claude/skills/ppp-cloud .claude/skills/shape .claude/skills/ship
cp path/to/ai-engineering-starter-kit/skills/ppp/SKILL.md .claude/skills/ppp/SKILL.md
cp path/to/ai-engineering-starter-kit/skills/ppp-cloud/SKILL.md .claude/skills/ppp-cloud/SKILL.md
cp path/to/ai-engineering-starter-kit/skills/shape/SKILL.md .claude/skills/shape/SKILL.md
cp path/to/ai-engineering-starter-kit/skills/ship/SKILL.md .claude/skills/ship/SKILL.md
```
