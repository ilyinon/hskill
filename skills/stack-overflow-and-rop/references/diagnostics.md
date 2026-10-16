# ROP: locate the first broken primitive or calling-contract assumption

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Architecture, ABI, and exact build/runtime | Inspect the supplied artifact and calling convention before using gadget/layout examples. |
| Actual overwrite and offset | Use an observed fault/marker and matching input transport; a crash alone is not instruction-pointer control. |
| Addresses and usable primitives | Verify exact gadget effects, argument setup, leaks/base assumptions, and mitigations for this build. |
| Stack position at transfer | Account for each consumed word, calls, pivots, and required target-entry alignment. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Crash before the intended return | Wrong offset, canary, truncated transport, or corrupted saved state | Locate the first divergent state in the supplied trace; do not debug later gadgets yet. |
| Correct target and argument, failure at entry | Alignment, hidden target constraints, invalid mapping, or a different ABI | Compute the actual target-entry stack state; compare against the known contract. |
| A tutorial adds a ret gadget | Useful alignment adjustment in that example | Count from this task's stack position. An extra ret can break a chain that is already aligned. |
| Local success, remote failure | Different binary/libc/loader, transport limits, ASLR state, or a false local effect | Compare artifacts and inputs before changing the chain; unknown addresses remain unknown. |
| Helper/tool errors | Parsing/version/syntax problem | Restore a working inspection baseline; an offline tool failure does not disprove the primitive. |

## Close the requested task

Track `input delivery → exact overwrite → first control transfer → argument/register state → target contract → requested local effect`. Fix the earliest unproved edge. A synthetic stack calculation proves only the supplied model; a working process chain requires an independently observed bounded effect in the authorized lab. Do not infer executable code from a crash or require a shell when the task asks for a marker/static correction. The worked fixture explicitly supplies its stack contract.
