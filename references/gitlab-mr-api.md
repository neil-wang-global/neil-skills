# GitLab MR API Reference

Operational syntax for GitLab branches of the PR workflow. Prefer stable native create/view operations here; later discussion operations use REST.

## Authentication and Repository

```bash
glab auth status --hostname <host>
glab api --hostname <host> --method GET "projects/<encoded-base-project>"
```

Do not print tokens. A failed auth check stops remote writes.

## Remote Base Configuration and Attestation

For every review/fix/merge automation decision, retrieve the normalized target base ref through GitLab; never read a clone, MR head, or fork:

```bash
glab api --hostname <host> --method GET \
  "projects/<encoded-project>/repository/files/.workflow-config.json?ref=<encoded-base-ref>"
```

Require `encoding:"base64"`; decode `content`, parse JSON, and retain `blob_id` as `configBlobSha`. Only literal `self-reviewed:true` authorizes automation. Missing file/field or `false` is false; a non-boolean field, unexpected encoding, unreadable response, or mismatched target stops. Repeat the read immediately before every automated write.

GitLab stores an attestation as a general non-diff MR note, which does not create a resolvable discussion. Read the authenticated merge actor and all notes; accept only an exact two-line body with exactly required JSON keys whose note `author.username` equals that actor. Create a note only after a converged current-head review and no exact existing tuple:

```bash
glab api --hostname <host> --method GET user
glab api --hostname <host> --method GET --paginate \
  "projects/<encoded-project>/merge_requests/<iid>/notes?per_page=100"
```
glab api --hostname <host> --method POST \
  "projects/<encoded-project>/merge_requests/<iid>/notes" \
  -f 'body=<neil-self-reviewed/v1 newline-delimited JSON body>'
```

The exact body is `neil-self-reviewed/v1`, a newline, then one compact JSON object with `provider`, `host`, `repository`, `number`, `headSha`, `baseRef`, and `configBlobSha`; it must not include closing keywords. The returned note ID/URL is provider evidence; keep it in the review result without treating it as an unresolved discussion.


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

## Merge State and Writes

Route every call through the host parsed from the MR URL. `glab` 1.115.0 supports native commands with a full `--repo <base-project-url>` and REST with `--hostname <host>`; URL-encode project and branch path components.

```bash
glab api --hostname <host> --method GET "projects/<encoded-project>/merge_requests/<iid>"
glab api --hostname <host> --method GET "projects/<encoded-project>/merge_requests/<iid>/approvals"
glab api --hostname <host> --method GET "projects/<encoded-project>/merge_requests/<iid>/approval_state"
glab api --hostname <host> --method GET "projects/<encoded-project>/protected_branches/<encoded-base-branch>"
glab api --hostname <host> --method GET --paginate "projects/<encoded-project>/merge_requests/<iid>/discussions?per_page=100"
```

The MR response supplies `draft`, `sha`, `has_conflicts`, `merge_status`, `detailed_merge_status`, `merge_when_pipeline_succeeds`, `state`, `merged_at`, and `merge_commit_sha`. Its current-head `detailed_merge_status` is the provider-authoritative merge/CI gate; do not infer required status from `pipelines` or `head_pipeline`. Only `mergeable` permits immediate merge. Only `ci_still_running` permits auto-merge, and only when `sha` equals `reviewed-head-sha`. `ci_must_pass`, `checking`, every other documented or unknown status, conflicts, missing approvals, protection blocks, or inaccessible required state stop. Independently require the current `sha`, approval-state rules, target protection, no conflicts, and every discussion resolved.

After all gates and authorization pass, make a draft ready and re-read every gate:

```bash
glab mr update <iid> --repo <base-project-url> --ready --yes
```

Use the reviewed SHA for every merge write. Current `glab mr merge --help` documents `--auto-merge=false` for immediate merge and `--auto-merge` for provider auto-merge; it has no `--when-pipeline-succeeds` flag.

```bash
# Only current-head detailed_merge_status=mergeable: request merge now.
glab mr merge <iid> --repo <base-project-url> --sha <reviewed-head-sha> --auto-merge=false --yes
# Only current-head detailed_merge_status=ci_still_running: register auto-merge.
glab mr merge <iid> --repo <base-project-url> --sha <reviewed-head-sha> --auto-merge --yes
```

GitLab's current merge REST schema is `PUT /projects/:id/merge_requests/:merge_request_iid/merge` with `sha` and `auto_merge`; `merge_when_pipeline_succeeds` is deprecated. Re-read the MR until `state` is `merged`, then return `merge_commit_sha` and `merged_at`. Auto-merge registration or a queue is pending, not success.

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
