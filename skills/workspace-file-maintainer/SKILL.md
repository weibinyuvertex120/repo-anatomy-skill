---
name: workspace-file-maintainer
description: Safely creates, reads, and incrementally updates local text, code, configuration, and Markdown files inside the active workspace, with preflight inspection, minimal edits, post-write verification, and continued iteration from current file state. This skill should be used whenever the user asks to create, write, read, edit, update, patch, or continue a local workspace file, including requests such as 创建文件、写入本地路径、修改配置、更新 README、修补代码文件 or 继续完善已有文件. It should not be used for file deletion, moving, batch renaming, personal-directory cleanup, binary or Office/PDF/media files, or cloud documents.
compatibility: Requires local filesystem Read, Write, Edit, Glob, and Grep tools. Shell use is limited to path inspection, directory creation, and user-requested project verification commands.
allowed-tools: Read Write Edit Glob Grep Bash
metadata:
  version: "0.1.0"
  category: "productivity"
  scope: "local-text-files"
agent_created: true
---

# Workspace File Maintainer

Maintain local text files through a conservative, verifiable workflow. Reuse native filesystem tools rather than generating ad hoc file-writing scripts.

## Critical Boundaries

- Default all writes to the active workspace.
- Require an explicit user-provided path before writing outside the workspace.
- Never delete, move, rename, archive, recursively clean, or batch-organize files.
- Never scan or organize Desktop, Downloads, Documents, Home, or another personal directory under this skill.
- Route Office, PDF, image, video, archive, and other binary formats to their dedicated skills.
- Route cloud documents and remote storage to the appropriate connector or library skill.
- Treat `.env`, credentials, SSH keys, tokens, keychains, and secret stores as sensitive. Do not read or modify them unless the user explicitly requests that exact file and the task requires it.
- Refuse to follow a symlink whose resolved destination is outside the authorized workspace or user-provided target.
- Never replace a failed precise edit with an unreviewed full-file overwrite.
- Never use shell redirection, `sed`, `awk`, `rm`, `mv`, or broad copy commands as substitutes for native file tools.

Read [references/safety-boundaries.md](references/safety-boundaries.md) before handling an outside-workspace path, a sensitive-looking path, a symlink, multiple files, or any ambiguous destructive request.

## Operating Workflow

Follow this sequence for every edit-style task:

1. **Resolve the target.** Identify the intended file, operation, output format, and acceptance condition. Ask only when a missing decision materially changes the result.
2. **Inspect the environment.** Locate files with `Glob`, locate content with `Grep`, and read the smallest relevant ranges or files before editing.
3. **Plan the smallest change.** Preserve the existing structure, conventions, encoding, and unrelated content.
4. **Apply through native tools.** Prefer `Edit` for precise existing-file changes and `Write` for new files. Rewrite an existing file only after reading it completely and confirming that a whole-file replacement is necessary.
5. **Verify immediately.** Re-read the affected area, search for stale or duplicate content, and run an existing project validation command when the user request or repository convention requires it.
6. **Report accurately.** Name the changed files, summarize material edits, state verification performed, and disclose unresolved errors or risks.

Read [references/workflow.md](references/workflow.md) for operation-specific decision rules and multi-file sequencing.

## Operation Rules

### Create a File

- Confirm the destination and file type.
- Inspect neighboring files when naming, structure, or style should match an existing project.
- Confirm the parent directory exists. Create only the required directory when it does not exist and the location is authorized.
- Do not overwrite an existing file as a creation shortcut. Read it and switch to the modification workflow.
- Write only requested content and necessary supporting structure.
- Re-read the complete new file after creation.

### Read a File

- Read the exact user-provided path when available.
- Use `Glob` or `Grep` only when the target is unknown or the task requires discovery.
- Avoid broad workspace scans when a focused read can answer the request.
- Preserve literal tokens such as `N/A`, placeholders, code, and formatting when reporting content.
- Do not write unless the user request implies an edit.

### Modify an Existing File

- Read the current file before changing it.
- Use `Edit` with enough surrounding context to make the replacement unique.
- If the match is absent, re-read the latest content and revise the patch. Do not guess.
- If the match is non-unique, expand the context or split the operation into explicit edits.
- Preserve unrelated user changes and repository conventions.
- Re-read the modified region and verify that the old content is removed only where intended.

### Continue an Earlier Task

- Treat current files as the source of truth; do not depend on prior chat memory.
- Re-read the target and inspect recent surrounding context before continuing.
- Identify what is complete, what remains, and whether the file changed since the prior iteration.
- Apply only the next required increment.
- Verify the resulting state and provide a concise handoff for the next session.

## Error Handling

Do not announce completion while a requested write is unverified. Follow the exact recovery rules in [references/error-handling.md](references/error-handling.md).

Core behavior:

- Missing target during a modification task: report the path mismatch; do not silently create a replacement.
- Existing target during a creation task: read it and preserve it unless overwrite is explicitly authorized.
- Permission failure: report the exact path and stop; do not escalate privileges.
- Concurrent change: re-read and re-plan from the newest content.
- Unknown or binary format: stop and route to the correct skill.
- No-op request: leave the file unchanged and report that it already satisfies the requirement.

## Verification Contract

Complete an edit only after all applicable checks pass:

- The requested file exists at the intended path.
- New or modified content is present exactly once where expected.
- Removed content is absent only from the intended location.
- Unrelated sections remain intact.
- No placeholder, template marker, code fragment, or empty output was accidentally left behind.
- Existing repository validation commands pass when required and available.

If a check fails, fix the issue and verify again. If it cannot be fixed safely, stop and report the blocker.

## Trigger and Quality Evaluation

Use [references/evaluation-cases.md](references/evaluation-cases.md) when changing the description, supported operations, or safety boundaries. Test obvious triggers, paraphrases, negative triggers, functional behavior, cross-session continuation, and refusal boundaries in a fresh session.

## Maintenance Rules

- Keep this `SKILL.md` focused and below 500 lines.
- Keep references one link level from this file.
- Add a regression evaluation before changing behavior after a real failure.
- Update `metadata.version` using Semantic Versioning whenever behavior changes.
- Keep destructive operations out of scope unless a future major version introduces a separately reviewed confirmation workflow.
- Prefer stronger tool-level restrictions when the host supports them; retain written boundaries because `allowed-tools` support varies across Agent Skills clients.
