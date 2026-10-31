# 真实项目验收：MarkItDown 开源项目首次使用

Verification date (UTC): 2026-10-31
Skill: `research-material-writer` 0.2.0
Invocation: explicit
Automatic semantic trigger matrix: deferred until after open-source publication

## 验收任务

Research an unfamiliar open-source project and produce a first-use onboarding assessment for a beginner. The assessment must answer what to prepare before first use, whether the project is ready to try, how to reach one controlled success result, which risks and permissions matter, how an Agent should be introduced, and when to stop or defer adoption.

Selected project: `microsoft/markitdown`

This is a separate onboarding evaluation from the earlier tutorial acceptance. It reuses verified runtime evidence where relevant but evaluates the new onboarding workflow and decision gates.

## 主要证据

- Official GitHub repository and README.
- Official `packages/markitdown/pyproject.toml`.
- Official `LICENSE` and `SECURITY.md`.
- Official GitHub Releases page.
- Official PyPI project metadata.
- Repository contribution, test, and plugin documentation.
- Local disposable virtual-environment execution from the prior real-project acceptance.

## Onboarding 事实账本摘要

| Claim | Evidence | Class | Verification |
|---|---|---|---|
| MarkItDown converts files and office documents to Markdown for LLM and text-analysis workflows | Official README | source claim | 2026-10-31 |
| Python requirement is `>=3.10,<3.15` | PyPI metadata and official `pyproject.toml` | verified fact | 2026-10-31 |
| License is MIT | official `LICENSE` and package metadata | verified fact | 2026-10-31 |
| Package status is Beta | PyPI classifiers | verified fact | 2026-10-31 |
| PyPI exposes `0.1.9` while the inspected GitHub Releases page exposes `v0.1.3` | official PyPI and GitHub sources | verified source conflict | 2026-10-31 |
| The project warns that conversion runs with the current process I/O permissions and that untrusted input needs path, URI, network, and cloud-metadata restrictions | official README security guidance | source claim | 2026-10-31 |
| `convert_local()` is the narrower first-use API for a local trusted file; broader conversion entry points require more careful input control | official README and API documentation | source claim | 2026-10-31 |
| The controlled HTML conversion succeeded with the pinned PyPI package and `[all]` environment | local disposable environment | reproduced fact | 2026-10-30 |
| The repository contained no Agent instruction file visible in the inspected page excerpt | partial page inspection only | unknown, not a negative finding | 2026-10-31 |

## 首次使用准备清单

### 项目与采用决策

- Project identity and maintainer are clear: `microsoft/markitdown`.
- The first-use target is narrow: convert one trusted local HTML or text-like document to Markdown.
- It is suitable for a controlled local trial and for machine-oriented document preprocessing.
- It should not be presented as a high-fidelity visual conversion tool or as proof that all supported formats work in the target environment.
- The package's Beta status is a reason to pin the version and keep a rollback path.

### 运行环境

- Python 3.10 through 3.14 is required by the inspected package metadata.
- A disposable virtual environment is the primary preparation recommendation.
- Install only the optional dependency groups needed for the target format; `[all]` was used for the earlier broad acceptance test, not as a universal recommendation.
- The first test uses a local trusted fixture and does not require a cloud account, API key, or remote URL.

### 信任与安全

- Inspect `LICENSE` before redistribution or embedding in a product.
- Read the repository security guidance before passing user-controlled files or URLs.
- Do not begin with untrusted uploads, arbitrary remote URLs, cloud metadata addresses, or server-side conversion of unrestricted user input.
- Keep secrets and production data outside the first test directory.
- If used through an Agent, begin with a read-only inventory and a controlled local fixture. Do not enable broad auto-approval, unrestricted shell, or unnecessary network access.

### 安装来源

- Use the official PyPI project name only after matching it to the official repository.
- Pin the tested version in the onboarding record or project lock configuration.
- Record the channel difference between PyPI and GitHub Releases instead of silently calling one source "latest".
- Treat third-party wrappers, copied install scripts, and unverified mirrors as outside the primary path.

## 最短成功路径

The accepted beginner path is:

1. Create a disposable directory and Python virtual environment.
2. Install the pinned package from the official PyPI project.
3. Create a small trusted HTML fixture.
4. Run the CLI or `convert_local()` against that fixture.
5. Verify that the generated Markdown contains the expected heading, link, list, and table structure.
6. Run `pip check` and record the package version.

This path intentionally excludes remote URLs, OCR, audio transcription, third-party plugins, Azure services, and untrusted input. Those are separate adoption decisions.

## 可观察验证

| Layer | Verification | Result |
|---|---|---|
| Existence | `markitdown --version` | Returned `markitdown 0.1.9` in the disposable environment |
| Dependency health | `pip check` | Returned `No broken requirements found` |
| Functionality | CLI conversion of a controlled HTML fixture | Passed; expected Markdown structure was present |
| API path | `MarkItDown().convert_local()` | Passed; returned `DocumentConverterResult` with expected content |
| Boundary | Security and untrusted-input guidance review | Confirmed as a documented constraint; hostile-input behavior was not independently tested |

The local results are execution evidence for the tested package and fixture only. They do not prove every converter, plugin, or deployment mode works.

## Agent 接入准备

Before allowing an Agent to modify a repository or process a batch of files, use a first prompt with a bounded read-only task:

```text
请先只读分析当前 MarkItDown 使用目录：
1. 说明目标输入、输出和当前安装版本；
2. 检查项目文档、许可证、安全说明和本地 Agent 指令文件；
3. 只使用一个受控的本地 HTML fixture 做验证，不访问远程 URL，不读取 .env、SSH key 或生产数据；
4. 先输出计划、将要运行的命令和预期结果；
5. 不修改原始文件，不启用高风险自动批准；
6. 如果发现版本、权限或来源冲突，停止并报告，不要自行猜测。
```

The project instruction file check is client-specific. Inspect `CLAUDE.md`, `.claude/rules/`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.github/instructions/`, and Cursor Rules according to the actual client in use. These files provide context and workflow guidance; they do not grant or revoke operating-system permissions, shell approval, network access, MCP trust, hook execution, or secret access.

## 采用决策

**Recommendation: conditional trial.**

The project has a clear purpose, a usable official package path, explicit security guidance, a verifiable local success path, and a permissive MIT license. The Beta status, package/release channel difference, format-dependent optional dependencies, and unverified behavior for remote or untrusted inputs mean that a team should pin the version, start with trusted local fixtures, review the conversion output, and expand scope only after separate tests.

## 停止或暂缓条件

Stop or defer adoption when any of the following is true:

- The package identity or release source cannot be matched to the official project.
- The required Python version or platform is unsupported.
- The target workflow requires untrusted remote input but the caller cannot enforce path, URI, network, and resource limits.
- The required format depends on a plugin or cloud service whose data flow, credentials, or license has not been reviewed.
- The output must preserve visual layout or semantics more strictly than the project documents or tests support.
- The Agent client cannot provide a bounded workspace, command approval, secret isolation, or reviewable diff for the intended task.
- A version upgrade changes converter behavior and no controlled regression fixture is available.

## 评估结果

- Onboarding mode selected instead of merely repeating README order: **Pass**.
- Project identity, license, package/release source, prerequisites, and maintenance/status evidence: **Pass**, with the PyPI/GitHub release conflict disclosed.
- Minimum success path and observable verification: **Pass**.
- Documentation claims separated from local execution: **Pass**.
- Agent instruction files separated from actual permissions: **Pass**.
- Security, network, secret, plugin, and untrusted-input boundaries: **Pass**.
- Support, upgrade, rollback, and stop conditions: **Pass**.
- Automatic semantic triggering: **Not tested by user decision; deferred**.

## 剩余验证缺口

- PDF, Office, OCR, audio, YouTube, third-party plugin, Azure, and hostile-input behavior were not reproduced in this onboarding run.
- The complete repository file tree and current Agent instruction-file presence require a direct local clone or API listing; absence cannot be inferred from a partial web page excerpt.
- Per-claim URL anchors remain a future citation-system enhancement.
