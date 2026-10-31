# Draft: v0.2.0-preview.1

This is the draft release note for the first public preview of the repository. The Draft Pre-release may exist before publication, but this file does not imply that a signed tag, verified assets, or a public release already exists.

## Release Level

- Intended signed tag: `v0.2.0-preview.1`
- Repository release version: `0.2.0-preview.1`
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

## Release Assets

The public pre-release must contain exactly these generated assets:

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

Before publication, record these people in the Draft Release review record:

- release owner and workflow trigger actor;
- independent code owner and environment reviewer;
- artifact builder;
- independent post-release verifier;
- rollback decision owner and executor.

The trigger actor cannot approve the release environment, and the artifact builder cannot be the only post-release verifier.

## Release Stop Conditions

Do not create the tag or publish when any of the following is true:

- PVR is disabled or `SECURITY.md` does not direct reporters to the active private channel;
- GitHub-native test or release-failure notification reachability is unverified;
- required `main` or `v*` rulesets, CODEOWNERS review, or the protected release environment is missing;
- the 40-character `RELEASE_SHA` is not locked, the local tree or stash is not clean, or the exact-SHA CI is not green;
- release-scope commit verification is invalid or the signed annotated tag cannot be verified locally, in CI, and on GitHub;
- repository version declarations do not agree with `v0.2.0-preview.1`;
- WorkBuddy and open-spec packages have not been independently validated;
- ZIP content, version, source commit, asset name, or SHA-256 does not match its manifest and `SHA256SUMS`;
- a P0 or P1 security issue affects the release path;
- licensing, third-party ownership, or material compatibility claims are unresolved.

## Rollback And Observation

During the 72-hour observation window, monitor security reports, installation failures, digest mismatches, and materially false compatibility guidance.

- Before a tag is pushed, draft assets and local tags may be recreated while logs are retained.
- After a tag is pushed, never move or delete it; abandon the version and create a new preview or patch.
- After publication, preserve the release and tag as history, add a warning or retain the pre-release designation when needed, and publish a corrected version.
