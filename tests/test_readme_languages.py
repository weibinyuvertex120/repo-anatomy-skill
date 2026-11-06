#!/usr/bin/env python3
"""Validate the bilingual README navigation and local links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ENGLISH = ROOT / "README.md"
CHINESE = ROOT / "README.zh-CN.md"

SECTIONS = {
    "top": ("# Repo Anatomy Skill", "# Repo Anatomy Skill"),
    "what-it-does": ("## What It Does", "## 当前能力"),
    "quick-start": ("## Quick Start", "## 快速开始"),
    "verified-example": ("## Verified Example: MarkItDown", "## 已验证示例：MarkItDown"),
    "validation": ("## Validate the Repository", "## 验证仓库"),
    "project-layout": ("## Project Layout", "## 项目结构"),
    "license": ("## License", "## 许可证"),
}

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_LINK = re.compile(r'href="([^"]+)"')
ANCHOR = re.compile(r'<a id="([a-z0-9-]+)"></a>')


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_readme(path: Path, peer_name: str, headings: list[str], errors: list[str]) -> None:
    if not path.is_file():
        fail(errors, f"Missing {path.name}")
        return

    text = path.read_text(encoding="utf-8")
    anchors = set(ANCHOR.findall(text))
    expected_anchors = set(SECTIONS)
    if anchors != expected_anchors:
        fail(errors, f"{path.name}: anchors mismatch: {sorted(anchors)}")

    for heading in headings:
        if heading not in text:
            fail(errors, f"{path.name}: missing heading {heading}")

    for anchor in SECTIONS:
        target = f"{peer_name}#{anchor}"
        if target not in text:
            fail(errors, f"{path.name}: missing language link to {target}")

    links = MARKDOWN_LINK.findall(text) + HTML_LINK.findall(text)
    for raw_target in links:
        target = unquote(raw_target.strip())
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative, _, fragment = target.partition("#")
        resolved = (path.parent / relative).resolve()
        if not resolved.is_file():
            fail(errors, f"{path.name}: local link target does not exist: {target}")
            continue
        if fragment and resolved in {ENGLISH.resolve(), CHINESE.resolve()}:
            peer_text = resolved.read_text(encoding="utf-8")
            if f'<a id="{fragment}"></a>' not in peer_text:
                fail(errors, f"{path.name}: target anchor does not exist: {target}")


def main() -> int:
    errors: list[str] = []
    validate_readme(
        ENGLISH,
        CHINESE.name,
        [headings[0] for headings in SECTIONS.values()],
        errors,
    )
    validate_readme(
        CHINESE,
        ENGLISH.name,
        [headings[1] for headings in SECTIONS.values()],
        errors,
    )

    if errors:
        print("README language validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("README language navigation passed")
    print(f"- sections: {len(SECTIONS)}")
    print("- local links: valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
