# v0.2.0-preview.1

This is the first public preview of the research-writing and conservative file-maintenance Skill repository.

## Release Level

- Git tag: `v0.2.0-preview.1`
- Semantic version: `0.2.0-preview.1`
- GitHub release type: pre-release
- Stability: public evaluation; not a stable production release

Do not replace assets under this version after publication. Any correction must use a new version such as `0.2.0-preview.2`.

## Included Skills

- `workspace-file-maintainer` 0.1.0
- `research-material-writer` 0.2.0-preview.1

## Verified Scope

- Explicit Skill invocation and deterministic repository behavior
- Trigger dataset structure and semantic field validation
- Functional-evaluation and acceptance-manifest gates
- Markdown structural regression checks
- Symlink-safe repository packaging
- ZIP content, version, and SHA-256 manifest verification
- WorkBuddy-targeted package validation
- Open Agent Skills package validation when the open-spec variant is generated

## Known Limitations

- Automatic semantic triggering remains `blocked / unmeasured`; no precision, recall, or stability claim is made.
- Skills are instruction packages, not operating-system sandboxes.
- `allowed-tools` is experimental in the open Agent Skills specification and client support varies.
- WorkBuddy requires a host-specific `agent_created: true` field; open-spec packages omit this field.
- The repository's historical real-project acceptance records include manual observations that are not reproduced by CI.
- Stable installation must use a versioned ZIP and manifest. Development symlinks expose uncommitted changes immediately.

## Release Assets

The draft release must contain both variants for each Skill:

- WorkBuddy-targeted ZIP and `.manifest.json`
- Open-spec ZIP and `.manifest.json`

Each manifest must identify the Skill, semantic version, variant, source commit, archive filename, file list, and SHA-256. Assets must be produced from the clean tagged commit.

## Installation And Rollback

Use the WorkBuddy variant only with WorkBuddy. Use the open-spec variant with clients that validate the Agent Skills specification. Verify SHA-256 before installation.

Keep the previous known-good ZIP and manifest. Roll back by replacing the installed version with the prior verified package; do not point a stable installation at a development symlink.

## Release Stop Conditions

Do not publish when any of the following is true:

- the source commit is not on `main`, the working tree is dirty, or CI has not passed;
- a P0 or P1 security issue affects the release path;
- WorkBuddy and open-spec packages have not been independently validated;
- ZIP content, version, source commit, or SHA-256 does not match its manifest;
- private vulnerability reporting or the Code of Conduct private contact channel is unavailable;
- licensing, third-party ownership, or compatibility claims are unresolved.
