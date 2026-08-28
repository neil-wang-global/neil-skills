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
