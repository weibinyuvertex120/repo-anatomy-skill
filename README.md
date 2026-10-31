# Repo Anatomy Skill

A cross-host Agent Skills repository for evidence-driven repository research, technical writing, and conservative local text-file maintenance.

The repository contains two cooperating Skills rather than one oversized workflow:

| Skill | Responsibility | Use it when |
|---|---|---|
| [`research-material-writer`](skills/research-material-writer/SKILL.md) | Research, verify, structure, draft, and review technical material | You need a repository analysis, beginner tutorial, first-use onboarding guide, or comparison based on current sources |
| [`workspace-file-maintainer`](skills/workspace-file-maintainer/SKILL.md) | Inspect, apply the smallest authorized text change, re-read, and verify | You need to create, read, or precisely modify local text files without widening filesystem scope |

The project name describes the primary workflow: understand the anatomy of an unfamiliar repository before recommending, documenting, or changing it. File persistence remains a separate safety layer.

## Task Example

Start with a repository and the result you need. For example:

```text
Research [GitHub repository URL] for [intended reader]. Help me [goal or decision].
I need a [project analysis, first-use guide, or technical tutorial].
Make important claims traceable to available project evidence, and mark anything you could not verify.
```

Replace the bracketed parts with your project and task. Choose the deliverable that fits your goal; the example is a starting point, not a fixed prompt or required output format.

## Status And Evidence Boundary

This repository is preparing its first public preview. The current candidate validates explicit Skill invocation, deterministic repository checks, safe packaging, and WorkBuddy/open-spec distribution. It does not claim stable automatic semantic routing.

- `workspace-file-maintainer` automatic loads: historical `0/7` relevant prompts.
- `research-material-writer` automatic routing: not yet measured in a repeated observable host matrix.
- Use explicit Skill invocation for development and acceptance testing.
- Agent instructions are not an operating-system sandbox and do not replace filesystem permissions, command approval, network controls, IAM, or secret management.

See [`evals/acceptance-results.md`](evals/acceptance-results.md) for the evidence ledger and [`RELEASE_NOTES_v0.2.0-preview.1.md`](RELEASE_NOTES_v0.2.0-preview.1.md) for preview limitations.

## Quick Start

### 1. Clone And Validate

Python 3.11 and 3.13 are exercised in CI. Run all commands from the repository root.

```bash
git clone https://github.com/weibinyuvertex120/repo-anatomy-skill.git
cd repo-anatomy-skill
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
```

Expected result: every command exits with status 0 and reports that its validation or regression suite passed.

### 2. Build Both Distribution Variants

```bash
python3 scripts/package_skills.py dist
```

Each Skill produces:

- `<skill>-workbuddy.zip` and its `.manifest.json`;
- `<skill>-open-spec.zip` and its `.manifest.json`.

The packager rejects symlinks and non-regular files, fixes ZIP metadata for reproducible output, and records the version, variant, source commit, dirty-tree state, exact file list, and SHA-256.

### 3. Install A Verified WorkBuddy Copy

Stable installation uses a versioned copy rather than a development symlink:

```bash
for skill in workspace-file-maintainer research-material-writer; do
  python3 scripts/install_stable.py \
    "dist/${skill}-workbuddy.zip" \
    "dist/${skill}-workbuddy.manifest.json" \
    "$HOME/.workbuddy-ai/stable-skills" \
    --variant workbuddy
done
```

The installer verifies SHA-256 and the exact archive file list, rejects an existing target, and writes `.install-receipt.json`. It does not change the currently active Skill link. Keep the previous versioned directory for rollback.

For another Agent Skills client, use the `open-spec` archive only after checking that client's installation path, supported frontmatter, and tool-approval behavior. Structural validation does not guarantee runtime compatibility.

## What The Skills Cover

`research-material-writer` can:

- research current technical projects and products from primary sources;
- distinguish verified facts, source claims, reproduced behavior, inference, conflicts, and unknowns;
- write beginner tutorials, repository onboarding assessments, project analyses, and comparison guides;
- inspect repository identity, governance, license, release source, prerequisites, minimum success path, Agent context files, permissions, security boundaries, and maintenance entry points;
- preserve an established series voice while independently rechecking facts;
- run a deterministic Markdown structure check for repeated content, heading defects, unbalanced fences, and placeholders.

`workspace-file-maintainer` can:

- create, read, and precisely modify authorized local text files;
- continue from current disk state and preserve unrelated content;
- reject ambiguous, destructive, binary, secret-oriented, or personal-directory organization requests outside its documented boundary;
- re-read and verify every write.

Out of scope includes generic unresearched marketing copy, fabricated commands or benchmarks, recursive cleanup, personal-directory organization, binary or Office editing, cloud-document editing, symlink escape, and credential access without exact task-specific authorization.

## Repository Layout

| Path | Purpose |
|---|---|
| [`skills/`](skills/) | Source Skills. Detailed rules remain one reference link from each `SKILL.md`. |
| [`evals/`](evals/) | Trigger datasets, functional cases, and real-project acceptance evidence. |
| [`tests/`](tests/) | Repository, validator, draft-checker, packaging, and installation regressions. |
| [`scripts/package_skills.py`](scripts/package_skills.py) | Safe reproducible WorkBuddy/open-spec packager. |
| [`scripts/install_stable.py`](scripts/install_stable.py) | Manifest-verified versioned installer. |
| [`.github/`](.github/) | CI, issue forms, pull-request template, and vulnerability report template. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Development and evidence requirements. |
| [`COLLABORATION.md`](COLLABORATION.md) | Pull Request, review, approval, merge, branch, and exception rules. |
| [`SECURITY.md`](SECURITY.md) | Private reporting route and security boundaries. |
| [`RELEASING.md`](RELEASING.md) | GitHub Flow, versioning, release gates, and rollback. |
| [`SOURCES.md`](SOURCES.md) | Design references, adopted practices, and non-adopted patterns. |

`dist/` contains generated packages and is intentionally ignored by Git.

## Compatibility

| Target | Package | Validation | Current boundary |
|---|---|---|---|
| WorkBuddy AI | `-workbuddy.zip` | Repository tests plus WorkBuddy `quick_validate.py` | Retains required `agent_created: true`; runtime validation performed on macOS |
| Open Agent Skills | `-open-spec.zip` | Pinned `skills-ref` in CI | Removes only `agent_created`; runtime behavior depends on the client |
| Python | Test and packaging scripts | CI on 3.11 and 3.13 | Other versions are not a release claim |
| Operating systems | Skill instructions | Deterministic CI on Ubuntu; host-specific validation on macOS | Windows runtime behavior is not yet verified |

The open Agent Skills `allowed-tools` field is experimental. Tool pre-approval can differ by client even when a package validates structurally.

## Validation

Run the deterministic suite from the repository root:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
git diff --check
```

WorkBuddy maintainers can additionally run its bundled host validator:

```bash
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" skills/workspace-file-maintainer
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" skills/research-material-writer
```

Open-spec packages are validated in CI against a pinned `skills-ref` revision. Do not substitute structural validation for an end-to-end client test.

## Development Workflow

1. Add or update an evaluation before changing observable behavior.
2. Edit one Skill or one referenced rule at a time.
3. Run all deterministic regression tests.
4. Test obvious, paraphrased, boundary, competing, and negative prompts in a fresh observable host when routing behavior changes.
5. Test researched writing quality separately from file persistence behavior.
6. Update the affected Skill version and [`CHANGELOG.md`](CHANGELOG.md) when behavior or package contracts change.
7. Package only a clean, validated revision for release.

For local WorkBuddy development, clone the repository and link from the current checkout rather than using a maintainer-specific absolute path:

```bash
repo_root="$(pwd)"
ln -s "$repo_root/skills/workspace-file-maintainer" "$HOME/.workbuddy-ai/skills/workspace-file-maintainer"
ln -s "$repo_root/skills/research-material-writer" "$HOME/.workbuddy-ai/skills/research-material-writer"
```

This is a development installation: uncommitted edits become immediately visible. Do not replace an existing path blindly, and do not use a development symlink as a stable release installation.

## Project Governance

- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security reports: [`SECURITY.md`](SECURITY.md)
- Community conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- Release process: [`RELEASING.md`](RELEASING.md)
- Design references and attribution: [`SOURCES.md`](SOURCES.md)

## License

Copyright (c) 2026 Veretex. Released under the [MIT License](LICENSE). External projects and standards referenced by this repository retain their own licenses; see [`SOURCES.md`](SOURCES.md).
