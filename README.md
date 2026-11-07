<a id="top"></a>

# Repo Anatomy Skill

<p align="right"><strong>English</strong> · <a href="README.zh-CN.md#top"><kbd>简体中文</kbd></a></p>

`Repo Anatomy Skill` helps an Agent research an unfamiliar software project and turn verified evidence into clear, practical technical material.

The current project focuses on [`research-material-writer`](skills/research-material-writer/SKILL.md).

<a id="what-it-does"></a>

## What It Does

[简体中文](README.zh-CN.md#what-it-does)

`research-material-writer` can:

- analyze an arbitrary software project, repository, library, tool, or service;
- route the research through a primary project type: CLI/local tool, library/SDK, API/hosted service, plugin/extension, Agent Skill/MCP integration, model, dataset/resource collection, or deployable service application;
- verify important facts from primary sources such as official documentation, repositories, release pages, source code, specifications, manifests, model or data cards, and package metadata;
- build an **understanding map** of the problem, input, processing, output, core components, flow, responsibility boundary, and first observable success;
- build a **practice path** with one recommended setup route, step-level expected observations, failure signals, recovery, boundary verification, and cleanup;
- test practical understanding through orientation, boundary, and transfer tasks instead of treating a copied example as independent use;
- support a complete one-shot guide or a staged **guided run** that waits for the user's actual result before continuing;
- produce a project analysis, onboarding guide, beginner tutorial, or comparison guide;
- distinguish verified facts, project claims, reproduced behavior, inferences, recommendations, conflicts, and unknowns;
- record completed, partially completed, blocked, and not-verified outcomes plus structured user feedback when persistence is requested and allowed;
- review a technical draft for unsupported current claims, broken task flow, structural problems, and inconsistent terminology.

The Skill organizes research around the reader's decision and working path. It does not simply reproduce a project's README or claim that a reader succeeded without observed evidence.

<a id="quick-start"></a>

## Quick Start

[简体中文](README.zh-CN.md#quick-start)

Clone the repository and inspect the Skill:

```bash
git clone https://github.com/weibinyuvertex120/repo-anatomy-skill.git
cd repo-anatomy-skill
sed -n '1,220p' skills/research-material-writer/SKILL.md
```

For a local WorkBuddy-compatible installation, link the Skill into the user Skill directory:

```bash
set -e
mkdir -p "$HOME/.workbuddy-ai/skills"
test ! -e "$HOME/.workbuddy-ai/skills/research-material-writer"
ln -s "$PWD/skills/research-material-writer" \
  "$HOME/.workbuddy-ai/skills/research-material-writer"
```

Start a new Agent session after installation, then explicitly ask the Agent to use the Skill. A general research request can use this pattern:

```text
Use research-material-writer to analyze [repository URL] for [intended reader].

Explain what the project does, how its repository is organized, the shortest practical path to first use, and the main adoption considerations. Verify important claims from primary sources, separate documented capabilities from behavior reproduced during the research, and include sources and observable verification steps.
```

To research a specific decision, make the reader and goal explicit:

```text
Use research-material-writer to compare [Project A] and [Project B] for [workflow].

Define the comparison criteria first. Use equivalent evidence and versions where possible, explain the trade-offs by scenario, and identify which conclusions were verified, reproduced, or inferred.
```

To help a reader understand and actually try a project:

```text
Use research-material-writer to analyze [project URL] for [reader and target task].

First classify the primary project type. Build a compact understanding map of its input, processing, output, components, workflow position, and responsibility boundary. Then give one safe practice path with expected observations, failure signals, cleanup, one boundary check, and one transfer task that changes the original example. Separate documented behavior, locally reproduced behavior, user-reported results, and unverified steps.
```

For staged assistance instead of a long one-shot tutorial:

```text
Use research-material-writer in guided-run mode for [project and target task].

Give me only the next bounded stage. Start with the brief and preflight, wait for my actual output or error, then diagnose the smallest correction. Do not continue past a blocking result or claim that I completed a step without evidence. End with orientation, boundary, transfer, and adoption checks.
```

The portable core does not grant network, shell, filesystem, credential, memory, or tracing access. A host adapter must expose those capabilities, and unavailable checks remain explicit. The deterministic repository tests validate the contract and package consistency; they do not prove real-reader understanding or host behavior. The `evals/copilot-readonly-*` assets and manual run templates retain their recorded historical core/adapter identities and are evidence fixtures, not a runtime conclusion for the current adapter.

<a id="verified-example"></a>

## Verified Example: MarkItDown

[简体中文](README.zh-CN.md#verified-example)

The repository includes a source-linked walkthrough for [`microsoft/markitdown`](https://github.com/microsoft/markitdown):

- [`demos/markitdown-repository-analysis.md`](demos/markitdown-repository-analysis.md)

The example asked the Skill to evaluate MarkItDown for a document-to-Markdown preprocessing workflow. The research:

- identified the project's purpose and intended output;
- mapped the multi-package repository structure;
- checked the official package configuration, release information, license, and security guidance;
- selected a pinned installation path in a disposable Python environment;
- reproduced conversion of a controlled HTML fixture through `convert_local()`;
- checked the package version and dependency state;
- separated local execution results from capabilities described only by project documentation;
- ended with a conditional adoption recommendation and a concrete next test.

The same workflow is recorded in the related evaluation notes:

- [`evals/real-project-markitdown-2026-10-30.md`](evals/real-project-markitdown-2026-10-30.md)
- [`evals/real-project-markitdown-onboarding-2026-10-31.md`](evals/real-project-markitdown-onboarding-2026-10-31.md)

<a id="validation"></a>

## Validate the Repository

[简体中文](README.zh-CN.md#validation)

Run the repository checks from the project root:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_readme_languages.py
python3 tests/test_draft_checker.py
python3 tests/test_project_learning_contract.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
```

The bundled draft checker can review a Markdown result for structural issues:

```bash
python3 skills/research-material-writer/scripts/check_draft.py path/to/draft.md
```

<a id="project-layout"></a>

## Project Layout

[简体中文](README.zh-CN.md#project-layout)

```text
skills/research-material-writer/       Skill definition and research/learning references
demos/                                 Source-linked research walkthroughs
evals/                                 Functional, type-learning, and feedback contracts
tests/                                 Repository, learning-contract, and packaging checks
docs/                                  Host and compatibility documentation
```

<a id="license"></a>

## License

[简体中文](README.zh-CN.md#license)

Copyright (c) 2026 Veretex. Released under the [MIT License](LICENSE).
