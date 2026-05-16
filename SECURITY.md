# Security

This repository contains AI agent skills and instructions.

Treat skills as operational instructions that can affect agent behaviour.

## Do not include

- secrets
- credentials
- tokens
- internal-only URLs
- customer data
- sensitive examples
- production incident details

## Review expectations

Changes to `SKILL.md` files should be reviewed carefully.

Pay particular attention to instructions that:

- grant broad autonomy
- weaken validation
- skip tests
- bypass review
- alter commit/PR behaviour
- change security, privacy, auth, permissions, data, migration, tenancy, billing, or public API guardrails
