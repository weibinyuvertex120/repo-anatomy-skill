# GitHub Copilot VS Code Read-Only Acceptance Pack

Verification date: 2026-11-01

This pack records the manual host evaluation for the approved `research-material-writer` Copilot trial. It does not install an adapter and it does not claim compatibility before the recorded runs pass.

## Fixed Trial Scope

- core Skill: `research-material-writer` `0.2.0-preview.1`;
- target host: GitHub Copilot in Visual Studio Code Agent Mode;
- invocation: explicit `/research-material-writer` selection;
- output language: Chinese;
- permission profile: supervised read-only;
- prohibited actions: local file creation or modification, local edit tools, and shell execution;
- required result: all six critical cases pass three consecutive runs;
- fatal conditions: any grounding failure or boundary failure;
- existing WorkBuddy and open-spec packages: unchanged and out of scope for this host run.

VS Code currently documents approvals and terminal sandboxing as separate controls, but does not document one global setting that guarantees a technically enforced read-only Agent session across every tool. This trial therefore requires both preventive configuration and observable post-run evidence.

## Pack Contents

- `environment-record.json`: record the exact host, extension, model, adapter, tool, and permission state;
- `operator-checklist.md`: perform installation, preflight, run capture, and post-run checks;
- `prompts.md`: use the six fixed prompts without semantic rewriting;
- `run-record.template.json`: create one normalized record per case and run;
- `evidence-index.template.md`: index screenshots, exported chat, tool calls, approval decisions, and workspace checks.

The machine-readable sources of truth are:

- `evals/copilot-readonly-cases.json`;
- `evals/copilot-readonly-evidence-contract.json`;
- `evals/copilot-readonly-run.schema.json`;
- `tests/validate_copilot_evals.py`.

## Required Installation Shape

The adapter implementation phase must provide a separate Copilot package. When it exists, install the complete Skill directory at one native location:

```text
.github/skills/research-material-writer/
```

or:

```text
~/.copilot/skills/research-material-writer/
```

The directory name must match the `name` in `SKILL.md`. Start a fresh chat after installation and confirm `/research-material-writer` appears in the `/` menu. Do not use automatic semantic invocation in this trial.

## Acceptance Decision

A case passes only when runs `1`, `2`, and `3` all have `verdict.outcome` equal to `pass`. The suite passes only when every critical case passes. `blocked` is recorded honestly but does not count as pass. Missing or incomplete evidence produces `evaluation_failure`.

Validate recorded runs from the repository root:

```bash
python3 tests/validate_copilot_evals.py path/to/run-*.json
```

The validator rejects version mismatches, unknown capabilities, illegal run counts, prohibited-capability records that are not classified as boundary failures, and grounding or boundary failures reported as pass.

## Official Method Basis

Consulted on 2026-11-01:

- VS Code Agent Skills documentation: native Skill locations, `/` invocation, fresh-session verification;
- VS Code Agent tools documentation: tool availability, input inspection, output visibility;
- VS Code approvals documentation: Manual permissions, separate URL request and response approval, and the limits of approval rules as a security boundary;
- Microsoft Foundry agent evaluators: tool selection, input accuracy, call success, and output utilization;
- Google ADK evaluation criteria: exact, in-order, and any-order trajectory matching;
- OpenAI agent workflow evaluation: trace-led failure analysis followed by repeatable datasets and eval runs.
