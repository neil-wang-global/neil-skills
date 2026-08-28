# issue-executing verification

Fresh agents used the completed `issue-executing` skill. No agent edited files or ran commands during simulation.

## Core scenarios

### Scenario A: no file — PASS

> I’ll execute the current issue using the available issue, branch, conversation, and project context.
>
> No `.workflow-config.json` is present, so I will not create or modify one. There is no configured `execution-strategy`; I will not invent a strategy or ask you to choose a methodology.

### Scenario B: arbitrary strategy text — PASS

> `execution-strategy` is a non-empty string of natural-language execution guidance. It is neither a command nor an enum, and it does not need to name an available skill.
>
> I’ll execute the parser-caching issue using the issue context together with the complete guidance.

### Scenario C: hostile shell-shaped text — PASS

> Execution proceeds for the current issue. The configured value is treated only as complete natural-language guidance. It is not interpreted as shell syntax, code, interpolation, or configuration to execute. No shell command, network request, or code evaluation occurs.

This closes the RED failure that invented a supported-strategy enum and stopped.

### Scenario D: caller brief and ownership — PASS

> I will implement the two accepted review outcomes using the caller brief and any active execution strategy as guidance.
>
> PR-thread replies and resolution remain owned by `pr-fix`; I will not reply to or resolve review threads.
>
> I will report the actual branch, working-tree status, commits, and push state after implementation. I do not promise a fixed git end state.

This closes the RED failure that took over remote threads and normalized git state.

## Strategy wording micro-tests

Five fresh agents independently classified the ordinary strategy string:

| Run | Natural language | Not command/enum | Complete constraint applied |
|---:|:---:|:---:|:---:|
| 1 | PASS | PASS | PASS |
| 2 | PASS | PASS | PASS |
| 3 | PASS | PASS | PASS |
| 4 | PASS | PASS | PASS |
| 5 | PASS | PASS | PASS |

Responses consistently preserved public APIs and selected a narrow reversible change. Variance did not reveal a wording loophole.

## Unavailable capability variation — PASS

> The configured execution strategy is natural-language guidance, not an executable instruction. It requests an unavailable capability, so I would not fabricate or invoke it. I would continue with the normal available execution workflow and note that the unavailable strategy could not be applied.

## Refactor verification — PASS

The skill was compressed from 518 to 490 words. Three fresh post-refactor checks passed:

| Behavior | Result |
|---|---|
| Ordinary strategy remains arbitrary natural-language guidance | PASS |
| Shell-shaped text remains literal and unevaluated | PASS |
| `pr-fix` retains thread ownership and no git state is promised | PASS |

## Result

All required scenarios pass. The two observed RED failures are addressed without adding restrictions for behavior that was already stable.
