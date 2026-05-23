# Agent Guide

This repository uses AI agents as manually invoked helpers.

There is no automatic multi-agent pipeline unless explicitly configured and tested.

For normal implementation work:

- Shape rough or oversized work first: `/shape`
- Route or coordinate delivery safely: `/ship`
- Human/IDE use: `/ppp`
- Autonomous cloud agent use: `/ppp-cloud`

Agents must follow repo instructions and stop for guardrailed work.

## Quick reference

| I want to... | Use |
| --- | --- |
| Clarify or split rough work before implementation | `/shape` |
| Choose the safest delivery path or coordinate multiple tasks | `/ship` |
| Complete a normal ticket in my IDE | `/ppp` |
| Create a draft PR from a clear bounded task | `/ppp-cloud` |
| Review a PR or diff | review agent / PR review workflow |
| Plan architecture | architecture agent or human-led planning |
| Add or improve tests | `/ppp` or `/ppp-cloud` with test-only scope |
| Handle auth/security/migration/API changes | human-led first |

## Recommended sequences

### Bug fix / small change

1. Use `/ppp` in IDE, or assign `/ppp-cloud` for a clear bounded cloud-agent task.
2. Review the resulting PR.

### New feature with unclear architecture

1. Use `/shape` first.
2. Human reviews/approves plan.
3. Use `/ship` if routing is still unclear, otherwise use `/ppp` or `/ppp-cloud` for the first bounded implementation task.

### Adding tests

1. Use `/ppp` or `/ppp-cloud` with test-only scope.
2. Review tests against behaviour, not implementation details.

### Review only

1. Use review workflow/agent.
2. Return findings as `APPROVE`, `NEEDS_CHANGES`, or `BLOCKED`.

## Context to provide

For implementation:

- task/ticket
- expected behaviour
- files/modules if known
- constraints and non-goals
- tests/checks expected
- ticket reference if available

For architecture:

- problem statement
- relevant modules
- constraints
- options considered
- risks
- non-goals

For review:

- original task
- PR/diff
- tests run
- known risks
- areas needing attention

## Guardrails

Stop and ask before:

- database migrations
- auth/security/permissions changes
- new dependencies
- public API changes
- data model changes
- tenant/billing behaviour
- destructive or irreversible changes
- privacy/compliance-sensitive behaviour
- module enablement/build configuration changes

## Instruction Files Reference

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Agent selection and usage guide |
| `.github/copilot-instructions.md` | Repo-wide Copilot guidance |
| `.github/instructions/*.instructions.md` | Path or task-specific instructions |
| `.github/skills/shape/SKILL.md` | Repo-local shaping skill |
| `.github/skills/ship/SKILL.md` | Repo-local delivery-routing skill |
| `.github/skills/ppp/SKILL.md` | Repo-local PPP skill |
| `.github/skills/ppp-cloud/SKILL.md` | Repo-local autonomous cloud-agent skill |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR format |
| `CONTRIBUTING.md` | Contributor workflow and local development notes |
