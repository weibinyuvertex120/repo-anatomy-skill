# Learning, Validation, And Feedback

Use this reference when the deliverable must help a reader understand a project and actually use it. Do not force the full learning loop into a news summary, pure reference page, or decision-only analysis unless the user also asks for onboarding or practical adoption.

## Learning Outcome

A successful result moves through five states:

```text
understand
-> reproduce
-> verify
-> transfer
-> decide
```

- **Understand:** the reader can explain the project's role, flow, and responsibility boundary.
- **Reproduce:** the reader can follow one safe path to the promised first result.
- **Verify:** the reader can distinguish the expected result, actual result, and failure signal.
- **Transfer:** the reader can complete a bounded variation without copying the original example.
- **Decide:** the reader can choose to adopt, trial, defer, or reject based on evidence and remaining gaps.

Do not describe example reproduction as independent mastery.

## Two-Layer Deliverable

### Understanding Map

Use the shared map from `project-type-profiles.md`. Keep it before commands and detailed architecture. It should let the reader answer:

- What problem does the project solve?
- What enters and leaves it?
- What important transformation or decision occurs?
- Where does it sit in the larger workflow?
- What does it not own?
- What will the first useful success look like?

### Practice Path

The practice path converts the map into action:

1. adoption goal and success artifact;
2. risk gate and stop conditions;
3. prerequisites and preflight;
4. one primary setup route;
5. first useful operation;
6. observable verification;
7. one material boundary check;
8. cleanup or rollback;
9. orientation, boundary, and transfer checks;
10. next adoption decision.

Keep detailed reference data and deep explanation outside the uninterrupted first path. Link or place them after the action when the output channel supports it.

## Verification Card

Use the following fields for consequential actions. Tiny steps may combine fields, but none of the information should disappear.

```text
Goal
Why now
Environment and entry point
Action or exact value
Expected observation
Actual result
Failure signal
Smallest correction
Cleanup or rollback
Evidence class and scope
```

Rules:

- `Expected observation` comes from evidence and is not an execution claim.
- `Actual result` appears only when the action was executed or the user reported a result.
- If execution is unavailable, mark the actual result `not run` and give the safest self-check.
- Put the common failure signal next to the action, not in a distant FAQ.
- Do not continue past a blocking failure in guided-run mode.
- Do not request broader permission merely to make the tutorial look complete.

## Interaction Modes

### One-Shot

Use when the user requests a standalone report or complete tutorial, or when the host cannot preserve a staged interaction.

The result should include:

- the understanding map;
- the full bounded practice path;
- expected observations and self-checks;
- explicit unexecuted or user-executed steps;
- a compact run-record template when feedback is useful.

Do not claim the user completed anything.

### Guided Run

Use when the user asks to be led through the project, when environment differences materially affect the path, or when actual user feedback is part of the goal.

Proceed through these stages:

1. **Brief:** confirm target task, reader experience, environment, risk, and project type.
2. **Preflight:** run or ask for only the checks needed before setup.
3. **First practice:** provide the next bounded verification card, not the entire tutorial at once.
4. **Observe:** ask for the actual output, state, or error; preserve exact evidence where safe.
5. **Diagnose:** classify the result and give the smallest correction.
6. **Boundary:** verify one important refusal, limitation, or failure mode.
7. **Transfer:** give a safe variation that tests independent use.
8. **Decision:** summarize completed, partial, blocked, and unverified areas, then recommend adopt, trial, defer, or reject.

Advance only when the current stage has enough evidence. Ask one focused question at a time when a user result is required.

## Three Learning Checks

### Orientation Check

Ask the reader to explain or select:

- what the project receives and produces;
- where it sits in the larger workflow;
- which responsibility belongs to the caller, host, operator, or external service;
- one situation where the project is unnecessary.

Use a concrete scenario rather than asking “Do you understand?”

### Boundary Check

Ask the reader to identify or safely observe one:

- unsupported platform or version;
- invalid input or documented error;
- denied permission or consent gate;
- unsafe, unsuitable, or prohibited use;
- quality, coverage, scale, or maintenance limit.

The check must not require a destructive, paid, production, privacy-invasive, or high-permission action.

### Transfer Task

Change exactly one material dimension of the first example:

- input;
- option or configuration;
- public API composition;
- endpoint or parameter;
- target file or workspace;
- model input and acceptance criterion;
- dataset entry;
- non-secret service configuration.

Ask the reader to predict the result before execution. Verify with the same evidence discipline as the first example. If the transfer task cannot run, mark it `not verified`; do not infer success from the original example.

## Result States

Use these task-result values consistently:

- `completed`: the required result and verification were observed;
- `partially_completed`: some required outcomes were observed, but a non-blocking part remains;
- `blocked`: a prerequisite, permission, source, environment, project failure, or safety condition prevents continuation;
- `not_verified`: instructions or evidence exist, but no actual result was observed.

Do not convert `blocked` or `not_verified` into success based on documentation alone.

## Feedback Record

When persistence is requested and allowed, use `evals/user-run-record.schema.json` or an equivalent host-native structure. Otherwise collect a compact summary in the response.

Record:

- Skill version and project type;
- reader role, experience, and target task;
- interaction mode;
- environment, project version, executed checks, and blocked checks;
- orientation, boundary, and transfer results;
- completed, partial, blocked, or unverified task state;
- failed step, completion time, help requests, and before/after confidence when known;
- adoption decision;
- categorized feedback.

Feedback categories:

- `factual_error`: a claim, version, command, or expected result is wrong;
- `missing_step`: required information or an action is absent;
- `environment_difference`: the path does not match the actual platform, version, or host;
- `hard_to_understand`: the information exists but the reader cannot form the intended model;
- `hard_to_find`: the reader cannot locate the needed information;
- `project_failure`: the project or dependency fails despite correct instructions;
- `insufficient_evidence`: the material asks for a conclusion not supported by available evidence;
- `other`: a described issue that does not fit the categories.

Never store credentials, secrets, personal data, proprietary input, or unnecessarily complete logs in the feedback record.

## Evaluation Model

Evaluate both outcome and process.

### Outcome

Check:

- task completion;
- correctness and evidence grounding;
- orientation, boundary, and transfer results;
- usefulness of the final adoption decision.

### Process

Check when observable:

- source and capability selection;
- command, tool, or parameter accuracy;
- result utilization;
- failure handling and stop behavior;
- unnecessary steps, retries, latency, and context cost.

Do not require one exact trajectory when several safe strategies can produce the correct outcome. Require exact steps only for safety, permission, compliance, or an invariant dependency.

## Evaluation Maintenance

- Start with a small set of real, high-value tasks.
- Keep capability evaluations challenging and regression evaluations near fully passing.
- Run multiple independent trials before making reliability claims about non-deterministic hosts.
- Preserve the available transcript or trace separately from the final outcome.
- Read failed traces to distinguish Agent failure, task ambiguity, grader defects, host limitations, and environment failures.
- Turn real user failures into regression cases after removing sensitive data.
- Use deterministic checks where possible, model judgment for semantic quality, and human review for calibration and high-impact decisions.
- Track completion, failure distribution, errors, time, tool or source calls, and user feedback rather than one aggregate score.

## Completion Gate

Before reporting a practical learning result, confirm:

- the understanding map precedes deep detail;
- the first path has one recommended route;
- consequential steps define expected observations and failure signals;
- actual results are distinguished from documented expectations;
- a safe boundary check exists or is marked blocked;
- orientation and transfer are checked or explicitly left to the user;
- feedback and unresolved gaps can be recorded without secrets;
- the conclusion reflects completed, partial, blocked, and unverified evidence.
