# Workflow Language Propagation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repository-configured free-text language that governs every newly generated human-readable workflow artifact.

**Architecture:** `/issue-init` creates and locally consumes `language`, returning a normalized `textLanguage` handoff. Target stages independently re-resolve language from the provider's normalized target base ref before text-bearing operations, so head, fork, worktree, envelope, and user prose cannot override it. The coordinator only validates and forwards the leaf.

**Tech Stack:** Markdown Agent Skills, GitHub CLI/API references, GitLab CLI/API references, JSON configuration, Git.

## Global Constraints

- Add exact flat field `"language": ""` after `self-reviewed` and before `remarks`.
- The field is a trimmed free-text language name; non-string stops the relevant stage and empty/absent preserves current behavior.
- Only `/issue-init` creates `.workflow-config.json`.
- Non-empty language governs every new human-readable issue, commit, PR/MR, review, reply, defer, merge, and close artifact produced by workflow stages.
- Preserve quotations, code identifiers, branch ASCII English slugs, SHA/URL/API/JSON values, and exact `neil-self-reviewed/v1` protocol payloads.
- Issue init uses local config; target stages resolve remote target-base config and bind provider/host/repository/baseRef/blob SHA before text writes.
- Do not rewrite existing remote text; a changed remote language affects only the next new text.
- `/using-neil-workflows` never translates or performs provider/Git business operations.
- Keep every `SKILL.md` at or below 500 words, leave plugin versions unchanged, and do not run an executable test suite at the user's request.

---

### Task 1: Configuration, Handoff, and Issue/Commit Language

**Files:**
- Modify: `skills/issue-init/SKILL.md`
- Modify: `skills/issue-executing/SKILL.md`
- Modify: `references/pr-workflow-contract.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: repository-local `.workflow-config.json` during `/issue-init`.
- Produces: `textLanguage: string` in the issue-init handoff, trimmed from local config or `""` when absent.
- Target resolver adds: `textLanguage`, `baseRef`, and `configBlobSha` to its owned remote configuration result.

- [ ] **Step 1: Define the exact configuration and validation rules**

Add this ordered default fragment to both JSON examples:

```json
"self-reviewed": false,
"language": "",
"remarks": ""
```

Document trim behavior, non-string stop, and empty/absent compatibility. State that only issue-init creates the field.

- [ ] **Step 2: Apply local language to issue-init and handoff**

Require issue-init to generate a new issue title/body entirely in non-empty `language`, excluding exact quotes and code identifiers. Return:

```json
"textLanguage": "简体中文"
```

Keep original opaque input confined to issue-init. Existing issue title/body remain provider data and are not rewritten.

- [ ] **Step 3: Apply handed-off language to implementation commits**

Require issue-executing to use validated non-empty `textLanguage` for any commit subject/body it produces. Preserve actual Git reporting and do not prescribe implementation methods or test commands.

- [ ] **Step 4: Extend the shared remote-base resolver contract**

Define that target stages parse `language` from target-base remote configuration, retain provider/host/repository/baseRef/configBlobSha, reject a non-string, and choose remote non-empty language for their next new text. Explicitly reject head/fork/local/envelope/prose overrides.

- [ ] **Step 5: Verify and commit**

Run:

```bash
node -e "const fs=require('fs'),keys=['type','base-branch','branch-template','need-worktree','execution-strategy','pr-draft','pr-auto-close-issue','self-reviewed','language','remarks'];for(const f of ['README.md','skills/issue-init/SKILL.md']){const m=fs.readFileSync(f,'utf8').match(/```json\\n([\\s\\S]*?)\\n```/);const v=JSON.parse(m[1]);if(JSON.stringify(Object.keys(v))!==JSON.stringify(keys)||v.language!=='')throw Error('invalid language default: '+f)}"
git diff --check
wc -w skills/issue-init/SKILL.md skills/issue-executing/SKILL.md
```

Expected: valid JSON, exact equality, no whitespace errors, each skill at most 500 words. Commit with `feat(workflow): add configured content language`.

### Task 2: Target-Stage Text Generation

**Files:**
- Modify: `skills/pr-create/SKILL.md`
- Modify: `skills/pr-review/SKILL.md`
- Modify: `skills/pr-fix/SKILL.md`
- Modify: `skills/pr-merge/SKILL.md`
- Modify: `skills/issue-close/SKILL.md`
- Modify: `references/github-pr-api.md`
- Modify: `references/gitlab-mr-api.md`

**Interfaces:**
- Consumes: remote target-base resolver result including `textLanguage` and its bound config identity.
- Produces: language-conforming newly generated provider/Git text while preserving exact machine protocol fields.

- [ ] **Step 1: Constrain PR/MR titles and bodies**

Require pr-create to resolve language before creating a target and generate its title, `Summary`, `Testing`, and `Issue` body sections in it when non-empty. Existing-target idempotent results stay unchanged.

- [ ] **Step 2: Constrain review publication**

Require pr-review to resolve language before its preview and re-resolve before provider writes. Generate finding titles/explanations, inline comments, non-inline comments, and report prose in it. Keep location data, hidden fingerprints, URL bindings, and exact attestation marker/payload unchanged.

- [ ] **Step 3: Constrain fixes and workflow commits**

Require pr-fix to use the current remote language for classification reasons, accept/reject/clarify/defer replies, and completion commit subject/body. Re-resolve it at the existing authorization/provider-write gates so changed language affects only later content.

- [ ] **Step 4: Cover merge and close text-bearing writes**

Require pr-merge and issue-close to use remote language whenever their provider operation supports a generated human-readable body. Do not add messages where an existing operation has no text body; do not alter merge/merged-proof/cleanup safeguards.

- [ ] **Step 5: Document provider neutral behavior and commit**

Update provider references to distinguish generated prose from fixed provider/API protocol values. Run:

```bash
git diff --check
wc -w skills/pr-create/SKILL.md skills/pr-review/SKILL.md skills/pr-fix/SKILL.md skills/pr-merge/SKILL.md skills/issue-close/SKILL.md
```

Expected: no whitespace errors and every skill at most 500 words. Commit with `feat(workflow): localize generated workflow content`.

### Task 3: Coordinator, Documentation, and Cross-Skill Verification

**Files:**
- Modify: `skills/using-neil-workflows/SKILL.md`
- Modify: `README.md`
- Modify: `tests/skills/issue-init/scenarios.md`
- Modify: `tests/skills/issue-init/verification.md`
- Modify: `tests/skills/pr-create/scenarios.md`
- Modify: `tests/skills/pr-review/scenarios.md`
- Modify: `tests/skills/pr-fix/scenarios.md`
- Modify: `tests/skills/using-neil-workflows/scenarios.md`
- Modify: `tests/skills/using-neil-workflows/verification.md`

**Interfaces:**
- Consumes: `textLanguage` and target-bound remote resolver state.
- Produces: validated language-preserving stage handoffs; no coordinator-generated content.

- [ ] **Step 1: Preserve coordinator ownership boundary**

Require the parent to validate/forward `textLanguage`, retain remote config identity with target handoffs, and never translate, create provider text, or create commits. A remote language change is forwarded to the next stage only.

- [ ] **Step 2: Add pressure scenarios and verification records**

Record exact cases for: default object order; local `简体中文` issue text; base `English` overriding local/head/fork `简体中文`; empty/absent compatibility; language-conforming PR/review/reply/commit content; preservation of quotations/identifiers/machine marker; and base language change applying only to later generated content.

- [ ] **Step 3: Update Chinese README and run structural verification**

Document the free-text field, local-vs-remote resolution, covered content, exceptions, and compatibility behavior. Run:

```bash
node -e "const fs=require('fs'),keys=['type','base-branch','branch-template','need-worktree','execution-strategy','pr-draft','pr-auto-close-issue','self-reviewed','language','remarks'];for(const f of ['README.md','skills/issue-init/SKILL.md']){const m=fs.readFileSync(f,'utf8').match(/```json\\n([\\s\\S]*?)\\n```/);const v=JSON.parse(m[1]);if(JSON.stringify(Object.keys(v))!==JSON.stringify(keys)||v.language!=='')throw Error('invalid language default: '+f)}"
git diff --check
wc -w skills/{issue-init,issue-executing,pr-create,pr-review,pr-fix,pr-merge,issue-close,using-neil-workflows}/SKILL.md
git status --short
```

Expected: valid matching defaults, no whitespace errors, all skills at most 500 words, only intended files changed. Do not run an executable test suite. Commit with `docs(workflow): document configured content language`.
