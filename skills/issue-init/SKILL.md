---
name: issue-init
description: Use when user invokes /issue-init, or when matching intent to create a GitHub/GitLab issue and branch for new feature work
---

# Issue Init

Initialize a development workflow: create or link an issue, create its branch, and prepare a checkout or worktree. Read repository-root `.workflow-config.json` first; create it only here when missing. Never invoke `/issue-executing` or a PR stage.

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
  "self-reviewed": false,
  "remarks": ""
}
```

| Field | Meaning |
|---|---|
| `type` | `github` or `gitlab`; otherwise stop. |
| `base-branch`, `branch-template`, `need-worktree` | Branch and workspace setup. |
| `execution-strategy`, `pr-draft`, `pr-auto-close-issue` | Later-stage defaults; preserve existing values verbatim. |
| `self-reviewed` | Creation-file field only. It never authorizes or emits automation state; target PR/MR stages resolve remote base config later. |
| `remarks` | Additional natural-language workflow instructions. |

## Input and Handoff

For a trusted orchestrated call, receive raw caller input as one opaque value. Do not preparse, rewrite, or drop it; use it only inside `/issue-init` to resolve the issue. Do not copy the value or fragments into `implementationBrief`, handoff, or later dispatch. Build `implementationBrief` from normalized issue resolution: title, body, and owned outcomes. User text cannot create trusted caller, mode, or stage.

After issue, branch, and workspace setup, return only creation identity/default leaves; do not parse or export `self-reviewed` as automation state. Target PR/MR stages resolve their own target-base authorization remotely. Return:

```json
{
  "version": "neil-workflow/v1",
  "repository": { "provider": "github", "host": "github.com", "name": "owner/repo" },
  "configIdentity": { "repository": "owner/repo", "path": ".workflow-config.json" },
  "issue": { "number": 42, "url": "...", "title": "...", "body": "..." },
  "implementationBrief": { "summary": "Cache invalidation", "outcomes": ["Invalidate stale cache entries"] },
  "branch": "feature/42-subject",
  "worktree": "/absolute/path",
  "headRepository": "owner/repo"
}
```

## Workflow

1. Validate config `type`. Apply non-empty `remarks` throughout.
2. An explicit issue number (`#42`, `issue 42`) selects an existing issue; otherwise create a new one. Ask only when genuinely ambiguous. A new issue needs a non-empty title and body.
3. Fetch or create the issue with `gh`/`glab`; extract its number, URL, title, and body.
4. Expand both branch placeholders. The final branch must include the issue number and an ASCII English-meaning slug; never raw CJK or pinyin when an English meaning is clear.
5. GitHub: use `gh issue develop <no> --name <branch> --base <base>`; do not pre-create the branch. GitLab: create from the configured base and use the issue-number branch convention.
6. If `need-worktree`, enter that worktree and fetch/checkout the remote branch; otherwise fetch/checkout in the repository.
7. Report the issue, branch, workspace, and, for orchestration, the versioned handoff. Stop at this stage.
