# Copilot Read-Only Adapter And Version Contract

Verification date: 2026-11-01

This document defines the responsibilities, version boundaries, compatibility levels, installation assumptions, and change rules for a future GitHub Copilot VS Code Agent adapter for the approved read-only subset of `research-material-writer`.

It is an architecture contract. It does not define the final package file layout, modify the source Skill, or claim runtime compatibility.

## Scope

The adapter is limited to:

- GitHub Copilot Agent Mode in Visual Studio Code;
- explicit user invocation;
- Chinese research, analysis, planning, and conversational output;
- public or user-provided evidence;
- read-only host capabilities;
- core Skill version `0.2.0-preview.1`;
- a separately versioned adapter artifact.

The adapter does not cover automatic Skill selection, Copilot CLI, cloud agent, code review, the GitHub Copilot app, local writing, shell execution, other languages, other Agent hosts, or `workspace-file-maintainer`.

## External Platform Assumptions

GitHub currently documents Agent Skills support in VS Code Agent Mode and accepts project Skills in `.github/skills`, `.claude/skills`, or `.agents/skills`, and personal Skills in `~/.copilot/skills` or `~/.agents/skills`. GitHub CLI Skill management is in public preview and may change.

GitHub also documents that:

- Skills are selected from prompt relevance and the Skill description;
- selected `SKILL.md` instructions are injected into context;
- Skill resources are made available to Copilot;
- third-party Skills are not verified by GitHub;
- users should preview Skills before installation;
- shell or Bash pre-approval increases risk;
- installation can be pinned to a version or commit;
- installed provenance metadata can include the source repository, ref, and tree SHA.

These are platform facts checked on 2026-11-01, not guarantees about the user's specific Copilot build or available tools. The real host evaluation must record the observed versions and behavior.

## Architecture Responsibilities

### Core Skill

The existing source Skill remains authoritative for:

- research principles and source priority;
- fact classification;
- dynamic-fact verification;
- document modes and reader path;
- factual and editorial quality requirements;
- security and compatibility caveats;
- honest reporting of blocked or untested behavior.

The adapter must not redefine these rules or maintain a second behavioral copy.

### Host-Independent Contract

The host-independent contract defines:

- canonical capabilities;
- normalized read-only capability classes;
- observable ordering constraints;
- allowed and disallowed variation;
- success, block, failure, and evaluation-error semantics.

Evaluation compares host behavior to this contract rather than to WorkBuddy tool names.

### Copilot Adapter

The Copilot adapter is responsible only for:

- presenting a valid Agent Skill entry compatible with the selected Copilot installation path;
- declaring the trial's host, language, invocation, and read-only boundaries;
- guiding Copilot to use available read-only capabilities for the canonical operations;
- prohibiting file writes and shell execution in the trial;
- referencing or including the minimum approved core material without creating an independently evolving behavioral fork;
- exposing version and provenance information needed for verification;
- documenting platform requirements, known limitations, and blocked behavior;
- failing closed when required capabilities are unavailable.

### Evaluation Assets

Evaluation assets remain outside the runtime adapter unless a later design proves a runtime resource is necessary. They are responsible for:

- portable test cases;
- normalized trace evidence;
- repeat-run records;
- compatibility-level decisions.

The runtime package should not contain test-only fixtures by default.

## Packaging Separation

The Copilot adapter must be an independent distribution artifact. It must not change:

- the source contents of either existing Skill;
- the current WorkBuddy archives;
- the current open-spec archives;
- the open-spec transformation that removes only `agent_created: true`;
- existing archive names, manifests, installation behavior, or checksum semantics;
- current release assets unless a later separately authorized release includes the adapter.

The implementation phase must add explicit regression checks proving this separation.

## Installation Model

The initial adapter should support a documented manual installation into one Copilot-supported Skill directory. The exact primary path will be selected during implementation after confirming the package layout and test harness.

Requirements:

- install into a new dedicated Skill directory;
- never overwrite an existing directory silently;
- allow inspection before activation;
- preserve source provenance and version information;
- recommend pinning the tested source revision for evaluation;
- keep the test installation isolated from personal sensitive repositories;
- provide removal or rollback by deleting only the dedicated installed adapter directory, subject to explicit user action.

Use of `gh skill` may be offered only when the tested CLI version and repository layout support the adapter. Because the feature is in public preview, manual directory installation must remain an available evaluation path unless a later decision changes this requirement.

## Permission Contract

The adapter must not pre-approve or request:

- shell or Bash;
- local write, edit, delete, move, or rename operations;
- credential, secret-store, or unrestricted filesystem access;
- unbounded connector or MCP access.

The Agent Skills `allowed-tools` field is experimental and is not a portable security boundary. The implementation may omit it when a precise, verified Copilot read-only value is unavailable. Written restrictions and host permission controls must remain explicit.

If Copilot cannot complete the research task without a prohibited capability, the correct result is `blocked`, not a request to broaden permissions during the trial.

## Version Model

### Core Version

`core_version` identifies the behavior contract inherited from `research-material-writer`. The initial value is:

```text
0.2.0-preview.1
```

A change to research requirements, boundaries, document modes, evidence classes, or output guarantees requires review as a core behavior change and follows the core Skill's Semantic Versioning policy.

### Adapter Version

`adapter_version` identifies Copilot-specific installation, mapping, packaging, or compatibility logic. The initial implementation should start at:

```text
0.1.0
```

The Agent Skills specification does not define a standard `adapter_version` field. The implementation must store it in a namespaced or project-owned metadata/manifest location that does not conflict with standard fields.

Adapter version changes follow these rules:

- patch: clarification or defect fix that does not change supported capability or permission scope;
- minor: backward-compatible addition to the adapter mapping, packaging, or supported tested Copilot version range;
- major: incompatible install, manifest, permission, capability, or compatibility-contract change.

### Version Identity

Every compatibility record must identify:

- core Skill name and `core_version`;
- `adapter_version`;
- repository source commit or tree identity;
- adapter package digest;
- host product and surface;
- VS Code and GitHub Copilot versions;
- test-set version;
- verification date;
- observed permission profile.

A compatibility result for one identity must not be generalized to another identity without rerunning the applicable tests.

## Provenance Contract

The adapter artifact must provide enough information to trace it to:

- the source repository;
- the source commit or tree;
- the core Skill version;
- the adapter version;
- the exact packaged file list;
- the artifact SHA-256;
- whether the source tree was dirty.

GitHub CLI may add installation provenance during `gh skill install`, but the repository's deterministic manifest remains the project-controlled evidence. CLI-added metadata must not silently change the core behavior or invalidate reproducibility checks.

## Compatibility Levels

### `Untested`

The package or design exists, but no applicable structural or host validation has completed.

### `Format Compatible`

The adapter passes the Agent Skills structural checks and applicable Copilot package/installation checks. This level does not claim task success or correct tool behavior.

### `Read-Only Verified`

The adapter successfully installs and completes the approved read-only workflow cases in the recorded Copilot environment, with no prohibited side effects. This level requires evidence for source retrieval, grounded output, and blocked behavior, but may be withheld if the full repeated critical set is incomplete.

### `Behavior Verified`

All critical host cases pass three of three independent runs under the recorded identity, with no grounding, boundary, or safety failure. The evaluation must confirm both normalized process behavior and final task completion.

### `Blocked`

A required host capability, permission profile, installation mechanism, or evaluation prerequisite is unavailable. The record must identify the missing condition and must not imply compatibility.

Compatibility levels are scoped evidence, not permanent certification.

## Change Classification

### Adapter-Only Change

A change is adapter-only when it affects:

- Copilot installation guidance;
- native-to-canonical capability mapping;
- adapter-specific metadata or manifest;
- tested host-version range;
- adapter packaging that leaves core and existing distributions unchanged.

It changes `adapter_version` and its tests, but not `core_version`.

### Core Behavior Change

A change is a core behavior change when it alters:

- research source priority;
- claim classes;
- dynamic-fact rules;
- document modes;
- required output quality;
- safety or permission boundaries;
- success or failure semantics shared across hosts.

It must not be introduced through an adapter PR.

### Distribution Contract Change

A change to existing WorkBuddy/open-spec archive content, name, transformation, manifest, installer, or release contract is outside the adapter phase. It requires separate scope, regression analysis, versioning, and release authorization.

## Maintenance And Cost Controls

To reduce long-term cost:

- maintain one core behavior source;
- keep adapter instructions limited to host differences;
- avoid duplicating large references when deterministic generation or inclusion from the same source can be verified;
- keep test fixtures outside runtime packages;
- add a host only after defining an owner, capability mapping, version identity, and repeatable test environment;
- expire or downgrade compatibility records when the tested host surface changes materially;
- prefer clear `Blocked` results over accumulating fallback branches for unsupported environments.

## Security Risks And Controls

| Risk | Required control |
|---|---|
| Third-party Skill contains hidden or malicious instructions | Require package preview and provenance verification before installation |
| Web content contains prompt injection | Treat retrieved content as untrusted evidence and preserve task/system priority |
| `allowed-tools` differs across hosts | Do not treat it as the sole enforcement mechanism |
| Shell permission is accidentally granted | Omit shell requirements and fail the trial on shell use |
| Adapter silently writes files | Define any write as a boundary failure and inspect host evidence |
| Host or CLI preview behavior changes | Record exact versions and rerun structural and behavioral tests |
| Adapter diverges from core | Use one authoritative core, version binding, and regression review |
| Compatibility claim outlives evidence | Bind claims to host/version/test identity and verification date |

## Adapter Acceptance Criteria

The adapter architecture is acceptable when:

- responsibilities among core, contract, adapter, and evaluation assets are non-overlapping;
- the adapter cannot broaden the approved read-only capability set by design;
- existing WorkBuddy and open-spec contracts remain unchanged;
- `core_version` and `adapter_version` have distinct ownership and change rules;
- provenance and compatibility records identify the exact source and environment;
- compatibility levels cannot be inferred from format validation alone;
- public-preview platform behavior is treated as versioned and revalidated;
- rollback affects only the dedicated adapter installation;
- implementation can proceed without a core behavior refactor.

## Official References

Consulted on 2026-11-01:

- [Agent Skills specification](https://agentskills.io/specification)
- [Adding agent skills for GitHub Copilot](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [`gh skill` manual](https://cli.github.com/manual/gh_skill)
