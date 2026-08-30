# Task 3 Report: Guarded Internal PR Fix

## Status

Implemented Task 3 only. The working changes are limited to the `pr-fix` skill, shared PR workflow contract, Q-S scenarios, RED baseline evidence, and GREEN verification evidence. This report is ignored by the task worktree's SDD directory.

## RED

Added fresh pressure scenarios Q, R, and S before changing guidance. Current-skill simulations showed that `/pr-fix` required the standalone confirmation table, had no `defer` outcome, and could confuse review-publication preauthorization with fix authorization. The observed rationalizations are recorded in `tests/skills/pr-fix/baseline.md`.

## GREEN

- Internal preauthorization now requires all three trusted predicates: valid parent-created `neil-workflow/v1` envelope, owned caller/mode leaves, and matching boolean `self-reviewed` target config.
- Valid internal calls auto-accept only localized, clear, directly verifiable findings. Architectural/public-interface, migration, security-policy, cross-module, unclear, and high-risk findings use internal-only `defer`.
- A defer posts a concise reason, remains unresolved, returns URL/fingerprint, and performs no worktree, delegation, commit, or push.
- Standalone calls retain `accept`/`reject`/`clarify`, the human confirmation table, and no `defer` bypass.
- Accepted work returns `headBefore`, `headAfter`, `commits`, `pushed`, accepted/deferred fingerprints, and per-thread `threadOutcomes`.

## Verification

Fresh read-only simulations passed scenarios A-S. The final Q-S simulation verified the exact final wording; M/N used the GitHub and GitLab provider references. `wc -w skills/pr-fix/SKILL.md` returned 500. `git diff --check` completed cleanly. No project test command was run, per the Task 3 constraint.

## Commit

Created: `2ce72ab` — `feat(pr-fix): defer complex internal findings`.

## Concerns

The commit succeeded but printed `Can't find lefthook in PATH`. A generated, untracked `.build/` directory (`CACHEDIR.TAG` and `.buildSystem_debug`) appeared during the commit. It was neither staged nor removed.

## Configuration-Authorization Revision

**RED:** direct `self-reviewed:true` simple and complex findings still required the confirmation table because the prior branch depended on envelope provenance; false/absent behavior was not contrasted.

**GREEN:** direct or orchestrated calls with matching `self-reviewed:true` auto-accept only simple findings and classify complex/high-risk findings as `defer`. Direct false/absent calls retain one `accept`/`reject`/`clarify` confirmation table and cannot use `defer`. Envelopes only validate orchestration handoff/sequencing.
