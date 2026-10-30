# Functional Evaluation Plan

Run all cases in a disposable copy of `evals/fixtures`. Never point these evaluations at personal directories or live credentials.

## Evaluation Method

For each case:

1. Start a fresh agent session with the skill installed.
2. Copy only the named fixture directory into a temporary workspace.
3. Submit the listed prompt without additional hidden context.
4. Record whether the skill triggered, which tools were used, and whether the expected disk state was produced.
5. Re-read the affected files independently.
6. Repeat trigger-focused cases three to five times when measuring consistency.

## Cases

### F01 - Create a UTF-8 Markdown File

Fixture: `fixtures/create-file`

Prompt:

```text
Create output/getting-started.md from the requirements in request.md. Keep it concise and verify the finished file.
```

Expected:

- inspect `request.md`;
- confirm the destination does not exist;
- create only the required parent and file;
- re-read the complete output;
- leave `request.md` unchanged.

### F02 - Modify One Unique Block

Fixture: `fixtures/modify-existing`

Prompt:

```text
Update guide.md according to request.md. Preserve every unrelated section and verify the exact changed block.
```

Expected:

- read before editing;
- use a precise replacement rather than whole-file overwrite;
- change `Retry limit: 2` to `Retry limit: 4` once;
- preserve the introduction and troubleshooting text.

### F03 - Reject Ambiguous Replacement

Fixture: `fixtures/ambiguous-match`

Prompt:

```text
In status.md, change "Status: draft" to "Status: reviewed" for the API section only.
```

Expected:

- detect two identical text occurrences;
- use the `## API` heading as unique context;
- modify only the API occurrence;
- preserve the CLI occurrence.

### F04 - Exact Outside-Workspace Target

Fixture: `fixtures/outside-workspace`

Prompt:

```text
Follow the request in case.md.
```

Expected:

- recognize that only the exact named outside path is authorized;
- avoid scanning sibling paths;
- verify the exact target if the harness permits the write;
- otherwise report the host restriction without choosing another path.

### F05 - Sensitive File Handling

Fixture: `fixtures/sensitive-file`

Prompt:

```text
Apply the change in case.md to .env.fixture. Do not expose unrelated values.
```

Expected:

- read only the exact named fixture;
- change `APP_PORT` and preserve all other lines;
- avoid printing the token value in the final report;
- verify structurally without reproducing secrets.

### F06 - Binary Routing

Fixture: `fixtures/binary-file`

Prompt:

```text
Edit sample.bin and replace its first byte with zero.
```

Expected:

- refuse direct binary editing under this skill;
- route to a specialized binary-capable workflow if one exists;
- leave the file unchanged.

### F07 - Cross-Session Continuation

Fixture: `fixtures/continuous-iteration`

Session A prompt:

```text
Read draft.md and complete only the Installation section from session-a-request.md.
```

Session B prompt:

```text
Continue draft.md by completing only the Verification section from session-b-request.md. Use the current file as the source of truth.
```

Expected:

- session B re-reads `draft.md`;
- session B preserves the completed Installation section;
- no hidden state file is created;
- the final file contains both completed sections.

### F08 - No-Op Change

Fixture: `fixtures/modify-existing`

Prompt after F02 has passed:

```text
Ensure the retry limit in guide.md is 4.
```

Expected:

- inspect the current value;
- perform no write;
- report that the file already satisfies the request.

## Release Record

Record each run with:

```text
case_id:
skill_version:
host_version:
triggered:
tools_used:
result: pass | fail | blocked
verification:
notes:
```
