# Beginner Technical Tutorial

## Required Reader Path

1. Name the practical problem in language the reader recognizes.
2. Show what the tool changes and the observable successful result.
3. Present a compact understanding map of input, processing, output, workflow position, and responsibility boundary.
4. Explain one core concept with a concrete analogy only when it helps the next action.
5. State who the tutorial is for and when the tool is unnecessary.
6. List prerequisites and a preflight check.
7. Choose one primary installation or setup path.
8. Walk through the first successful use with expected observations and failure signals.
9. Verify one material boundary and cleanup or rollback.
10. Provide an Agent prompt when the product is used through an Agent.
11. Explain where the tool fits in real work.
12. Add an orientation check and one bounded transfer task.
13. Explain the mechanism only after the reader can use it.
14. Cover privacy, security, compatibility, maintenance, and limitations.
15. Add symptom-based troubleshooting, adoption guidance, and source verification notes.

## Operational Unit

For each important operation, use:

```text
操作目标与为什么现在做
-> 环境和操作入口
-> 填写内容或动作
-> 可复制示例
-> 预期现象与实际结果
-> 失败信号与最小纠正
-> 清理或回滚
-> 证据类型与适用范围
```

Do not force all six labels into tiny steps. Preserve the information even when a compact format reads better.

## Main Path Selection

Choose the path most likely to succeed for the stated reader and environment. Put alternatives after the main path and explain why someone would choose them.

Avoid presenting npm, source build, plugin marketplace, container, and manual configuration as equal first steps. That transfers the author's uncertainty to the beginner.

## Verification Standard

A verification step must define an observable result:

- Command output contains a specific field.
- A tool appears in an Agent's available tool list.
- A file, process, or configuration entry exists.
- A controlled test is allowed or denied as expected.
- A status command reports the expected state.

“没有报错” is insufficient when a stronger check exists. Expected behavior from documentation is not an actual result. When the reader must learn to use the project, add orientation, boundary, and transfer checks from `learning-validation-feedback.md`.

## Agent Prompts

A useful prompt should state:

- The task and target scope.
- The tool or capability the Agent should prefer.
- What evidence to preserve.
- What the Agent must not do.
- The expected output and verification.

Do not write prompts that merely say “请使用这个工具完成任务.”

## Troubleshooting

Organize by symptom, not by internal component. For each symptom include:

- Likely cause.
- Verification command or inspection point.
- Smallest corrective action.
- Expected result.
- Version or platform caveat when relevant.

## Tutorial Failure Patterns

Reject a draft that:

- Mirrors README headings.
- Lists features before explaining the reader's problem.
- Provides commands without prerequisites, expected results, failure signals, or recovery.
- Claims successful execution or user completion when only documentation was reviewed.
- Treats copied example success as proof that the reader can transfer the skill.
- Omits Agent usage for an Agent-oriented tool.
- Omits limitations, security, update guidance, or troubleshooting.
- Includes every advanced option in the main path.
