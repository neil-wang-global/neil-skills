---
name: pr-fix
description: Use when addressing PR/MR review feedback by URL, number, exact comment URL, or current branch from a writable head-repository clone
---

# PR Fix

## Contract

Classify and confirm, delegate accepts to `/issue-executing`, then finish missing Git/thread operations. Never write `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Target and Scope

Comment URL selects one thread; PR/MR URL or number selects unresolved target threads; no argument uses current branch.

Require a clone matching `headRepository`; accepted changes also require writable head. Never clone. URL identity controls base-target APIs.

## Workflow

1. Resolve target and threads; authenticate and fetch remote state.
2. Verify remote matches `headRepository`; record whether `headBranch` is writable.
3. Check each comment against current code. Classify `accept`, `reject`, or `clarify` with reason and intended reply.
4. Show one table (`Thread | Decision | Reason | Intended outcome or reply`) and wait once. User edits are authoritative.
5. With no accepts, skip worktree/delegation/Git and continue to replies. Otherwise require writable head; stop before implementation if not.
6. Prepare head: reuse a safe current/existing worktree; otherwise fetch it. With `need-worktree:false`, require a clean current worktree then check out the head; otherwise create an isolated worktree (branch slashes become plus signs).
7. Snapshot head, worktree status, local-only commits, upstream, and ahead/behind counts.
8. Delegate accepted items to `/issue-executing` with worktree path and an implementation-neutral brief.
9. After return, inspect actual Git state instead of trusting a claimed commit/push state.
10. Preserve existing commits and pushes. Commit once only when accepted changes remain uncommitted; include only those changes. Push only commits absent upstream.
11. Verify each accepted outcome. Before replying, skip an equivalent latest reply of your own when no reviewer message followed it; if only resolution failed, retry resolution only.
12. Reply with result and commit, then resolve accepted threads only after reply success and permission. Reply to reject/clarify with rationale/question and leave unresolved. Report all outcomes.

## Delegation Boundary

The brief contains accepted feedback, context, locations, observable outcomes, worktree, and target IDs only. It excludes coding methods, architecture, algorithms, techniques, and test commands. `/issue-executing` chooses implementation and verification.

## Git Preservation

| Returned state | Completion action |
|---|---|
| Pushed commits; clean | Nothing |
| Unpushed commits; clean | Push |
| Commits plus accepted dirty changes | One completion commit; push missing commits |
| Accepted dirty changes only | One completion commit; push |

Never squash, amend, recommit, rebase, force-push, or redundantly push delegated results.

## Thread State

| Decision | Reply | Resolve |
|---|---|---|
| accept | Verified result and commit | Only after reply succeeds |
| reject | Technical rationale | Never |
| clarify | Focused question/interpretation | Never |

A failed reply leaves that thread unresolved. Preserve other successful remote operations and retry only incomplete steps.

## Boundary

Do not review the full diff, merge, close issues, clean branches/worktrees, or chain public stages. This skill contains no implementation or test guidance.
