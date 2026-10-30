# File Maintenance Workflow

## Contents

- Target resolution
- Tool selection
- New-file workflow
- Existing-file workflow
- Multi-file workflow
- Continued iteration
- Verification and handoff

## Target Resolution

Resolve these facts before writing:

1. Authorized root: active workspace or an explicit user-provided outside path.
2. Target path: exact file when known; otherwise the smallest search scope.
3. Operation: create, read, modify, or continue.
4. Output contract: format, required sections, naming, and acceptance condition.
5. Existing conventions: neighboring filenames, formatting, schemas, or project instructions.

Ask a clarification question only when no reasonable conservative default exists and the answer changes the user-visible result, target path, or safety boundary.

## Tool Selection

Use tools in this order of preference:

| Need | Preferred tool | Rule |
|---|---|---|
| Read a known file | `Read` | Read the smallest useful scope. |
| Find files by name | `Glob` | Limit the search root and result count. |
| Find labels or content | `Grep` | Search before assuming line locations. |
| Modify existing text | `Edit` | Match exact unique content with context. |
| Create a new file | `Write` | Confirm parent path and absence first. |
| Create a required directory | restricted `Bash(mkdir:*)` | Create only the explicit parent directory. |
| Inspect paths | restricted `pwd`, `ls`, `test`, `realpath` | Do not mutate content. |

Do not use shell text-processing or redirection as a fallback for native file tools.

## New-File Workflow

1. Check whether the target already exists.
2. Inspect neighboring files if project conventions apply.
3. Confirm the parent directory is authorized.
4. Create only a missing required parent directory.
5. Write the requested file once.
6. Read the complete result.
7. Check for missing sections, placeholder text, truncated content, and naming mistakes.

If the target exists, stop treating the operation as creation. Read the file and use the existing-file workflow.

## Existing-File Workflow

1. Read the current file before editing.
2. Locate the exact edit anchor with `Grep` when the file is large.
3. Choose the smallest coherent replacement.
4. Include enough surrounding text to make the edit unique.
5. Apply the edit.
6. Read the modified region.
7. Search for stale text, duplicate insertions, or incomplete replacement.
8. Run an existing validation command if the repository requires one.

Rewrite the whole file only when:

- the file has been read completely;
- the requested change truly affects most of its structure; and
- a precise patch would be less reliable than replacement.

## Multi-File Workflow

For multiple files:

1. List the explicit target set before writing.
2. Inspect shared conventions first.
3. Apply changes in dependency order.
4. Verify each file after its write rather than waiting until the end.
5. Re-run shared validation after all files are complete.
6. Report every changed path.

Do not expand from a named set into a recursive batch operation without explicit user authorization.

## Continued Iteration

Start every new session from disk state:

1. Read the target files again.
2. Compare current content with the requested next step.
3. Identify completed and incomplete portions.
4. Check whether another process or user changed the files.
5. Continue with the next smallest increment.
6. Leave a concise handoff stating current state, verification, and remaining work.

Do not create a hidden state database. The maintained files and visible repository history are the durable source of truth.

## Verification and Handoff

Before reporting completion, confirm:

- correct destination;
- correct content and format;
- no unintended duplicate or stale content;
- no unrelated file changes;
- applicable project checks completed;
- unresolved issues disclosed.

Use a concise final handoff:

```text
Changed:
- path/to/file: material change

Verified:
- re-read target
- validation command and result

Remaining:
- none, or an exact blocker
```
