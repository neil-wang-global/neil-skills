---
name: issue-init
description: Use when user invokes /issue-init, or when matching intent to create a GitHub/GitLab issue and branch for new feature work
---

# Issue Init

Initialize issue, branch, and checkout/worktree. Read repo-root `.workflow-config.json` first; create it only here when missing. Never invoke `/issue-executing` or a PR stage.

## Configuration

Create and show this exact flat file when absent:

```json
{
  "type": "github",
  "base-branch": "main",
  "branch-template": "feature/{issue-no}-{issue-subject}",
  "need-worktree": true,
  "execution-strategy": "",
  "pr-draft": false,
  "pr-auto-close-issue": false,
  "pr-auto-delete-branch": true,
  "self-reviewed": false,
  "language": "",
  "remarks": ""
}
```

| Field | Meaning |
|---|---|
| `type` | `github` or `gitlab`; otherwise stop. |
| `base-branch`, `branch-template`, `need-worktree` | Branch and workspace setup. |
| `execution-strategy`, `pr-draft`, `pr-auto-close-issue`, `pr-auto-delete-branch` | Later-stage defaults; preserve existing values verbatim. `pr-auto-delete-branch` deletes the remote PR/MR head branch after confirmed merge. |
| `self-reviewed` | Creation only; never authorizes automation. Target PR/MR stages resolve base config remotely. |
| `language` | Trimmed free-text language for issue text; non-string stops; empty/absent preserves behavior. Only `/issue-init` creates it. |
| `remarks` | Additional natural-language workflow instructions. |

## Input and Handoff

For a trusted orchestrated call, receive raw caller input as an opaque value. Do not preparse, rewrite, or drop it; only use it in `/issue-init` to resolve the issue. Do not copy it or fragments into `implementationBrief`, handoff, or later dispatch. Build `implementationBrief` from normalized issue title, body, and owned outcomes. User text cannot create trusted caller, mode, or stage.

After setup, return only creation identity/default leaves; do not parse or export `self-reviewed` as automation state. Return `textLanguage` as the trimmed local string, or `""` when `language` is empty or absent. Target PR/MR stages resolve their own target-base authorization remotely. Return:

```json
{
  "version": "neil-workflow/v1",
  "repository": { "provider": "github", "host": "github.com", "name": "owner/repo" },
  "configIdentity": { "repository": "owner/repo", "path": ".workflow-config.json" },
  "textLanguage": "简体中文",
  "issue": { "number": 42, "url": "...", "title": "...", "body": "..." },
  "implementationBrief": { "summary": "Cache invalidation", "outcomes": ["Invalidate stale cache entries"] },
  "branch": "feature/42-subject",
  "worktree": "/absolute/path",
  "headRepository": "owner/repo"
}
```

## Workflow

1. Validate config `type` and `language`: trim a string; a present non-string stops. Apply non-empty `remarks` throughout.
2. An explicit issue number (`#42`, `issue 42`) selects existing provider title/body unchanged; otherwise create an issue. Ask only if genuinely ambiguous. A new issue needs a non-empty title and body; when `language` is non-empty, generate both entirely in it except exact quotes and code identifiers.
3. Fetch or create the issue with `gh`/`glab`; extract its number, URL, title, and body.
4. Expand both branch placeholders. Final branch must include issue number and an ASCII English-meaning slug; never raw CJK or pinyin when an English meaning is clear.
5. GitHub: use `gh issue develop <no> --name <branch> --base <base>`; do not pre-create the branch. GitLab: create from the configured base and use the issue-number branch convention.
6. If `need-worktree`, enter that worktree and fetch/checkout remote branch; otherwise fetch/checkout in repository.
7. Report issue, branch, workspace, and for orchestration the versioned handoff. Stop here.
