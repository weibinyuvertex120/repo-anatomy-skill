# Design References And Attribution

This project was designed from its own requirements and evaluation results. The repositories below were reviewed for reusable open-source practices; no source code, project structure, or documentation was copied wholesale.

Verification date: 2026-10-30.

## Primary Standards And Platform Guidance

### Agent Skills Specification

- Source: [agentskills/agentskills](https://github.com/agentskills/agentskills)
- Consulted material: repository README, specification, contribution guidance, and the `skills-ref` reference validator.
- Adopted: a Skill as a directory containing `SKILL.md` plus optional scripts and references; progressive disclosure; independent structural validation; a standards-compatible package variant.
- Not adopted: treating `skills-ref` as proof of production runtime behavior. This repository uses it only as a pinned structural compatibility check.
- License boundary: the upstream repository publishes its own code and documentation under the licenses declared there. This repository links to those materials and does not redistribute them.

### Anthropic Skills Examples

- Source: [anthropics/skills](https://github.com/anthropics/skills)
- Consulted material: repository README, Skill examples, template, marketplace metadata, and third-party notices.
- Adopted: keeping independent Skills under `skills/`; separating concise `SKILL.md` instructions from focused references; distinguishing source layout from host-specific distribution metadata.
- Not adopted: Claude-specific marketplace metadata as a cross-host package format, or any upstream Skill content.
- License boundary: Anthropic's repository contains materials with different license terms. Nothing from those directories is bundled here.

### GitHub Repository Guidance

- Source: [GitHub Docs: Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- Adopted: a navigable README; explicit license, contribution, code-of-conduct, and security files; pull-request-based changes; required checks for the protected default branch; private vulnerability reporting for a public repository.
- Not adopted yet: repository-host settings that cannot be represented in Git, such as branch protection and private vulnerability reporting. They remain publication gates and must be configured on GitHub.

### img2threejs README

- Source: [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs)
- Consulted material: repository README structure and ordering.
- Adopted: a short opening position, a real result near the top, followed by capability, usage, installation, and explicit limits.
- Not adopted: upstream wording, badges, showcase data, sponsorship content, roadmap, scripts catalog, project structure, or implementation details.

## Mature Project Comparisons

### Microsoft Agent Framework

- Source: [microsoft/agent-framework](https://github.com/microsoft/agent-framework)
- Reused idea: separate contribution, security, conduct, and testing responsibilities; require behavior changes to include evidence; keep vulnerability details out of public issues.
- Deliberately omitted: its multi-language API compatibility machinery and organization-scale governance, which would be disproportionate for two instruction packages.

### OpenHands

- Source: [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- Reused idea: make repository boundaries and verification commands discoverable; separate credential-free pull-request tests from live tests that require secrets; make package contents part of CI validation.
- Deliberately omitted: its multi-repository ownership map, frontend end-to-end stack, and automated release machinery until this project has comparable maintenance needs.

### SWE-agent

- Source: [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent)
- Reused idea: treat evaluation evidence and observable execution artifacts as reviewable project assets rather than relying only on an Agent's narrative report.
- Deliberately omitted: large benchmark infrastructure and model-dependent CI. Current deterministic tests are intentionally credential-free.

### Aider

- Source: [Aider-AI/aider](https://github.com/Aider-AI/aider)
- Reused idea: keep local setup, exact test commands, behavior-test requirements, and release history visible to contributors.
- Deliberately omitted: Python package release mechanics, model benchmarks, and a contributor license agreement. The repository uses the MIT contribution rule in `CONTRIBUTING.md`.

## Community Document Attribution

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) is adapted from [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html).
- Its enforcement ladder is inspired by [Mozilla's code of conduct enforcement ladder](https://github.com/mozilla/diversity).
- [`LICENSE`](LICENSE) is the MIT License with project copyright attribution.

## Project-Specific Decisions

The following are original project decisions derived from local failures and acceptance work rather than upstream templates:

- Split evidence-driven writing from filesystem persistence into two Skills.
- Keep destructive file operations and personal-directory organization outside the maintenance Skill.
- Generate WorkBuddy and open-spec archives from one source tree, removing only the host-specific `agent_created` field for open-spec distribution.
- Reject symlinks and non-regular files during packaging.
- Record source commit, dirty-tree state, exact file list, and SHA-256 in each manifest.
- Fix ZIP timestamps and permissions so repeated builds of the same commit are byte-identical.
- Treat automatic semantic routing as `blocked / unmeasured` unless the host exposes auditable route/load events.
- Separate deterministic checks, reproduced runtime evidence, historical observations, source claims, and unsupported claims in acceptance records.

## Updating This File

When a future change materially adopts an external design, add the primary source, state what was adopted, state what was deliberately not adopted, and verify that no incompatible content or license has been copied into the distribution.
