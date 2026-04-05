# neil-skills

Claude Code 工作流自动化技能插件。

通过 [Superpowers Marketplace](https://github.com/superpowers-ai/marketplace) 安装，或直接在 Claude Code 设置中添加。

## 技能

### /issue-init

一条命令完成从 issue 到分支的开发环境初始化。

**功能：**

1. 读取仓库根目录的 `.workflow-config.json`（不存在则创建默认配置）
2. 创建新 issue 或关联已有 issue（GitHub `gh` / GitLab `glab`）
3. 根据可配置的模板生成分支名
4. 在远端创建分支并关联 issue
5. 设置工作环境（worktree 或 checkout）

**配置** — 仓库根目录的 `.workflow-config.json`：

```json
{
  "type": "github",
  "base-branch": "main",
  "branch-template": "feature/{issue-no}-{issue-subject}",
  "need-worktree": true
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `type` | `"github"` 或 `"gitlab"` | `"github"` |
| `base-branch` | 创建功能分支的基准分支 | `"main"` |
| `branch-template` | 分支命名模板 | `"feature/{issue-no}-{issue-subject}"` |
| `need-worktree` | 是否使用 git worktree 隔离工作环境 | `true` |

**模板变量：**

- `{issue-no}` — issue 编号（如 `42`）
- `{issue-subject}` — issue 标题的英文 slug（如 `optimize-search-performance`）

**前置依赖：**

- GitHub 仓库需安装 [GitHub CLI (`gh`)](https://cli.github.com/)
- GitLab 仓库需安装 [GitLab CLI (`glab`)](https://gitlab.com/gitlab-org/cli)

### /issue-close

功能开发完成后，清理本地环境。

**功能：**

1. 读取仓库根目录的 `.workflow-config.json`
2. 从当前分支名提取 issue 编号
3. 切回基准分支（如在 worktree 中则退出并删除 worktree）
4. 关闭远端 issue（GitHub `gh` / GitLab `glab`）
5. 强制删除**所有**非基准分支的本地分支（`git branch -D`）
6. 清理过期的远程跟踪引用并拉取最新代码

**与 `/issue-init` 共用同一份 `.workflow-config.json` 配置。**

## 许可证

MIT
