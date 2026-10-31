# Project Collaboration Standard

This document defines the default collaboration workflow for `repo-anatomy-skill`. It turns the repository's GitHub Flow, evidence requirements, review expectations, and release gates into an executable Pull Request (PR) process.

The document is normative unless a section is explicitly marked as a recommendation, a target configuration, or a current limitation. The repository's `CONTRIBUTING.md` remains the entry point for contribution scope and development setup; `RELEASING.md` remains the entry point for versioning and publication.

## Scope And Principles

This standard applies to changes to Skills, references, evaluations, tests, scripts, CI, documentation, package contracts, and repository governance.

The project uses these principles:

- Keep `main` releasable.
- Make one PR solve one coherent problem.
- Prefer evidence over assertion, and disclose what was not verified.
- Review behavior, compatibility, security, and maintainability, not only syntax.
- Automate deterministic checks and keep human judgment for intent, scope, and risk.
- Treat changes to permissions, destructive-operation boundaries, automatic routing, package formats, and supported clients as high-impact changes.
- Never bypass a failed required check or conceal an unresolved security concern.

## Collaboration States

A change normally moves through this state sequence:

```text
Issue or proposal
  -> topic branch
  -> draft PR
  -> ready for review
  -> review comments and revisions
  -> approval and passing checks
  -> squash merge into main
  -> post-merge verification
```

Use a draft PR while the design, scope, or verification plan is still being developed. Mark it ready only when the author believes the stated acceptance criteria can be checked by another person.

A PR may move back to revision after new commits, a failed check, a newly discovered risk, or a reviewer request. An approval is not a permanent release authorization: a material change to the diff requires re-review.

## Branch Management

`main` is the protected integration and release source branch. Contributors work on short-lived topic branches created from an up-to-date `main`.

Use the existing naming scheme:

- `feat/<topic>` for a backward-compatible feature or workflow;
- `fix/<topic>` for a defect or incorrect instruction;
- `docs/<topic>` for documentation-only changes;
- `test/<topic>` for evaluation or regression coverage;
- `release/<version>` for release metadata, compatibility packages, release notes, and release artifacts.

Branch rules:

1. Update local `main` before creating a topic branch.
2. Keep a branch focused on one coherent change and avoid unrelated cleanup.
3. Do not push directly to `main`.
4. Do not use a long-lived development branch.
5. Rebase or merge `main` into a topic branch when the PR is stale or the target branch has moved; describe conflict resolution in the PR when it changes behavior.
6. Do not force-push a branch after review unless the PR owner and active reviewers agree. If history is rewritten, explicitly request a fresh review.
7. Delete a topic branch after merge unless it is needed for release operations or an active follow-up.
8. Never put secrets, personal files, generated ZIP packages, caches, or local installation links in a branch.

These rules follow GitHub's documented pull-request and protected-branch model. A fork may be used when the contributor does not have direct write access; the same PR evidence and review requirements still apply.

## Commit Messages

Each commit should be focused, independently understandable, and safe to inspect. Use a short imperative subject with the repository's existing Conventional Commit-style prefixes:

```text
feat: add repository onboarding evaluation
fix: reject symlinked package entries

docs: clarify pull request review gates
test: cover duplicate trigger prompts
ci: pin validation action revision
```

Guidelines:

- Keep the subject concise and describe the resulting change.
- Use the body for motivation, compatibility impact, migration notes, or non-obvious trade-offs.
- Do not include credentials, tokens, local absolute paths, or generated artifacts.
- Do not use a misleading subject to hide a behavior or security change.
- Keep intermediate commits useful for review when they show meaningful stages; the final merge normally uses squash so `main` receives one coherent change.
- When a commit changes a Skill behavior or package contract, update the affected version and `CHANGELOG.md` in the same PR.

Commit prefixes are a project convention, not a claim that GitHub itself enforces a particular format.

## Creating A Pull Request

Before opening a PR:

1. Search existing issues and PRs for duplicates or related decisions.
2. Confirm the target is `main`, unless the release process explicitly names another base.
3. Create a short-lived topic branch from current `main`.
4. Add or update an evaluation before changing observable behavior.
5. Run the relevant local checks and inspect the complete diff.
6. Confirm that the change does not add secrets, personal data, generated release files, or unsupported compatibility claims.

Open a draft PR when discussion is needed. Convert it to ready for review only after the PR template is complete and the verification evidence is reproducible.

A ready PR must contain:

- **Problem:** the user, maintainer, or project problem;
- **Scope:** intended behavior and explicitly excluded behavior;
- **Changes:** files, Skills, versions, evaluations, and package contracts affected;
- **Compatibility and security:** tool permissions, destructive-operation boundaries, supported clients, network or filesystem scope, and security impact;
- **Verification:** exact commands, relevant output, CI jobs, and environment details;
- **Evidence scope:** deterministic results, manual observations, historical evidence, blocked checks, and unknowns clearly separated;
- **Risks and follow-up:** remaining risks, rollback path, and work intentionally deferred;
- **Issue links:** related issue or discussion when one exists.

Keep the PR title short and action-oriented. The description should remain understandable after the PR is merged, because it becomes part of the project's maintenance history.

Do not combine unrelated changes merely because they touch the same file. Split a PR when the review requires different expertise, different release timing, or different rollback decisions.

## Review Standard

Reviewers should first understand the PR's purpose and linked context, then examine the commits and the complete file diff. Review one file at a time, leave comments on the relevant lines, mark reviewed files as viewed, and submit one explicit review state with a summary.

A review must answer these questions:

### Correctness And Scope

- Does the implementation or documentation solve the stated problem?
- Does it preserve the repository's separation between research writing and conservative file maintenance?
- Are edge cases, negative paths, and failure handling covered?
- Is the change no broader than the stated scope?
- Are instructions, commands, paths, versions, and expected results internally consistent?

### Evidence And Documentation

- Are important technical claims tied to primary sources, reproduced behavior, or clearly labeled inference?
- Are dynamic facts dated when appropriate?
- Does the documentation distinguish verified facts, source claims, recommendations, and unknowns?
- Does a new evaluation demonstrate the intended observable behavior?
- Does the Markdown remain usable for a beginner without becoming a translated README?

### Security And Permissions

- Does the change widen filesystem, network, tool, credential, or package scope?
- Could a symlink, archive entry, path traversal, generated file, or secret leak bypass a boundary?
- Are destructive operations still excluded or explicitly authorized?
- Does the PR add or change a GitHub Action permission, dependency source, release asset, or installation path?
- Are security-sensitive changes covered by boundary regression tests and `SECURITY.md` guidance?

### Compatibility And Operations

- Does the change preserve WorkBuddy and open-spec package rules where applicable?
- Are supported Python versions, clients, operating systems, and known limitations accurate?
- Are package manifests, versions, and release notes updated when the package contract changes?
- Is rollback possible without moving or overwriting a published tag?

### Review Comment Classification

Use clear, actionable comments. Prefix a comment when severity or required action could be ambiguous:

- `blocker:` must be addressed before approval because it causes incorrect behavior, unsafe behavior, a broken contract, or an unsupported release claim;
- `important:` should be addressed before merge unless the author and maintainer record an explicit decision;
- `suggestion:` improves clarity or maintainability but is not a merge blocker;
- `question:` requests context or verifies an assumption;
- `nit:` is optional polish.

A reviewer should avoid approving while a known blocker or unresolved security boundary failure remains. When a comment is informational, say so rather than creating an accidental gate.

## Approval Conditions

A PR is eligible for approval only when all of the following are true:

1. The PR is ready for review, not a draft.
2. The stated problem, scope, affected files, and acceptance criteria are clear.
3. Required deterministic checks pass, or an explicitly recorded exception has maintainer approval.
4. The diff has been reviewed at the file and behavior level.
5. All blocker and important comments are resolved or have a recorded maintainer decision.
6. Compatibility, security, permission, and evidence boundaries are documented.
7. Required evaluations and regression tests are present for changed observable behavior.
8. No unresolved P0/P1 security issue affects the change or release path.
9. The branch is based on the current target branch when strict status checks or conflict-sensitive behavior requires it.

The PR author cannot approve their own PR. The approval must come from a reviewer with the repository permission required by the active protection rule. Approval should be renewed after a material code-modifying commit, especially when stale approvals are dismissed by branch protection.

Use **Comment** for feedback without a merge decision, **Request changes** when the PR must change before merge, and **Approve** only when the reviewer is satisfied with the stated scope and evidence. A GitHub review state is not a substitute for a complete CI result or maintainer release decision.

## Automated Checks

The repository CI is part of the merge gate. For the current project, the expected checks cover:

- repository validation;
- validator regression tests;
- draft-checker regression tests;
- packaging regression tests;
- stable-installation regression tests;
- whitespace validation;
- Open Agent Skills schema compatibility;
- reproducible package construction and manifest verification;
- Python 3.11 and Python 3.13 execution paths.

Authors should run the deterministic suite locally from the repository root:

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
git diff --check
```

A green check is necessary but not sufficient. CI cannot establish factual accuracy, source quality, suitability for every client, or the safety of a newly widened permission boundary. Those require human review and, where applicable, a real-project or host-specific evaluation.

When a check fails:

1. Identify whether the failure is caused by the change, the environment, or the workflow.
2. Reproduce it locally when practical and preserve the relevant command and output.
3. Fix the source problem and push a focused commit, or record why the failure is unrelated.
4. Do not dismiss, skip, or bypass a required check merely to unblock a merge.
5. Re-run the affected checks and request re-review if the diff changed materially.

Workflow job names should remain unique and stable before they are selected as required status checks. If a check is flaky, repair the workflow or document a temporary exception; do not silently weaken the merge gate.

## Merge Strategy

The default merge strategy for ordinary PRs is **Squash and merge** into `main`.

Use squash merge when the PR represents one coherent change and its intermediate commits are not independently useful. Preserve separate commits only when the history is intentionally meaningful, such as a release preparation whose stages must remain traceable and have been approved as such.

Before merging, the maintainer must confirm:

- the PR is not a draft;
- required reviews and conversations are complete;
- all required checks are successful, skipped, or neutral according to the active rule;
- the branch is mergeable and up to date when required;
- no new commit has invalidated the latest approval;
- the merge method matches branch protection and the release plan;
- the PR body and final commit message accurately describe the result.

Do not merge a PR with unresolved conflicts. Update the topic branch, resolve conflicts in the contributor's branch, run the relevant checks again, and request review when the resolution changes behavior.

Auto-merge may be enabled only when the maintainer has selected the intended merge method and the repository's required reviews and checks provide the actual gate. Auto-merge is not a replacement for a human approval decision, and it must be disabled or revisited when the base branch, scope, or security impact changes.

After merge:

1. Verify that `main` contains the expected merge commit and that the post-merge CI is green.
2. Delete the topic branch when it is no longer needed.
3. Do not create a tag or GitHub Release unless the release owner separately authorizes publication and the release gates in `RELEASING.md` pass.
4. Record follow-up work in an issue or the next PR rather than appending unrelated fixes to the merged change.

## Branch Protection Target

The following is the target configuration for `main`; repository administrators should implement it with GitHub branch protection rules or rulesets and keep the settings aligned with this document:

- require a pull request before merging;
- require at least one approving review from an eligible maintainer;
- dismiss stale approvals when the reviewed diff changes;
- require approval from someone other than the last pusher where supported and appropriate;
- require all designated CI checks to pass;
- require conversation resolution before merge;
- require the branch to be up to date before merge when strict checks are used;
- disallow force pushes and branch deletion;
- prevent bypass of the rules for administrators unless an emergency exception is recorded;
- allow the repository's selected merge method and keep the rule consistent with the linear-history policy if that policy is enabled.

The target configuration is a governance requirement, not proof that every setting is already enabled on the remote repository. Administrators must verify the effective rules in repository settings and avoid overlapping rules that make enforcement ambiguous.

## Exceptions And Incidents

### Urgent Security Fix

For an urgent security fix, keep the PR as narrow as possible, follow `SECURITY.md`, and involve an authorized maintainer. Use the minimum necessary exception only when normal review or CI would expose a secret or leave an active vulnerability unaddressed. Record the reason, approver, checks skipped, affected commits, and follow-up verification in a private or appropriately restricted channel. Never publish exploit details in a public issue before disclosure is coordinated.

### Broken CI Or Infrastructure

If CI is unavailable or fails for infrastructure reasons, do not mark the PR as normally approved. A maintainer may record a temporary exception only when the diff was independently verified, the failed job and reason are documented, the risk is understood, and a follow-up issue is created. Re-run the check as soon as the service is restored.

### Emergency Revert

For a merged regression, create a focused revert PR against `main`. Do not rewrite `main`, move a published tag, or force-push over the problematic history. After the revert is merged, investigate the root cause in a separate PR and preserve the previous verified package and manifest when release artifacts are involved.

### Unclear Ownership Or Approval

Stop the merge when required ownership, review eligibility, or security responsibility is unclear. Ask a repository maintainer to resolve the ownership question and record the decision before proceeding.

## Maintenance Of This Standard

Update this document when any of the following changes:

- branch names or merge strategy;
- PR template or required evidence;
- CI jobs selected as required checks;
- branch protection or ruleset requirements;
- package contracts, supported clients, or release gates;
- security reporting or emergency response procedures.

A change to this standard should itself use a PR, include the relevant official GitHub documentation links, explain the current-versus-target enforcement state, and run the repository's deterministic validation suite.

## Official References

The workflow is based on GitHub's public documentation, consulted on 2026-10-31:

- [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/creating-a-pull-request)
- [Reviewing proposed changes in a pull request](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)
- [Approving a pull request with required reviews](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews)
- [Merging a pull request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request)
- [Automatically merging a pull request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About pull request reviews](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/about-pull-request-reviews)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)

GitHub may reorganize documentation paths over time. The linked titles are the intended reference points; repository-specific decisions and current enforcement remain defined by this document and the active repository settings.
