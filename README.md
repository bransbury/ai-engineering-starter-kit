# AI Engineering Starter Kit

Most engineers using AI assistants fall into the same pattern: ask a question in chat, paste the answer in, skip the tests, move on. It's fast until it isn't — reviews catch things nobody fully understands, tests get weakened to make CI pass, and the agent confidently makes decisions it shouldn't.

This kit gives engineers two structured workflows that keep AI coding both fast and safe: inspect first, plan the smallest change, prove it works, then PR.

The starter kit includes:

- **Plan. Patch. Prove. (`/ppp`)** — an interactive workflow for engineers using an IDE agent
- **Plan. Patch. Prove. Cloud (`ppp-cloud`)** — a non-interactive workflow for autonomous cloud coding agents
- repo templates for agent guidance, Copilot instructions, PR templates, and Cursor rules
- practical docs and examples for adoption

## Plan. Patch. Prove.

```text
Inspect → Clarify → Plan → Prove → Patch → Review → PR
```

PPP helps engineers avoid snippet-copy coding by guiding AI agents to inspect the codebase, plan the smallest safe complete change, prove the behaviour, patch in small loops, review production readiness, and prepare a PR.

> Plan. Patch. Prove. The practical AI coding loop: inspect first, change safely, verify before PR.

## Quick start

```bash
git clone https://github.com/bransbury/ai-engineering-starter-kit
cd ai-engineering-starter-kit
./install.sh
```

Then use the slash command if your tool supports it:

```text
/ppp <paste ticket or task>
```

Or the fallback invocation (always works):

```text
Use ppp on this ticket:
<paste ticket>
```

Not sure which to use? See [IDE setup](docs/ide-setup.md).

## What gets installed?

The install script copies the skills to both common personal skill locations:

```text
~/.agents/skills/ppp/SKILL.md
~/.agents/skills/ppp-cloud/SKILL.md
~/.copilot/skills/ppp/SKILL.md
~/.copilot/skills/ppp-cloud/SKILL.md
```

If a `.cursor/` directory is detected in the current directory, it also installs the Cursor rule:

```text
.cursor/rules/ppp.mdc
```

Run `./install.sh` from each project where you want the Cursor rule active.

## When to use `/ppp`

Use `/ppp` for normal engineering work that should fit in one focused PR:

- bug fixes
- small features
- tests
- UI tweaks
- small refactors

Good examples:

```text
/ppp Fix whitespace-only report names being accepted.
/ppp Add an empty state to the experiment results table when there are no rows.
/ppp Update the token parser to preserve {{firstName|}} as an explicit empty fallback.
```

## When not to use `/ppp`

Do not use `/ppp` to implement a whole large feature in one go.

Examples that are too large:

```text
/ppp Build a new analytics dashboard.
/ppp Implement the new permissions system.
```

For large work, ask `/ppp` to identify the smallest first task, or use a feature-slicing workflow.

## What good looks like

A good PPP run should:

- inspect relevant code before editing
- ask only important questions
- define proof before patching
- add or update tests/checks where appropriate
- stop after two focused failed fix attempts
- review production readiness
- prepare a PR title/body using repo conventions

See a [full example run](examples/prompts/ppp-examples.md#what-good-output-looks-like).

## Cloud agent usage

| | `/ppp` | `ppp-cloud` |
|---|---|---|
| **Who drives it** | Engineer in IDE | Autonomous cloud agent |
| **Interaction** | Interactive menus | Non-interactive, runs to completion |
| **Output** | Guided session → PR handoff | Draft PR or blocker report |
| **Best for** | Any normal ticket with a human in the loop | Clear, bounded tasks you can assign and review |

Use `ppp-cloud` for autonomous coding agents. It is designed for clear, bounded, verifiable tasks where the agent should either:

- create one focused draft PR; or
- stop with a clear blocker explaining why it could not proceed safely.

See [Cloud agent usage](docs/cloud-agent-usage.md).

## Docs

- [How to use PPP](docs/how-to-use-ppp.md)
- [IDE setup](docs/ide-setup.md)
- [Cloud agent usage](docs/cloud-agent-usage.md)
- [Adoption rollout](docs/adoption-rollout.md)
- [Troubleshooting](docs/troubleshooting.md)

## Templates

Copy these into your repos to give AI agents consistent guidance:

| Template | Copy to | Purpose |
|---|---|---|
| `templates/AGENTS.md` | `AGENTS.md` (repo root) | Tells agents which workflow to use and what requires human approval |
| `templates/copilot-instructions.md` | `.github/copilot-instructions.md` | Repo-level Copilot instructions picked up automatically in VS Code |
| `templates/PULL_REQUEST_TEMPLATE.md` | `.github/PULL_REQUEST_TEMPLATE.md` | Consistent PR descriptions across human and AI-authored PRs |
| `templates/cursor-ppp-rule.mdc` | `.cursor/rules/ppp.mdc` | Cursor project rule — automatically installed by `./install.sh` if `.cursor/` exists |

Each template is intentionally minimal. Add repo-specific conventions (architecture rules, test commands, forbidden areas) directly in `AGENTS.md` and `copilot-instructions.md`.

## Security note

Skills are operational instructions that can influence AI agent behaviour. Review changes to `SKILL.md` files carefully.

Do not add secrets, credentials, internal-only URLs, or sensitive customer data to skills or examples.

## License

[MIT](LICENSE.md) © 2026 Marcus Bransbury
