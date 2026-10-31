#!/usr/bin/env python3
"""Regression tests for the research-material-writer draft checker."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills/research-material-writer/scripts/check_draft.py"


def run_case(name: str, text: str, expected_code: int, expected_text: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"draft-check-{name}-") as temporary:
        draft = Path(temporary) / "draft.md"
        draft.write_text(text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(draft)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout + result.stderr
        if result.returncode != expected_code:
            raise AssertionError(f"{name}: expected code {expected_code}, got {result.returncode}\n{output}")
        if expected_text not in output:
            raise AssertionError(f"{name}: expected {expected_text!r}\n{output}")
        print(f"PASS {name}")


def main() -> int:
    run_case(
        "clean",
        "# 示例教程\n\n## 安装\n\n运行以下命令。\n\n```bash\ntool install\n```\n\n## 验证\n\n命令输出版本号。\n",
        0,
        "Draft check passed",
    )
    run_case(
        "repeated-table-row",
        "# 分析\n\n| 名称 | 用途 |\n|---|---|\n| A | 测试 |\n| A | 测试 |\n",
        1,
        "repeated table row",
    )
    run_case(
        "english-heading",
        "# 中文教程\n\n## Command sandboxing\n\n这里解释命令沙箱。\n",
        1,
        "English-only heading",
    )
    run_case(
        "empty-heading",
        "# 教程\n\n## 安装\n\n## 验证\n\n查看版本号。\n",
        1,
        "heading has no body content",
    )
    run_case(
        "placeholder-and-fence",
        "# 教程\n\nTODO: 补充命令。\n\n```bash\ntool run\n",
        1,
        "placeholder text remains",
    )
    run_case(
        "heading-jump",
        "# 教程\n\n### 安装细节\n\n这里说明安装细节。\n",
        1,
        "heading level jumps",
    )
    run_case(
        "trailing-empty-heading",
        "# 教程\n\n正文内容。\n\n## 未完成章节\n",
        1,
        "heading has no body content",
    )
    run_case(
        "repeated-prose",
        "# 教程\n\n这是一段足够长而且内容完全相同的重复说明文字，用于验证检查器能够可靠发现意外复制的正文内容。\n\n## 验证\n\n这是一段足够长而且内容完全相同的重复说明文字，用于验证检查器能够可靠发现意外复制的正文内容。\n",
        1,
        "repeated content block",
    )
    run_case(
        "repeated-multiline-list",
        "# 教程\n\n- 第一步先检查运行环境、依赖版本和当前工作目录是否符合要求。\n- 第二步执行官方安装命令，并完整记录终端输出和异常信息。\n\n## 再次说明\n\n- 第一步先检查运行环境、依赖版本和当前工作目录是否符合要求。\n- 第二步执行官方安装命令，并完整记录终端输出和异常信息。\n",
        1,
        "repeated content block",
    )
    run_case(
        "fenced-headings-and-placeholder",
        "# 示例教程\n\n```markdown\n## TODO\n[insert command]\n```\n\n正文说明。\n",
        0,
        "Draft check passed",
    )
    run_case(
        "inline-backticks",
        "# 示例教程\n\n行内展示三个反引号 ` ``` ` 不构成代码围栏。\n",
        0,
        "Draft check passed",
    )
    run_case(
        "four-backtick-fence",
        "# 示例教程\n\n````markdown\n## TODO\n```\n````\n\n正文说明。\n",
        0,
        "Draft check passed",
    )
    run_case(
        "tilde-fence",
        "# 示例教程\n\n~~~markdown\n## TODO\n~~~\n\n正文说明。\n",
        0,
        "Draft check passed",
    )
    run_case(
        "mismatched-fence",
        "# 示例教程\n\n````text\n正文\n```\n",
        1,
        "unbalanced code fence",
    )
    run_case(
        "same-header-different-tables",
        "# 比较\n\n| 名称 | 用途 |\n|---|---|\n| A | 测试 |\n\n说明。\n\n| 名称 | 用途 |\n|---|---|\n| B | 测试 |\n",
        0,
        "Draft check passed",
    )
    print("Draft checker regression tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
