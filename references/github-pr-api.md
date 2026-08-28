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
