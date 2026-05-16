# How to use PPP

`/ppp` is a practical AI-assisted workflow for normal engineering tasks.

```text
Inspect → Clarify → Plan → Prove → Patch → Review → PR
```

## Start with a ticket

```text
/ppp Fix whitespace-only report names being accepted.
```

or:

```text
Use ppp on this ticket:
<paste ticket>
```

## Responding to menus

When PPP gives options, reply with the number:

```text
1
```

You can also say:

```text
continue
```

or:

```text
use recommended
```

## What PPP should do

A good PPP run should:

- inspect the relevant code before editing
- ask only blocking or high-impact questions
- recommend safe defaults where appropriate
- plan the smallest safe complete change
- define proof before patching
- add or update tests/checks where appropriate
- patch in small validated loops
- stop after two focused failed fix attempts
- review production readiness
- prepare a commit and PR handoff

## Before PR

Before committing or creating a PR, make sure you understand:

- what changed
- why it changed
- how it was tested
- what risks remain

During the Review phase, you can ask PPP to walk through the changes before committing.

## When PPP should stop

PPP should stop and ask for help when:

- the requirement is unclear
- the task grows beyond the agreed scope
- auth/security/permissions are involved
- data migrations are required
- public API changes are required
- validation fails after two focused attempts
- the code cannot be inspected
- checks cannot be run or meaningfully reasoned about
