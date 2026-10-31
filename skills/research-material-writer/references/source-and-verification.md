# Source and Verification Rules

## Source Priority

Use the strongest available source for each claim:

1. Official documentation, product pages, support articles, release notes, and repositories.
2. Official source code, schemas, examples, tests, and issue discussions from maintainers.
3. Standards bodies, original research papers, and authoritative platform documentation.
4. Reputable independent technical analysis with transparent methods.
5. Community posts, forums, and aggregators only for discovery, failure reports, or user experience.

Do not use a weaker source to contradict a stronger source without explaining the conflict.

## Claim Classes

Label claims mentally or in a working ledger:

- **Verified fact:** Directly supported by current evidence.
- **Source claim:** Reported by the project or vendor but not independently reproduced.
- **Inference:** Reasoned from multiple facts; state that it is an inference.
- **Recommendation:** Editorial judgment for a defined reader or scenario.
- **Unknown:** Evidence is unavailable, conflicting, or too old.

## Dynamic Facts

Treat these as time-sensitive:

- Versions, releases, installation commands, dependencies, supported platforms, pricing, limits, policies, maintainers, repository metrics, recent activity, and service availability.
- Add an exact verification date to dynamic facts that materially affect the document.
- Prefer release pages or package registries over a stale README badge.
- Never present a “latest” claim without checking the actual latest release or official update channel.

## Command Verification

For every command or configuration example:

1. Confirm the command exists in the referenced version.
2. Confirm required prerequisites and working directory.
3. Confirm platform differences.
4. Confirm the expected output or observable state.
5. Distinguish documentation review from successful local execution.
6. If execution is blocked by the environment, report the block and cite the official or source-level evidence used instead.

## Conflict Resolution

When sources disagree:

- Prefer the source closest to the implementation and current release.
- Check dates and version scopes.
- Report the disagreement if it changes user action or risk.
- Do not manufacture a single answer from incompatible versions.

## Citation Discipline

- Cite the evidence that directly supports the claim.
- Avoid citing a project homepage for a specific technical behavior only documented in source code.
- Do not overload every sentence with links; group stable background facts while citing consequential and dynamic claims precisely.
- Keep quotations short and prefer faithful paraphrase.

## Research Stop Rule

Stop researching when:

- All decision-critical questions have supported answers or explicit unknowns.
- The shortest successful path and its verification are known.
- Major platform, security, and maintenance constraints are covered.
- Additional sources only repeat existing evidence without changing the document.
