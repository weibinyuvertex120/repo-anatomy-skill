# Error Handling

## Contents

- Missing paths
- Existing targets
- Edit mismatches
- Permission and concurrency errors
- Format errors
- Verification failures
- No-op changes

## Missing Paths

### Read request

Report that the file does not exist. Offer focused discovery only when the user may have supplied an approximate name.

### Modify request

Do not create a new file automatically. Report the missing target and request or infer a corrected path only when evidence is strong.

### Create request

Create the file only after confirming the destination and authorized parent. Create a missing parent directory only when it is necessary and unambiguous.

## Existing Targets

When a create request targets an existing file:

1. Read the file.
2. Determine whether the request actually describes an update.
3. Preserve existing content unless overwrite is explicit.
4. Never use `Write` merely to bypass an `Edit` mismatch.

## Edit Mismatches

### Match not found

- Re-read the current file.
- Search for the intended anchor.
- Rebuild the edit from current content.
- Stop if the intended location cannot be established.

### Match is not unique

- Expand the matched context.
- Split the change into separate unique edits if necessary.
- Do not use replace-all unless every occurrence is intentionally in scope.

### File changed during work

- Re-read the latest version.
- Preserve external changes.
- Re-plan rather than restoring the earlier content.

## Permission and Concurrency Errors

On a permission failure:

- report the exact target and operation;
- do not use `sudo` or change permissions;
- do not move the work to another path without approval.

On a lock or concurrent-write failure:

- stop mutation;
- re-read after the writer completes when appropriate;
- avoid retry loops that may overwrite newer content.

## Format Errors

If content appears binary, encoded unexpectedly, generated, or owned by a specialized format:

- stop direct editing;
- identify the format when possible;
- route to the appropriate specialized skill;
- do not convert formats silently.

## Verification Failures

If post-write verification fails:

1. Do not report completion.
2. Determine whether the write failed, was overwritten, or produced incorrect content.
3. Read the current state again.
4. Apply the smallest corrective change.
5. Repeat verification.
6. If correction is unsafe, report the exact blocker and leave the current state visible.

## No-Op Changes

If the target already satisfies the request:

- do not write the file;
- report that no change was necessary;
- include the evidence checked when useful.

Avoid touching timestamps or formatting solely to demonstrate activity.
