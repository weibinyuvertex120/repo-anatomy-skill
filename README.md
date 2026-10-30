# Workspace File Maintainer

A focused Agent Skill for safely creating, reading, and incrementally modifying local text files inside the current workspace.

## Purpose

This repository contains the source, evaluations, and release process for the `workspace-file-maintainer` skill. The skill wraps existing filesystem tools in a reliable workflow:

```text
inspect -> plan -> apply the smallest change -> re-read -> verify -> report
```

It does not implement a second filesystem API. It teaches an agent when and how to use its native `Read`, `Write`, `Edit`, `Glob`, and `Grep` tools, with narrowly scoped shell use for directory inspection and creation.

## Repository Layout

```text
skills/workspace-file-maintainer/  distributable skill package
evals/                             trigger and functional evaluation cases
tests/                             deterministic repository validation
dist/                              generated packages, ignored by Git
```

The skill package intentionally contains no `README.md`, scripts, or assets in its first release. Detailed operating rules live in one-level `references/` files for progressive disclosure.

## Scope

Supported in the first release:

- Create local text, source-code, configuration, and Markdown files.
- Read and summarize local text files.
- Apply precise modifications to existing files.
- Continue iterative work from the current file state in later sessions.
- Verify each write by re-reading the affected content.

Out of scope:

- Delete, move, rename, archive, or recursively clean files.
- Organize personal directories such as Desktop, Downloads, Documents, or Home.
- Edit Office, PDF, image, video, archive, or other binary formats.
- Edit cloud documents or remote storage.
- Follow symlinks outside the active workspace.
- Read or change credentials and secrets without explicit, task-specific authorization.

## Validate

Run the deterministic repository checks and validator self-tests:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
```

Run the bundled WorkBuddy Skill validator:

```bash
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" \
  skills/workspace-file-maintainer
```

Package only after both validations pass:

```bash
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/package_skill.py" \
  skills/workspace-file-maintainer \
  dist
```

## Development Workflow

1. Add or update an evaluation before changing behavior.
2. Edit `SKILL.md` or one referenced rule file.
3. Run deterministic validation.
4. Test positive, paraphrased, and negative trigger prompts in a fresh session.
5. Test create, read, modify, verification, and continued-iteration fixtures.
6. Update the version and `CHANGELOG.md` when behavior changes.
7. Package and install only a validated revision.

## Portability Note

The WorkBuddy installation requires the top-level `agent_created: true` field. The open Agent Skills `skills-ref` validator currently rejects that host-specific extension. Treat the source package as WorkBuddy-targeted until the release process adds a standards-compatible distribution variant.

## Installation During Development

Use a symlink so the development tree remains the single source of truth:

```bash
ln -s "/Users/veretex/Developer/文件skill/skills/workspace-file-maintainer" \
  "$HOME/.workbuddy-ai/skills/workspace-file-maintainer"
```

Restart the agent if the skill does not appear after installation.
