# GitLab MR API Reference

Operational syntax for GitLab branches of the PR workflow. Prefer stable native create/view operations here; later discussion operations use REST.

## Authentication and Repository

```bash
glab auth status --hostname <host>
glab repo view -F json
```

Do not print tokens. A failed auth check stops remote writes.

## Issue and Existing MR

```bash
glab issue view <issue-iid>
glab mr view <head-branch> -F json
```

Treat an open MR returned for the head branch as the idempotent result.

## Create

```bash
glab mr create --related-issue <issue-iid> --source-branch <head> --target-branch <base> --title <title> --description <body> --yes
glab mr create --related-issue <issue-iid> --source-branch <head> --target-branch <base> --title <title> --description <body> --draft --yes
```

Use `--draft` only when `pr-draft` is true. `--related-issue` establishes the GitLab issue relationship in both modes.

### Issue relationship

When `pr-auto-close-issue` is false, include a non-closing reference in the description and avoid closing keywords.

When it is true, include GitLab's supported closing reference for the target issue. Closing happens after an eligible merge, never when the MR is opened.

## Result

Re-read the created MR with `glab mr view <head-branch> -F json`. Normalize the IID as `number` and return URL, state, draft flag, target/source branches, and head SHA when exposed.
