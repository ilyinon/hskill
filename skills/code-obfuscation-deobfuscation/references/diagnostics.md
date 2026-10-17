# code-obfuscation-deobfuscation: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Observable semantics | Define input/output and reachable side effects that the simplified version must preserve. |
| Bit width and state | Record signedness, overflow, initialization and self-modifying/VM stages before folding predicates. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Predicate looks algebraically constant | Mathematical integers or machine-width behavior | Evaluate it using the actual bit-vector contract. |
| Simplified output differs | Wrong predicate, missing state or bad emulator | Find the first divergence against the original trace. |

## Interpret failure and finish the task

A disassembler/emulator failure is not evidence that a branch is unreachable. Preserve the original and validate simplifications on independent inputs and side effects.

Track `original inputs/state -> exact machine semantics -> simplified representation -> matching outputs/effects`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
