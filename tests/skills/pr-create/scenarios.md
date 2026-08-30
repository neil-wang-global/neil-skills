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

## Scenario F: GitLab non-closing default
Prompt: With no config, create a GitLab MR related to issue #42.
Pass: Omit `--related-issue`; use only a non-closing description reference. The closing option is reserved for pr-auto-close-issue true.

## Scenario G: fork checkout to upstream
Prompt: Current branch is pushed to contributor/widgets, upstream/base is acme/widgets, and issue #42 belongs to acme/widgets.
Pass: Query/create against acme/widgets with contributor/widgets as qualified head; verify issue in base and commits in head. Ask if the base remote is ambiguous.

## Scenario H: organization-owned GitHub fork
Prompt: headRepository is tools-org/widgets and GitHub reports the head owner type as Organization.
Pass: Do not use unsupported `gh pr create --head`; create through the host-routed REST pulls endpoint with base/head pair and configured draft state.

## Scenario I: orchestrated normalized target
Prompt: using-neil-workflows supplies a validated `neil-workflow/v1` handoff for base `repository: acme/widgets`, `headRepository: contributor/widgets`, issue #42, branch `feature/42-cache`, and worktree `/repo/.worktrees/feature+42-cache`; remote creation returns GitHub PR #81 at `https://github.com/acme/widgets/pull/81`, base `main`, head `feature/42-cache`, and head SHA `abc123`.
Pass: Validate handoff/worktree identity, create or locate only this PR, and return `stage:"pr-create"`, `status:"completed"`, plus a `handoff` that re-emits the validated prior identity and Git state unchanged, then adds a target with exactly `provider`, `host`, `repository`, `number`, `url`, `baseBranch`, `headRepository`, `headBranch`, and `headSha`. Preserve the fork base/head repositories without aliases, write no config, and invoke no later stage.

## Scenario J: orchestrated existing target routing
Prompt: A trusted internal call resolves existing GitHub PR #81 for the validated base/head pair. The target-base provider read returns literal `self-reviewed:true` and `language:"简体中文"` at blob `cfg-a`.
Pass: Leave PR #81 unchanged, but independently resolve its normalized target-base config and return all nine normalized target leaves plus `automation.enabled`, `provider`, `host`, `repository`, `baseRef`, `configBlobSha`, and target-bound `textLanguage:"简体中文"`. The automation identity matches the target base; parent routing may use it but it grants no later-stage authority.

## Scenario K: base language overrides local, head, and fork
Prompt: The local worktree, PR head, and fork config each say `"language":"简体中文"`; the normalized base target `acme/widgets@main` provider read says `"language":"English"`. Create PR #81.
Pass: Retain the base resolver identity with `textLanguage:"English"`; generate the new PR title and `Summary`, `Testing`, and `Issue` prose in English. Never read those competing language values as authority.
