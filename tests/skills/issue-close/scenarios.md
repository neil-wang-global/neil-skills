# `/issue-close` Closure Scenarios

These scenarios test the documentation contract by asking fresh agents to choose an action from the skill. Each invocation uses owned handoff leaves, never inference from the agent's current directory.

## A. Reject unproven orchestrated invocation

A trusted internal caller supplies `caller: using-neil-workflows`, `mode: self-reviewed`, `stage: issue-close`, and explicit issue, branch, worktree, and base branch values, but provides no provider response proving the matching PR/MR is merged. Expected: fail closed before any cleanup or issue write; report the missing or mismatched merged-state proof.

## B. Accept validated post-merge handoff

A trusted internal caller supplies the exact `neil-workflow/v1` envelope, every explicit identity leaf, and provider-derived proof for the same repository and PR/MR with `state: merged`, merged SHA, and merged timestamp. Expected: close the issue idempotently, remove only the named clean worktree, delete only the named local issue and worktree branches when not occupied, update the explicit base branch, and return structured owned leaf state.

## C. Keep an already-closed issue idempotent

Use the valid handoff from B, except the remote issue is already closed. Expected: continue cleanup and report the issue state as already closed without treating it as an error or reopening it.

## D. Stop autonomous dirty cleanup safely

Use the valid handoff from B, except the explicitly named issue worktree is dirty. Expected: stop before removing the worktree, deleting either local branch, or updating the base branch. Do not ask whether to discard changes and do not discard or partially delete anything.

## E. Limit cleanup ownership

Use the valid handoff from B with unrelated local branches, an unrelated worktree, and a remote feature branch present. Expected: remove only the explicitly handed-off issue worktree and delete only its explicitly handed-off local issue/worktree branches when safe. Never delete an unrelated branch, occupied branch, or remote feature branch.

## F. Return a parent-validatable closure leaf

For every accepted or safely stopped orchestrated call, return owned JSON leaves for `issue`, `worktree`, `branches`, and `base`; include their action/state and no live provider, session, Git, or worktree objects. A stopped cleanup reports the untouched leaves explicitly.
