# Contributing

Thank you for helping improve these Skills. Contributions should preserve the separation between researched writing quality and conservative local file persistence.

## Before You Start

- Search existing issues and pull requests before opening a duplicate.
- Use a public bug or feature form for ordinary work. Follow `SECURITY.md` for security boundary failures or secret exposure.
- Discuss changes that alter tool permissions, destructive-operation boundaries, automatic triggering, package format, or supported clients before implementing them.
- Follow `CODE_OF_CONDUCT.md` in all project spaces.

## Development Setup

Python 3.11 and 3.13 are exercised in CI. Run commands from the repository root. The deterministic checks use only the Python standard library.

```bash
python3 tests/validate_repository.py
python3 tests/test_validator.py
python3 tests/test_draft_checker.py
python3 tests/test_packaging.py
python3 tests/test_installation.py
git diff --check
```

WorkBuddy's bundled validator is an additional host-specific check:

```bash
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" skills/workspace-file-maintainer
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/quick_validate.py" skills/research-material-writer
```

Contributors without WorkBuddy can still run the repository tests and the open-spec validation workflow once its dependencies are installed.

## Change Rules

- Add or update an evaluation before changing observable behavior.
- Keep `SKILL.md` below 500 lines and detailed material one reference link away.
- Keep references focused and avoid deep reference chains.
- Do not add secrets, personal files, production credentials, or real user data to fixtures.
- Use disposable directories and marker data for path, symlink, archive, or sensitive-file tests.
- Do not add generated ZIP files, caches, or local installation links to Git.
- Update the Skill version and `CHANGELOG.md` when behavior or package contracts change.
- Preserve WorkBuddy and open-spec compatibility rules defined by the release process.
- Cite primary external sources when a change adopts a standard, workflow, or compatibility claim; update `SOURCES.md` for material design influences.

## Trigger And Functional Evaluations

Trigger changes must cover obvious requests, paraphrases, near-negative cases, boundary cases, and competing Skills. A trigger dataset passing structural validation does not prove automatic routing.

Functional evidence must distinguish:

- deterministic checks reproduced by repository tests;
- manual or fresh-agent observations;
- historical narrative evidence;
- blocked or unmeasured behavior.

Do not report automatic trigger precision, recall, or stability without auditable host route/load events.

## Pull Requests

Follow `RELEASING.md` and use a short-lived topic branch. A pull request should include:

- the problem and intended behavior;
- files and Skill versions affected;
- compatibility, permission, and security impact;
- evaluation or regression coverage;
- exact verification commands and results;
- remaining risks, blocked checks, or follow-up work.

All CI checks must pass. Maintainers may request smaller commits, additional boundary tests, or changes to unsupported claims before merging.

## License

By submitting a contribution, you agree that your contribution is licensed under the repository's MIT License.
