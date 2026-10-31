# Changelog

All notable behavioral changes to the repository's Skills are recorded here.

## Repository validation and packaging - 2026-10-30

### Added

- Strict trigger-case field, group, and duplicate-prompt validation, plus functional-evaluation and acceptance-manifest gates.
- Repository-owned packaging that rejects symlinks and non-regular files and emits version/file-list/SHA-256 manifests.
- Regression tests for external symlink rejection and package contents.
- Fence-aware draft checking for backtick and tilde fences, with fenced content excluded from editorial scans and table-row checks scoped to each table.

### Changed

- README release instructions now use the repository packager and distinguish development symlinks from stable release installs.
- Acceptance records distinguish current working-tree validation from historical narrative evidence and mark the old 0.1.0 research archive as stale.

The project follows Semantic Versioning:

- MAJOR: changes triggering, permissions, or destructive-operation boundaries.
- MINOR: adds a backward-compatible workflow or supported text-file scenario.
- PATCH: clarifies instructions, improves errors, or fixes evaluations without widening scope.

## research-material-writer 0.2.0-preview.1 - 2026-10-31

### Added

- Open-source project onboarding mode for first-time use of unfamiliar repositories and Agent onboarding.
- A dedicated reference for project identity, governance, license, security, runtime prerequisites, trusted installation source, minimum success path, observable verification, client-specific Agent context, actual permission boundaries, maintenance, rollback, and stop conditions.
- Onboarding-specific quality checks and explicit trigger and functional evaluation cases.

### Changed

- Expanded README scope and repository validation to include onboarding references and evaluation coverage.

### Known Limitations

- Automatic semantic triggering remains deferred until after open-source publication by user decision; only explicit invocation is in scope for this revision.
- At the time of this entry, the WorkBuddy-required top-level `agent_created` field was incompatible with strict open-schema validators. Later packaging work adds a separate open-spec archive that removes this field; see the current compatibility matrix in `README.md`.

## research-material-writer 0.1.0 - 2026-10-30

### Added

- Evidence-led workflow for researched Chinese technical tutorials, project analyses, and comparison guides.
- Primary-source hierarchy, fact ledger, dynamic-fact dating, command verification, and conflict handling.
- Reader-centered tutorial pattern with one main path, observable verification, Agent prompts, security limits, and troubleshooting.
- Decision-oriented project and comparison modes with explicit unsuitable scenarios and evidence gaps.
- Markdown draft checker and regression tests for repeated table rows, empty headings, accidental language switches, unbalanced fences, and placeholders.
- Trigger and functional evaluation plans that distinguish researched writing from ordinary file maintenance.
- First real-project acceptance using `microsoft/markitdown`, including official-source conflict handling, isolated installation, CLI and Python API execution, and a standalone beginner tutorial.

### Known Limitations

- The structural checker cannot validate factual accuracy, source quality, or whether a tutorial genuinely succeeds in the target environment.
- Automatic semantic triggering has not yet been measured in a fresh host matrix; explicit invocation should be used during development.
- At the time of this entry, the WorkBuddy-required top-level `agent_created` field was incompatible with strict open-schema validators. Later packaging work adds a separate open-spec archive that removes this field; see the current compatibility matrix in `README.md`.

## workspace-file-maintainer 0.1.0 - 2026-10-30

### Added

- Initial workspace-scoped file creation, reading, precise modification, verification, and continued-iteration workflow.
- Explicit exclusions for destructive operations, personal-directory cleanup, binary formats, cloud documents, and secret handling.
- Progressive-disclosure references for workflow, safety, errors, and evaluations.
- Deterministic repository validation and reusable evaluation fixtures.
- Explicit-invocation acceptance coverage for creation, precise modification, continued iteration, ambiguous matches, sensitive fixtures, binary refusal, and exact outside-workspace paths.

### Known Limitations

- Automatic semantic triggering was not observed in the latest 7 relevant fresh-agent diagnostics. Explicit invocation is verified; stable tagging is deferred until automatic discovery improves.
- At the time of this entry, the only package retained `agent_created: true` and was rejected by strict open-schema validation. Later packaging work adds a separate open-spec archive; see the current compatibility matrix in `README.md`.
