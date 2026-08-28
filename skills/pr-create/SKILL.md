---
name: pr-create
description: Use when development on the current issue branch is ready to open or locate a GitHub pull request or GitLab merge request
---

# PR Create

## Overview

Create or locate the current branch's issue-related PR/MR. Never create or modify `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Defaults

When matching repository configuration is absent or a field is missing:

```text
base-branch = main
branch-template = feature/{issue-no}-{issue-subject}
pr-draft = false
pr-auto-close-issue = false
```

Use non-empty `remarks` as project instructions. An explicit Git remote determines the provider and repository; stop on a conflicting configured `type`.

## Workflow

1. Require a local Git repository and resolve its root, remote, provider, current branch, and optional config.
2. Require the current branch to differ from `base-branch`.
3. Extract the issue number by applying `branch-template` to the complete branch name. Use an explicitly supplied issue number when present. If neither works, ask; never guess.
4. Check provider authentication and verify the remote issue exists.
5. Query an open PR/MR for the current head branch. If found, return it unchanged and stop.
6. Require all intended changes to be committed and the remote head to contain the intended commits. Do not create from an ambiguous local-only state.
7. Build a concise title from the issue and a body with `Summary`, `Testing`, and `Issue` sections. Report only testing evidence already available in context; never invent it.
8. Relate the issue using non-closing wording by default. Use a provider closing reference only when `pr-auto-close-issue` is true.
9. Create a ready PR/MR by default. Create a draft only when `pr-draft` is true.
10. Re-read and report the remote result: URL, number, base/head, head SHA, issue, and draft state.

## Issue Relationship

Every PR/MR must relate one verified issue.

| Setting | Behavior |
|---|---|
| `pr-auto-close-issue: false` or absent | Link without a closing keyword |
| `pr-auto-close-issue: true` | Close the issue only after an eligible merge |

Opening a PR/MR never closes the issue immediately.

## Stage Boundary

`/pr-create` owns creation only. It never invokes `/pr-review`, approves, merges, closes the issue, deletes a branch, or changes an existing PR merely to match generated text. After success, report `/pr-review` as an available next command without invoking it.

## Failure Rules

Stop without a remote write when authentication fails, the issue is missing, the branch is the base branch, the issue number is unresolved, intended changes are uncommitted/unpushed, or provider identity conflicts.

Distinguish authentication, authorization, not-found/hidden, and invalid-state errors. Never expose credentials.

## Common Mistakes

| Mistake | Correct behavior |
|---|---|
| Create config when absent | Use defaults in memory |
| Default to a closing keyword | Use a non-closing relationship |
| Duplicate an existing PR/MR | Return the existing open target |
| Guess issue from an unrelated branch | Ask for the issue number |
| Start review after creation | Report the command only |
