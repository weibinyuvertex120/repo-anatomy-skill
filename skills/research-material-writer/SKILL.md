---
name: research-material-writer
description: Researches, verifies, structures, and writes high-quality Chinese technical materials from primary sources and existing drafts. This skill should be used when the user asks to study a GitHub project or technical product and produce a beginner tutorial, first-time open-source project onboarding, repository setup checklist, Agent repository onboarding, project analysis, comparison, selection guide, research note, or a continuation that must preserve an established writing style. It should also be used when current versions, installation steps, limitations, security boundaries, or factual claims must be checked before writing. It should not be used for simple file creation, ordinary code or configuration edits, fictional writing, generic copywriting without research, or Office/PDF/media editing.
license: MIT
compatibility: Requires web research or user-provided source access plus local Read, Write, Edit, Glob, Grep, and Bash tools. Use a dedicated file-maintenance skill or equivalent conservative workflow for final local writes.
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
metadata:
  version: "0.2.0-preview.1"
  category: "writing"
  scope: "researched-technical-materials"
agent_created: true
---

# Research Material Writer

Produce Chinese technical materials through evidence-led research and task-oriented writing. Treat source collection, factual verification, document design, drafting, and file persistence as separate stages.

## Critical Boundaries

- Research before writing whenever the subject, version, installation method, price, policy, compatibility, repository state, or product capability may have changed.
- Prefer first-party evidence: official documentation, official repositories, release pages, source code, issue trackers, and vendor support pages.
- Distinguish verified facts, source claims, reasonable inference, and editorial recommendation. Never strengthen a claim beyond its evidence.
- Do not translate a README section by section. Reorganize information around the reader's task and decision path.
- Do not invent commands, configuration fields, benchmarks, compatibility claims, or success results.
- Do not cite dynamic numbers without a verification date.
- Do not silently omit failed verification. State the limitation and use the strongest available evidence.
- Do not use this skill as a substitute for ordinary file editing. Delegate final persistence to `workspace-file-maintainer` or apply its inspect-edit-re-read discipline.

Read [references/source-and-verification.md](references/source-and-verification.md) before researching a current project, product, version, installation method, benchmark, or policy.

## Operating Workflow

Follow this sequence:

1. **Define the deliverable.** Identify the reader, document type, intended decision or working result, required depth, output location, and existing style baseline.
2. **Build research questions.** Convert the request into explicit questions about value, prerequisites, setup, operation, verification, limits, safety, maintenance, and failure modes.
3. **Collect primary evidence.** Start from official sources and inspect only the material needed to answer the research questions.
4. **Create a fact ledger.** Record each important claim, its evidence strength, verification date, version scope, limitations, and whether it is fact, inference, or recommendation.
5. **Choose a document mode.** Use tutorial, open-source onboarding, project analysis, or comparison and selection guidance. Load the matching reference before outlining.
6. **Design the reader path.** Lead with the problem, outcome, or conclusion; place action before theory; put caveats next to the decisions they affect.
7. **Draft from the ledger.** Use precise Chinese, concrete examples, copyable commands, explicit expected results, and honest uncertainty.
8. **Run factual review.** Recheck commands, versions, source strength, dates, terminology, platform differences, and security claims.
9. **Run editorial review.** Check task completeness, repetition, orphan headings, language consistency, heading hierarchy, unsupported numbers, and README-shaped organization.
10. **Persist and verify.** Write the requested file conservatively, re-read it, run the bundled draft checker when applicable, and report remaining risks.

Read [references/research-workflow.md](references/research-workflow.md) for the fact-ledger format and research stopping rules.

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

## Quality Gate

Before completion, apply [references/quality-checklist.md](references/quality-checklist.md) and run:

```bash
python3 scripts/check_draft.py <draft.md>
```

Treat the script as a warning system, not a factual validator. Manually confirm:

- The document answers the user's actual task.
- Every dynamic or consequential claim is traceable to evidence.
- The shortest successful path can be followed without guessing.
- Commands and configuration examples match the verified version and platform.
- Verification steps define observable success.
- Limitations, security boundaries, and unsupported scenarios are explicit.
- No section merely mirrors the source order without a reader-centered reason.
- No repeated table rows, orphan headings, accidental language switches, placeholders, or unfinished blocks remain.

## Persistence Contract

- Treat the current target file as the source of truth when continuing earlier work.
- Inspect neighboring documents when matching a series style.
- Apply the smallest file change that satisfies the writing task.
- Re-read the complete new file or all modified sections.
- Report the output path, research date, principal source types, checks performed, and unresolved verification gaps.

## Evaluation and Maintenance

- Test explicit triggers, paraphrases, negative triggers, factual research, structure selection, continuation, and quality review in fresh sessions.
- Add a regression case whenever a real draft exhibits a repeated row, orphan heading, unsupported dynamic fact, fabricated command, weak source, or README-shaped structure.
- Keep this file below 500 lines and detailed rules one link away in `references/`.
- Update `metadata.version`, evaluations, and the repository changelog whenever behavior changes.
- Revalidate time-sensitive examples before using them as exemplars; do not freeze current versions or repository metrics into the skill instructions.
