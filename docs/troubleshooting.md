# Troubleshooting

## The skill is not picked up

Try saying:

```text
Use the Plan. Patch. Prove workflow on this prompt:
<paste prompt>
```

Check the relevant skill is installed at one of:

```text
~/.agents/skills/<skill-name>/SKILL.md
~/.claude/skills/<skill-name>/SKILL.md
~/.copilot/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
.github/skills/<skill-name>/SKILL.md
```

Where `<skill-name>` is `shape`, `ship`, `ppp`, or `ppp-cloud`.

## It starts coding too early

Tell it:

```text
Stop. Follow PPP from the beginning. Inspect first, then plan. Do not code yet.
```

## It asks too many questions

Tell it:

```text
Use recommended defaults for low-risk questions and continue.
```

## It cannot create a PR

Ask it:

```text
Prepare the commit message, PR title, PR body, and exact git/gh commands for me to run.
```

## It gets stuck after test failures

PPP should stop after two focused fix attempts.

Ask a peer or senior engineer to review the debugging handoff.

## It ignores repo conventions

Check that your repo has one or more of:

```text
AGENTS.md
.github/copilot-instructions.md
.github/instructions/*.instructions.md
CONTRIBUTING.md
.github/PULL_REQUEST_TEMPLATE.md
```

Then remind the agent:

```text
Follow the repo instructions and nearby code/test conventions.
```
