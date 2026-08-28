# neil-skills

Claude Code 工作流自动化技能插件。

## 安装

```bash
claude plugin marketplace add neil-wang-global/neil-skills
claude plugin install neil-skills@neil-skills
```

## 更新

```bash
claude plugin marketplace update neil-skills
claude plugin update neil-skills@neil-skills
```

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
  "need-worktree": true,
  "execution-strategy": "",
  "pr-draft": false,
  "pr-auto-close-issue": false,
  "remarks": ""
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `type` | `"github"` 或 `"gitlab"` | `"github"` |
| `base-branch` | 创建功能分支的基准分支 | `"main"` |
| `branch-template` | 分支命名模板 | `"feature/{issue-no}-{issue-subject}"` |
| `need-worktree` | 是否使用 git worktree 隔离工作环境 | `true` |
| `execution-strategy` | 可选自然语言执行偏好；缺失或为空时自然执行，不作为 shell 命令 | `""` |
| `pr-draft` | 新 PR/MR 是否为 draft | `false` |
| `pr-auto-close-issue` | 合并后是否通过 closing keyword 自动关闭 issue | `false` |
| `remarks` | 额外指令，作为上下文载入技能执行流程（如 label 规则、命名约定等） | `""` |

**模板变量：**

- `{issue-no}` — issue 编号（如 `42`）
- `{issue-subject}` — issue 标题的英文 slug（如 `optimize-search-performance`）

**前置依赖：**

- GitHub 仓库需安装 [GitHub CLI (`gh`)](https://cli.github.com/)
- GitLab 仓库需安装 [GitLab CLI (`glab`)](https://gitlab.com/gitlab-org/cli)

### PR 工作流

推荐生命周期：

```text
/issue-init -> /issue-executing -> /pr-create -> /pr-review
                                                -> /pr-fix -> /pr-review ...
                                                -> 人工批准/合并 -> /issue-close
```

每个公开技能都独立调用，不会自动进入下一阶段。只有 `/issue-init` 会创建 `.workflow-config.json`；其他技能仅在文件存在且属于目标仓库时读取，缺失字段使用默认值。

### /issue-executing

执行当前 issue 或调用方给出的交付任务。可选的 `execution-strategy` 是自然语言偏好，不是枚举，也不会作为 shell 命令执行；缺失时按项目上下文自然完成实现与验证。调用方负责其自身的远程 API 收尾工作。

### /pr-create

从当前分支创建 GitHub PR 或 GitLab MR，或返回该分支已有的 open PR/MR。默认创建 ready、非自动关闭 issue 的请求；配置可切换 draft 和 closing relationship。创建完成后不会自动触发 review。

### /pr-review

按完整 URL、当前仓库中的编号或当前分支审查 PR/MR。完整 URL 可在任意目录直接使用，无需本地 clone。每次审查完整 diff，抑制已有重复 finding，先展示全部评论预览并等待一次确认，再发布行级评论。无 finding 时只返回本地报告，不自动 approve。

### /pr-fix

按 PR/MR URL、编号、当前分支或精确 review-comment URL 处理反馈；comment URL 只处理对应 thread。需要匹配且可写的本地 clone，默认使用隔离 worktree。先分类并确认 `accept` / `reject` / `clarify`，再将 accepted outcome 中性地委托给 `/issue-executing`。返回后保留其已有 commit/push，只补齐缺失提交、push、reply 和 resolve；reject/clarify thread 始终保持 unresolved。

### /issue-close

功能开发完成并经人工批准/合并后，清理本地环境。

**功能：**

1. 读取仓库根目录的 `.workflow-config.json`
2. 从当前分支名提取 issue 编号
3. 切回基准分支（如在 worktree 中则退出并删除 worktree）
4. 关闭远端 issue（GitHub `gh` / GitLab `glab`）
5. 删除当前 issue 关联的本地分支（`git branch -D`）
6. 清理过期的远程跟踪引用并拉取最新代码

**与 `/issue-init` 共用同一份 `.workflow-config.json` 配置。**

### /init-commit-hooks

为任意项目初始化标准提交钩子（lefthook + commitlint）。支持 Node.js、Go、Python、Rust 等任何 git 项目。

**功能：**

1. 确保 `package.json` 存在（非 Node 项目会自动创建）
2. 安装 `@commitlint/cli`、`@commitlint/config-conventional`、`lefthook` 为 devDependencies
3. 创建 `commitlint.config.cjs` — conventional commits 规范，要求 scope 和 body
4. 创建 `lefthook.yml` — commit-msg 阶段运行 commitlint + 禁止 co-author 信息
5. 在 `package.json` 中添加 `prepare` 脚本自动安装 hooks
6. 激活 hooks 并验证

**允许的 commit type：** `feat`、`fix`、`docs`、`style`、`refactor`、`test`、`chore`、`ci`、`perf`、`build`

**commit message 格式：**

```
<type>(<scope>): <subject>

<body>
```

示例：

```
feat(auth): add login page

Implement login form with email and password fields.
```

## 许可证

MIT
