# PR Workflow Contract

Shared contract for `pr-create`, `pr-review`, and `pr-fix`. Public skills own decisions; provider references own command and API syntax.

## Optional Configuration

The PR skills may read `.workflow-config.json` only when it belongs to the target repository. They never create or modify it.

| Field | Missing default |
|---|---|
| `base-branch` | `main` |
| `branch-template` | `feature/{issue-no}-{issue-subject}` |
| `need-worktree` | `true` |
| `pr-draft` | `false` |
| `pr-auto-close-issue` | `false` |

A malformed present config is an error for the fields the current skill needs. Do not silently rewrite it.

## Normalized Target

Use these field names across provider branches:

```text
provider, host, repository, number, url, baseBranch,
headRepository, headBranch, headSha
```

For `pr-create`, resolve provider and repository from the current Git remote, `headBranch` from the current branch, and `baseBranch` from config/defaults. Populate number, URL, and head SHA from an existing or newly created PR/MR response.

## Issue Resolution

Apply `branch-template` to the complete current branch and extract `{issue-no}`. If extraction fails, use an issue number explicitly supplied by the user. Otherwise ask; never guess from unrelated digits or branch text.

Verify the issue exists before creating a PR/MR.

## Identity and Configuration

An explicit future PR/MR URL is authoritative for provider, host, repository, and number. Ignore configuration from an unrelated local repository. Local configuration applies only when its Git remote matches the target repository.

## Error Semantics

Distinguish:

- Authentication failure: missing, invalid, or expired credentials.
- Authorization failure: authenticated identity lacks the required permission.
- Not found: resource is absent, or a private resource is hidden; report both possibilities.
- Invalid state: wrong branch, closed target, dirty state, or missing issue relationship.
- Stale state: remote head/diff changed; re-fetch before a write.

Never expose tokens or credential contents.

## Idempotency

Read remote state before every create. If the current head branch already has an open PR/MR, return it unchanged. Do not duplicate it, edit it merely to match generated text, or invoke the next workflow stage.
