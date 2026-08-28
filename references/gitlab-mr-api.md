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

## Review Metadata and Diff

```bash
glab mr view <iid-or-url> -R <group/project> -F json
glab api --hostname <host> "projects/<encoded-project>/merge_requests/<iid>"
glab api --hostname <host> "projects/<encoded-project>/merge_requests/<iid>/versions"
glab api --hostname <host> --paginate "projects/<encoded-project>/merge_requests/<iid>/diffs?per_page=100"
glab api --hostname <host> --paginate "projects/<encoded-project>/merge_requests/<iid>/discussions?per_page=100"
```

Use the newest diff version and retain `base_sha`, `start_sha`, and `head_sha`. Existing discussions provide semantic duplicate context.

## Create Inline Discussion

Use stable REST through `glab api --hostname <host>` rather than experimental `glab mr note` commands:

```text
POST projects/:id/merge_requests/:iid/discussions
```

Send `body` plus a text position containing:

```json
{
  "position_type": "text",
  "base_sha": "<base>",
  "start_sha": "<start>",
  "head_sha": "<head>",
  "old_path": "src/example.ts",
  "new_path": "src/example.ts",
  "new_line": 42
}
```

Use exactly one applicable `old_line` or `new_line`. Renames retain both paths. Multiline positions additionally require GitLab's `line_range` start/end objects.

Re-fetch MR/version/diff immediately before publication. If a position is stale, recompute it against the new SHA tuple and re-preview the changed finding. Discussions are separate writes; record each successful discussion and never resend it when a later item fails.

## Select and Finish Discussions

An exact discussion/note URL selects its containing discussion only. Match URL anchor or note ID against paginated discussion notes; never expand it to every unresolved discussion.

Reply through stable REST:

```text
POST projects/:id/merge_requests/:iid/discussions/:discussion_id/notes
body=<confirmed reply>
```

For an accepted discussion only, after the reply succeeds, resolve through:

```text
PUT projects/:id/merge_requests/:iid/discussions/:discussion_id?resolved=true
```

Execute both with `glab api --hostname <host>`. Reject and clarify discussions remain unresolved. Re-fetch the discussion after each write and record actual note and resolved state. On failure, retain prior successes and retry only the incomplete reply or resolution.
