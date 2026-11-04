# Research Material Writer Functional Evaluation

Run each case in a fresh session. Verify the output document independently rather than relying only on the agent report.

## R00 - Functional Evaluation Scope

This file defines nine executable functional cases, R00-R08. Each run must record the Release Record fields below and distinguish deterministic checks, manual review, and blocked runtime verification.

## R00 - Comprehensive Arbitrary Project Analysis

Prompt:

```text
请系统研究我指定的任意项目，并输出一份全面、可靠且结构清晰的中文项目分析。覆盖项目概述、核心功能、适用与不适用场景、安装与配置、基础使用、典型工作流、进阶使用、最佳实践、常见问题、限制与风险、同类方案对比及综合结论。核验当前版本和关键事实，优先使用权威来源，区分已核验事实、项目方声明、已复现行为、合理推断、建议、冲突和未知项，并标明核验日期。不要创建或修改文件；如果工具、来源或运行环境不可用，明确说明并给出有边界的结论。
```

Expected:

- all applicable sections from `references/project-research-contract.md` are present or explicitly marked unavailable;
- one decision-oriented conclusion and one primary adoption path appear before exhaustive detail;
- dynamic facts, commands, compatibility, and risks have source and date/version scope;
- documentation review, source inspection, reproduced behavior, and blocked checks are separate;
- missing capabilities or inaccessible sources are reported without fabricated execution;
- the final response is usable on a host that exposes equivalent semantic capabilities without requiring a specific vendor tool name.

## R01 - Beginner Tutorial From Primary Sources

Prompt:

```text
Research a current GitHub developer tool and write a Chinese beginner tutorial. Verify the current release, choose one primary installation path, include an Agent prompt, observable verification, workflow placement, security limits, and troubleshooting.
```

Expected:

- primary sources dominate the evidence;
- dynamic facts include a verification date;
- the outline follows the reader's task rather than README order;
- one main path is primary;
- execution claims match actual testing evidence;
- the final draft passes `scripts/check_draft.py` or all warnings are justified and resolved.

## R02 - Open-Source Project Onboarding

Prompt:

```text
I received an unfamiliar GitHub open-source project. Research what a beginner must prepare before first use, decide whether it is ready to try, and write an onboarding guide that covers license, release source, runtime prerequisites, minimum success path, observable verification, Agent instruction files, permissions, security boundaries, support, upgrade, rollback, and stop conditions.
```

Expected:

- project identity, intended use, unsuitable scenarios, and a dated maintenance/status snapshot are clear;
- `LICENSE`, `SECURITY.md`, contribution/support entry points, release/package source, and relevant governance files are checked when available;
- runtime, platform, dependency, credential, service, network, and permission prerequisites appear before installation actions;
- exactly one beginner-oriented minimum path is primary and its success result is observable;
- documentation claims, source inspection, and locally reproduced behavior are separated;
- Agent instruction files are client-specific and are not presented as a substitute for sandbox, command approval, network, IAM, or secret controls;
- plugin, MCP, hook, auto-approval, and untrusted-input risks are included when relevant;
- upgrade, rollback, help channels, and explicit stop-or-defer conditions are present;
- Scorecard or similar health metrics are treated as signals rather than security certification.

## R03 - Decision-Oriented Project Analysis

Prompt:

```text
Analyze an active open-source resource repository for production adoption. Cover maintenance, license, capability map, limitations, risks, suitable scenarios, and a practical evaluation workflow.
```

Expected:

- conclusion appears before exhaustive detail;
- repository metrics are dated and not treated as quality proof;
- project facts and editorial recommendations are distinguishable;
- unsuitable scenarios and verification gaps are explicit.

## R04 - Comparison With Unequal Evidence

Prompt:

```text
Compare three tools whose public documentation has different levels of detail. Write a selection guide for a small engineering team.
```

Expected:

- comparable scope and versions are defined;
- missing evidence remains unknown rather than becoming zero or unsupported;
- trade-offs are organized by decision dimension;
- recommendations are scenario-specific.

## R05 - Continue an Existing Series

Prompt:

```text
Use an existing tutorial as the style baseline, research a new project, and write the next article in the series.
```

Expected:

- voice, reader level, terminology, and operational rhythm are preserved;
- factual content is independently researched;
- known defects in the baseline are not copied;
- the current target file is re-read before continuation.

## R06 - Blocked Runtime Verification

Prompt:

```text
Write a tutorial for a tool that cannot execute in the current sandbox. Use official documentation and source-level evidence without claiming end-to-end success.
```

Expected:

- the runtime block is disclosed;
- documentation, source inspection, and actual execution are clearly separated;
- expected results are labeled as documented behavior where appropriate;
- no fabricated terminal output appears.

## R07 - Editorial Regression Detection

Run the checker against drafts containing:

- a repeated Markdown table row;
- an English-only orphan heading in an otherwise Chinese document;
- an empty heading;
- an unbalanced code fence;
- a TODO placeholder.

Expected: each defect produces a non-zero result and a specific warning.

## R08 - Negative Simple File Task

Prompt:

```text
Create notes.md with the exact text supplied by the user.
```

Expected: do not invoke research or restructure the content; route to the file-maintenance workflow.

## Release Record

```text
case_id:
skill_version:
host_version:
triggered:
source_types:
output_path:
result: pass | fail | blocked
factual_review:
editorial_review:
notes:
```
