#!/usr/bin/env python3
"""Run deterministic structural checks on a Markdown research draft."""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

PLACEHOLDERS = re.compile(r"\b(?:TODO|TBD|FIXME)\b|\[insert .+?\]|待补充|占位符", re.IGNORECASE)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR_ROW = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")
ENGLISH_ONLY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 /:+&().,_'`-]*$")
ALLOWED_ENGLISH_HEADINGS = {
    "macOS",
    "Windows",
    "Fedora",
    "Arch Linux",
    "Docker Socket",
    "Apple Events",
    "Node.js",
}


def normalize(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def fence_marker(line: str) -> tuple[str, int] | None:
    match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
    if not match:
        return None
    marker, info = match.groups()
    if marker[0] == "`" and "`" in info:
        return None
    return marker[0], len(marker)


def is_fence_close(line: str, marker: str, length: int) -> bool:
    match = re.match(r"^ {0,3}(`+|~+)[ \t]*$", line)
    return bool(match and match.group(1)[0] == marker and len(match.group(1)) >= length)


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    warnings: list[str] = []

    if not text.strip():
        return ["draft is empty"]

    headings: list[tuple[int, int, str]] = []
    repeated_table_rows: dict[str, list[int]] = collections.defaultdict(list)
    repeated_blocks: dict[str, list[int]] = collections.defaultdict(list)
    content_block: list[str] = []
    block_start = 0
    table_rows: dict[str, list[int]] = collections.defaultdict(list)
    table_active = False
    fence: tuple[str, int] | None = None

    def record_block() -> None:
        nonlocal content_block, block_start
        normalized_block = normalize(" ".join(content_block))
        if len(normalized_block) >= 40:
            repeated_blocks[normalized_block].append(block_start)
        content_block = []
        block_start = 0

    def record_table() -> None:
        nonlocal table_rows, table_active
        for row, locations in table_rows.items():
            if len(locations) > 1:
                repeated_table_rows[row].extend(locations)
        table_rows = collections.defaultdict(list)
        table_active = False

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if fence is not None:
            if is_fence_close(line, *fence):
                fence = None
            continue
        opener = fence_marker(line)
        if opener is not None:
            record_block()
            record_table()
            fence = opener
            continue

        if PLACEHOLDERS.search(line):
            warnings.append(f"line {line_number}: placeholder text remains")

        heading = HEADING.match(line)
        if heading:
            headings.append((line_number, len(heading.group(1)), heading.group(2)))

        if TABLE_ROW.match(line):
            record_block()
            table_active = True
            if not SEPARATOR_ROW.match(line):
                table_rows[normalize(line)].append(line_number)
            continue

        record_table()
        if not stripped or heading:
            record_block()
            continue
        if not content_block:
            block_start = line_number
        content_block.append(stripped)

    if fence is not None:
        warnings.append("unbalanced code fence")
    record_block()
    record_table()

    for index, (line_number, level, title) in enumerate(headings):
        if index and level > headings[index - 1][1] + 1:
            warnings.append(f"line {line_number}: heading level jumps from H{headings[index - 1][1]} to H{level}")
        normalized_title = re.sub(r"^\d+\.\s*", "", title)
        if (
            ENGLISH_ONLY.fullmatch(title)
            and normalized_title not in ALLOWED_ENGLISH_HEADINGS
            and not re.search(r"`|API|CLI|SDK|MCP|FAQ|GitHub|README", title)
        ):
            warnings.append(f"line {line_number}: English-only heading may be an accidental language switch: {title}")

        next_heading = headings[index + 1] if index + 1 < len(headings) else None
        next_heading_line = next_heading[0] if next_heading else len(lines) + 1
        body = [line for line in lines[line_number:next_heading_line - 1] if line.strip()]
        is_trailing_heading = next_heading is None
        is_empty_before_peer = next_heading is not None and next_heading[1] <= level
        if not body and (is_trailing_heading or is_empty_before_peer):
            warnings.append(f"line {line_number}: heading has no body content: {title}")

    for row, locations in repeated_table_rows.items():
        if len(locations) > 1:
            warnings.append(f"lines {locations}: repeated table row: {row[:100]}")
    for block, locations in repeated_blocks.items():
        if len(locations) > 1:
            warnings.append(f"lines {locations}: repeated content block: {block[:100]}")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Markdown draft to check")
    args = parser.parse_args()

    if not args.draft.is_file():
        print(f"ERROR: draft does not exist: {args.draft}", file=sys.stderr)
        return 2

    warnings = check(args.draft)
    if warnings:
        print(f"Draft check found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("Draft check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
