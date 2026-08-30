# GitHub PR API Reference

Operational syntax for GitHub branches of the PR workflow. Use live `gh` results as business data; this file is guidance only.

## Authentication and Repository

```bash
gh auth status --hostname <host>
gh repo view <host>/<base-owner>/<base-repo> --json nameWithOwner,url,defaultBranchRef
```

Do not print tokens. A failed auth check stops remote writes.

## Remote Base Configuration and Attestation

For every review/fix/merge automation decision, first resolve the normalized target base ref remotely. Do not read a clone, PR head, or fork:

```bash
gh api --hostname <host> --method GET \
  "repos/<owner>/<repo>/contents/.workflow-config.json?ref=<base-ref>"
```

Require response `encoding:"base64"`; decode `content`, parse the JSON, and retain response `sha` as `configBlobSha`. Only literal `self-reviewed:true` authorizes automation. Missing file/field or `false` is false; a non-boolean field, unexpected encoding, unreadable response, or mismatched target stops. Re-run this exact read immediately before every automated write.

GitHub stores an attestation as a PR-level COMMENT review, not an approval. Read the authenticated merge actor and paginated reviews; accept only a body with exactly two lines and exactly the required JSON keys, whose review `user.login` equals that actor:

```bash
gh api --hostname <host> --method GET user --jq .login
gh api --hostname <host> --method GET --paginate \
  "repos/<owner>/<repo>/pulls/<number>/reviews?per_page=100"
```
gh api --hostname <host> --method POST \
  "repos/<owner>/<repo>/pulls/<number>/reviews" \
  -F 'event=COMMENT' -f 'body=<neil-self-reviewed/v1 newline-delimited JSON body>'
```

Create only after a full converged current-head review and no exact existing tuple. The exact body is `neil-self-reviewed/v1`, a newline, then one compact JSON object with `provider`, `host`, `repository`, `number`, `headSha`, `baseRef`, and `configBlobSha`; it contains no `close`, `closes`, `fixes`, or `resolves` keyword.


```bash
gh issue view <issue-no> --repo <host>/<base-owner>/<base-repo> --json number,title,url,state
gh api --hostname <host> --method GET --paginate \
  -f state=open -f base='<base>' -f head='<head-owner>:<head-branch>' -F per_page=100 \
  "repos/<base-owner>/<base-repo>/pulls"
```

Treat an open PR returned for the base/head pair as the idempotent result. `<head-selector>` is `<head-branch>` for same-repository work or `<head-owner>:<head-branch>` for a fork.

## Create

For same-repository work or a user-owned fork, use native creation (`<head-selector>` is the branch or `<user>:<branch>`):

```bash
gh pr create --repo <host>/<base-owner>/<base-repo> --base <base> --head <head-selector> --title <title> --body <body>
gh pr create --repo <host>/<base-owner>/<base-repo> --base <base> --head <head-selector> --title <title> --body <body> --draft
```

For a fork, run `gh api --hostname <host> --method GET "users/<head-owner>" --jq .type`. When it returns `Organization`, do not use unsupported owner-qualified `gh pr create`; use REST:

```bash
gh api --hostname <host> --method POST "repos/<base-owner>/<base-repo>/pulls" \
  -f title='<title>' -f body='<body>' -f head='<head-owner>:<head-branch>' -f base='<base>' -F draft=false
gh api --hostname <host> --method POST "repos/<base-owner>/<base-repo>/pulls" \
  -f title='<title>' -f body='<body>' -f head='<head-owner>:<head-branch>' -f base='<base>' -F draft=true
```

Use the command whose draft value matches `pr-draft`.

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

Re-read the created PR by number:

```bash
gh pr view <number> --repo <host>/<base-owner>/<base-repo> \
  --json number,url,state,isDraft,baseRefName,headRefName,headRefOid,headRepository,headRepositoryOwner
```

Return its number, URL, state, draft flag, base, head repository/branch, and head SHA.

## Merge State and Writes

Route every command through the target host. `gh` 2.98.0 validates `--repo <host>/<owner>/<repo>` and `gh api --hostname <host>`.

```bash
gh pr view <number> --repo <host>/<owner>/<repo> --json state,isDraft,headRefOid,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,autoMergeRequest,mergedAt,mergeCommit
gh pr checks <number> --repo <host>/<owner>/<repo> --required --json name,state,bucket,link
gh api --hostname <host> --method GET "repos/<owner>/<repo>/branches/<base>/protection"
gh api --hostname <host> --method GET --paginate "repos/<owner>/<repo>/pulls/<number>/reviews?per_page=100"
```

Use `reviewDecision`, reviews, required check buckets for the current `headRefOid`, branch protection, `mergeable`, `mergeStateStatus`, and the paginated `reviewThreads` query below. If required protection data is inaccessible, stop rather than infer it.

Only after all gates and authorization pass, convert a draft:

```bash
gh pr ready <number> --repo <host>/<owner>/<repo>
```

Re-read every gate and use the allowed merge method. `--match-head-commit` binds either write to the reviewed SHA; do not use `--admin` or `--delete-branch`.

```bash
# Green required checks: request merge.
gh pr merge <number> --repo <host>/<owner>/<repo> --merge --match-head-commit <reviewed-head-sha>
# Pending required checks only: register auto-merge.
gh pr merge <number> --repo <host>/<owner>/<repo> --merge --auto --match-head-commit <reviewed-head-sha>
```

`gh pr merge --help` specifies that merge queues may enqueue these requests. Re-read until `state` is `MERGED`; return `mergedAt` and `mergeCommit.oid` only then. A non-merged `autoMergeRequest`, queue, or command response is pending.

### Orchestrated Issue-Close Proof Reread

For each bounded trusted `/issue-close` side effect, independently run this exact target read immediately before the effect:

```bash
gh pr view <number> --repo <host>/<owner>/<repo> \
  --json state,baseRefName,headRefName,headRefOid,mergedAt,mergeCommit
```

Require `state: MERGED`; bind and compare provider/host/repository/number, base/head branches, `headRefOid`, `mergeCommit.oid`, and `mergedAt` with the handoff. Missing, unreadable, non-merged, or mismatched data stops that effect.

## Review Metadata and Diff

A number, URL, branch, or omitted current branch is accepted by native `gh pr` commands. Normalize `headRepository.nameWithOwner` (with `headRepositoryOwner` as context) separately from the base URL repository; code checkout/push uses the head repository while all PR/review endpoints use the base repository:

```bash
gh pr view <selector> --json id,number,url,state,isDraft,headRefOid,baseRefName,headRefName,headRepository,headRepositoryOwner
gh api --hostname <host> --paginate "repos/<owner>/<repo>/pulls/<number>/files?per_page=100"
gh api --hostname <host> --paginate "repos/<owner>/<repo>/pulls/<number>/reviews?per_page=100"
gh api --hostname <host> -H 'Accept: application/vnd.github.diff' "repos/<owner>/<repo>/pulls/<number>"
```

Changed files may omit patches for binary or large content. Never invent a line location. Retain prior review IDs, authors, timestamps, and bodies; their hidden fingerprints cover previously confirmed PR-level findings that have no inline thread.

Query all threads with the root query below:

```bash
gh api graphql --hostname <host> --paginate \
  -f owner='<owner>' -f repo='<repo>' -F number='<number>' \
  -f query='<root reviewThreads query below>'
```

```graphql
query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
  viewer { login }
  repository(owner: $owner, name: $repo) {
    viewerPermission
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line startLine diffSide
          viewerCanReply viewerCanResolve
          comments(first: 100) {
            totalCount
            nodes { id databaseId url body createdAt author { login } }
          }
        }
      }
    }
  }
}
```

Use `--paginate`; its `$endCursor` variable drives this single root connection. When `comments.totalCount` exceeds 100, execute the node query separately:

```bash
gh api graphql --hostname <host> --paginate \
  -F threadId='<thread-node-id>' \
  -f query='<per-thread comments query below>'
```

```graphql
query($threadId: ID!, $endCursor: String) {
  node(id: $threadId) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes { id databaseId url body createdAt author { login } }
      }
    }
  }
}
```

Retain `viewer.login`, permissions, IDs/URLs, and timestamps for selection, duplicate detection, and reply idempotency. Handle nullable author/database ID defensively; the REST fallback requires an available `databaseId`.

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

For explicitly confirmed PR-level feedback, use the same endpoint with `event: "COMMENT"` and the fingerprinted finding in `body`, omitting `comments`. The reviews listing makes that body available for later duplicate suppression.

Added/context lines use `RIGHT`; deleted lines use `LEFT`. Multiline comments add `start_line` and `start_side`. Use modern line/side fields, never deprecated `position`.

Re-fetch `headRefOid` immediately before POST. One invalid location can reject the entire review, so validate every comment first. This skill uses `COMMENT`, never `APPROVE` or `REQUEST_CHANGES`.

## Select and Finish Threads

A URL fragment such as `#discussion_r<database-id>` selects that review comment only. Page GraphQL `reviewThreads` comments and match the comment database ID or exact URL to obtain its containing thread ID. Never expand a comment URL to every unresolved thread. Require repository write access plus authoritative per-thread permission fields; treat mutation results as final.

Use this mutation only when `viewerCanReply` is true:

```bash
gh api graphql --hostname <host> \
  -F threadId='<thread-node-id>' -f body='<confirmed reply>' \
  -f query='<reply mutation below>'
```

```graphql
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId,
    body: $body
  }) { comment { id url } }
}
```

When `viewerCanReply` is true but the thread mutation is unavailable, use the selected review-comment ID as the REST fallback through `gh api --hostname <host>`:

```bash
gh api --hostname <host> --method POST \
  "repos/<owner>/<repo>/pulls/<number>/comments/<comment-id>/replies" \
  -f 'body=<confirmed reply>'
```

After a successful accepted reply, resolve only when `viewerCanResolve` is true and the thread is unresolved:

```bash
gh api graphql --hostname <host> \
  -F threadId='<thread-node-id>' \
  -f query='<resolve mutation below>'
```

```graphql
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}
```

Do not call `resolveReviewThread` when reply creation failed, `viewerCanResolve` is false, or classification is reject/clarify. Outdated status alone never authorizes resolution. Re-query after each mutation and inspect GraphQL `errors` even on HTTP success.

Before replying on a repeated run, compare the authenticated author's latest equivalent reply timestamp with later reviewer comments. With no later reviewer message, skip a duplicate reply; when only resolution previously failed, retry resolution only.
