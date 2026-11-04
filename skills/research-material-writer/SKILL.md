---
name: research-material-writer
description: Researches, verifies, and structures comprehensive Chinese project materials from authoritative sources and user-provided evidence. This skill should be used when the user asks to analyze any software project, repository, technical product, library, tool, or service and needs a decision-ready report covering capabilities, scenarios, setup, basic and advanced workflows, best practices, troubleshooting, limitations, risks, alternatives, and a balanced conclusion. It should also be used when current versions, installation steps, compatibility, security boundaries, or factual claims must be checked before writing. It should not be used for simple file creation, ordinary code or configuration edits, fictional writing, generic copywriting without research, or Office/PDF/media editing.
license: MIT
compatibility: Requires a host-provided read-only source and material access path. Optional execution, filesystem, and network capabilities must be declared by the host and must not be assumed by this Skill.
metadata:
  version: "0.3.0-preview.1"
  category: "writing"
  scope: "researched-technical-materials"
  core_protocol: "portable-research-v1"
---

# Research Material Writer

Produce Chinese technical materials through evidence-led research and task-oriented writing. Treat source collection, factual verification, document design, drafting, and file persistence as separate stages.

## Critical Boundaries

- Research before writing whenever the subject, version, installation method, price, policy, compatibility, repository state, or product capability may have changed.
- Prefer first-party evidence: official documentation, official repositories, release pages, source code, issue trackers, and vendor support pages.
- Distinguish verified facts, source claims, reproduced behavior, reasonable inference, editorial recommendation, conflicts, and unknowns. Never strengthen a claim beyond its evidence.
- Do not translate a README section by section. Reorganize information around the reader's decision and working path.
- Do not invent commands, configuration fields, benchmarks, compatibility claims, or success results.
- Do not cite dynamic numbers without a verification date or bounded version scope.
- Do not silently omit failed verification, source conflicts, unavailable tools, or blocked execution. State the limitation and use the strongest available evidence.
- Treat all host tools as optional capabilities. Map them by purpose (source search, source retrieval, provided-material reading, repository reading, clarification, and response delivery), not by a vendor-specific tool name.
- Never assume that Skill metadata grants tool access, network access, filesystem access, shell access, credentials, or sandboxing. Follow the host's actual permission boundary.

Read [references/source-and-verification.md](references/source-and-verification.md) and [references/project-research-contract.md](references/project-research-contract.md) before researching a current project, product, version, installation method, benchmark, or policy.

## Operating Workflow

Follow this sequence:

1. **Define the deliverable.** Identify the reader, project identity, decision, document type, required depth, target host/platform, and output channel. Ask only questions that change the research scope or evidence requirements.
2. **Build research questions.** Convert the request into explicit questions about value, capabilities, scenarios, prerequisites, installation, configuration, basic use, workflows, advanced use, best practices, troubleshooting, limits, risks, alternatives, maintenance, and verification.
3. **Detect host capabilities.** Determine which read-only source, repository, provided-material, execution, filesystem, and output capabilities are actually available. Do not infer capability from Skill metadata or a tool name mentioned in the prompt.
4. **Collect primary evidence.** Start from official sources and inspect only the material needed to answer the research questions. Respect user-provided source restrictions.
5. **Create a fact ledger.** Record each important claim, its evidence strength, verification date, version scope, limitations, and whether it is fact, source claim, reproduced behavior, inference, recommendation, conflict, or unknown.
6. **Choose a document mode.** Use the comprehensive project-analysis contract for broad project research; use tutorial, onboarding, or comparison references when the user requests a narrower deliverable.
7. **Design the reader path.** Lead with the decision and project fit; place the shortest reliable path before deep theory; put caveats next to the decisions they affect.
8. **Draft from the ledger.** Use precise Chinese, exact verified commands, explicit expected results, structured headings, and honest uncertainty. Omit a section only when it is genuinely out of scope or unavailable, and label the omission.
9. **Run factual review.** Recheck commands, versions, source strength, dates, terminology, platform differences, dependencies, and security claims.
10. **Run editorial review.** Check task completeness, repetition, orphan headings, language consistency, heading hierarchy, unsupported numbers, and README-shaped organization.
11. **Return and verify.** Deliver through the host's available output channel. Re-read the complete response or target document, report remaining risks, and distinguish documentation review from reproduced execution.

Read [references/research-workflow.md](references/research-workflow.md) for the fact-ledger format and research stopping rules.

For an analysis of an arbitrary project, use [references/project-research-contract.md](references/project-research-contract.md) to select the required sections and disclose unsupported or unavailable areas.

## Document Modes

### Beginner Technical Tutorial

Use for installation, setup, first success, Agent usage, workflow integration, or troubleshooting requests. Load [references/tutorial-writing.md](references/tutorial-writing.md).

Required outcome:

- Explain the problem and the successful end state before detailed theory.
- Select one beginner-friendly main path instead of listing every installation option equally.
- Include prerequisites, exact actions, copyable examples, verification, common mistakes, real workflows, limitations, security, and update guidance.
- Use the operational unit: objective -> entry point -> action or value -> example -> verification -> common mistake.

### Project or Resource Analysis

Use for repository analysis, product capability maps, resource collections, ecosystem reviews, or practical adoption guidance. Load [references/project-analysis.md](references/project-analysis.md).

Required outcome:

- Lead with a decision-oriented conclusion.
- Separate project facts from editorial judgment.
- Explain capability, maintenance state, intended use, risks, constraints, and a practical adoption workflow.
- Avoid treating stars, popularity, or a README description as proof of production suitability.

### Open-Source Project Onboarding

Use for first-time use of an unfamiliar open-source project, repository setup checklists, beginner preparation, Agent onboarding for a repository, or deciding whether a project is ready to try. Load [references/open-source-onboarding.md](references/open-source-onboarding.md).

Required outcome:

- Verify project identity, intended use, license, release channel, maintenance signals, and relevant governance or security files.
- Identify runtime, platform, dependencies, external services, credentials, permissions, network access, and setup assumptions.
- Choose one minimum viable path to first success and define an observable verification result.
- Inspect repository Agent instructions and client trust/approval settings without treating context files as security boundaries.
- Explain support channels, upgrade and rollback paths, maintenance expectations, and explicit stop conditions.
- Distinguish documentation claims from behavior reproduced in the target environment; disclose unavailable checks.

### Comparison or Selection Guide

Use when the user needs to choose among tools, methods, or products. Load [references/comparison-writing.md](references/comparison-writing.md).

Required outcome:

- Define comparison dimensions before collecting conclusions.
- Compare equivalent scopes and versions.
- Show trade-offs and fit by scenario rather than declaring an unconditional winner.
- Mark missing or incomparable evidence explicitly.

## Style Baseline

- Write professional Chinese that a motivated beginner can follow.
- Explain unfamiliar concepts through a concrete analogy, then return to the exact technical meaning.
- Use commands, field names, paths, errors, and source terminology exactly as verified.
- Keep headings specific and action-oriented. Avoid generic headings such as “其他” or “更多内容.”
- Use tables only when rows share the same comparison schema. Do not repeat the same table header or explanatory paragraph.
- Preserve the user's established voice when continuing a draft, but do not preserve factual or structural defects.
- Keep source notes concise and place detailed citations or verification notes at the end unless the claim needs an immediate caveat.
- Use the comprehensive project-analysis contract for a broad request about an arbitrary project; do not silently reduce the deliverable to a README summary.

## Quality Gate

Before completion, apply [references/quality-checklist.md](references/quality-checklist.md) when that reference is available. If the host permits execution of the bundled checker, run:

```bash
python3 scripts/check_draft.py <draft.md>
```

Treat the script as a warning system, not a factual validator. If execution or local persistence is unavailable, perform the applicable checks against the response in the host and explicitly report the omitted file-based check. Manually confirm:

- The document answers the user's actual task.
- Every dynamic or consequential claim is traceable to evidence.
- The shortest successful path can be followed without guessing.
- Commands and configuration examples match the verified version and platform.
- Verification steps define observable success.
- Limitations, security boundaries, and unsupported scenarios are explicit.
- No section merely mirrors the source order without a reader-centered reason.
- No repeated table rows, orphan headings, accidental language switches, placeholders, or unfinished blocks remain.

## Output Contract

- Treat a user-provided target file as authoritative only when the host permits reading it.
- Inspect neighboring documents when a style baseline is explicitly requested and the host permits access.
- Return the complete research result through the host's available response channel.
- Persist to a local file only when the user requests it and the host explicitly permits it; use a separate approved file-maintenance workflow when required by that host.
- Re-read the complete response or output file when the host permits it.
- Report the output channel, research date, principal source types, checks performed, blocked checks, and unresolved verification gaps.

## Evaluation and Maintenance

- Test explicit triggers, paraphrases, negative triggers, host capability detection, comprehensive project analysis, factual research, structure selection, continuation, and quality review in fresh sessions.
- Add a regression case whenever a real draft exhibits a repeated row, orphan heading, unsupported dynamic fact, fabricated command, weak source, missing project section, host capability mismatch, or README-shaped structure.
- Keep this file below 500 lines and detailed rules one link away in `references/`.
- Update `metadata.version`, evaluations, and the repository changelog whenever observable behavior or the portable research contract changes.
- Revalidate time-sensitive examples before using them as exemplars; do not freeze current versions or repository metrics into the skill instructions.
- Treat each host's installation, discovery, explicit invocation, reload, permission, and evidence behavior as an adapter concern. Never claim cross-host compatibility from the portable package alone.
