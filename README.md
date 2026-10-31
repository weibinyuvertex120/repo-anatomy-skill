# Research Writing and File Maintenance Skills

A two-layer Agent Skill repository for researching and writing high-quality Chinese technical materials, then safely persisting local text files.

## Purpose

This repository separates content quality from filesystem safety:

```text
research-material-writer
-> research -> verify -> structure -> draft -> review

workspace-file-maintainer
-> inspect -> plan -> apply the smallest change -> re-read -> verify -> report
```

`research-material-writer` turns primary evidence and existing drafts into beginner tutorials, open-source project onboarding guides, project analyses, and comparison guides. `workspace-file-maintainer` remains the lower-level persistence layer for conservative local text-file operations. Neither skill implements a second filesystem API.

## Repository Layout

```text
skills/workspace-file-maintainer/  safe local text persistence
skills/research-material-writer/   researched technical material writing
evals/                             trigger, functional, and real-project acceptance cases
tests/                             repository and draft-checker regression tests
dist/                              generated packages, ignored by Git
```

Both packages keep detailed rules in one-level `references/` files for progressive disclosure. The research skill additionally includes a deterministic Markdown structure checker; it is a heuristic that warns about editorial defects and does not replace factual review. Fence parsing follows common backtick/tilde block forms, but the checker is not a complete CommonMark parser.

## Scope

Supported in the first release:

- Research current technical projects and products from primary sources.
- Write beginner tutorials, first-time open-source project onboarding guides, project analyses, and comparison or selection guides.
- Check repository identity, governance, license, release source, prerequisites, minimum success path, Agent context files, permissions, security boundaries, and maintenance entry points before recommending first use.
- Preserve an established series voice while independently rechecking facts.
- Detect repeated Markdown rows, empty headings, accidental English-only headings, unbalanced fences, and placeholders.
- Create, read, and precisely modify local text files through the separate maintenance skill.
- Continue iterative work from the current file state and verify each write.

For an unfamiliar open-source project, use this order:

```text
identity and purpose
-> status, governance, license, and security
-> runtime and permissions
-> trusted installation source and version
-> minimum successful path
-> observable verification
-> Agent context versus actual permissions
-> workflow, support, upgrade, rollback, and stop conditions
```

README is the entry point, not proof of safety or production suitability. Repository health scores are signals for follow-up checks, not security certification. Agent instruction files such as `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, Copilot instructions, or Cursor Rules provide context and do not replace sandboxing, command approval, network controls, IAM, or secret management.

Out of scope:

- Generic creative writing or marketing copy without a research requirement.
- Fabricated commands, benchmarks, compatibility claims, or execution results.
- Delete, move, rename, archive, or recursively clean files.
- Organize personal directories such as Desktop, Downloads, Documents, or Home.
- Edit Office, PDF, image, video, archive, or other binary formats.
- Edit cloud documents or remote storage.
- Follow symlinks outside the active workspace.
- Read or change credentials and secrets without explicit, task-specific authorization.

## Validate

Run the deterministic repository checks and validator self-tests from the repository root:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
```

The repository packager rejects symlinks and non-regular files before writing ZIP entries. It creates a WorkBuddy-targeted variant and an open Agent Skills variant from the same source:

```bash
python3 scripts/package_skills.py dist
```

Run the bundled WorkBuddy Skill validator:

```bash
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" \
  skills/workspace-file-maintainer
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" \
  skills/research-material-writer
```

Package only after the repository and WorkBuddy validations pass. The repository packager is the supported release path because it refuses symlinks before creating archives:

```bash
python3 scripts/package_skills.py dist
```

Each Skill produces `-workbuddy.zip` and `-open-spec.zip` artifacts, each with a matching `.manifest.json` containing the Skill version, variant, source commit, file list, and SHA-256. The WorkBuddy variant retains `agent_created: true`; the open-spec variant removes only that host-specific top-level field. Inspect archives with `unzip -l` and verify manifests before installation. Do not use the bundled WorkBuddy packager for release until it independently enforces the same symlink boundary.

## Development Workflow

1. Add or update an evaluation before changing behavior.
2. Edit one Skill or one referenced rule file at a time.
3. Run repository, validator, and draft-checker regression tests.
4. Test positive, paraphrased, boundary, and negative trigger prompts in a fresh session.
5. Test researched writing quality separately from file persistence behavior.
6. Update the relevant Skill version and `CHANGELOG.md` when behavior changes.
7. Package and install only a validated revision.

## Portability Note

The source tree is WorkBuddy-targeted and retains the top-level `agent_created: true` field required by the local WorkBuddy validator. Release packaging also creates an open-spec variant that removes only this host-specific field. The open Agent Skills `allowed-tools` field remains experimental, so tool pre-approval behavior can still differ by client even when the package validates structurally.

## Installation During Development

For development only, use a symlink so the development tree remains the single source of truth. This is not a stable release installation: uncommitted edits become immediately visible to the running Skill.

```bash
ln -s "/Users/veretex/Developer/文件skill/skills/workspace-file-maintainer" \
  "$HOME/.workbuddy-ai/skills/workspace-file-maintainer"
ln -s "/Users/veretex/Developer/文件skill/skills/research-material-writer" \
  "$HOME/.workbuddy-ai/skills/research-material-writer"
```

Restart the agent if the skill does not appear after installation.

## Stable Installation

Stable installation uses a verified, versioned copy instead of a development symlink. Generate release packages, verify the manifest, and install into a dedicated version store:

```bash
python3 scripts/package_skills.py dist --variant workbuddy
python3 scripts/install_stable.py \
  dist/research-material-writer-workbuddy.zip \
  dist/research-material-writer-workbuddy.manifest.json \
  "$HOME/.workbuddy-ai/stable-skills" \
  --variant workbuddy
```

The installer verifies SHA-256 and the exact archive file list, rejects an existing target, and writes `.install-receipt.json`. It does not replace the active Skill link. Activate a stable version only after verifying it, and keep the previous version directory and receipt for rollback. Never point a stable installation at the development working tree.

## License

Copyright (c) 2026 Veretex. Released under the [MIT License](LICENSE).
