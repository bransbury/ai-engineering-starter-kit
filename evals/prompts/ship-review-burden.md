# Eval prompt: ship review burden

We need to rename the `experimentStatus` values used across the stack:

- backend enum and serializer
- shared frontend contract
- results table rendering
- filters
- API docs
- tests

The file overlap is not huge, but all of the PRs would affect the same user-visible behaviour and reviewers would need to reason about the same mapping.

Choose the safest delivery path.
