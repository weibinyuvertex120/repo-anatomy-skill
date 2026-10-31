# Real Repository Walkthrough: Microsoft MarkItDown

This walkthrough shows how `research-material-writer` handles a real repository. It records the input, research path, evidence, conclusions, and final deliverable rather than presenting a fictional prompt.

- Repository: [`microsoft/markitdown`](https://github.com/microsoft/markitdown)
- Analysis mode: open-source project analysis with first-use verification
- Verification date: 2026-10-31
- Skill invocation: explicit

## Input

```text
Use research-material-writer to analyze https://github.com/microsoft/markitdown for a developer who is evaluating it for a document-to-Markdown preprocessing workflow.

Explain what the project does, how the repository is organized, the shortest safe path to a working result, and the main adoption risks. Verify current versions and consequential claims from primary sources. Separate documented capabilities from behavior reproduced locally, and state what was not tested.
```

The requested result is a decision-ready repository analysis, not a rewrite of the upstream README.

## Analysis process

The Skill turned the request into five questions:

1. What problem does MarkItDown solve, and what kind of output is it designed to produce?
2. Which installation source, Python range, license, and release should a new user rely on?
3. How is the repository divided, and where are the CLI, library, plugins, and integrations represented?
4. What is the smallest controlled test that demonstrates useful behavior?
5. Which security and quality limits affect adoption?

It then checked the following primary evidence:

| Evidence | What it established |
|---|---|
| Official repository README | Intended use, supported input categories, CLI and Python entry points, optional dependencies, plugin behavior, and security guidance |
| `packages/markitdown/pyproject.toml` | Package identity, Python range, MIT license, Beta classifier, dependencies, optional feature groups, and CLI entry point |
| GitHub Releases | `v0.1.9` is an official non-prerelease release published on 2026-10-21 |
| PyPI JSON metadata | Package `0.1.9`, Python `>=3.10,<3.15`, release files, and publication time |
| Repository tree | Separate packages for the core library, MCP server, OCR plugin, and sample plugin |
| `DocumentConverter` source | Converter selection and conversion are represented by `accepts()` and `convert()` contracts; results expose Markdown and an optional title |
| `LICENSE` and `SECURITY.md` | MIT terms and Microsoft's private vulnerability-reporting route |
| Disposable local environment | Whether the pinned core package installs, reports its version, has consistent dependencies, and converts a controlled HTML fixture |

Claims were classified before drafting:

- **Verified fact:** directly supported by current repository, release, or package metadata.
- **Reproduced behavior:** observed in the isolated test described below.
- **Source claim:** documented by MarkItDown but not reproduced in this walkthrough.
- **Inference or recommendation:** an adoption judgment based on the verified facts.
- **Unknown:** not established by the inspected evidence.

## Key findings

### Project position

MarkItDown is a Python utility for turning documents and other supported inputs into Markdown for LLM and text-analysis pipelines. Its stated priority is preserving useful structure such as headings, lists, tables, and links. The project explicitly says that the output is not intended to be a high-fidelity visual document conversion.

This makes it a reasonable candidate for search indexing, retrieval preparation, content inspection, and other machine-oriented text workflows. It is not evidence that layout-sensitive publishing or archival conversion requirements will be met.

### Current package and repository shape

At the verification date:

- the official GitHub Release and PyPI package both identify version `0.1.9`;
- the package requires Python `>=3.10,<3.15`;
- package metadata classifies it as Beta;
- the core package is MIT-licensed;
- optional dependencies are grouped by formats and integrations rather than forced into the minimum install;
- third-party plugins are supported but disabled by default.

The repository is a small multi-package project:

```text
packages/
  markitdown/               core library and CLI
  markitdown-mcp/           MCP integration
  markitdown-ocr/           OCR plugin
  markitdown-sample-plugin/ plugin development example
```

Within the core package, `__main__.py` provides the command-line entry, `_markitdown.py` contains the main orchestration layer, and converter modules implement format-specific handling. The base converter contract returns a `DocumentConverterResult` containing Markdown and an optional title.

### Reproduced minimum path

A fresh temporary virtual environment was created with the host's Python 3.13 interpreter. The test installed only the pinned core package:

```bash
python3 -m venv .venv
.venv/bin/pip install "markitdown==0.1.9"
```

The fixture contained one heading, link, list, and table. It was converted with the narrower local-file API:

```python
from markitdown import MarkItDown

result = MarkItDown().convert_local("sample.html")
print(result.markdown)
```

Observed output:

```markdown
# Quarterly Notes

See [source](https://example.com).

* Revenue
* Risk

| Item | Value |
| --- | --- |
| Status | Reviewed |
```

The same environment reported:

```text
markitdown 0.1.9
No broken requirements found.
```

This verifies installation, package identity, dependency consistency, and HTML conversion for one controlled fixture. It does not verify every supported format or deployment mode.

### Security boundary

MarkItDown performs I/O with the permissions of its current process. Its own guidance recommends validating untrusted input and calling the narrowest applicable method, such as `convert_local()` or `convert_stream()`, instead of assuming the general `convert()` entry point is harmless.

For a first evaluation, the bounded path is therefore:

1. use a disposable virtual environment;
2. pin the package version;
3. begin with a trusted local fixture;
4. avoid arbitrary URLs, user uploads, plugins, cloud credentials, and production data;
5. inspect generated Markdown before expanding the workflow.

## Final output

**Decision:** suitable for a controlled trial in machine-oriented document preprocessing.

**Why:** the project has a clear scope, an official package and release at the same current version, a permissive core license, explicit Python requirements, narrow local conversion APIs, and a locally reproduced path from HTML to structured Markdown.

**Conditions:** pin the version, install only the optional groups required by the target formats, keep the first tests local, and add regression fixtures for the actual documents the workflow depends on.

**Do not infer:** the walkthrough does not establish high-fidelity rendering, safe handling of hostile input, production readiness for an unrestricted upload service, or equal conversion quality across all documented formats.

**Recommended next test:** select one representative document for each required format, define the structure that must survive conversion, and compare output across a pinned upgrade before adopting the tool in a production pipeline.

## What was not tested

This walkthrough did not reproduce PDF, Word, PowerPoint, Excel, OCR, audio, YouTube, ZIP, third-party plugin, MCP, Azure Document Intelligence, or Azure Content Understanding behavior. It did not test hostile files, unrestricted remote URLs, resource exhaustion, conversion fidelity at scale, or production deployment controls.

Those remain separate evaluation tasks. The official README documents many of these capabilities, but a documented capability is not reported here as reproduced behavior.

## Sources

- [Microsoft MarkItDown repository and README](https://github.com/microsoft/markitdown)
- [Core package configuration](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/pyproject.toml)
- [GitHub Release v0.1.9](https://github.com/microsoft/markitdown/releases/tag/v0.1.9)
- [PyPI project](https://pypi.org/project/markitdown/0.1.9/)
- [MIT License](https://github.com/microsoft/markitdown/blob/main/LICENSE)
- [Security policy](https://github.com/microsoft/markitdown/blob/main/SECURITY.md)
