# PR Workflow Skills Design

## Status

Approved design for four reusable skills in `neil-skills`:

- `/issue-executing`
- `/pr-create`
- `/pr-review`
- `/pr-fix`

This document defines responsibilities, inputs, observable outcomes, configuration, platform boundaries, and validation scenarios. It does not prescribe how feature code or review fixes must be implemented.

## Context

The repository already provides `/issue-init` and `/issue-close`. The new skills extend the workflow without automatically chaining its stages:

```text
issue-init -> issue-executing -> pr-create
-> pr-review -> pr-fix -> pr-review/pr-fix
-> human approval and merge -> issue-close
```

This is a recommended invocation order, not an orchestrator. Each public skill remains directly invocable.

## Goals

1. Create a GitHub pull request or GitLab merge request for the current development branch and link it to its issue.
2. Review a PR/MR by URL, number, or current branch and publish actionable inline comments after a preview gate.
3. Process all unresolved review threads or one explicitly linked web comment, implement accepted feedback through `/issue-executing`, and finish the remote conversation safely.
4. Allow `/pr-review <URL>` to run without a local clone.
5. Allow `/pr-fix` to prepare or reuse an isolated worktree by default.
6. Keep GitHub and GitLab behavior consistent while using each platform's stable APIs.
7. Let each project optionally supply an execution strategy without making that strategy mandatory.

## Non-Goals

- Automatically invoking the next workflow stage.
- Automatically approving or merging a PR/MR.
- Automatically cloning repositories for `/pr-fix`.
- Defining coding methods, architecture rules, test commands, or implementation prompts inside `/pr-fix`.
- Persisting PR numbers or review state in local files.
- Rewriting commits produced by an execution strategy.
- Deleting remote branches.

## Configuration

The repository-root `.workflow-config.json` remains the shared optional configuration file. `/issue-init` creates it when missing. The four new skills never create or modify it.

The default file created by `/issue-init` is:

```json
{
  "type": "github",
  "base-branch": "main",
  "branch-template": "feature/{issue-no}-{issue-subject}",
  "need-worktree": true,
  "execution-strategy": "",
  "pr-draft": false,
  "pr-auto-close-issue": false,
  "remarks": ""
}
```

### New fields

| Field | Type | Default | Owner |
|---|---|---:|---|
| `execution-strategy` | string | `""` | `/issue-executing` |
| `pr-draft` | boolean | `false` | `/pr-create` |
| `pr-auto-close-issue` | boolean | `false` | `/pr-create` |

`need-worktree` is shared by `/issue-init` and `/pr-fix` because both prepare development environments.

### Missing configuration

When `.workflow-config.json` or a relevant field is absent, the new skills continue with defaults. They do not create the file.

For a URL targeting a repository different from the current local repository, local configuration and `remarks` are ignored. The URL determines the host, provider, repository, and PR/MR number. This prevents rules from an unrelated working directory from affecting a remote review.

## Shared Target Resolution

All PR skills normalize a target to the following conceptual fields:

```text
provider, host, repository, number, url, base branch,
head repository, head branch, head SHA
```

Selector precedence is:

1. Explicit review-comment URL.
2. Explicit PR/MR URL.
3. Explicit number in the current repository.
4. PR/MR associated with the current branch.

A bare number or omitted selector requires local repository context. A full URL does not require local context for `/pr-review`.

Provider selection follows the explicit URL first, then the matching local repository remote, then local configuration. Authentication and permissions are checked against the selected host without exposing tokens.

## Skill: `/issue-executing`

### Purpose

Execute development work using the current task context and an optional project-defined execution strategy.

### Inputs

The skill may receive context from:

- The direct user request.
- The current issue and branch.
- The current conversation.
- A structured remediation brief supplied by `/pr-fix`.

### Strategy behavior

If the matching repository contains a non-empty `execution-strategy`, its complete string is added as natural-language execution guidance.

The value is not treated as a shell command. It is not restricted to a skill name. If the text itself requests an available skill, normal skill discovery and invocation rules apply.

If the field or file is absent, the skill adds no strategy guidance and execution proceeds naturally under the active agent and project instructions.

### Responsibility boundary

`/issue-executing` may edit code, create commits, or push if its effective strategy leads it to do so. It does not promise any particular git end state to callers. Callers must inspect the repository after it returns.

The skill does not own PR review threads, replies, or resolution.

## Skill: `/pr-create`

### Invocation

```text
/pr-create
```

It requires the current directory to belong to the target local repository and the current branch to be the intended PR/MR head branch.

### Flow

1. Read optional configuration and applicable `remarks`.
2. Resolve provider, base branch, current head branch, and issue number.
3. Extract the issue number from `branch-template`; if this is impossible, ask for an issue number instead of guessing.
4. Verify the remote issue exists.
5. Check whether the current branch already has an open PR/MR. If so, return it without creating a duplicate.
6. Require committed branch content and ensure the remote head contains the intended commits.
7. Generate a title and a body containing summary, testing information available from context, and an issue relationship.
8. Create a ready PR/MR by default; use draft mode only when `pr-draft` is true.
9. Return the PR/MR URL, base/head branches, related issue, and draft state.

### Issue relationship

Every created PR/MR must link its issue.

- `pr-auto-close-issue: false`: use a non-closing relationship.
- `pr-auto-close-issue: true`: use the provider's closing reference so merging closes the issue.

Creating the PR/MR never closes the issue immediately.

### Boundaries

The skill does not invoke `/pr-review`, approve, merge, or delete branches.

## Skill: `/pr-review`

### Invocation

```text
/pr-review
/pr-review <number>
/pr-review <PR-or-MR-URL>
```

A full URL can be reviewed from any directory without a local clone. A number or omitted selector uses the current repository.

### Review flow

1. Resolve the target and provider authentication.
2. Require an open PR/MR and capture its current head SHA.
3. Fetch the complete available changed-file metadata, diff, and existing review threads.
4. Perform a full review on every invocation.
5. Retain only actionable findings and map each one to a reliable diff location.
6. Compare findings with existing threads and skill fingerprints to suppress duplicate comments.
7. Present the complete review draft before any remote write.
8. Let the user remove or revise findings, then obtain one publication confirmation.
9. Re-fetch the head SHA and diff immediately before publishing. Re-map and re-preview any finding affected by a changed head.
10. Publish inline comments and report exact successes and failures.

### Finding contract

Each draft finding contains:

- Severity: `critical`, `high`, `medium`, or `low`.
- Concise title.
- Why the issue is valid.
- Observable consequence or risk.
- Suggested correction direction.
- File path and old/new side line coordinates.

The skill does not publish speculative style preferences as defects.

### Publication behavior

GitHub publishes one review containing multiple inline comments through the pull-request review REST API. Its event is `COMMENT`, not approval or request changes.

GitLab creates inline diff discussions through the REST API. Because this is not atomic, the skill records each successful discussion and retries only failed items.

Each published finding includes a hidden versioned fingerprint based on the finding identity. Duplicate prevention combines the fingerprint with semantic comparison against existing threads.

If a binary, truncated, outdated, or otherwise unavailable diff cannot support a reliable inline location, the draft marks the finding as non-inline. The user may explicitly choose a PR-level comment. The skill never attaches a comment to a guessed line.

No findings results in a local report only. The skill does not auto-approve or publish a no-op review.

## Skill: `/pr-fix`

### Invocation

```text
/pr-fix
/pr-fix <number>
/pr-fix <PR-or-MR-URL>
/pr-fix <review-comment-URL>
```

A review-comment URL identifies one GitHub review thread or GitLab discussion. A PR/MR selector processes its unresolved review threads. An omitted selector uses the current branch.

### Local repository requirement

Unlike `/pr-review`, `/pr-fix` requires a local clone matching the target repository because it may change and push code. It does not automatically clone an absent repository.

### Worktree behavior

The default is `need-worktree: true` even when no configuration exists.

1. Reuse the current worktree when it already holds the target head branch.
2. Otherwise reuse an existing worktree for that branch when safe.
3. Otherwise fetch the writable head branch and create an isolated worktree.
4. With `need-worktree: false`, require a clean current worktree before checking out the target branch.
5. Stop before implementation when the target head is not writable.

Worktree names follow the existing issue workflow convention by replacing branch slashes with plus signs. `/pr-fix` keeps the worktree after completion so another review/fix iteration can reuse it. It reports the path explicitly.

### Thread classification

Before implementation, classify each selected unresolved thread as:

- `accept`: the feedback is valid and requires a code change.
- `reject`: the feedback is inapplicable or based on an incorrect technical premise.
- `clarify`: the expected behavior is ambiguous or information is missing.

Present one classification table with reasons and obtain one confirmation. Do not interrupt once per thread.

### Implementation delegation

`/pr-fix` builds one remediation brief containing the accepted thread text, relevant PR context, affected paths and lines, and required observable outcomes. It invokes `/issue-executing` with that brief.

The brief describes what feedback was accepted. It does not prescribe coding methods, architecture, test commands, or implementation techniques.

Before delegation, `/pr-fix` records the worktree status, local head, upstream head, and remote PR/MR head. After delegation it re-reads all four states.

### Git completion

`/pr-fix` treats the result of `/issue-executing` as authoritative and does not rewrite its history:

1. Preserve any commits already created.
2. Preserve any pushes already completed.
3. If accepted changes remain uncommitted, create one completion commit.
4. If any resulting commits are not on the remote head, push them.
5. Do not create an empty commit.

This replaces the earlier single-commit-per-round constraint. The execution strategy controls commits it creates; `/pr-fix` only completes missing git work.

### Remote thread completion

After the git state is complete:

- `accept`: verify the accepted outcome exists, reply with the result and relevant commit identity, then resolve only after the reply succeeds.
- `reject`: reply with the technical reason and leave unresolved.
- `clarify`: reply with the specific question and leave unresolved.

An outdated thread is not automatically resolved. A failure to edit, commit, push, reply, or verify the outcome prevents resolution of the affected thread.

On a repeated run, the skill re-fetches remote state. It does not repeat its own reply when no reviewer message has appeared after that reply.

## Platform Adapter Boundary

The public skills use one shared conceptual contract while provider references hold exact operations.

### GitHub

- Native `gh pr` operations: locate, view, create, and fetch a human-readable diff.
- REST through `gh api`: changed files and one review with multiple inline comments using `path`, `line`, `side`, and current `commit_id`.
- GraphQL through `gh api graphql`: enumerate review threads, inspect reply/resolve permissions, reply by thread ID, and resolve accepted threads.

Modern line/side coordinates are required. Deprecated patch positions are not used.

### GitLab

- Native `glab mr` operations: locate, view, create, and fetch a raw diff.
- REST through `glab api`: current diff version, changed files, inline discussions, replies, and resolution.

Inline positions use the current `base_sha`, `start_sha`, and `head_sha`, both paths, and exactly the applicable old or new line. Native `glab mr note` is not the durable core because that command surface is experimental.

## Error and Idempotency Contract

The skills distinguish authentication failure, insufficient permission, hidden or missing resources, stale diff state, dirty worktree state, and partial remote publication.

They always report:

- The resolved target.
- The head SHA used.
- Completed remote writes.
- Failed or skipped writes.
- Whether any thread was resolved.
- The resulting local branch/worktree when applicable.

A push failure cannot be reported as fixed. A reply failure cannot be followed by resolution. A stale head forces re-fetching and re-evaluation. Existing PRs, comments, replies, commits, pushes, and resolved threads are detected before creating duplicates.

## Relationship to Existing Skills

### `/issue-init`

Update its default configuration and documentation with `execution-strategy`, `pr-draft`, and `pr-auto-close-issue`. Its existing issue and branch initialization behavior remains intact.

### `/issue-close`

It remains independently invoked and does not call PR skills. Its cleanup must remain limited to the current issue's worktree and local branches. No remote feature branch is deleted.

### No automatic chaining

Only `/pr-fix` has one explicit internal delegation to `/issue-executing`. No other skill invokes the next workflow stage.

## Repository Layout

Planned additions and updates:

```text
skills/issue-executing/SKILL.md
skills/pr-create/SKILL.md
skills/pr-review/SKILL.md
skills/pr-fix/SKILL.md
references/pr-workflow-contract.md
references/github-pr-api.md
references/gitlab-mr-api.md
skills/issue-init/SKILL.md
README.md
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

Exact provider payloads live in references so the public skills remain concise and consistent.

## Skill Validation Strategy

Each new skill is developed and validated separately using the `writing-skills` RED-GREEN-REFACTOR process. A later skill is not authored before the current skill passes its scenarios.

Required scenario coverage includes:

- GitHub and GitLab.
- Current branch, number, PR/MR URL, and review-comment URL selectors.
- Missing configuration and missing individual fields.
- Empty and non-empty execution strategies.
- `/pr-review <URL>` outside a local repository.
- Existing, reusable, new, dirty, and non-writable worktrees.
- Execution that makes no commit, commits without pushing, and commits plus pushes.
- Added, removed, renamed, binary, truncated, and stale diff locations.
- Repeated review and fix invocations without duplicate remote writes.
- Rejected and clarification threads remaining unresolved.
- Authentication failure, insufficient permissions, hidden resources, stale heads, and partial API publication.

Validation checks the observable behavior and decisions of the skills. It does not introduce project implementation instructions into `/pr-fix`.

## Acceptance Criteria

1. All four public skills can be discovered and invoked by name.
2. The three PR skills work without creating configuration files.
3. `/pr-review <URL>` works without a local clone.
4. `/pr-create` always relates an issue and honors the two PR configuration fields.
5. `/pr-review` previews before publishing and creates reliable inline comments without duplicates.
6. `/pr-fix` uses a worktree by default, delegates accepted implementation to `/issue-executing`, completes missing commit/push work, and resolves only successfully addressed threads.
7. Rejected and clarification threads receive replies but remain unresolved.
8. `execution-strategy` is optional natural-language guidance and does not execute as a shell command.
9. No skill automatically approves, merges, advances to the next public stage, or deletes remote branches.
10. Existing issue workflow behavior remains compatible with the expanded default configuration.
