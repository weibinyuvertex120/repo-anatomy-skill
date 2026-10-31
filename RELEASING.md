# Release Process

This repository follows GitHub Flow with a protected `main` branch and short-lived topic branches.

## Branches

- `main` must remain releasable and may receive changes only through pull requests after CI passes.
- Use `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, or `release/<version>` for isolated work.
- Delete topic branches after merging. Do not maintain a long-lived development branch.
- Prepare a release on `release/<version>` only to finalize version metadata, compatibility packages, release notes, and artifacts.

## Commits And Pull Requests

See [`COLLABORATION.md`](COLLABORATION.md) for the complete project collaboration standard, including PR creation, review, approval, branch protection, exception handling, and automation rules.

- Keep each commit focused and independently understandable.
- Use descriptive imperative commit subjects such as `feat: add open specification package`.
- A pull request must explain the problem, behavioral or documentation changes, verification commands, compatibility impact, and remaining risks.
- Squash merge ordinary pull requests into `main`. Preserve a separate commit only when its history is independently useful.
- Require the repository CI workflow before merge. Do not merge by bypassing failed checks.

## Versioning

Skill behavior follows Semantic Versioning:

- MAJOR changes triggering, permissions, destructive-operation boundaries, or incompatible package contracts.
- MINOR adds backward-compatible workflows or document modes.
- PATCH fixes instructions, validation, packaging, or tests without widening scope.
- Pre-release identifiers such as `-preview.1` mark public evaluation builds that are not yet stable.

The first public release is planned as `v0.2.0-preview.1`. It verifies explicit invocation and deterministic repository behavior. Automatic semantic triggering remains `blocked / unmeasured` until the host exposes auditable route/load events.

## Release Gate

A release candidate is acceptable only when:

1. The source commit is on `main`, the working tree is clean, and CI passes.
2. Repository validation, validator regression, draft-checker regression, and packaging regression pass.
3. Both WorkBuddy-targeted and open-spec packages validate against their intended schema.
4. ZIP contents, Skill versions, and SHA-256 manifests match the source commit.
5. `CHANGELOG.md`, compatibility statements, supported versions, and known limitations are current.
6. No unresolved P0 or P1 security issue affects the release path.
7. Release notes distinguish reproduced results, historical evidence, blocked checks, and unsupported clients.

## Tag And Publish

1. Merge the release pull request into `main` after all gates pass.
2. Create an annotated tag on the exact release commit: `v0.2.0-preview.1`.
3. Generate packages from that clean tagged commit with `python3 scripts/package_skills.py dist --require-clean`. Never publish archives produced from an uncommitted working tree.
4. Verify manifests and attach ZIP and manifest files to the GitHub pre-release.
5. Include installation, compatibility, verification, known limitations, and rollback information in the release notes.

Do not create or push a tag before the remote repository exists and the release owner explicitly approves publication.

## Rollback

- For unpublished changes, close the pull request or revert the topic-branch commits.
- For a merged regression, create a new pull request that reverts the merge commit or the focused offending commit.
- Do not move or overwrite a published tag. Publish a new patch or pre-release version with corrected artifacts.
- Keep the previous verified ZIP and manifest available so stable installations can return to the last known-good version.
