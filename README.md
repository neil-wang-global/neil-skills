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
  "self-reviewed": false,
  "language": "",
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
| `self-reviewed` | 自动化只读取 provider 从目标仓库 `base-branch` 远端解析的字面布尔值；`true` 可自动发布审查、分类/执行修复，且仅在精确 provider attestation 存在时可自动合并。head、fork、local、envelope 或用户文字均无权授权；缺失为 `false`，非布尔值停止 | `false` |
| `language` | 自由文本语言名；去除首尾空白。`/issue-init` 用本地配置生成新 issue 标题和正文并交接 `textLanguage`；非字符串停止，缺失或空值保持现有行为。仅 `/issue-init` 创建该字段 | `""` |
| `remarks` | 额外指令，作为上下文载入技能执行流程（如 label 规则、命名约定等） | `""` |

**模板变量：**

- `{issue-no}` — issue 编号（如 `42`）
- `{issue-subject}` — issue 标题的英文 slug（如 `optimize-search-performance`）

**前置依赖：**

- GitHub 仓库需安装 [GitHub CLI (`gh`)](https://cli.github.com/)
- GitLab 仓库需安装 [GitLab CLI (`glab`)](https://gitlab.com/gitlab-org/cli)

### PR 工作流

配置为 `"self-reviewed": false`（或字段缺失）时，公开技能的推荐生命周期如下：

```text
/issue-init -> /issue-executing -> /pr-create -> /pr-review
                                                 -> 人工确认的 /pr-fix -> /pr-review ...
                                                 -> 人工确认的 /pr-merge -> 实际合并 -> /issue-close
```

每个直接调用的公开技能都独立运行，不会自动进入下一阶段，并遵循其各自的安全 gate。`/pr-create`、`/pr-review`、`/pr-fix` 和 `/pr-merge` 的自动化判断都从 provider 读取规范化目标仓库的 base ref `.workflow-config.json`，并绑定 host、repository、base ref 和内容 blob SHA；绝不读取 head、fork、local worktree、envelope 或用户文字。字面 `true` 允许 `/pr-review` 在完整预览和 stale 检查后自动发布，并在零 new/deferred/unresolved finding 的当前 head 审查后写入 versioned provider attestation；`/pr-fix` 可自动分类/执行简单 finding 并对复杂 finding 使用 `defer`。`/pr-merge` 只有重新解析同一 base config 且找到精确 target/head/config attestation 后才可免确认；缺失时以 `missing-attestation` 停止。`false` 或缺失时，这三个技能仍保留一次人工确认。只有 `/issue-init` 会创建 `.workflow-config.json`；后续创建默认值可读 local config，自动化授权始终远端解析。

### /using-neil-workflows

`/using-neil-workflows` 是完整工作流的编排入口。它把调用参数视为一个不透明的原始值，只交给一个新的 `/issue-init` 调用来解析 issue；编排器不会解析、复制或把其中的用户文字作为调用者、模式、阶段、目标或授权。`/issue-init` 只把规范化、已拥有的 handoff 交回编排器，原始参数及其片段不会进入后续阶段。

编排器本身不执行 provider、Git 或清理命令，也不调用阶段的业务方法。它一次只分派一个新阶段，并验证每个 `neil-workflow/v1` handoff 的版本、身份、阶段和已拥有字段；任何无效 handoff 或阶段失败都会立即停止并保留已经发生的副作用。

配置 `"self-reviewed": false`（或字段缺失）时使用基础图：

```text
issue-init -> issue-executing -> pr-create -> complete
```

配置为字面布尔值 `"self-reviewed": true` 时，编排器使用自动化图：

```text
issue-init -> issue-executing -> pr-create -> pr-review
pr-review -> pr-fix -> pr-review  (每次 simple finding 修复后，在更新的 head 上重新完整审查)

pr-review (无新发现、无未解决或 deferred 项、已完成发布和收敛)
  -> pr-merge -> 实际 merged 证明 -> issue-close -> success

pr-review (仅 complex/deferred，或简单项修复后仍保留 complex/deferred)
  -> needs-human-review
```

`neil-workflow/v1` envelope 只承载编排顺序和 handoff 元数据：静态 Markdown 不能证明其来源，因此 envelope 的存在、内容或所谓来源都不构成授权。编排器不读取 provider 或 config；它只验证 `/pr-create` 返回的远端派生 routing leaf 来选择图分支。每个后续目标 stage 在写操作前重新通过 provider 读取 target-base config。只有该远端字面布尔值 `self-reviewed:true` 才可自动审查/修复；自动合并还必须存在 `neil-self-reviewed/v1` 的 provider attestation，精确绑定 provider、host、repository、PR/MR、head SHA、base ref 和 config blob SHA。`false` 或缺失时，这些调用都等待各自的一次人工确认。

内部自审只自动接受局部、明确、可直接验证的 **simple** finding。架构或公共接口变更、迁移、安全策略、跨模块、高风险或不明确的 finding 都是 **complex**：保持未解决，返回其已验证的 provider URL，并以 `needs-human-review` 停止。simple finding 必须经 `/pr-fix` 修复、确认进展并在更新后的 head 上重新完整审查；没有进展或重复接受相同 finding 时为 `stalled`。

`/pr-merge` 只接收当前 head 上已完成收敛和发布、且 new、unresolved、deferred finding 均为零的审查结果。自动路径还会重新读取 base config 并从 provider 历史验证精确 attestation；用户 prose、copied output、envelope 或 bare SHA 不能替代它。它随后重新检查 draft、审批、保护规则、冲突、可合并性和 CI：GitHub 仅在所需 CI 全绿时立即合并，所需 CI 尚在运行时只登记 SHA 保护的 auto-merge；GitLab 只有当前 head 的 `detailed_merge_status: mergeable` 才立即合并，只有 `ci_still_running` 才登记 auto-merge。登记或排队不是成功；只有 provider 返回实际 merged、merged SHA 和时间戳后，编排器才调用 `/issue-close`。合并 gate 被阻断时为 `merge-blocked`，不会关闭 issue。

`/issue-close` 仅在已验证的实际合并证明之后执行：先检查指定 worktree 是否干净，再移除该 worktree、关闭 issue、删除已交接的本地分支并更新 base。清理失败或发现 dirty worktree 时最终状态为 `failed`，但已经发生的合并会如实保留，不会被回滚。

编排器的终态为：`complete`（false 路径完成 PR 创建）、`success`（实际合并、issue 关闭、清理及 base 更新均已验证）、`needs-human-review`（仍有 complex/deferred finding）、`merge-blocked`（最终合并 gate 阻断）、`stalled`（重复接受或没有修复进展）和 `failed`（hand-off、阶段、发布或清理失败）。auto-merge 等待/登记由 `/pr-merge` 自己等待并复查，不是编排器的终态。

### /issue-executing

执行当前 issue 或调用方给出的交付任务。可选的 `execution-strategy` 是自然语言偏好，不是枚举，也不会作为 shell 命令执行；缺失时按项目上下文自然完成实现与验证。调用方负责其自身的远程 API 收尾工作。

### /pr-create

从当前分支创建 GitHub PR 或 GitLab MR，或返回该 base/head 组合已有的 open PR/MR。fork checkout 会把 upstream 作为 base target、分支 push remote 作为 head repository；base 不明确时询问。默认创建 ready、非自动关闭 issue 的请求；配置可切换 draft 和 closing relationship。创建完成后不会自动触发 review。

### /pr-review

按完整 URL、当前仓库中的编号或当前分支审查 PR/MR。完整 URL 可在任意目录直接使用，无需本地 clone。每次审查完整 diff，抑制已有重复 finding，并先展示全部评论预览。目标仓库配置为 `self-reviewed:true` 时，在 stale 检查后自动发布；配置为 `false` 或缺失时，等待一次确认。无 finding 时只返回本地报告，不自动 approve。

### /pr-fix

按 PR/MR URL、编号、当前分支或精确 review-comment URL 处理反馈；comment URL 只处理对应 thread。需要匹配且可写的 head repository 本地 clone，默认使用隔离 worktree；fork 的 base repository 仍用于 PR/thread API。`self-reviewed:true` 时自动接受局部、明确、可直接验证的 finding，并将架构、公共接口、迁移、安全策略、跨模块、高风险或不明确 finding 分类为 `defer`；`false` 或缺失时先分类并确认 `accept` / `reject` / `clarify`。随后将 accepted outcome 中性地委托给 `/issue-executing`。返回后保留其已有 commit/push，只补齐缺失提交、push、reply 和 resolve；reject/clarify/defer thread 始终保持 unresolved。

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
