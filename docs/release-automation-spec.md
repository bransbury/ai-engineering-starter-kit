# Release Automation Spec

## Recommendation

Use a tag-driven release workflow as the first automated release model.

Recommended flow:

1. Merge the release branch into `main`.
2. Push an annotated tag such as `v0.3.0`.
3. GitHub Actions validates the tag and creates the GitHub Release automatically.

This is safer than releasing automatically on every merge to `main`. It keeps the release moment explicit, while removing the repetitive GitHub UI work.

## Why this approach

For this repo, a release is more than "whatever just merged":

- the changelog should be ready;
- skill versions should match the release;
- docs and install behavior should be coherent;
- the release should be intentional and reviewable.

A tag-driven workflow is the right middle ground:

- less manual work than creating releases in the GitHub UI;
- less risk than auto-publishing on every merge;
- compatible with semver tags like `v0.3.0`;
- easy to understand for contributors.

## Goals

- Create a GitHub Release automatically when a valid release tag is pushed.
- Ensure the tagged commit passed CI before the release is published.
- Use the repo changelog as the source of release notes.
- Prevent obvious mismatches such as tag `v0.3.0` with skill version `0.2.0`.
- Keep the release process simple enough for a small OSS repo.

## Non-goals

- Fully automatic version bumping on merge.
- Conventional-commits-based semantic release.
- Publishing packages to npm, PyPI, or another package registry.
- Building binary artifacts.

## Functional requirements

### Trigger

- The workflow must run on `push` for tags matching `v*`.
- Example valid tags:
  - `v0.3.0`
  - `v1.0.0`
- Pre-release support is optional for v1 of the workflow.
  - If supported, allow forms such as `v0.4.0-rc.1`.

### Preconditions

- The tag must point to a commit on `main`.
- Existing CI checks must pass for the tagged commit.
- `CHANGELOG.md` must contain a section matching the tag version without the `v` prefix.
  - Example: tag `v0.3.0` requires `## 0.3.0` in `CHANGELOG.md`.
- `skills/ppp/SKILL.md` and `skills/ppp-cloud/SKILL.md` must have frontmatter `version` values matching the release version.
  - Example: tag `v0.3.0` requires `version: 0.3.0`.

### Release creation

- The workflow must create a GitHub Release if one does not already exist for the tag.
- The release title should default to the tag.
  - Example: `v0.3.0`
- The release body should be derived from the matching `CHANGELOG.md` section.
- The workflow should mark the release as non-draft and non-prerelease by default.

### Failure behavior

- If validation fails, the workflow must fail without creating a release.
- Failure output should clearly say which check failed:
  - tag not on `main`
  - missing changelog section
  - skill version mismatch
  - CI not green
- The workflow must not silently create partial or malformed releases.

## Recommended implementation

### Workflow design

Add a new workflow such as:

```text
.github/workflows/release.yml
```

Recommended high-level jobs:

1. `validate-release-tag`
2. `extract-release-notes`
3. `create-github-release`

### Validation logic

The workflow should:

1. Parse the tag version.
2. Confirm the tagged commit is reachable from `origin/main`.
3. Confirm the relevant CI workflow completed successfully for that commit.
4. Check `CHANGELOG.md` for the matching version heading.
5. Check both skill files for matching `version:` values.

This logic can live in a small script under `scripts/`, which is preferable to embedding everything in shell in the workflow YAML.

Suggested script split:

- `scripts/validate_release.py`
- optional: `scripts/extract_release_notes.py`

### Release notes source

Preferred source:

- parse the matching section from `CHANGELOG.md`

Fallback:

- fail the workflow if the changelog section cannot be extracted

Do not generate release notes from commit history as the primary source for this repo. The changelog is already the curated release narrative.

### GitHub permissions

The workflow will need:

- `contents: write`

This is required to create a GitHub Release via the Actions token.

## Operational requirements

### Developer workflow

The intended release flow should be:

1. Merge the prepared release branch into `main`.
2. Pull latest `main` locally.
3. Create and push the tag.
4. Let GitHub Actions create the release.

Example:

```bash
git checkout main
git pull origin main
git tag -a v0.3.0 -m "v0.3.0"
git push origin v0.3.0
```

### Rollback

If a bad tag is pushed before the release succeeds:

- delete the tag locally and remotely;
- fix the repo state;
- create and push the corrected tag.

If a release is created incorrectly:

- delete the GitHub Release;
- delete the tag if needed;
- fix the issue;
- re-tag and re-push.

## Nice-to-have later

- Support pre-releases such as `v0.4.0-rc.1`.
- Add a workflow-dispatch option for maintainers to dry-run release validation.
- Add validation that the release tag is newer than the latest published release.
- Add a check that README badge/version references remain coherent.
- Add automatic discussion or announcement generation from release notes.

## Open questions

- Should pre-releases be supported in the first implementation?
- Should the workflow create releases only from annotated tags, or accept lightweight tags too?
- Should release validation be reusable as a pull-request check before tagging?

## Acceptance criteria

The automation is complete when:

- pushing `v0.3.0` on a valid `main` commit creates a GitHub Release automatically;
- the release body is populated from `CHANGELOG.md`;
- a mismatched skill version causes the workflow to fail;
- a missing changelog section causes the workflow to fail;
- a tag outside `main` does not publish a release.
