# Quality Checklist

## Deliverable Fit

- The document type matches the user's decision or working goal.
- The reader and assumed knowledge are clear.
- The opening states the value, conclusion, or successful result.
- The document can stand alone without the research transcript.

## Evidence

- Consequential claims are supported by appropriate sources.
- Current versions, commands, policies, metrics, and compatibility were checked recently.
- Project claims are not presented as independent proof.
- Inference and recommendation are identified as such.
- Failed or partial verification is disclosed.

## Task Completeness

For tutorials:

- Prerequisites, main path, first success, verification, workflow, limits, security, and troubleshooting are present.

For project analysis:

- Current state, capability map, adoption workflow, maintenance, risks, fit, and non-fit are present.

For open-source project onboarding:

- Project purpose, intended user, and unsuitable use cases are explicit.
- License, release/package source, version scope, and maintenance signals are checked and dated where dynamic.
- Runtime, platform, dependency, service, credential, permission, and network prerequisites are stated.
- One minimum successful setup path is actionable and has observable verification.
- Repository governance and security entry points are checked, including `LICENSE`, `SECURITY.md`, contribution guidance, and support channels where available.
- Agent instruction files and execution permissions are assessed separately; context instructions are not described as a sandbox or security boundary.
- MCP servers, hooks, plugins, auto-approval, network access, and secret exposure are considered when relevant.
- Upgrade, rollback, issue/community help, and explicit stop-or-defer conditions are included.
- Scorecard or similar repository-health ratings are treated as signals, not certification or proof of safety.
- Documentation claims, source inspection, and locally reproduced behavior are clearly distinguished.

For comparisons:

- Comparable scope, decision dimensions, evidence gaps, trade-offs, and scenario recommendations are present.

## Editorial Integrity

- Heading hierarchy is coherent.
- No heading is empty or followed immediately by a same-level heading.
- No table header, row, paragraph, or command block is accidentally duplicated.
- Heading language is consistent unless a source term must remain in English.
- Terms, product names, versions, and paths are consistent.
- Tables have a real comparison schema and do not hide caveats.
- Code fences are balanced and language labels are appropriate.
- No TODO, TBD, placeholder, template instruction, or unfinished sentence remains.

## Reader Experience

- Actions appear before deep theory.
- One main path is visibly primary.
- Commands are copyable and include execution context.
- Verification defines observable success.
- Common mistakes are placed near the relevant action.
- Advanced options do not interrupt the beginner path.
- The ending gives a bounded conclusion or next decision, not a generic summary.

## Final File Check

- Re-read the written file from disk.
- Confirm the requested path and filename.
- Confirm no unrelated file was changed.
- Run `scripts/check_draft.py` and investigate warnings.
- Report research date, output path, verification performed, and remaining uncertainty.
