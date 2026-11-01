# Initial candidate record: v0.2.0-preview.1

This file records the initial release candidate, which remains an unpublished empty Draft Pre-release. The public evaluation release is `v0.2.0-preview.2`; the repository release version is distinct from the individual Skill metadata versions.

## Release Level

- Initial candidate tag: `v0.2.0-preview.1` (pushed and intentionally unpublished)
- Published signed tag: `v0.2.0-preview.2`
- Repository release version: `0.2.0-preview.2`
- Skill metadata versions: `workspace-file-maintainer` `0.1.0`; `research-material-writer` `0.2.0-preview.1`
- GitHub release type: pre-release
- Stability: public evaluation; not a stable production release
- Observation window: 72 hours after publication

Once the tag is pushed, do not move, delete, or reuse it. Any correction must use a new version such as `0.2.0-preview.2`.

## Included Skills

- `workspace-file-maintainer` `0.1.0`
- `research-material-writer` `0.2.0-preview.1`

## Verified Scope

The release is intended to verify:

- explicit Skill invocation and deterministic repository behavior;
- Agent-neutral task contracts for research, file maintenance, and combined use;
- trigger-dataset structure and semantic field validation;
- functional-evaluation and acceptance-manifest gates;
- Markdown structural regression checks;
- symlink-safe reproducible repository packaging;
- ZIP content, version, source commit, and SHA-256 manifest verification;
- WorkBuddy-targeted package validation;
- open Agent Skills package validation for the open-spec variant;
- signed tag verification, exact-commit builds, and aggregate asset checksums.

## Known Limitations

- Automatic semantic triggering remains `blocked / unmeasured`; no precision, recall, or stability claim is made.
- Skills are instruction packages, not operating-system sandboxes.
- `allowed-tools` is experimental in the Agent Skills specification and client support varies.
- WorkBuddy packages retain the host-specific `agent_created: true` field; open-spec packages omit it.
- Historical real-project acceptance records include manual observations that are not reproduced by CI.
- Stable installation must use a versioned ZIP and manifest. Development symlinks expose uncommitted changes immediately.
- Runtime behavior has not been verified across every Agent client or operating system.

## Published Release Record

The published public pre-release is [`v0.2.0-preview.2`](https://github.com/weibinyuvertex120/repo-anatomy-skill/releases/tag/v0.2.0-preview.2), signed and bound to source commit `d07d36de0ce1378cded884c9c6e123044d48580b`. It contains exactly the nine assets listed below. The initial `v0.2.0-preview.1` candidate remains an empty draft and must not be presented as published.

Post-publication verification downloaded all nine assets to a new temporary directory, passed `sha256sum -c SHA256SUMS --strict`, matched every GitHub API `digest` and `size`, verified every manifest's `source_commit` and `source_dirty=false`, independently rebuilt from a clean detached worktree at the tag with matching outputs, and installed all four Skill/variant ZIPs using the stable installer. The tag signature was verified locally and by the successful `Verify Release Tags` workflow; GitHub reports the target commit as verified.

The first candidate workflow exposed two real gates: the hosted runner had no SSH `allowedSignersFile`, and dispatching the release workflow from `main` did not satisfy the release Environment's `v*` ref policy. The verifier was fixed through PR #9; the corrected workflow was dispatched from `v0.2.0-preview.2`. The pushed `v0.2.0-preview.1` tag was not moved, deleted, or reused.

## Release Assets

The public pre-release contains exactly these generated assets:

- `workspace-file-maintainer-workbuddy.zip`
- `workspace-file-maintainer-workbuddy.manifest.json`
- `workspace-file-maintainer-open-spec.zip`
- `workspace-file-maintainer-open-spec.manifest.json`
- `research-material-writer-workbuddy.zip`
- `research-material-writer-workbuddy.manifest.json`
- `research-material-writer-open-spec.zip`
- `research-material-writer-open-spec.manifest.json`
- `SHA256SUMS`

Each manifest must identify the Skill, semantic version, variant, exact tagged source commit, clean-tree state, flat archive filename, ZIP SHA-256, and exact package file list. Assets must be produced from the signed tag's exact commit.

## Installation And Verification

Use a WorkBuddy archive only with WorkBuddy. Use an open-spec archive with a client that supports the Agent Skills specification after checking that client's installation path and tool-approval behavior.

Download all nine assets into one directory and run:

```bash
sha256sum -c SHA256SUMS --strict
```

Keep the previous known-good ZIP and manifest. Do not point a stable installation at a development symlink.

## Publication Roles

Before publication, record these roles in the Draft Release review record:

- release owner and workflow trigger actor;
- code owner and environment reviewer, when an eligible independent collaborator is available;
- artifact builder;
- post-release verifier;
- rollback decision owner and executor.

In the current solo-maintainer preview mode, record the unavailable independent reviewer and environment separation as explicit limitations, perform a separate verification pass, and do not describe it as independent approval. The trigger actor cannot approve the release environment whenever self-review prevention is enabled, and the artifact builder cannot be the only post-release verifier once an independent verifier is available.

## Release Stop Conditions

Do not create the tag or publish when any of the following is true:

- PVR is disabled or `SECURITY.md` does not direct reporters to the active private channel;
- GitHub-native test or release-failure notification reachability is unverified;
- an active required `main` or `v*` ruleset is missing, or the `release` environment does not restrict deployment to approved tags; for solo preview, unavailable independent review or CODEOWNERS is a disclosed limitation, not a claimed control;
- the 40-character `RELEASE_SHA` is not locked, the local tree or stash is not clean, or the exact-SHA CI is not green;
- release-scope commit verification is invalid or the signed annotated tag cannot be verified locally, in CI, and on GitHub;
- repository release notes do not identify `v0.2.0-preview.2` as the published release;
- WorkBuddy and open-spec packages have not been independently validated;
- ZIP content, version, source commit, asset name, or SHA-256 does not match its manifest and `SHA256SUMS`;
- a P0 or P1 security issue affects the release path;
- licensing, third-party ownership, or material compatibility claims are unresolved.

## Rollback And Observation

During the 72-hour observation window, monitor security reports, installation failures, digest mismatches, and materially false compatibility guidance.

- Before a tag is pushed, draft assets and local tags may be recreated while logs are retained.
- After a tag is pushed, never move or delete it; abandon the version and create a new preview or patch.
- After publication, preserve the release and tag as history, add a warning or retain the pre-release designation when needed, and publish a corrected version.
