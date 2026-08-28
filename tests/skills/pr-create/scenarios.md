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
