# Repo Anatomy Skill

Repo Anatomy Skill helps an Agent turn an unfamiliar open-source repository into an evidence-backed project analysis, first-use guide, or technical tutorial.

## Current preview scope

The current preview is focused on [`research-material-writer`](skills/research-material-writer/SKILL.md). It is the only Skill in the new release scope: it researches current technical facts and produces task-oriented material for an arbitrary project. The portable core is designed for Codex, 豆包 and other Agent hosts, but host behavior remains separately verified.

[`workspace-file-maintainer`](skills/workspace-file-maintainer/SKILL.md) remains in the repository as a paused, separately validated Skill and historical reference. It is not part of the current preview's implementation promise or default release assets. Do not treat the two Skills as a combined first-version workflow.

The research task contract does not depend on one Agent, model provider, or client command. A host is responsible for discovery, explicit loading, permissions, source access, and output delivery.

## Real repository walkthrough

The included walkthrough analyzes [`microsoft/markitdown`](https://github.com/microsoft/markitdown) from a developer's evaluation request. It records the input, evidence path, local verification, conclusions, and untested areas.

**Input**

```text
Use research-material-writer to analyze https://github.com/microsoft/markitdown for a developer who is evaluating it for a document-to-Markdown preprocessing workflow.

Explain what the project does, how the repository is organized, the shortest safe path to a working result, and the main adoption risks. Verify current versions and consequential claims from primary sources. Separate documented capabilities from behavior reproduced locally, and state what was not tested.
```

**Analysis**

The Skill checked the official README, package configuration, GitHub Releases, PyPI metadata, repository tree, converter contract, license, and security policy. It classified each consequential statement as a verified fact, reproduced behavior, source claim, recommendation, or unknown.

A disposable Python 3.13 environment was then used to install `markitdown==0.1.9` and convert a controlled HTML fixture with `convert_local()`. The output retained the tested heading, link, list, and table; `markitdown --version` returned `0.1.9`, and `pip check` reported no broken requirements.

**Conclusion**

MarkItDown is a reasonable candidate for a controlled trial in machine-oriented document preprocessing. The walkthrough does not treat that result as proof of high-fidelity rendering, hostile-input safety, production readiness for unrestricted uploads, or equal quality across every documented format.

Read the complete, source-linked result in [`demos/markitdown-repository-analysis.md`](demos/markitdown-repository-analysis.md).

## What it does

### Research a repository

`research-material-writer` is for work where the difficult part is deciding what is true and how to explain it. It can:

- verify project identity, versions, installation paths, runtime requirements, license, governance, and security guidance from primary sources;
- separate verified facts, project claims, reproduced behavior, inference, recommendations, conflicts, and unknowns;
- produce a project analysis, first-use onboarding guide, beginner tutorial, or comparison guide;
- define one observable path to a working result and state which checks were not performed;
- review an existing technical draft for unsupported current claims and broken task flow.

It does not invent commands, compatibility, benchmarks, or successful execution. Repository popularity is not treated as evidence of reliability or production suitability.

### Maintain a local text file

`workspace-file-maintainer` handles the persistence step after the content and destination are clear. It can:

- create, read, or precisely modify an authorized local text, code, configuration, or Markdown file;
- continue from the current disk state and preserve unrelated content;
- re-read changes and run available project validation;
- stop on ambiguous edits, sensitive paths, binary formats, permission failures, concurrent changes, or symlink escape.

Deletion, moving, batch cleanup, personal-directory organization, Office or other binary editing, cloud-document editing, and unrestricted secret access are outside its scope.

## When to use it

Use `research-material-writer` when you need to understand an unfamiliar repository, decide whether it fits a workflow, help a beginner reach a first success, compare projects on equivalent evidence, or turn primary sources into a technical document.

Use `workspace-file-maintainer` when the content is already decided and the task is to make a small, verifiable local text change.

Use both when a researched deliverable needs to be written into a repository without mixing factual judgment with filesystem authorization.

## Basic usage

Explicit invocation is the verified path for the current preview. Adapt the wording to the Agent Skills client you use.

Research a repository:

```text
Use the available repository-research Skill to inspect [repository URL] for [intended reader].
Produce [project analysis, first-use guide, tutorial, or comparison] for [goal or decision].
Verify consequential claims from primary sources, distinguish reproduced behavior from source claims, and state unknowns and unperformed checks.
```

Maintain a local file:

```text
Use the local text-file maintenance Skill for [authorized path].
Apply [exact change] while preserving unrelated content and existing conventions.
Re-read the result, run [available validation], and report any unresolved risk.
```

Combined workflow:

```text
Research [repository URL] for [reader and decision], then prepare [deliverable].
After the content and destination are approved, write it to [authorized path] with the file-maintenance Skill.
Verify both the technical claims and the final file state.
```

A compatible client remains responsible for Skill discovery, installation paths, command approval, network access, filesystem permissions, and sandboxing. Agent instructions do not replace operating-system security controls.

## Install and validate

The historical public evaluation release `v0.2.0-preview.2` is available from [GitHub Releases](https://github.com/weibinyuvertex120/repo-anatomy-skill/releases/tag/v0.2.0-preview.2). It contains the earlier two-Skill asset set and must not be confused with the current research-only preview. The current candidate is `research-material-writer` `0.3.0-preview.1`; its release scope is limited to WorkBuddy and open-spec packages for that Skill. To inspect the source and run the deterministic checks:

```bash
git clone https://github.com/weibinyuvertex120/repo-anatomy-skill.git
cd repo-anatomy-skill
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
```

For local WorkBuddy development, link only the research Skill after confirming that the destination does not already exist:

```bash
repo_root="$(pwd)"
ln -s "$repo_root/skills/research-material-writer" "$HOME/.workbuddy-ai/skills/research-material-writer"
```

This development setup exposes uncommitted edits immediately. It is not a stable installation method. The paused file-maintenance Skill is not installed by the current preview instructions.

The current candidate provides separate WorkBuddy and open-spec archives for `research-material-writer`. The open-spec variant uses the portable core without WorkBuddy-only fields. Package manifests and `SHA256SUMS` are generated by the repository release process. Verify all downloaded assets from one directory with `sha256sum -c SHA256SUMS --strict` before installation.

## Current limits

- Explicit Skill invocation is tested; stable automatic semantic routing is not yet claimed.
- The Markdown checker catches structural warnings but cannot prove factual accuracy or source quality.
- Cross-client behavior can differ; the portable core does not grant source, network, execution, filesystem, or credential access.
- Codex and 豆包 host installation, discovery, explicit loading, and runtime behavior require host-version-specific evidence; the current matrix does not claim those runs are complete.
- Research output states the evidence and verification scope; it does not turn a limited reproduction into a general guarantee.
- `workspace-file-maintainer` is paused and is not part of the current preview release scope.

Evaluation evidence is recorded in [`evals/acceptance-results.md`](evals/acceptance-results.md). Historical release limits and asset details are in [`RELEASE_NOTES_v0.2.0-preview.1.md`](RELEASE_NOTES_v0.2.0-preview.1.md); that file documents the earlier two-Skill candidate, while the current candidate is research-only.

## Development

- Contribution requirements: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Pull Request and review rules: [`COLLABORATION.md`](COLLABORATION.md)
- Security reports: [`SECURITY.md`](SECURITY.md)
- Release process: [`RELEASING.md`](RELEASING.md)
- Design sources and attribution: [`SOURCES.md`](SOURCES.md)

## License

Copyright (c) 2026 Veretex. Released under the [MIT License](LICENSE). Referenced projects retain their own licenses.
