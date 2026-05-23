# Contributing

## What to contribute

Good contributions include:

- improvements to the shipped skill definitions (`shape`, `ship`, `ppp`, or `ppp-cloud`)
- new or improved examples
- fixes to docs that are unclear or wrong
- improvements to the install/uninstall scripts
- new templates that are broadly useful

Before working on a large change, open an issue to discuss the direction first.

## Skill changes

The shipped skills (`skills/shape/SKILL.md`, `skills/ship/SKILL.md`, `skills/ppp/SKILL.md`, and `skills/ppp-cloud/SKILL.md`) are the core of this project. Changes to them should:

- solve a real problem observed in practice, not a theoretical one
- not add complexity without clear benefit
- preserve the hard rules and safety properties
- keep token discipline — skills should stay concise and scannable
- keep related skills consistent where sections are shared (marked `<!-- Shared with ... — keep in sync -->`)

Changes that weaken safety rules, add unnecessary verbosity, or introduce model-specific hacks will not be merged.

## Testing a skill change

There is no automated test for skill behaviour. To validate a change:

1. Install the modified skill locally: `./install.sh`
2. Run it against two or three realistic tickets in your IDE
3. Verify the change produces the intended behaviour without regressing the core loop
4. Note results in your PR description

## Pull requests

- Keep PRs small and focused.
- Describe what changed and why.
- Include examples of the before/after behaviour for skill changes where possible.
- Use the PR template.

## Scripts

Run shellcheck before submitting changes to `install.sh` or `uninstall.sh`:

```bash
shellcheck install.sh uninstall.sh
```

## Versioning

When making a meaningful change to a skill, increment the `version` field in the skill's frontmatter and add an entry to `CHANGELOG.md`.
