<a id="top"></a>

# Repo Anatomy Skill

<p align="right"><a href="README.md#top"><kbd>English</kbd></a> · <strong>简体中文</strong></p>

`Repo Anatomy Skill` 帮助 Agent 研究陌生的软件项目，并把经过核验的证据整理成清晰、可执行的技术资料。

当前项目聚焦于 [`research-material-writer`](skills/research-material-writer/SKILL.md)。

<a id="what-it-does"></a>

## 当前能力

[English](README.md#what-it-does)

`research-material-writer` 可以：

- 分析任意软件项目、代码仓库、类库、工具或服务；
- 从官方文档、官方仓库、发布页面、源代码和包管理器元数据等一手来源核验重要事实；
- 解释项目目标、核心能力、仓库结构、安装配置、典型工作流和采用建议；
- 输出项目分析、首次使用指南、入门教程或项目比较指南；
- 区分已核验事实、项目方声明、已复现行为、合理推断、编辑建议、信息冲突和未知项；
- 在证据支持时提供准确命令、可观察的验证步骤和来源说明；
- 检查技术草稿中的当前事实依据、任务流程、结构问题和术语一致性。

这个 Skill 会围绕读者的决策和实际工作路径组织内容，而不是简单复述项目 README。

<a id="quick-start"></a>

## 快速开始

[English](README.md#quick-start)

克隆仓库并查看 Skill 定义：

```bash
git clone https://github.com/weibinyuvertex120/repo-anatomy-skill.git
cd repo-anatomy-skill
sed -n '1,220p' skills/research-material-writer/SKILL.md
```

在本地 WorkBuddy 兼容环境中，可以将 Skill 链接到用户级 Skill 目录：

```bash
set -e
mkdir -p "$HOME/.workbuddy-ai/skills"
test ! -e "$HOME/.workbuddy-ai/skills/research-material-writer"
ln -s "$PWD/skills/research-material-writer" \
  "$HOME/.workbuddy-ai/skills/research-material-writer"
```

安装后启动新的 Agent 会话，并明确要求 Agent 使用该 Skill。通用项目研究可以使用以下提示词：

```text
请使用 research-material-writer 分析 [项目仓库地址]，读者是 [目标读者]。

说明项目解决的问题、仓库如何组织、首次使用的最短实践路径和主要采用考量。请优先从一手来源核验重要事实，区分文档描述的能力与研究过程中实际复现的行为，并给出来源和可观察的验证步骤。
```

如果研究服务于具体决策，请明确读者和目标：

```text
请使用 research-material-writer，围绕 [工作流] 比较 [项目 A] 和 [项目 B]。

先定义比较维度。在可能的情况下使用同等范围和版本的证据，按场景说明取舍，并标明哪些结论已经核验、实际复现或属于推断。
```

<a id="verified-example"></a>

## 已验证示例：MarkItDown

[English](README.md#verified-example)

仓库包含一份针对 [`microsoft/markitdown`](https://github.com/microsoft/markitdown) 的带来源项目拆解：

- [`demos/markitdown-repository-analysis.md`](demos/markitdown-repository-analysis.md)

这个示例要求 Skill 面向文档转 Markdown 预处理工作流评估 MarkItDown。研究过程包括：

- 识别项目目标和预期输出；
- 拆解多包仓库结构；
- 检查官方包配置、发布信息、许可证和安全说明；
- 在临时 Python 环境中选择固定版本的安装路径；
- 使用 `convert_local()` 对受控 HTML 样例进行实际转换；
- 检查包版本和依赖状态；
- 将本地执行结果与仅由项目文档描述的能力分开；
- 最终给出有条件的采用建议和下一步测试建议。

相关验收记录如下：

- [`evals/real-project-markitdown-2026-10-30.md`](evals/real-project-markitdown-2026-10-30.md)
- [`evals/real-project-markitdown-onboarding-2026-10-31.md`](evals/real-project-markitdown-onboarding-2026-10-31.md)

<a id="validation"></a>

## 验证仓库

[English](README.md#validation)

在项目根目录运行仓库检查：

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_readme_languages.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
```

内置草稿检查器可以检查 Markdown 结果中的结构问题：

```bash
python3 skills/research-material-writer/scripts/check_draft.py path/to/draft.md
```

<a id="project-layout"></a>

## 项目结构

[English](README.md#project-layout)

```text
skills/research-material-writer/       Skill 定义和研究参考资料
demos/                                 带来源的项目研究示例
evals/                                 功能案例和验收记录
tests/                                 仓库和打包检查
docs/                                  宿主与兼容性文档
```

<a id="license"></a>

## 许可证

[English](README.md#license)

Copyright (c) 2026 Veretex。根据 [MIT License](LICENSE) 发布。
