# Repo Anatomy Skill

Repo Anatomy Skill turns an unfamiliar repository into an evidence-backed technical deliverable, then applies approved local text changes through a separate conservative file-maintenance workflow.

The repository contains two composable Agent Skills. They can be used independently or in sequence, and the task contracts are not tied to one Agent, model provider, or client command.

## Choose The Right Skill

| Need | Skill | Typical input | Result | Primary boundary |
|---|---|---|---|---|
| Understand a repository, verify current facts, or write technical material | [`research-material-writer`](skills/research-material-writer/SKILL.md) | Repository URL, intended reader, goal, source material, or an existing draft | Project analysis, first-use guide, beginner tutorial, comparison, or evidence review | Does not invent commands, versions, benchmarks, compatibility, or successful execution |
| Create, read, or precisely update an authorized local text file | [`workspace-file-maintainer`](skills/workspace-file-maintainer/SKILL.md) | Exact file path, requested change, and acceptance condition | A minimal verified file change that preserves unrelated content | Does not delete, move, batch-organize, edit binary/Office files, or scan personal directories |
| Research first and save the approved result safely | Use both in sequence | Repository and writing goal, followed by an authorized output path | Evidence-backed content persisted with post-write verification | Research conclusions and filesystem authorization remain separate decisions |

Use `research-material-writer` when the difficult part is deciding what is true and how to explain it. Use `workspace-file-maintainer` when the difficult part is changing the correct file without widening scope. Use both when a researched deliverable must be written to disk.

## What The Skills Can Do

### Research Material Writer

- Research current technical projects and products from primary sources.
- Separate verified facts, source claims, reproduced behavior, inference, conflicts, recommendations, and unknowns.
- Produce repository analyses, first-use onboarding guides, beginner tutorials, and comparison or selection guides.
- Inspect project identity, governance, license, release source, prerequisites, minimum success path, permissions, security boundaries, support, maintenance, and rollback.
- Preserve an established writing voice while independently rechecking consequential claims.
- Run a deterministic Markdown warning check for repeated content, heading defects, unbalanced fences, and placeholders.

Best-fit problems include:

- "What does this repository actually do, and is it ready for my use case?"
- "Give a beginner one reliable path from installation to an observable first success."
- "Compare these tools using equivalent evidence and explain the trade-offs."
- "Review this technical draft for unsupported current facts and task-flow problems."

### Workspace File Maintainer

- Create, read, and precisely modify authorized local text, code, configuration, and Markdown files.
- Continue from current disk state instead of relying on stale conversation memory.
- Preserve unrelated content and existing repository conventions.
- Re-read each change, check for stale or duplicate content, and run relevant project validation when available.
- Stop on ambiguous matches, permission failures, concurrent changes, binary formats, sensitive paths, or symlink escape.

Best-fit problems include:

- "Create this exact Markdown file and verify its complete contents."
- "Change one configuration value without rewriting the rest of the file."
- "Continue the previous documentation edit from the current file state."
- "Apply the approved research result to this path and confirm the repository still validates."

## Use The Skills

These examples are capability contracts. Adapt their placeholders to the Agent Skills client you use. A client may expose Skills through explicit names, a Skill picker, or semantic discovery; explicit invocation is the verified path for this preview.

### Research A Repository

```text
Use the available repository-research Skill to inspect [repository URL] for [intended reader].
Produce [project analysis, first-use guide, tutorial, or comparison] that helps with [goal or decision].
Verify consequential claims from available primary evidence, label unknowns and unperformed checks, and define an observable success result.
```

### Maintain A Local Text File

```text
Use the local text-file maintenance Skill for [authorized path].
Apply [exact requested change] while preserving unrelated content and existing conventions.
Re-read the result, run [available validation or acceptance check], and report any unresolved risk.
```

### Research And Persist A Deliverable

```text
Research [repository URL or technical subject] for [intended reader] and produce [deliverable] for [goal].
Keep facts, source claims, reproduced behavior, inference, and recommendation distinct.
After the content is approved, use the file-maintenance Skill to write it to [authorized output path].
Apply the smallest file change, re-read the result, and report both factual and filesystem verification.
```

Do not freeze a project name, Agent name, model provider, installation path, or output schema into reusable task candidates. Put client-specific commands in a clearly labeled client subsection and keep the primary task contract portable.

## Basic Workflow

```text
Define the result and acceptance condition
  -> inspect primary evidence or current file state
  -> perform one focused research or edit task
  -> verify facts, commands, files, and observable results
  -> report limitations, blocked checks, and next decisions
```

For the combined path:

1. `research-material-writer` defines the reader, decision, research questions, and evidence ledger.
2. It selects the appropriate document mode and produces a task-oriented draft.
3. The user approves the content and exact destination.
4. `workspace-file-maintainer` inspects the current target and applies the smallest authorized change.
5. The result is re-read and checked with the repository's available validation commands.

Success is observable: research output states what was verified and what was not; file output exists at the intended path, contains the requested change exactly where expected, and leaves unrelated content intact.

## Install Or Integrate

The first public preview is being prepared. No stable public release assets are available yet. Source users and maintainers can clone and validate the repository now; release users should wait for the signed `v0.2.0-preview.1` pre-release and verify its manifests and `SHA256SUMS` before installation.

Each Skill will be distributed in two variants:

| Target | Asset | Difference | Runtime boundary |
|---|---|---|---|
| WorkBuddy AI | `<skill>-workbuddy.zip` | Retains the host-required `agent_created: true` field | Host-specific validation has been performed on macOS; installation and tool approval remain client-controlled |
| Agent Skills specification | `<skill>-open-spec.zip` | Removes only the WorkBuddy-specific field | Validated with pinned `skills-ref`; structural validation does not guarantee runtime behavior in every Agent client |

A compatible client is responsible for its own Skill installation path, activation behavior, tool approvals, network access, filesystem permissions, and sandboxing. The experimental `allowed-tools` field may be interpreted differently by different clients.

### Development From Source

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

For local WorkBuddy development, link the current checkout only after confirming that the destination paths do not already exist:

```bash
repo_root="$(pwd)"
ln -s "$repo_root/skills/workspace-file-maintainer" "$HOME/.workbuddy-ai/skills/workspace-file-maintainer"
ln -s "$repo_root/skills/research-material-writer" "$HOME/.workbuddy-ai/skills/research-material-writer"
```

This is a development installation. Uncommitted edits become immediately visible, so it must not be treated as a stable release installation.

## Status And Safety Boundary

This repository is preparing `v0.2.0-preview.1`, its first public preview. The candidate validates explicit Skill invocation, deterministic repository checks, safe reproducible packaging, and separate WorkBuddy/open-spec distribution. It does not claim stable automatic semantic routing.

- `workspace-file-maintainer` automatic loads: historical `0/7` relevant prompts.
- `research-material-writer` automatic routing: not yet measured in a repeated observable host matrix.
- Use explicit Skill invocation for development and acceptance testing.
- Agent instructions are not an operating-system sandbox and do not replace filesystem permissions, command approval, network controls, IAM, secret management, or host isolation.
- Out of scope includes fabricated technical claims, recursive cleanup, personal-directory organization, binary or Office editing, cloud-document editing, symlink escape, and credential access without exact task-specific authorization.

See [`evals/acceptance-results.md`](evals/acceptance-results.md) for the evidence ledger and [`RELEASE_NOTES_v0.2.0-preview.1.md`](RELEASE_NOTES_v0.2.0-preview.1.md) for preview limitations.

## Maintainer Workflow

Build both distribution variants from a clean revision:

```bash
python3 scripts/package_skills.py dist --require-clean
sha256sum -c dist/SHA256SUMS --strict
```

The release build produces four ZIP files, four manifest files, and one aggregate `SHA256SUMS`. The packager rejects symlinks and non-regular files, fixes ZIP metadata for reproducibility, and records each Skill version, variant, source commit, dirty-tree state, exact package file list, archive filename, and SHA-256.

Run the deterministic suite before opening or updating a pull request:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
git diff --check
```

Development rules:

1. Add or update an evaluation before changing observable behavior.
2. Edit one Skill or one referenced rule at a time.
3. Keep researched writing quality separate from file persistence behavior.
4. Update the affected Skill version and [`CHANGELOG.md`](CHANGELOG.md) when behavior or package contracts change.
5. Package only a clean, reviewed, exact revision for release.
6. Follow [`COLLABORATION.md`](COLLABORATION.md) for PR review and [`RELEASING.md`](RELEASING.md) for release gates.

## Repository Layout

| Path | Purpose |
|---|---|
| [`skills/`](skills/) | Source Skills and their progressively disclosed references. |
| [`evals/`](evals/) | Trigger datasets, functional cases, and real-project acceptance evidence. |
| [`tests/`](tests/) | Repository, validator, draft-checker, packaging, and installation regressions. |
| [`scripts/package_skills.py`](scripts/package_skills.py) | Safe reproducible WorkBuddy/open-spec packager. |
| [`scripts/install_stable.py`](scripts/install_stable.py) | Manifest-verified versioned installer. |
| [`.github/`](.github/) | CI, release workflows, issue forms, ownership, and pull-request templates. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Development and evidence requirements. |
| [`COLLABORATION.md`](COLLABORATION.md) | Pull Request, review, approval, merge, branch, and exception rules. |
| [`SECURITY.md`](SECURITY.md) | Private reporting route and security boundaries. |
| [`RELEASING.md`](RELEASING.md) | Versioning, release gates, asset verification, publication, and rollback. |
| [`SOURCES.md`](SOURCES.md) | Design references, adopted practices, and non-adopted patterns. |

`dist/` contains generated packages and is intentionally ignored by Git.

## Help And Governance

- Usage or compatibility question: open a GitHub issue with the target Agent client, operating system, Skill version, task, and observed result.
- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Collaboration standard: [`COLLABORATION.md`](COLLABORATION.md)
- Security reports: [`SECURITY.md`](SECURITY.md)
- Community conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- Release process: [`RELEASING.md`](RELEASING.md)
- Design references and attribution: [`SOURCES.md`](SOURCES.md)

## License

Copyright (c) 2026 Veretex. Released under the [MIT License](LICENSE). External projects and standards referenced by this repository retain their own licenses; see [`SOURCES.md`](SOURCES.md).
