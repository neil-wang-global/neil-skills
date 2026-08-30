# Deferred Coding Handoff Design

## Purpose

Make Neil workflow development portable across ordinary AI chat sessions without relying on child-agent APIs, client adapters, background tasks, or automatic message routing.

When a workflow reaches code implementation, the current session creates a self-contained development handoff prompt. The user opens a separate session, pastes that prompt, and performs the actual multi-turn development work with any preferred framework. When development is ready, the user returns to the original Neil session and enters the exact phrase:

```text
编码完毕
```

Only that phrase resumes the paused Neil context. The original context determines what happens next; the handoff prompt never exposes or predicts that route.

## Scope

This change updates `/using-neil-workflows`, `/issue-executing`, and `/pr-fix`. It adds a shared handoff reference and pressure scenarios. It does not add a child session protocol, client plugin, external service, completion command, workflow state file, or framework dependency.

## Development Handoff

`/issue-executing` no longer performs code changes when used as a Neil implementation stage. It constructs a copyable prompt from the validated issue handoff and stops at the handoff boundary.

The handoff prompt contains only:

- absolute worktree path and expected feature branch;
- issue number, title, URL, normalized summary, and observable outcomes;
- the complete literal non-empty `execution-strategy`, or a neutral repository-conventions fallback when absent;
- constraints to work only on the issue, preserve actual Git state, and avoid PR/MR, review-thread, merge, issue-close, configuration, and Neil orchestration operations;
- a request to report actual modified files, verification evidence, worktree, branch, HEAD, dirty state, commits, and push state to the user in the development session.

After it displays the prompt, it displays exactly:

```text
已准备开发交接提示词。请新建一个 session 并粘贴执行；研发完成后回到这里输入“编码完毕”告诉我。
```

No extra sentence describes `pr-create`, review, fix, merge, close, or any other later route.

The new development session is independent. The user may use Superpowers, SDD, or any other process there. That session must not invoke Neil later stages. Its text, completion claim, tool output, commits, tests, or Git activity do not themselves resume the original session.

## Waiting and Resume

The original session retains its validated pre-development handoff and enters `awaiting-coding`.

| Current context | On `编码完毕` in the original session |
|---|---|
| standalone `/issue-executing` | read and report the actual worktree Git state; do not invoke a later public stage |
| `/using-neil-workflows` after issue initialization | validate actual worktree identity and Git state, append owned `git` data, then continue with fresh `pr-create` |
| `/pr-fix` after accepted implementation outcomes | validate actual fix-worktree Git state, then complete only `/pr-fix`'s existing commit/push/reply/resolve ownership and return to its existing review route |

The phrase is considered only in the original session while its latest active Neil context is `awaiting-coding`. It is not a global command. A matching phrase in the development session, a different session, or an original session that is not waiting has no workflow effect.

No alternative wording, including "完成", "继续", "done", a commit message, or a child/framework report, resumes work. If the user has not entered the exact phrase in the original session, the session remains waiting.

On resume, the owner rereads the recorded worktree and validates repository, provider/host identity, branch, head repository, and actual Git head before any next-stage dispatch. A missing, inaccessible, dirty-when-clean-required, mismatched, or otherwise invalid worktree stops the current context and does not infer state from the development-session prose.

## PR Fix Handoff

When `/pr-fix` has accepted implementation outcomes that require coding, it creates a repair-oriented development handoff prompt rather than implementing the changes itself. The prompt identifies the matching PR/MR worktree, accepted outcomes, relevant locations, and required observable behavior. It retains the same boundaries and exact final display text as `/issue-executing`.

The prompt contains no thread reply text, resolution decision, provider command, commit subject, or test command. Those remain owned by the original `/pr-fix` context after `编码完毕`.

Rejected, clarified, deferred, or non-implementation outcomes do not create a development handoff. Existing review authorization and thread safeguards remain unchanged.

## Orchestration Boundaries

The `/using-neil-workflows` coordinator still owns stage sequence and validates only owned handoff leaves. It dispatches fresh `issue-init`, then asks its current implementation context to produce the development handoff and enters `awaiting-coding`; it does not dispatch `pr-create` until the user returns with the exact phrase and actual Git validation succeeds.

The coordinator does not edit code, run Git/provider business operations, create a development session, inspect the development session, or parse its prose. It only displays a prompt for the user to copy and resumes from its retained handoff when the user explicitly signals completion.

The existing post-`pr-create` self-review graph, remote authorization, review/fix convergence, merge gates, and issue-close rules are unchanged.

## Verification Strategy

Use RED-GREEN-REFACTOR pressure scenarios and static contract checks.

1. A Neil issue workflow produces the complete copyable handoff prompt and exact final display text, then does not dispatch `pr-create`.
2. A standalone `/issue-executing` produces the same handoff but does not create or invoke a later stage.
3. Empty and arbitrary non-empty execution strategies retain the documented fallback and literal-guidance semantics.
4. Commits, tests, tool output, a development-session "done", "完成", and "继续" in the original session do not resume a waiting workflow.
5. Only `编码完毕` in the original waiting context rechecks the actual worktree Git state.
6. A valid workflow resume appends owned actual Git state and dispatches exactly one fresh `pr-create`; an invalid worktree, branch, identity, or head stops first.
7. An accepted `/pr-fix` creates the repair handoff and waits; its valid resume performs only existing fix ownership before the next review. A rejected, clarified, or deferred finding does not create a handoff.
8. The handoff prompt never creates a PR/MR, writes configuration, replies/resolves threads, merges, closes issues, or routes later workflow stages.
9. Existing remote authorization and all post-`pr-create` terminal behavior remain unchanged.

## Non-Goals

- Do not create a subagent, client adapter, workflow service, session router, command, callback, or state file.
- Do not infer completion from any event except the exact user phrase in the original waiting context.
- Do not make the copied development session responsible for Neil workflow progression.
- Do not alter provider authorization, review/fix classification, merge criteria, or issue-close behavior.
