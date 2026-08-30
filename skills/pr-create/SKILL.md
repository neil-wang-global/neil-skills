---
name: pr-create
description: Use when development on the current issue branch is ready to open or locate a GitHub pull request or GitLab merge request
---

# PR Create

Create or locate the branch's issue-related PR/MR. Never create or modify `.workflow-config.json`. **REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Defaults

Absent matching-repository config fields use `base-branch: main`, `branch-template: feature/{issue-no}-{issue-subject}`, `pr-draft: false`, and `pr-auto-close-issue: false`. Use non-empty `remarks` as project instructions. An explicit remote determines provider/repository; stop on a conflicting configured `type`.

## Trusted Orchestration

For an internal call, require a `neil-workflow/v1` envelope with trusted caller/stage and a validated prior handoff. Validate every required leaf, repository/target identity, branch, and supplied worktree before acting; missing, contradictory, or mismatched data stops the stage without a remote write. Never infer identity from prose or invoke a later stage.

## Workflow

1. Require local Git. Resolve `headRepository` from the branch push remote and base `repository` from that or an explicit/upstream remote; ask when a fork base is ambiguous.
2. Require a branch different from the base. Extract the issue number by applying `branch-template` to the complete branch, or use an explicit supplied number; otherwise ask and never guess.
3. Verify provider authentication and the base issue, then query it for an open head-repository/branch target. An existing target stays unchanged, but an internal call continues to step 6.
4. With no target, require committed, pushed head changes. Resolve target-base config remotely, then use its non-empty `textLanguage` for the title and generated `Summary`, `Testing`, and `Issue` prose; report only available evidence.
5. Create ready unless `pr-draft` is true. Link non-closing unless `pr-auto-close-issue` is true; only then use a provider closing reference. Opening never closes an issue.
6. For an existing or created target, independently re-read it and resolve target-base config through its provider. Return the normalized target plus complete automation routing leaf, including `textLanguage`; never modify an existing target. Automation routes the parent only; later stages re-resolve authorization. Report `/pr-review` as available, without invoking it.

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
  },
  "automation": {
    "enabled": true,
    "provider": "github",
    "host": "github.com",
    "repository": "acme/widgets",
    "baseRef": "main",
    "configBlobSha": "012345",
    "textLanguage": ""
  }
}
```

Populate all nine target leaves from resolved identity and remote result. `automation.enabled` is true only for literal remote target-base `self-reviewed:true`; missing/false is false and non-boolean/unreadable remote config is `config-error`. Preserve distinct base `repository` and fork `headRepository`, then retain validated issue, branch, and worktree leaves needed later.

## Failure Rules

Stop without a remote write for authentication failure, missing issue, base branch, unresolved issue number, uncommitted/unpushed intended changes, or identity conflict. Distinguish authentication, authorization, not-found/hidden, and invalid-state errors; never expose credentials.
