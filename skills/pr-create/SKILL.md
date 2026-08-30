---
name: pr-create
description: Use when development on the current issue branch is ready to open or locate a GitHub pull request or GitLab merge request
---

# PR Create

Create or locate the branch's issue-related PR/MR. Never create or modify `.workflow-config.json`. **REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Defaults

Absent or missing matching-repository config fields use `base-branch: main`, `branch-template: feature/{issue-no}-{issue-subject}`, `pr-draft: false`, and `pr-auto-close-issue: false`. Use non-empty `remarks` as project instructions. An explicit remote determines provider/repository; stop on a conflicting configured `type`.

## Trusted Orchestration

For an internal call, require a `neil-workflow/v1` envelope with trusted caller/stage and a validated prior handoff. Validate every required leaf, repository/target identity, branch, and supplied worktree before acting; missing, contradictory, or mismatched data stops the stage without a remote write. Never infer identity from prose or invoke a later stage.

## Workflow

1. Require local Git. Resolve `headRepository` from the branch push remote and base `repository` from that or an explicit/upstream remote; ask when a fork base is ambiguous.
2. Require a branch different from the base. Extract the issue number by applying `branch-template` to the complete branch, or use an explicit supplied number; otherwise ask and never guess.
3. Verify provider authentication and the issue in the base repository. Query it for an open target from the head repository and branch; return an existing target unchanged.
4. Require committed, pushed changes in the head repository. Build a concise title and body with `Summary`, `Testing`, and `Issue`; report only available evidence.
5. Create ready by default; create draft only when `pr-draft` is true. Link non-closing by default; use a provider closing reference only when `pr-auto-close-issue` is true. Opening never closes an issue.
6. Re-read remote state. Report `/pr-review` as available, without invoking it.

For an internal result, return owned leaf JSON with exactly this normalized target:

```json
{
  "version": "neil-workflow/v1",
  "stage": "pr-create",
  "target": {
    "provider": "github",
    "host": "github.com",
    "repository": "acme/widgets",
    "number": 81,
    "url": "https://github.com/acme/widgets/pull/81",
    "baseBranch": "main",
    "headRepository": "contributor/widgets",
    "headBranch": "feature/42-subject",
    "headSha": "abc123"
  }
}
```

Populate all nine leaves from resolved identity and the remote result; never return `base` or `head` aliases. Preserve distinct base `repository` and fork `headRepository`, then retain validated issue, branch, and worktree leaves needed later.

## Failure Rules

Stop without a remote write for authentication failure, missing issue, base branch, unresolved issue number, uncommitted/unpushed intended changes, or identity conflict. Distinguish authentication, authorization, not-found/hidden, and invalid-state errors; never expose credentials.

## Common Mistakes

| Mistake | Correct behavior |
|---|---|
| Create config when absent | Apply defaults in memory. |
| Duplicate an existing target | Return it unchanged. |
| Guess issue from unrelated branch | Ask for the issue number. |
| Start review after creation | Report the command only. |
| Return a prose result internally | Return the normalized leaf-only target. |
