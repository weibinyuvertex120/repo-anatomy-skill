---
name: research-material-writer
description: Researches, verifies, and structures comprehensive Chinese project materials from authoritative sources and user-provided evidence. This skill should be used when the user asks to analyze any software project, repository, technical product, library, tool, or service and needs a decision-ready report covering capabilities, scenarios, setup, basic and advanced workflows, best practices, troubleshooting, limitations, risks, alternatives, and a balanced conclusion. It should also be used when current versions, installation steps, compatibility, security boundaries, or factual claims must be checked before writing. It should not be used for simple file creation, ordinary code or configuration edits, fictional writing, generic copywriting without research, or Office/PDF/media editing.
license: MIT
compatibility: Requires a host-provided read-only source and material access path. Optional execution, filesystem, and network capabilities must be declared by the host and must not be assumed by this Skill.
metadata:
  version: "0.4.0-preview.1"
  category: "writing"
  scope: "researched-technical-materials"
  core_protocol: "portable-research-v1"
  learning_protocol: "portable-project-learning-v1"
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

Read [references/source-and-verification.md](references/source-and-verification.md) and [references/project-research-contract.md](references/project-research-contract.md) before researching a current project, product, version, installation method, benchmark, or policy. Read [references/project-type-profiles.md](references/project-type-profiles.md) when the result must explain how a project works or guide adoption. Read [references/learning-validation-feedback.md](references/learning-validation-feedback.md) when the reader must practice, verify, transfer, or report feedback.

## Operating Workflow

Follow this sequence:

1. **Define the deliverable.** Identify the reader, project identity, decision, target task, document type, required depth, target host/platform, interaction mode, and output channel. Ask only questions that change the research scope, safety, project type, or evidence requirements.
2. **Classify the project.** Select one primary project type from the type profiles and at most one secondary type. Base the choice on the interface the reader operates, not every component in the repository.
3. **Build research questions.** Convert the request into explicit shared and type-specific questions about value, input, processing, output, components, flow, scenarios, prerequisites, setup, operation, workflows, limits, risks, alternatives, maintenance, and verification.
4. **Detect host capabilities.** Determine which read-only source, repository, provided-material, execution, filesystem, interaction, and output capabilities are actually available. Do not infer capability from Skill metadata or a tool name mentioned in the prompt.
5. **Collect primary evidence.** Start from official sources and inspect only the material needed to answer the research questions. Use the type profile to locate authoritative artifacts. Respect user-provided source restrictions.
6. **Create a fact ledger.** Record each important claim, its evidence strength, verification date, version scope, limitations, and whether it is fact, source claim, reproduced behavior, inference, recommendation, conflict, or unknown.
7. **Choose a document and interaction mode.** Use the comprehensive contract for broad research; use tutorial, onboarding, or comparison references for narrower work. Choose one-shot delivery or a guided run when practical adoption and user-reported results matter.
8. **Design the reader path.** Lead with the decision and project fit. Build an understanding map before detailed setup, then a practice path with one reliable route. Keep reference and deep explanation from interrupting the first-use sequence.
9. **Draft from the ledger.** Use precise Chinese, exact verified commands, verification cards for consequential actions, explicit expected and actual results, structured headings, and honest uncertainty. Omit a section only when it is genuinely out of scope or unavailable, and label the omission.
10. **Verify learning and behavior.** When practical use is in scope, include an orientation check, one safe boundary check, and a transfer task. Record completion as completed, partially completed, blocked, or not verified; reproducing the example alone is not independent use.
11. **Run factual and process review.** Recheck commands, versions, sources, dates, terminology, platform differences, dependencies, permissions, result utilization, failure handling, and security claims. Do not require one exact trajectory unless safety or an invariant dependency requires it.
12. **Run editorial review.** Check task completeness, repetition, orphan headings, language consistency, hierarchy, unsupported numbers, mixed document intents, and README-shaped organization.
13. **Return, verify, and capture feedback.** Deliver through the host's available channel. Re-read the complete response or target document, report executed and blocked checks, distinguish documentation from reproduced execution, and record structured user feedback when requested and permitted.

Read [references/research-workflow.md](references/research-workflow.md) for the fact-ledger format and research stopping rules.

For an analysis of an arbitrary project, use [references/project-research-contract.md](references/project-research-contract.md) to select the required sections and disclose unsupported or unavailable areas.

## Project Understanding And Practice

When the reader must understand or try the project:

- Route the work through one primary project type and at most one secondary type.
- Start with an **understanding map**: problem, input, processing, output, core components, data or control flow, responsibility boundary, and first observable success.
- Follow with a **practice path**: risk gate, prerequisites, one setup route, first useful operation, verification, boundary check, cleanup, and next decision.
- For consequential steps, state the goal, environment, action, expected observation, actual result, failure signal, smallest correction, rollback, and evidence scope.
- Use a **guided run** when the user wants staged help or actual environment feedback; stop at blocking results and never invent user completion.
- Test understanding with orientation, boundary, and **transfer task** checks. A transfer task changes one material dimension of the example and verifies the result independently.
- Record user outcomes and feedback only when requested and permitted. Never persist secrets, credentials, personal data, or unnecessarily complete logs.

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
- The primary project type and type-specific evidence needs are explicit when project understanding is in scope.
- The understanding map explains input, processing, output, flow, responsibility, and first success without becoming a full reference.
- The shortest successful path can be followed without guessing.
- Commands and configuration examples match the verified version and platform.
- Consequential steps define expected observations, actual results or `not run`, failure signals, and recovery.
- Verification steps define observable success and at least one material boundary.
- Orientation and transfer are checked or explicitly left unverified when practical learning is in scope.
- Limitations, security boundaries, and unsupported scenarios are explicit.
- No section merely mirrors the source order without a reader-centered reason.
- No repeated table rows, orphan headings, accidental language switches, placeholders, or unfinished blocks remain.

## Output Contract

- Treat a user-provided target file as authoritative only when the host permits reading it.
- Inspect neighboring documents when a style baseline is explicitly requested and the host permits access.
- Return the complete research result through the host's available response channel.
- Persist to a local file only when the user requests it and the host explicitly permits it; use a separate approved file-maintenance workflow when required by that host.
- Re-read the complete response or output file when the host permits it.
- Report the output channel, research date, primary project type, principal source types, interaction mode, checks performed, blocked checks, learning checks when applicable, and unresolved verification gaps.

## Evaluation and Maintenance

- Test explicit triggers, paraphrases, negative triggers, host capability detection, project-type routing, comprehensive analysis, practical learning, guided runs, feedback capture, factual research, structure selection, continuation, and quality review in fresh sessions.
- Add a regression case whenever a real run exhibits a repeated row, orphan heading, unsupported dynamic fact, fabricated command, weak source, wrong project type, missing understanding or practice stage, missing boundary or transfer check, host capability mismatch, user-blocking documentation defect, or README-shaped structure.
- Keep this file below 500 lines and detailed rules one link away in `references/`.
- Update `metadata.version`, evaluations, and the repository changelog whenever observable behavior or the portable research contract changes.
- Revalidate time-sensitive examples before using them as exemplars; do not freeze current versions or repository metrics into the skill instructions.
- Treat each host's installation, discovery, explicit invocation, reload, permission, and evidence behavior as an adapter concern. Never claim cross-host compatibility from the portable package alone.
