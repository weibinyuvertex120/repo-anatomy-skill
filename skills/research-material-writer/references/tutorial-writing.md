# Beginner Technical Tutorial

## Required Reader Path

1. Name the practical problem in language the reader recognizes.
2. Show what the tool changes and the observable successful result.
3. Explain the core concept with one concrete analogy.
4. State who the tutorial is for and when the tool is unnecessary.
5. List prerequisites and a preflight check.
6. Choose one primary installation or setup path.
7. Walk through the first successful use.
8. Provide an Agent prompt when the product is used through an Agent.
9. Explain where the tool fits in real work.
10. Explain the mechanism only after the reader can use it.
11. Cover privacy, security, compatibility, maintenance, and limitations.
12. Add symptom-based troubleshooting and source verification notes.

## Operational Unit

For each important operation, use:

```text
操作目标
-> 操作入口
-> 填写内容或动作
-> 可复制示例
-> 验证方法
-> 常见错误
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

“没有报错” is insufficient when a stronger check exists.

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
- Provides commands without prerequisites or expected results.
- Claims successful execution when only documentation was reviewed.
- Omits Agent usage for an Agent-oriented tool.
- Omits limitations, security, update guidance, or troubleshooting.
- Includes every advanced option in the main path.
