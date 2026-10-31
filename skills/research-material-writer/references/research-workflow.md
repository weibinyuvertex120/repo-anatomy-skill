# Research Workflow

## Define the Research Brief

Record:

- Reader and existing knowledge.
- Intended outcome or decision.
- Document mode and expected depth.
- Required platforms, versions, or environments.
- Output path and style baseline.
- Facts that are likely to change.

## Build Research Questions

Use these categories as applicable:

- What problem does the subject solve?
- What does success look like?
- Who should and should not use it?
- What must be installed, configured, or authorized?
- What is the shortest reliable path to a working result?
- How is success verified?
- Where does it fit in a real workflow?
- What are the security, privacy, compatibility, and maintenance limits?
- What commonly fails and how is it diagnosed?

## Maintain a Fact Ledger

Use a compact working table:

| Claim | Source | Verified date | Scope/version | Class | Caveat |
|---|---|---|---|---|---|
| Example capability | Official docs | YYYY-MM-DD | vX.Y | verified fact | Platform limitation |

The ledger is working material, not automatically part of the final document.

## Separate Evidence From Narrative

Research in source order, write in reader order.

Source order often follows repository history, API taxonomy, or product ownership. Reader order should follow:

```text
problem or decision
-> successful outcome
-> prerequisites
-> shortest path
-> verification
-> real workflow
-> explanation
-> limitations and troubleshooting
```

## Use Existing Drafts Correctly

When continuing a series:

1. Read the representative baseline draft, not every historical file by default.
2. Extract stable traits: reader level, section rhythm, terminology, command presentation, verification style, and caveat style.
3. Preserve the intended voice and useful structure.
4. Correct repeated rows, unsupported facts, inconsistent headings, and accidental language changes instead of copying them.

## Handle Missing Evidence

- State what could not be verified.
- Explain whether the gap blocks action or only reduces confidence.
- Offer the safest bounded recommendation.
- Do not fill gaps with plausible-looking commands or values.
