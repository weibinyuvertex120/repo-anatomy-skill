# research-material-writer 宿主适配操作说明

本文只覆盖 `research-material-writer`。`workspace-file-maintainer` 暂停，不应按本文安装或声明兼容。

## 通用安装前检查

1. 固定 Skill 核心版本和发布资产哈希。
2. 确认目标宿主的产品、表面和版本。
3. 确认宿主是否支持 Agent Skills 标准、项目/用户作用域、显式调用、刷新和来源/加载证据。
4. 安装后在新会话中检查发现，再进行显式调用；不要用回答内容反推加载成功。
5. 记录 `ARTIFACT_VALID`、`INSTALLED`、`DISCOVERED`、`SELECTED`、`LOADED`、`EXECUTED`、`ACCEPTED` 状态。

## OpenAI Codex

Codex 的官方技能文档描述了项目和用户级 `.agents/skills` 目录、`SKILL.md`、`$` 显式引用和 `/skills` 管理入口。使用 open-spec 核心包，不添加 WorkBuddy 专有字段。

推荐操作：

1. 将发布包中的 `research-material-writer/` 安装到目标仓库的 `.agents/skills/research-material-writer/`，或按照当前 Codex 版本的用户级目录规则安装。
2. 启动新的 Codex 会话，使用 `/skills` 检查名称、来源和描述是否可见。
3. 使用 `$research-material-writer` 显式请求任意项目研究，并要求按 `project-research-contract.md` 输出。
4. 检查 Skill 正文是否实际加载；若宿主只显示名称而不提供加载事件，最多记录为 `DISCOVERED`。
5. 对当前宿主版本运行综合项目分析、来源受限和工具不可用三个案例。

降级：如果 `$research-material-writer` 不可用，将核心研究提示和 `project-research-contract.md` 的要求直接粘贴到用户提示中；结果只能标记为 `content-assisted research`，不声明 Skill 已加载。

注意：Codex 文档所述目录和入口是宿主能力，不是 Agent Skills 规范的一部分。版本升级后必须重跑发现和显式加载验证。

## 豆包/火山方舟 Skills

火山方舟官方 Skills 文档公开了 SkillHub 预置 Skills、CreateSkill 上传自定义 Skills 以及在 Agent 中引用 Skills 的能力。当前没有足够证据证明豆包桌面/网页/IDE 各表面都接受原生 `SKILL.md` 目录、支持 `.agents/skills` 本地扫描、提供统一显式调用语法或暴露正文加载事件。

在官方入口明确支持前，不执行以下假设：

- 不假设豆包识别 Codex 的 `$research-material-writer`；
- 不假设豆包识别 Claude 的 `/research-material-writer`；
- 不假设上传一个 ZIP 会自动映射到本地 Skill 目录；
- 不假设 Skill 元数据会授予搜索、浏览器、Shell 或文件权限；
- 不假设豆包回答中提到 Skill 名称就等于加载成功。

建议验证顺序：

1. 在官方 Skills/SkillHub/CreateSkill 入口确认支持的文件格式、字段、版本和来源显示。
2. 上传或引用无宿主专有字段的核心包，记录平台返回的 Skill 标识和版本。
3. 在新 Agent 会话中显式引用 Skill，保存可见的选择/加载证据。
4. 运行综合项目研究案例，核验来源、日期、章节覆盖和未知项披露。
5. 在没有来源搜索、网络受限或执行能力时运行降级案例，确认不会伪造结果。
6. 只有在 L2-L5 证据完整后，才更新兼容矩阵。

降级：如果官方入口不能提供可验证的加载流程，将 `SKILL.md` 和研究契约作为用户提供的研究规范，要求 Agent 按规范回答。该路径验证的是内容可复用性，不是豆包 Skill 运行兼容性。

## 其他宿主

新宿主必须先完成 Host Probe：

- 支持的 Skill 目录和作用域；
- 发现与刷新机制；
- 显式调用入口；
- 同名冲突和优先级；
- 网络/仓库/材料读取能力；
- 文件和 Shell 权限；
- Skill 加载与工具轨迹的可观测性。

若无法回答其中任一关键问题，适配等级不高于 `L1 Content-compatible`。
