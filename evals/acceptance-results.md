# Acceptance Results

Verification date: 2026-10-30
Skills: `workspace-file-maintainer` 0.1.0; `research-material-writer` 0.2.0-preview.1
Host scope: local WorkBuddy validation on macOS plus credential-free repository CI designed for Ubuntu

## Verification Record

- skill_versions: `workspace-file-maintainer` 0.1.0; `research-material-writer` 0.2.0-preview.1
- host: WorkBuddy AI local validation environment; exact application build was not recorded
- source_revision: release manifests are authoritative for the exact source commit and clean-tree state of generated archives
- evidence_scope: deterministic checks are current and reproducible; fresh-agent and real-project observations are historical narrative evidence unless explicitly rerun
- package_scope: four candidates are generated from one source tree: two Skills multiplied by WorkBuddy and open-spec variants
- routing_scope: explicit invocation is the development and acceptance requirement; automatic semantic routing remains blocked or unmeasured
- remote_scope: branch protection, private vulnerability reporting, hosted CI, pull-request review, tags, and GitHub Releases require verification on the publishing repository

## Current Deterministic Validation

| Check | Current result |
|---|---|
| Repository validator | Pass: both Skill manifests, references, evaluation schemas, versions, license, changelog, and repository hygiene |
| Trigger datasets | Pass: 14 workspace cases and 16 research cases; structural coverage is not a routing metric |
| Validator regression | Pass: baseline plus missing reference, version mismatch, invalid JSON, invalid field types, empty values, unknown group, duplicate prompt, external symlink, and empty functional evidence failures |
| Draft-checker regression | Pass: clean input and 14 defect/boundary cases including fence forms, repeated content, table scope, heading defects, and placeholders |
| Packaging regression | Pass: rejects external symlinks; builds four variants; repeated builds are byte-identical |
| Stable-installation regression | Pass: versioned copy, both variants, duplicate-install rejection, and checksum rejection |
| WorkBuddy quick validation | Pass for both source Skills in the recorded local host environment |
| Open-spec validation | Pass for both generated open-spec packages using the pinned `skills-ref` revision in CI |
| Whitespace validation | Pass with `git diff --check` |

Run the current deterministic suite from the repository root:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
git diff --check
```

The package release gate additionally requires a clean Git tree:

```bash
python3 scripts/package_skills.py dist --require-clean
```

Each manifest records `skill`, `version`, `variant`, `source_commit`, `source_dirty`, archive name, SHA-256, and exact file list. A valid release manifest must identify the tagged source commit and set `source_dirty` to `false`.

## Current Capability Decision

### Research Material Writer

Validated when explicitly invoked:

- primary-source research and dynamic-fact verification;
- fact, source claim, reproduced behavior, inference, conflict, and unknown separation;
- beginner tutorial, project analysis, comparison, and open-source onboarding modes;
- established-style continuation without inheriting stale facts;
- structural Markdown review with disclosed heuristic limits.

The checker does not prove factual accuracy, source quality, command correctness, or end-to-end success. Those remain manual evidence-review responsibilities.

### Workspace File Maintainer

Validated when explicitly invoked with disposable fixtures:

- create, exact read, precise modification, and continued iteration;
- no-op recognition and preservation of unrelated content;
- ambiguous replacement handling;
- missing/existing target handling;
- sensitive marker handling without reporting secret content;
- symlink escape rejection;
- personal-directory organization refusal;
- binary/Office routing;
- exact user-authorized outside-workspace target handling.

These results test instruction-following behavior and disk state; they do not turn the Skill into an operating-system sandbox.

## Distribution Compatibility

| Distribution | Current result | Boundary |
|---|---|---|
| WorkBuddy source/package | Pass in the recorded host-specific validation | Retains `agent_created: true`; other WorkBuddy builds are not implied |
| Open-spec package | Pass with pinned `skills-ref` structural validation | Removes only `agent_created`; client runtime behavior is not implied |
| Reproducibility | Pass | Same clean commit produces byte-identical ZIP, manifest, and aggregate `SHA256SUMS` files |
| Stable installation | Pass | Installer verifies SHA-256 and exact entries; activation remains host-specific |

The `allowed-tools` field remains experimental in the open Agent Skills specification. Structural validation does not guarantee tool pre-approval or identical runtime behavior across clients.

## Automatic Routing Evidence

Historical fresh-agent observations for `workspace-file-maintainer` recorded:

| Prompt type | Runs | Automatic loads |
|---|---:|---:|
| Create a local text file | 3 | 0 |
| Precisely modify a configuration file | 3 | 0 |
| Read an exact local text file | 1 | 0 |
| Unrelated negative prompts | 2 | 0 |

Relevant automatic load rate was `0/7`; negative false-positive rate was `0/2`. This is a historical host observation, not a general model benchmark.

`research-material-writer` has not completed a repeated fresh-host routing matrix. No precision, recall, false-positive rate, or stability claim is made for either Skill. Future routing claims require auditable host route/load events and repeated runs.

## Real-Project Narrative Evidence

The repository retains two explicit-invocation MarkItDown evaluations:

- [`real-project-markitdown-2026-10-30.md`](real-project-markitdown-2026-10-30.md): beginner tutorial workflow and controlled runtime checks.
- [`real-project-markitdown-onboarding-2026-10-31.md`](real-project-markitdown-onboarding-2026-10-31.md): onboarding decision workflow recorded as a separate historical artifact.

The first evaluation reproduced a pinned PyPI installation, `pip check`, CLI version output, controlled HTML conversion, and `convert_local()` behavior. It also preserved a PyPI-versus-GitHub Release version conflict instead of silently choosing one source.

These files are narrative evidence with their own recorded dates and source limitations. CI does not recreate their external network, package installation, or fresh-agent observations. Their source sections identify primary upstream locations, but they do not yet provide a per-claim citation anchor for every statement.

## Release Decision

The repository is suitable for a public preview pull request, not yet for a published tag.

A `v0.2.0-preview.1` release remains blocked until:

1. the release changes are reviewed by an independent write collaborator and merged into `main`;
2. hosted CI and GitHub-native failure-notification reachability pass on the publishing repository;
3. PVR, CODEOWNERS, the protected release environment, and the `main` and `v*` rulesets are configured and verified;
4. a clean 40-character `RELEASE_SHA` is frozen and the exact-SHA CI and commit verification are green;
5. a signed annotated tag is verified locally, in CI, and on GitHub and resolves exactly to `RELEASE_SHA`;
6. both distribution variants are regenerated from that exact tag commit and all four ZIP files, four manifests, and `SHA256SUMS` agree;
7. an independent verifier rechecks the public assets and no unresolved P0 or P1 release-path issue remains.

Automatic semantic routing is explicitly not a release guarantee for this preview.
