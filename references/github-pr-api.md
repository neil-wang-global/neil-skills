# GitHub PR API Reference

Operational syntax for GitHub branches of the PR workflow. Use live `gh` results as business data; this file is guidance only.

## Authentication and Repository

```bash
gh auth status --hostname <host>
gh repo view --json nameWithOwner,url,defaultBranchRef
```

Do not print tokens. A failed auth check stops remote writes.

## Issue and Existing PR

```bash
gh issue view <issue-no> --json number,title,url,state
gh pr view <head-branch> --json id,number,url,state,isDraft,headRefName,headRefOid,baseRefName
```

Treat an open PR returned for the head branch as the idempotent result.

## Create

```bash
gh pr create --base <base> --head <head> --title <title> --body <body>
gh pr create --base <base> --head <head> --title <title> --body <body> --draft
```

Use `--draft` only when `pr-draft` is true.

### Issue relationship

When `pr-auto-close-issue` is false, use a non-closing line:

```text
Related to #<issue-no>
```

Do not use `Fixes`, `Closes`, or `Resolves` in that mode.

When it is true, use:

```text
Closes #<issue-no>
```

A closing keyword closes the issue after an eligible merge, never when the PR is opened.

## Result

Re-read the created PR with `gh pr view` and return its number, URL, state, draft flag, base, head branch, and head SHA.

## Review Metadata and Diff

A number, URL, branch, or omitted current branch is accepted by native `gh pr` commands:

```bash
gh pr view <selector> --json id,number,url,state,isDraft,headRefOid,baseRefName,headRefName
gh api --hostname <host> --paginate "repos/<owner>/<repo>/pulls/<number>/files?per_page=100"
gh api --hostname <host> -H 'Accept: application/vnd.github.diff' "repos/<owner>/<repo>/pulls/<number>"
```

Changed files may omit patches for binary or large content. Never invent a line location.

Query existing threads with `gh api graphql --hostname <host>`, using `repository.pullRequest.reviewThreads` and paging through all results. Read thread ID, resolution/outdated state, path, line/range, diff side, and comment bodies/URLs for duplicate detection.

## Submit One Inline Review

`gh pr review` cannot batch inline comments. Use `gh api --hostname <host>` with REST:

```text
POST /repos/{owner}/{repo}/pulls/{number}/reviews
```

Payload shape:

```json
{
  "commit_id": "<current-head-sha>",
  "event": "COMMENT",
  "body": "<review summary>",
  "comments": [
    {
      "path": "src/example.ts",
      "line": 42,
      "side": "RIGHT",
      "body": "<finding plus hidden fingerprint>"
    }
  ]
}
```

Added/context lines use `RIGHT`; deleted lines use `LEFT`. Multiline comments add `start_line` and `start_side`. Use modern line/side fields, never deprecated `position`.

Re-fetch `headRefOid` immediately before POST. One invalid location can reject the entire review, so validate every comment first. This skill uses `COMMENT`, never `APPROVE` or `REQUEST_CHANGES`.

## Select and Finish Threads

A URL fragment such as `#discussion_r<database-id>` selects that review comment only. Page GraphQL `reviewThreads` comments and match the comment database ID or exact URL to obtain its containing thread ID. Never expand a comment URL to every unresolved thread.

Use `gh api graphql --hostname <host>` for replies:

```graphql
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId,
    body: $body
  }) { comment { id url } }
}
```

After a successful accepted reply, resolve with:

```graphql
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}
```

Do not call `resolveReviewThread` when reply creation failed or classification is reject/clarify. Re-query the thread after each mutation and record its actual state. GraphQL failures may return HTTP success with an `errors` array; treat any error as failure.
