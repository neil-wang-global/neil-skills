---
name: pr-fix
description: Use when addressing GitHub pull-request or GitLab merge-request feedback by PR/MR URL, number, exact review-comment URL, or current branch from a matching writable local clone
---

# PR Fix

## Contract

Classify feedback, confirm once, delegate accepted outcomes to `/issue-executing`, then complete missing Git and thread operations. Never create or modify `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Target and Scope

An exact review-comment URL selects only its thread. A PR/MR URL or number selects unresolved target threads. No argument selects the target for the current branch.

Require a matching writable clone; never clone. URL provider, host, and repository override unrelated local state.

## Workflow

1. Resolve target and selected threads; authenticate and fetch current remote state.
2. Verify local remote identity and permission to push the PR/MR head branch.
3. Check each comment against current code. Classify `accept`, `reject`, or `clarify` with reason and intended reply.
4. Show one table (`Thread | Decision | Reason | Intended outcome or reply`) and wait once. User edits are authoritative.
5. Unless matching config explicitly sets `need-worktree` false, create or reuse an isolated worktree at the exact head branch. Never alter the caller's base checkout.
6. If no items are accepted, skip delegation and all commits.
7. Snapshot head, worktree status, local-only commits, upstream, and ahead/behind counts.
8. Delegate accepted items to `/issue-executing` with worktree path and an implementation-neutral brief.
9. After return, inspect actual Git state instead of trusting a claimed commit/push state.
10. Preserve existing commits and pushes. Commit once only when accepted changes remain uncommitted; include only those changes. Push only commits absent upstream.
11. Verify each accepted observable outcome. Reply with result and relevant commit; resolve only after reply success.
12. Reply to reject/clarify threads with confirmed rationale/question and leave them unresolved. Report every Git, reply, and resolution outcome.

## Delegation Boundary

The `/issue-executing` brief includes accepted feedback, context, relevant locations, observable outcomes, worktree, and target identifiers. It excludes coding methods, architecture, algorithms, implementation techniques, and test commands. `/issue-executing` chooses implementation and verification.

## Git Preservation

| Returned state | Completion action |
|---|---|
| Commits pushed; tree clean | No commit and no push |
| Commits unpushed; tree clean | Push only |
| Existing commits plus accepted dirty changes | One completion commit, then push missing commits |
| Only accepted dirty changes | One completion commit, then push |

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
