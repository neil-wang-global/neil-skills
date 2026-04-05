# neil-skills

A Claude Code skill plugin for workflow automation.

Install via [Superpowers Marketplace](https://github.com/superpowers-ai/marketplace) or add directly in Claude Code settings.

## Skills

### /issue-init

Initialize a development workflow from issue to branch in one command.

**What it does:**

1. Reads `.workflow-config.json` from repo root (creates defaults if missing)
2. Creates a new issue or links an existing one (GitHub `gh` / GitLab `glab`)
3. Generates a branch name from a configurable template
4. Creates the branch on remote, linked to the issue
5. Sets up the working environment (worktree or checkout)

**Configuration** — `.workflow-config.json` at repo root:

```json
{
  "type": "github",
  "base-branch": "main",
  "branch-template": "feature/{issue-no}-{issue-subject}",
  "need-worktree": true
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `type` | `"github"` or `"gitlab"` | `"github"` |
| `base-branch` | Branch to create feature branch from | `"main"` |
| `branch-template` | Branch naming template | `"feature/{issue-no}-{issue-subject}"` |
| `need-worktree` | Use git worktree for isolation | `true` |

**Template variables:**

- `{issue-no}` — issue number (e.g. `42`)
- `{issue-subject}` — slugified issue title in English (e.g. `optimize-search-performance`)

**Prerequisites:**

- [GitHub CLI (`gh`)](https://cli.github.com/) for GitHub repos
- [GitLab CLI (`glab`)](https://gitlab.com/gitlab-org/cli) for GitLab repos

### /issue-close

Clean up the local environment after finishing feature work.

**What it does:**

1. Reads `.workflow-config.json` from repo root
2. Extracts issue number from the current branch name
3. Returns to base branch (exits and removes worktree if applicable)
4. Closes the remote issue (GitHub `gh` / GitLab `glab`)
5. Force-deletes **all** non-base local branches (`git branch -D`)
6. Prunes stale remote-tracking refs and pulls latest

**Uses the same `.workflow-config.json` as `/issue-init`.**

## License

MIT
