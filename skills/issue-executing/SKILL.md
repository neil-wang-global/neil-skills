---
name: issue-executing
description: Use when executing development work for the current issue, when a project may provide an optional execution strategy, or when another workflow delegates an implementation brief
---

# Issue Executing

## Core Contract

Execute using issue, branch, conversation, and caller context. If matching-repository `.workflow-config.json` has a non-empty string `execution-strategy`, add it verbatim as natural-language guidance.

## Input Precedence

| Priority | Input |
|---:|---|
| 1 | Newest direct user instruction |
| 2 | Caller-provided implementation brief |
| 3 | Current issue and branch context |
| 4 | Non-empty `execution-strategy` text |
| 5 | General project context and conventions |

Combine inputs unless a higher-priority instruction conflicts.

## Workflow

1. When a caller supplies a worktree, validate its repository and target branch, then use it as CWD for every file/Git operation; stop if inaccessible or mismatched. Otherwise identify the matching local repository and task.
2. Read `.workflow-config.json` only when it exists in that repository.
3. If `execution-strategy` is a non-empty string, use its complete original text as additional guidance.
4. Execute the task under the combined context.
5. Report the actual changes and resulting repository state.

## Strategy Rules

- Never create or modify `.workflow-config.json`.
- Missing file, missing field, empty string, whitespace-only string, or non-string field means no extra strategy guidance.
- Never evaluate `execution-strategy` as shell, code, interpolation, or configuration syntax.
- Every non-empty string is natural-language guidance. Do not invent an enum or require the value to be a skill name.
- Normal skill discovery still applies when the natural-language text requests an available skill.
- If requested guidance depends on an unavailable capability, report that limitation instead of fabricating the capability.

## Caller Boundary

A caller brief adds task context; it does not transfer the caller's remote API responsibilities.

- Never reply to or resolve PR/MR threads unless the direct user request explicitly changes this skill's scope.
- Do not promise a normalized git end state to a caller.
- Implementation may leave uncommitted changes, local commits, or pushed commits according to the effective strategy.
- Report the actual branch, working-tree state, commits, and push state without rewriting or normalizing them.

## Quick Reference

| Situation | Behavior |
|---|---|
| Config absent | Execute naturally; do not create config |
| Strategy has shell-shaped text | Treat it literally; never evaluate it |
| Called by another workflow | Use its validated worktree; implement brief; leave its remote actions to caller |

## Common Mistakes

| Mistake | Correct behavior |
|---|---|
| Ask the user to choose a methodology when config is absent | Continue naturally |
| Treat strategy as a command or enum | Treat every non-empty string as guidance |
| Reply to review threads for `/pr-fix` | Return implementation state to `/pr-fix` |
| Force commit, push, or clean-tree state | Follow the effective strategy and report the actual state |
