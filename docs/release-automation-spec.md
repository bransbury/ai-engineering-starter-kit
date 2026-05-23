# Release Automation Spec

## Recommendation

Use a tag-driven release workflow as the first automated release model.

Recommended flow:

1. Merge the release branch into `main`.
2. Push an annotated tag such as `v0.3.0`.
3. GitHub Actions validates the tag, publishes the npm package, and creates the GitHub Release automatically.

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

## Status

Implemented in:

- `.github/workflows/release.yml`
- `scripts/validate_release.py`
- `scripts/extract_release_notes.py`

This document now describes the intended behavior of that implementation and the follow-on improvements that may still be worth adding later.

## Goals

- Create a GitHub Release automatically when a valid release tag is pushed.
- Ensure the tagged commit passes release-critical validation before npm or GitHub publishing happens.
- Use the repo changelog as the source of release notes.
- Publish the npm package automatically from the release tag.
- Prevent obvious mismatches such as tag `v0.3.0` with skill version `0.2.0`.
- Prevent package version mismatches such as tag `v0.5.0` with `package.json` version `0.4.0`.
- Keep the release process simple enough for a small OSS repo.

## Non-goals

- Fully automatic version bumping on merge.
- Conventional-commits-based semantic release.
- Publishing packages to registries other than npm.
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
- The tagged commit must pass release-critical validation in the release workflow.
- `CHANGELOG.md` must contain a section matching the tag version without the `v` prefix.
  - Example: tag `v0.3.0` requires `## 0.3.0` in `CHANGELOG.md`.
- `skills/ppp/SKILL.md`, `skills/ppp-cloud/SKILL.md`, `skills/shape/SKILL.md`, and `skills/ship/SKILL.md` must have frontmatter `version` values matching the release version.
  - Example: tag `v0.3.0` requires `version: 0.3.0`.
- `package.json` must have a `version` value matching the release version.
  - Example: tag `v0.5.0` requires `"version": "0.5.0"`.

### Release creation

- The workflow must publish the npm package before creating the GitHub Release.
- npm publishing should use npm trusted publishing via GitHub Actions OIDC.
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
  - package version mismatch
- The workflow must not silently create partial or malformed releases.

## Recommended implementation

### Workflow design

Add a new workflow such as:

```text
.github/workflows/release.yml
```

Current high-level flow:

1. run release-critical checks
2. validate the tag, branch ancestry, changelog, skill versions, and package version
3. publish the npm package
4. extract release notes from `CHANGELOG.md`
5. create the GitHub Release

### Validation logic

The workflow should:

1. Parse the tag version.
2. Confirm the tagged commit is reachable from `origin/main`.
3. Run release-critical validation on the tagged commit.
4. Check `CHANGELOG.md` for the matching version heading.
5. Check both skill files for matching `version:` values.
6. Check `package.json` for the matching `version` value.

This logic can live in a small script under `scripts/`, which is preferable to embedding everything in shell in the workflow YAML.

Current script split:

- `scripts/validate_release.py`
- `scripts/extract_release_notes.py`

### Release notes source

Preferred source:

- parse the matching section from `CHANGELOG.md`

Fallback:

- fail the workflow if the changelog section cannot be extracted

Do not generate release notes from commit history as the primary source for this repo. The changelog is already the curated release narrative.

### GitHub permissions

The workflow will need:

- `contents: write`
- `id-token: write`

These are required for:

- npm trusted publishing via OIDC
- `softprops/action-gh-release` to create a GitHub Release via the Actions token

## Operational requirements

### Developer workflow

The intended release flow should be:

1. Merge the prepared release branch into `main`.
2. Pull latest `main` locally.
3. Create and push the tag.
4. Let GitHub Actions publish the npm package and create the release.

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
- Add an optional dry-run release validation workflow-dispatch path that skips `npm publish`.

## Open questions

- Should pre-releases be supported in the first implementation?
- Should the workflow create releases only from annotated tags, or accept lightweight tags too?
- Should release validation be reusable as a pull-request check before tagging?

## Acceptance criteria

The automation is complete when:

- pushing `v0.3.0` on a valid `main` commit creates a GitHub Release automatically;
- pushing `v0.5.0` on a valid `main` commit publishes the npm package automatically;
- the release body is populated from `CHANGELOG.md`;
- a mismatched skill version causes the workflow to fail;
- a mismatched package version causes the workflow to fail;
- a missing changelog section causes the workflow to fail;
- a tag outside `main` does not publish a release.
