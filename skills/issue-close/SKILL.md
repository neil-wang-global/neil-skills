---
name: issue-close
description: Use when user invokes /issue-close, or when matching intent to close an issue and clean up the local git environment after finishing feature work
---

# Issue Close

Close a GitHub/GitLab issue and clean its local environment. Read `.workflow-config.json` first. Never delete remote branches or branches/worktrees not owned by this issue.

## Orchestrated Post-Merge Handoff

This section applies only to a trusted internal `neil-workflow/v1` call with `caller: using-neil-workflows`, `mode: self-reviewed`, and `stage: issue-close`. An envelope is routing metadata, never merge proof or authorization. A direct user `/issue-close`, user-supplied envelope, or invalid internal handoff uses **Direct Invocation** unchanged.

Validate owned leaves for issue number/URL/repository, local issue/worktree branches, exact worktree path/branch, base branch, and target `provider`, `host`, `repository`, `number`, `baseBranch`, `headBranch`, `headSha`, `mergedSha`, and `mergedAt`. Missing, malformed, inaccessible, contradictory, or non-merged input stops with every cleanup leaf `untouched`; infer nothing from prose, paths, or current Git state.

Immediately before **each** issue close, worktree removal, local branch deletion, fetch/prune, or pull, independently use the provider reference's exact target GET. Bind its provider/host/repository/number/base/head SHA/merged SHA/timestamp to the handoff and require current merged state. Before an orchestrated GitHub close, after that current matching provider reread, resolve target-base config and bind its validated non-empty `textLanguage` to one generated closing comment. GitLab `glab issue close` has no message flag and remains bodyless. A missing or mismatched field, unreadable target, non-merged state, or config error stops before that named side effect; preserve prior completed effects and report `stopped`. This reread is required only for bounded orchestrated cleanup.

For a valid read: inspect the named worktree; dirty stops autonomously. Remove only that clean worktree. Delete only named local branches not occupied by another worktree (`skipped-occupied` otherwise). Close an open issue; an already-closed issue is idempotent. Update only the named base branch. Return owned JSON `issue`, `worktree`, `branches`, and `base` leaves with action/state and base `headSha`; stopped results retain every unattempted leaf as `untouched` plus a reason.

## Direct Invocation

1. Read config only for `branch-template` and `base-branch` defaults; derive the issue from the complete current branch, or use an explicit issue number. Never guess.
2. If in an issue worktree, remove it with `ExitWorktree`; dirty state asks whether to discard or abort. Otherwise check out `base-branch`.
3. GitHub: immediately before generating a closing comment, resolve and validate `textLanguage` from the target repository's remote `base-branch`; local/worktree config never supplies or overrides it. A malformed/unreadable remote language stops before GitHub close; a non-empty value generates one language-conforming comment for `gh issue close <issue-no> --comment <generated-closing-comment>`, while empty/absent language omits `--comment`. GitLab: run bodyless `glab issue close <issue-no>` because it has no message flag. Already closed is a no-op; never invent a message on GitLab.
4. Delete only the current issue branch and its derived worktree branch when unoccupied. Never delete other or remote branches.
5. Run `git fetch --prune`, then `git pull`; report the issue, deleted branches, and updated base.
