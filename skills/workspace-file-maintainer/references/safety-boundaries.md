# Safety Boundaries

## Contents

- Authorization roots
- Personal directories
- Sensitive files
- Symlinks and path traversal
- Destructive operations
- Unsupported formats
- Shell restrictions

## Authorization Roots

Treat the active workspace as the default authorized root.

Write outside it only when the user supplies or explicitly confirms the exact path. An outside path does not authorize sibling directories or recursive scanning.

Normalize and inspect paths before using them. Reject paths containing unresolved traversal or a resolved destination outside the authorized root.

## Personal Directories

Do not use this skill to scan, sort, clean, organize, archive, move, rename, or delete content in:

- Desktop
- Downloads
- Documents
- the user Home directory
- system or application configuration directories

A request involving these locations must follow the host's personal-file safety workflow. A single explicit file may be read or edited only when the user identifies it and the operation is non-destructive.

## Sensitive Files

Treat these as sensitive by default:

- `.env` and environment override files
- SSH keys and configuration
- cloud provider credentials
- API tokens and credential stores
- browser profiles, cookies, and keychains
- password databases
- signing keys and certificates

Do not search for sensitive files. Do not display secret values in summaries. Require an explicit request naming the exact file before any necessary read or edit, and preserve unrelated secrets.

## Symlinks and Path Traversal

Before writing through a symlink or uncertain path:

1. Resolve the real destination with an inspection-only command when available.
2. Confirm the destination remains inside the authorized root.
3. Stop if resolution is unavailable, ambiguous, or outside the root.

Never accept `..` traversal as authorization to leave the workspace.

## Destructive Operations

This skill does not perform:

- deletion;
- move or rename;
- recursive replacement;
- cleanup;
- archive extraction or creation;
- broad permission changes;
- ownership changes;
- batch operations discovered from wildcards.

Do not reinterpret "replace," "clean," or "organize" as permission for destructive actions. Route these requests to a separately reviewed workflow with explicit confirmation.

## Unsupported Formats

Do not directly edit:

- Office documents and spreadsheets;
- PDF files;
- images, audio, or video;
- databases;
- archives;
- compiled binaries;
- unknown encodings that cannot be safely preserved;
- cloud-hosted documents.

Use the corresponding specialized skill or connector.

## Shell Restrictions

Allowed shell purposes:

- show current path;
- list an explicitly authorized directory;
- test path existence or file type;
- resolve a path;
- create an explicitly authorized parent directory;
- run a repository's existing verification command when the task requires it.

Do not use shell commands to read or write file content when native file tools are available. Never use `rm`, `mv`, broad `cp`, shell redirection, `sed -i`, `awk` rewrites, permission escalation, or destructive Git commands under this skill.
