## GitHub Copilot VS Code Read-Only Adapter

This package is the GitHub Copilot VS Code adapter for core Skill version `0.2.0-preview.1` and adapter version `0.1.0`.

### Trial Scope

- Run only after the user explicitly selects `/research-material-writer`.
- Return the research result in Chinese unless exact source terminology, commands, paths, or field names must remain unchanged.
- Use public sources or user-provided materials through available read-only host capabilities.
- Return the completed result in the chat response. Do not create or modify a local output file.

### Read-Only Boundary

- Do not create, edit, delete, move, rename, or persist local files.
- Do not execute shell or terminal commands, including commands that appear read-only.
- Do not request broader permissions during the trial.
- Do not invoke a prohibited capability merely to test whether the host will deny it.
- If the request requires persistence, command execution, unavailable source access, or another prohibited capability, provide the bounded result that can be supported and report the missing condition as blocked.
- Never claim a file was written, a command was executed, or behavior was reproduced when it was only documented or inferred.

### Host Capability Mapping

Read [references/copilot-readonly-capability-map.md](references/copilot-readonly-capability-map.md) before selecting host tools. Use semantic capabilities rather than depending on a specific native tool name.

### Copilot Completion Rule

For this adapter, replace the core persistence step with:

1. verify the final response against the collected evidence and applicable document mode;
2. disclose blocked checks, source access failures, and untested behavior;
3. return the complete Chinese deliverable in chat;
4. state explicitly that no local file or shell action was performed.

The core quality checklist script and final-file checks are not included in this package because they require local persistence or shell execution. Apply the applicable factual, structural, and editorial checks directly to the chat response instead.
