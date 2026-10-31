# Real Project Acceptance: Microsoft MarkItDown

Date: 2026-10-30
Skill: `research-material-writer` 0.1.0
Invocation: explicit
Automatic semantic trigger matrix: deferred until after open-source publication

## Task

Research an unfamiliar active open-source project and produce a beginner Chinese tutorial that can be followed to a working result. The test must exercise current-version verification, source conflict handling, installation, runtime verification, Agent workflow design, limitations, security boundaries, troubleshooting, file persistence, and draft quality review.

Selected project: `microsoft/markitdown`

Output: a local tutorial artifact outside this repository. The generated tutorial was intentionally not committed; this file records the evaluation method and result.

## Primary Evidence

- Official GitHub README.
- PyPI project page and package metadata.
- Official `packages/markitdown/pyproject.toml`.
- Official `LICENSE` and `SECURITY.md`.
- GitHub release page for `v0.1.3`.

## Fact Ledger Highlights

| Claim | Evidence | Class | Verification |
|---|---|---|---|
| PyPI package version is 0.1.9 | PyPI | verified fact | 2026-10-30 |
| PyPI release date is 2026-10-21 | PyPI | verified fact | 2026-10-30 |
| Python requirement is >=3.10,<3.15 | PyPI and official pyproject | verified fact | 2026-10-30 |
| License is MIT | official pyproject and LICENSE | verified fact | 2026-10-30 |
| Package status is Beta | PyPI classifiers | verified fact | 2026-10-30 |
| GitHub release page exposes v0.1.3 while PyPI exposes 0.1.9 | official release page and PyPI | verified source conflict | 2026-10-30 |
| CLI and convert_local preserve the tested HTML heading, link, list, and table | local isolated execution | reproduced fact | 2026-10-30 |
| PDF, Office, OCR, audio, YouTube, plugins, and Azure capabilities | official docs and package configuration | source claim, not reproduced | explicitly disclosed |

## Runtime Verification

A disposable directory and Python virtual environment were used.

Verified:

- installation of `markitdown==0.1.9`;
- installation of `markitdown[all]==0.1.9`;
- `pip check` returned `No broken requirements found`;
- `markitdown --version` returned `markitdown 0.1.9`;
- CLI converted a controlled HTML document to Markdown;
- `MarkItDown().convert_local()` returned `DocumentConverterResult`;
- converted Markdown preserved the tested heading, link, list, table, and value.

Not verified:

- PDF and Office conversion quality;
- OCR, image description, audio or YouTube transcription;
- third-party plugins;
- Azure Document Intelligence or Content Understanding;
- untrusted-input attack scenarios.

## Skill Behavior Observed

- Selected one primary beginner path: venv plus pinned PyPI `[all]` install.
- Detected and explained the GitHub Release versus PyPI version conflict instead of choosing one silently.
- Separated reproduced behavior from documentation-only capability claims.
- Used the tutorial operation pattern: objective, entry point, action, example, verification, and common error.
- Added an Agent prompt with path limits, output requirements, validation, failure handling, and source-file preservation.
- Placed security and unsuitable scenarios in the tutorial rather than treating conversion as a harmless formatting step.
- Persisted a standalone tutorial and re-read it from disk.

## Deterministic Quality Check

Command:

```bash
python3 skills/research-material-writer/scripts/check_draft.py \
  /path/to/markitdown-tutorial-real-eval.md
```

Result: pass.

The checker reported no repeated tables or content blocks, empty headings, heading jumps, accidental English-only headings, unbalanced fences, or placeholders.

## Independent Review

A fresh agent explicitly loaded `research-material-writer`, ran a read-only review, and returned `pass` with no blocking issues.

Two documentation gaps were fixed after review:

- the tutorial's verification note now distinguishes the initial base-package install from the tested `[all]` main path;
- the tutorial now records the successful `pip check` result.

One non-blocking improvement remains: the final source section names primary sources but does not yet include per-claim links or source anchors. This is recorded as a future citation-system enhancement, not a failure of the current tutorial workflow.

## Final Result

Functional real-project evaluation: pass.

Automatic semantic trigger repetition is intentionally deferred by user decision until after open-source publication.
