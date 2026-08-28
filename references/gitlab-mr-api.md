# GitLab MR API Reference

Operational syntax for GitLab branches of the PR workflow. Prefer stable native create/view operations here; later discussion operations use REST.

## Authentication and Repository

```bash
glab auth status --hostname <host>
glab api --hostname <host> --method GET "projects/<encoded-base-project>"
```

Do not print tokens. A failed auth check stops remote writes.

## Issue and Existing MR

```bash
glab issue view <issue-iid> --repo <base-project-url>
glab api --hostname <host> --method GET --paginate "projects/<encoded-base-project>/merge_requests?state=opened&target_branch=<encoded-base-branch>&source_branch=<encoded-head-branch>&source_project_id=<head-project-id>"
```

Treat an open MR returned for the head branch as the idempotent result.

## Create

```bash
# pr-auto-close-issue false: non-closing ready/draft
glab mr create --repo <base-project-url> --head <head-project> --source-branch <head> --target-branch <base> --title <title> --description '<body with Related to #<issue-iid>>' --yes
glab mr create --repo <base-project-url> --head <head-project> --source-branch <head> --target-branch <base> --title <title> --description '<body with Related to #<issue-iid>>' --draft --yes

# pr-auto-close-issue true: provider closing relationship
glab mr create --repo <base-project-url> --head <head-project> --related-issue <issue-iid> --source-branch <head> --target-branch <base> --title <title> --description <body> --yes
glab mr create --repo <base-project-url> --head <head-project> --related-issue <issue-iid> --source-branch <head> --target-branch <base> --title <title> --description <body> --draft --yes
```

Use `--draft` only when `pr-draft` is true. Omit `--related-issue` when `pr-auto-close-issue` is false because `glab` generates a closing relationship for that option.

### Issue relationship

When `pr-auto-close-issue` is false, omit `--related-issue`, include `Related to #<issue-iid>` in the description, and avoid closing keywords.

When it is true, use `--related-issue <issue-iid>` (or an equivalent supported closing reference). Closing happens after an eligible merge, never when the MR is opened.

## Result

Re-read the created MR with `glab mr view <iid> --repo <base-project-url> -F json`. Normalize the IID as `number` and return URL, state, draft flag, target/source branches, source project, and head SHA.

## Review Metadata and Diff

Route every call with the host parsed from the target URL:

```bash
glab api --hostname <host> --method GET user
glab api --hostname <host> --method GET "projects/<encoded-project>/merge_requests/<iid>"
# For a fork, resolve the returned source_project_id:
glab api --hostname <host> --method GET "projects/<source-project-id>"
glab api --hostname <host> --method GET "projects/<encoded-project>/merge_requests/<iid>/versions"
glab api --hostname <host> --method GET --paginate "projects/<encoded-project>/merge_requests/<iid>/diffs?per_page=100"
glab api --hostname <host> --method GET --paginate "projects/<encoded-project>/merge_requests/<iid>/discussions?per_page=100"
```

`GET user` supplies the authenticated `username`. Normalize MR `source_branch` as `headBranch`, its current source SHA as `headSha`, and the source project's `path_with_namespace` as `headRepository`. Checkout/push uses that source project; MR/discussion APIs continue using the base `<encoded-project>`.

The versions response is newest first. Map its fields into the position payload:

| Version response | Position field |
|---|---|
| `base_commit_sha` | `base_sha` |
| `start_commit_sha` | `start_sha` |
| `head_commit_sha` | `head_sha` |

Existing discussion notes provide selection, permissions, and duplicate context.

## Create Inline Discussion

Use stable REST rather than experimental `glab mr note`. Send `body` and a nested position object:

```bash
glab api --hostname <host> --method POST \
  "projects/<encoded-project>/merge_requests/<iid>/discussions" \
  -F 'body=<finding plus hidden fingerprint>' \
  -F 'position={"position_type":"text","base_sha":"<base>","start_sha":"<start>","head_sha":"<head>","old_path":"src/example.ts","new_path":"src/example.ts","new_line":42}'
```

For explicitly confirmed MR-level feedback, use the same `POST .../discussions` with `-F 'body=<fingerprinted finding>'` and omit `position`. Paginated discussions expose that body for later duplicate suppression.

Added lines use `new_line`, removed lines use `old_line`, and unchanged context uses both. Renames retain both paths. Multiline positions add GitLab `line_range` start/end objects.

Re-fetch MR/version/diff immediately before publication. If stale, recompute against the new SHA tuple and re-preview changed findings. Record each successful discussion and never resend it after a later item fails.

## Select and Finish Discussions

An exact note URL selects its containing discussion only. Match note ID/URL in paginated `notes[]`; never expand scope. Identify the root review note by `type == "DiffNote"` and non-null `position` (or the earliest root note for a non-diff discussion).

Reply through stable REST:

```bash
glab api --hostname <host> --method POST \
  "projects/<encoded-project>/merge_requests/<iid>/discussions/<discussion-id>/notes" \
  -F 'body=<confirmed reply>'
```

For an accepted thread only, resolve the whole discussion after verified outcome and successful reply:

```bash
glab api --hostname <host> --method PUT \
  "projects/<encoded-project>/merge_requests/<iid>/discussions/<discussion-id>" \
  -F 'resolved=true'
```

Require the selected root note's `resolvable == true` and `resolved == false`. Outdated status alone is insufficient. Reject/clarify remain unresolved. Re-fetch after each write; retain successes and retry only incomplete operations.

Before replying again, compare `GET user`'s username with note authors. Skip an equivalent own reply when no later reviewer note exists; if only resolution failed, retry resolution only.
