# Research Material Writer Copilot Read-Only Capability Baseline

Verification date: 2026-11-01

This document records the behavior that must remain stable before creating a GitHub Copilot VS Code Agent adapter for `research-material-writer`. It is an architecture baseline, not a compatibility claim and not an implementation specification.

## Decision Scope

The first compatibility trial is intentionally limited to:

- Skill: `research-material-writer` `0.2.0-preview.1`;
- host surface: GitHub Copilot Agent Mode in Visual Studio Code;
- invocation: explicit user request to use the installed Skill;
- output language: Chinese;
- operation class: read-only research, analysis, planning, and response generation;
- evidence: official or user-provided sources;
- persistence: no local file creation or modification;
- distribution: a future independent Copilot adapter package;
- compatibility promise: none until the defined host evaluation passes.

The trial does not include automatic semantic routing, local draft persistence, shell execution, multi-language output, `workspace-file-maintainer`, Copilot CLI, Copilot cloud agent, Copilot code review, Claude Code, Codex, or a new public release.

## Evidence Base

The baseline is derived from:

- `skills/research-material-writer/SKILL.md`;
- all references linked directly from that file;
- `evals/research-trigger-cases.json`;
- `evals/research-functional-cases.md`;
- `evals/acceptance-results.md`;
- the Agent Skills specification, checked on 2026-11-01;
- GitHub documentation for Agent Skills in Copilot, checked on 2026-11-01.

The Agent Skills specification defines the package shape, frontmatter, relative resource references, and progressive disclosure. It does not guarantee equivalent tool permissions, runtime behavior, or automatic activation across clients. GitHub documents that Copilot selects Skills from their descriptions and injects the selected `SKILL.md` into context. GitHub also warns that third-party Skills are not verified and that pre-approved shell access increases risk.

## Existing Capability Baseline

### Research Brief And Task Fit

When explicitly invoked, the Skill must identify:

- the intended reader;
- the decision or working outcome;
- the requested document or analysis mode;
- the required depth and environment;
- the relevant version or date scope;
- the expected output form;
- the facts most likely to have changed.

The read-only trial may return this analysis in the conversation. It must not create or modify a local file.

### Primary-Source Research

The Skill must:

- research current, consequential facts before presenting them as current;
- prefer official documentation, repositories, releases, source code, schemas, issue discussions, standards, and original papers;
- use community material only for discovery, failure reports, or user experience when stronger evidence is unavailable;
- respect a user instruction that limits research to supplied sources;
- disclose when current evidence cannot be obtained.

Research is not required when the user supplies sufficient authoritative material and explicitly prohibits additional search. The limitation and date scope must remain visible.

### Evidence Classification

Consequential claims must be distinguishable as one of:

- verified fact;
- source claim;
- reproduced behavior;
- inference;
- recommendation;
- conflict;
- unknown.

The Skill must not upgrade a source claim into independently verified fact or present an undocumented inference as project behavior.

### Dynamic Facts

Versions, releases, installation commands, dependencies, supported platforms, policies, maintainers, service availability, and similar changing facts must be checked against a current authoritative source. Material dynamic facts must include an exact verification date or an equivalent clear time scope.

The Skill must not claim that an item is the latest without checking the official release or update channel.

### Research Questions And Reader Path

The Skill must convert the request into decision-relevant questions covering applicable topics such as value, prerequisites, setup, operation, verification, workflow placement, limitations, security, maintenance, and failure modes.

It must research in source order but present conclusions in reader order. A tutorial or onboarding response should prioritize the problem, successful outcome, prerequisites, shortest reliable path, observable verification, workflow fit, explanation, limits, and troubleshooting rather than reproduce README order.

### Document Modes

The existing Skill supports four modes:

- beginner technical tutorial;
- project or resource analysis;
- open-source project onboarding;
- comparison or selection guidance.

The trial must preserve the mode-specific quality rules that apply to the request. It must not add a new document mode.

### Command And Runtime Claims

When the response includes commands or configuration examples, the Skill must distinguish:

- behavior confirmed by official documentation;
- behavior confirmed by source inspection;
- behavior reproduced in the current environment;
- behavior that could not be executed.

It must not invent commands, fields, output, benchmarks, compatibility, or successful runtime results. If execution is unavailable, it may provide documented expected behavior only when clearly labeled.

The read-only Copilot trial does not require command execution. A request that requires execution may be answered with a bounded plan or marked blocked; it must not be reported as executed.

### Security And Compatibility Boundaries

The Skill must keep instructions separate from enforcement. Skill text, repository instructions, `allowed-tools`, and client context are not operating-system sandboxes, IAM controls, network policy, credential protection, or command authorization.

When relevant, the response must identify:

- filesystem, network, shell, plugin, hook, MCP, credential, and auto-approval requirements;
- untrusted-input or prompt-injection exposure;
- client-specific limitations;
- missing verification that changes adoption risk.

The trial must not request or use local write, edit, or shell capabilities.

### Editorial Integrity

The response must:

- answer the user's actual task;
- state its conclusion or successful outcome early;
- keep heading hierarchy coherent;
- avoid duplicated rows, paragraphs, commands, empty headings, unfinished placeholders, and accidental language changes;
- use tables only when rows share a real schema;
- preserve an established series voice without copying stale facts or structural defects;
- end with a bounded decision or next action rather than a generic summary.

The bundled Markdown checker is heuristic evidence only. In a read-only conversational run, inability to execute it must be disclosed when the request asks for a validated persisted draft. It must not be simulated.

### Honest Completion Reporting

The final response must disclose:

- sources or source classes used;
- verification date for material dynamic facts;
- what was reproduced, reviewed only, blocked, or not tested;
- important remaining uncertainty;
- the compatibility and environment scope of recommendations.

A polished answer is not sufficient if the evidence scope is misleading.

## Allowed Host Variation

A future Copilot adapter may vary in these areas without changing the core capability:

- native tool names and parameter schemas;
- exact order of independent read-only searches;
- number of searches needed to resolve the same fact;
- wording, heading labels, and non-material formatting;
- whether a source is opened directly or found through search;
- whether the host presents permission prompts for read-only tools;
- internal context-loading details that do not change the result or boundaries.

Variation is acceptable only when required evidence, safety boundaries, and final task completion remain equivalent.

## Prohibited Regression

The adapter must not:

- silently broaden the trial into file writing or shell execution;
- claim automatic routing reliability;
- remove primary-source preference or dynamic-fact verification;
- omit evidence classification or blocked-verification disclosure;
- treat `allowed-tools` as a portable security boundary;
- use a weaker source to override a stronger current source without explaining the conflict;
- fabricate successful execution;
- claim compatibility for Copilot surfaces that were not tested;
- change the source WorkBuddy or open-spec packages;
- copy the complete core Skill into an independently maintained behavioral fork.

## Existing Verification And Unknowns

### Verified In The Existing Project

The repository currently records:

- structural validation of the source Skill and open-spec package;
- explicit-invocation WorkBuddy observations;
- trigger-case schema coverage;
- eight functional evaluation definitions;
- project-analysis and onboarding narrative evaluations;
- deterministic packaging and installation checks;
- Markdown checker regression tests.

### Not Yet Verified For Copilot

The following remain unknown until real host evaluation:

- Copilot VS Code Agent's interpretation of the current description;
- the exact read-only tools available in the user's Copilot environment;
- source retrieval and result-grounding behavior;
- adherence to fact classes and verification dates;
- behavior when search is prohibited or unavailable;
- behavior when the task implies a file output but the trial forbids writing;
- repeated-run reliability;
- prompt-injection resistance for researched web content;
- automatic Skill selection;
- equivalence with WorkBuddy behavior.

No Copilot compatibility level above untested may be claimed from this baseline alone.

## Architecture Consequences

The remaining architecture work must use this baseline to define:

1. canonical host-independent capabilities and failure states;
2. a Copilot-specific mapping that exposes only the approved read-only subset;
3. separate core and adapter versions;
4. an evaluation schema that tests results and normalized tool behavior;
5. compatibility levels that distinguish structural installation from repeated behavioral success.

Any proposal that requires changing the existing core behavior or package contract is outside this phase and requires a separately approved scope.

## Official References

Consulted on 2026-11-01:

- [Agent Skills specification](https://agentskills.io/specification)
- [Adding agent skills for GitHub Copilot](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
