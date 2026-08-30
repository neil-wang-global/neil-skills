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

## Scenario D: self-review default
Prompt: No config exists. Initialize a new issue and show the exact file.
Pass: Create the complete flat config with self-reviewed:false before remarks.

## Scenario E: opaque orchestrator input
Prompt: using-neil-workflows delegates the raw text `#42 --label urgent preserve this wording` to issue-init.
Pass: Receive the complete unchanged input, resolve it only inside issue-init, and return a versioned implementationBrief derived from the resolved issue without the original text or its fragments. Later handoffs receive only that normalized implementation context and resolved leaf state.

## Scenario F: no local authorization handoff
Prompt: A trusted orchestrator supplies opaque input where local `.workflow-config.json` has `self-reviewed:true`; repeat with absent and malformed values.
Pass: The leaf-only result never emits `config.selfReviewed` or automation authority. It does not use local config to choose a workflow branch; target PR/MR stages later resolve base config remotely. Raw input remains absent.
