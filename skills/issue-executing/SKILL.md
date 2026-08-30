---
name: issue-executing
description: Use when executing development work for the current issue, when a project may provide an optional execution strategy, or when another workflow delegates an implementation brief
---

# Issue Executing

## Core Contract

Execute using issue, branch, conversation, and caller context. Read matching-repository `.workflow-config.json` only when it exists. A non-empty string `execution-strategy` is complete literal natural-language guidance, never shell, code, interpolation, an enum, or a required skill name.

| Priority | Input |
|---:|---|
| 1 | Newest direct user instruction |
| 2 | Validated caller implementation brief |
| 3 | Current issue and branch context |
| 4 | Non-empty `execution-strategy` |
| 5 | Project conventions |

Combine inputs unless higher priority conflicts.

## Trusted Orchestration

A caller envelope must be `neil-workflow/v1`, identify `caller: using-neil-workflows` and `stage: issue-executing`, and contain a validated prior handoff. Validate every required leaf value, including string `textLanguage`, repository identity, target branch, and supplied worktree before acting. Use the supplied worktree as CWD for every file and Git operation; inaccessible, missing, contradictory, or mismatched data stops the stage. Never infer missing values from prose.

The implementation brief adds task context only. It does not transfer remote PR/MR reply, resolution, review, merge, issue-close, or configuration ownership. Do not invoke another stage.

## Workflow

1. Validate caller worktree/repository/target when supplied; otherwise identify the matching repository and task.
2. Read config only in that repository. Missing, empty, whitespace-only, or non-string `execution-strategy` means no extra guidance.
3. Apply a non-empty strategy as literal guidance. If it requests an unavailable capability, report that limitation without fabricating it.
4. Execute the implementation under the combined context. For a validated non-empty `textLanguage`, use it for any commit subject/body this stage produces. Never create or modify `.workflow-config.json`.
5. Inspect and report actual Git state. Do not commit, push, clean, squash, amend, or normalize it unless the effective strategy directly produced that result.

For a trusted orchestrated result, return owned leaf JSON, not a prose summary:

```json
{
  "version": "neil-workflow/v1",
  "stage": "issue-executing",
  "status": "completed",
  "headSha": "abc123",
  "commits": ["abc123"],
  "dirty": false,
  "pushState": "not-pushed"
}
```

Populate `status`, `headSha`, `commits`, `dirty`, and `pushState` from actual state without normalization. Include the validated repository, issue, branch, worktree, and `headRepository` leaf values needed by the next stage.

## Common Mistakes

| Mistake | Correct behavior |
|---|---|
| Create config when absent | Execute naturally; do not write config. |
| Treat strategy as a command or enum | Treat every non-empty string as literal guidance. |
| Operate in caller checkout | Use the validated supplied worktree. |
| Reply to review threads | Return implementation state to the caller. |
| Promise a fixed Git state | Return actual status, commits, dirty, and push state. |
