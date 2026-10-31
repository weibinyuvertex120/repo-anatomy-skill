# Release Process

This repository follows GitHub Flow with a protected `main` branch, short-lived topic branches, signed immutable release tags, reproducible packages, and fail-closed publication gates.

## Branches

- `main` must remain releasable and may receive changes only through pull requests after required reviews and checks pass.
- Use `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `test/<topic>`, or `release/<version>` for isolated work.
- Delete topic branches after merging. Do not maintain a long-lived development branch.
- Prepare a release on `release/<version>` only to finalize version metadata, compatibility packages, release notes, workflows, and artifacts.
- Follow [`COLLABORATION.md`](COLLABORATION.md) for pull-request review, approval, merge, and exception handling.

## Versioning

Skill behavior follows Semantic Versioning:

- MAJOR changes triggering, permissions, destructive-operation boundaries, or incompatible package contracts.
- MINOR adds backward-compatible workflows or document modes.
- PATCH fixes instructions, validation, packaging, or tests without widening scope.
- Pre-release identifiers such as `-preview.1` mark public evaluation builds that are not yet stable.

The first public repository release is planned as `v0.2.0-preview.1` and contains:

- `workspace-file-maintainer` `0.1.0`;
- `research-material-writer` `0.2.0-preview.1`.

Automatic semantic triggering remains `blocked / unmeasured` and is not a release guarantee.

## Roles And Separation

The first public preview requires an independent collaborator with repository write access.

- **Release owner:** proposes the candidate, records `RELEASE_SHA`, initiates the tag and release workflow, and makes the Go/No-Go request.
- **Code owner reviewer:** reviews repository and workflow changes and must not be the PR author.
- **Environment reviewer:** approves the release job and must not be the workflow trigger actor.
- **Post-release verifier:** downloads published assets and independently verifies tag, checksums, provenance evidence when present, and rollback conditions.
- **Rollback decision owner:** decides whether an observation requires warning, marking the release as pre-release, or publishing a corrected version.

One person may hold more than one role only when the separation requirement is still met. The release owner cannot approve their own PR or environment deployment, and the artifact builder cannot be the only post-release verifier. A solo-maintainer mode does not satisfy the first-preview Go criteria.

## Governance Gate

Do not create or push a release tag until all of these conditions are true:

1. GitHub private vulnerability reporting is enabled and [`SECURITY.md`](SECURITY.md) directs reporters to the active PVR channel.
2. GitHub-native test and release-failure notifications have been demonstrated with an auditable Actions run or issue record and acknowledged by the responsible recipient.
3. A `main` ruleset requires pull requests, code-owner review, conversation resolution, successful required checks, and an up-to-date branch; it blocks force pushes and deletion and requires signed commits from the governance baseline forward.
4. The required check names were added only after each check completed successfully in the repository.
5. A `v*` tag ruleset blocks tag updates, deletion, and force pushes without an ordinary maintainer bypass.
6. A release environment requires an independent reviewer, prevents self-review, restricts deployments to approved tags, and does not permit administrator bypass during the release path.
7. Release workflow permissions are minimal and every third-party action is pinned to a full commit SHA.
8. `CODEOWNERS` names an eligible independent reviewer and protects its own file and release workflow paths.

Do not rewrite existing history merely to add signatures. Signed-commit enforcement applies from the approved governance baseline forward. Existing release-scope commits must show a valid GitHub verification state before the candidate is frozen.

## Freeze The Candidate

After all release changes are reviewed and merged, synchronize a clean local `main` and record an immutable 40-character commit ID:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
RELEASE_SHA="$(git rev-parse HEAD)"
test "${#RELEASE_SHA}" -eq 40
```

A candidate is frozen only when:

- `git status --porcelain` is empty;
- `git stash list` is empty;
- `RELEASE_SHA` equals `git rev-parse origin/main`;
- CI completed successfully on that exact SHA;
- GitHub reports the release-scope commit signatures as valid;
- Skill metadata, `CHANGELOG.md`, release notes, workflow version input, and intended tag all agree;
- no local or remote tag with the intended name exists;
- no unresolved P0 or P1 issue affects the release path.

Never use a floating reference such as “latest main” as the build source after `RELEASE_SHA` is recorded.

## Sign And Push The Tag

Create a signed annotated tag that points exactly to `RELEASE_SHA`:

```bash
git tag -s v0.2.0-preview.1 "$RELEASE_SHA" -m "v0.2.0-preview.1"
git verify-tag v0.2.0-preview.1
test "$(git rev-list -n 1 v0.2.0-preview.1)" = "$RELEASE_SHA"
git push origin refs/tags/v0.2.0-preview.1
```

Required results:

- local `git verify-tag` reports a good signature;
- the tag object resolves to `RELEASE_SHA`;
- the tag-verification workflow succeeds;
- GitHub displays the tag as **Verified**;
- the tag is pushed explicitly and separately from branches.

A local tag that has never been pushed may be recreated. Once a `v*` tag is pushed, do not move, delete, or reuse it, even before public release. Correct an error with a new preview or patch version.

## Build And Verify Assets

The build must check out the exact tag commit with full history and tags, verify the tag signature, and confirm the resolved commit equals the workflow's recorded release SHA. It must fail closed on any mismatch.

Build from the clean tagged revision:

```bash
python3 scripts/package_skills.py dist --require-clean
cd dist
sha256sum -c SHA256SUMS --strict
```

The release asset contract is exactly:

- four ZIP files: two Skills times WorkBuddy/open-spec variants;
- four `.manifest.json` files;
- one aggregate `SHA256SUMS`.

Each manifest uses a flat release asset filename and records the Skill, semantic version, variant, source commit, dirty-tree state, ZIP SHA-256, and exact package file list. It must not contain timestamps, absolute paths, runner names, or mutable branch labels. Each manifest must set `source_dirty` to `false` and `source_commit` to the tag's exact commit.

`SHA256SUMS` must use flat asset filenames, sorted deterministically. `sha256sum -c SHA256SUMS --strict` and an independent per-file digest comparison must both pass. A hash match does not replace tag-signature or source-provenance verification.

GitHub artifact attestations may be added later. For this preview, exact signed-tag checkout, manifest source binding, clean-tree enforcement, and reproducible byte comparison are the required provenance controls. Any inconsistency fails closed.

## Draft And Publish

1. Create or reuse the GitHub Draft Pre-release for the exact tag.
2. Upload all nine release assets only after local and CI verification pass.
3. Compare each uploaded GitHub asset digest with `SHA256SUMS` and the locally recorded digest.
4. Have the independent reviewer inspect the draft title, tag, target commit, notes, asset names, digests, installation guidance, limitations, and rollback plan.
5. Run the publish job through the protected `release` environment. The trigger actor cannot approve the deployment.
6. Publish only when every required gate reports Go. Recommended items may be deferred only with a recorded technical-debt issue.

The publish job receives only the permissions needed for release mutation. Build and validation jobs remain read-only.

## Post-Release Verification

A person other than the artifact builder must:

1. download all assets from the public release page into a new disposable directory;
2. run `sha256sum -c SHA256SUMS --strict`;
3. compare each downloaded asset with GitHub's displayed or API-provided digest;
4. run `git verify-tag` against a fresh fetch and confirm the tag commit equals the recorded `RELEASE_SHA`;
5. verify manifest source binding and provenance evidence when present;
6. test one WorkBuddy installation and one open-spec structural validation from downloaded assets;
7. record the result and start the observation window defined in the release notes.

## Rollback

Before publication, name the rollback decision owner, executor, triggers, and evidence location and perform a dry run of the commands that do not destroy remote history.

- **Draft stage before a tag is pushed:** delete or replace the draft assets and recreate only local unpushed tags; retain logs.
- **After a tag is pushed but before publication:** do not move or delete the tag. Abandon the version and create a new preview or patch candidate.
- **After publication:** never move, delete, or rewrite the tag. Add a prominent warning or retain the pre-release designation as appropriate, preserve the historical release and logs, and publish a corrected preview or patch.
- **Merged source regression:** use a focused revert PR. Do not rewrite `main`.

Stop publication or begin rollback review for signature failure, source-SHA mismatch, checksum mismatch, missing asset, installation failure, P0/P1 security issue, or materially false compatibility guidance.
