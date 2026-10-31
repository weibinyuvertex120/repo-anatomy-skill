# Security Policy

## Supported Versions

This project is preparing its first public preview. Security fixes are provided for the latest published preview or stable release only.

| Version | Supported |
|---|---|
| `0.2.0-preview.x` | Yes, after the first public preview is published |
| Unreleased working-tree builds | No |
| `0.1.x` development revisions | No |

## Report A Vulnerability

Do not open a public issue for a suspected vulnerability, secret exposure, or exploit proof of concept.

Use GitHub's **Report a vulnerability** button on the repository Security page. Include:

- the affected Skill, version, source commit, host, and operating system;
- a concise summary and expected security boundary;
- complete reproduction steps using non-sensitive fixtures;
- the actual result and potential impact;
- whether symlinks, paths outside the workspace, archives, credentials, network access, hooks, MCP servers, or automatic tool approval are involved;
- logs or screenshots with secrets, personal paths, and user data removed;
- any known mitigation or safe workaround.

If private vulnerability reporting is not available, do not publish exploit details. Contact the repository owner through a private GitHub channel and state only that a private security report is needed.

Never include real API keys, tokens, SSH keys, `.env` contents, private documents, or third-party personal data in a report. Use temporary marker files and disposable workspaces.

## Scope

Security reports are appropriate for issues such as:

- writing, reading, packaging, or following paths outside the authorized workspace;
- symlink, path traversal, archive, or package-content boundary bypasses;
- secret disclosure or unsafe handling of credential-like files;
- destructive behavior that contradicts the documented Skill boundary;
- dangerous automatic triggering or tool execution without the documented approval boundary;
- release artifacts whose contents or hashes do not match the published source;
- an instruction or example that creates a reproducible security failure in a supported workflow.

Ordinary documentation errors, feature requests, and unsupported-client compatibility questions should use public issue templates unless they expose a security boundary.

## Coordinated Disclosure

The maintainer will acknowledge a complete report when it is reviewed, assess affected versions and mitigations, and coordinate a disclosure date with the reporter when a vulnerability is confirmed. Response and remediation times depend on severity and maintainer availability; this preview project does not promise a fixed service-level agreement.

Please allow time to investigate and release a fix before public disclosure. Confirmed vulnerabilities may be handled through a GitHub Security Advisory, a patched release, release notes, and credit to the reporter when requested.

## Security Boundaries

These Skills are instruction packages, not operating-system sandboxes. Written rules do not replace filesystem permissions, command approval, network controls, IAM, secret management, or host isolation. `allowed-tools` support varies across Agent clients. Automatic semantic triggering is not yet treated as a verified security boundary.
