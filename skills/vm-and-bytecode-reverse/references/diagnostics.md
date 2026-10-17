# vm-and-bytecode-reverse: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Instruction grammar and VM state | Map opcode/operand lengths, widths, signedness, byte order and PC updates. |
| Observed semantics | Compare each small step with original supplied traces before solving the whole program. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Native disassembler gives nonsense | Custom bytecode or wrong native architecture | Identify the fetch/decode/dispatch loop and bytecode region. |
| Emulator output differs | Operand decoding, PC width, initialization or side-effect error | Find the first divergent instruction, not just final output. |

## Interpret failure and finish the task

A solver candidate for an unverified emulator is not a recovered native input. Preserve widths and initialization; a tool decoding error is not evidence of obfuscation strength.

Track `bytecode bytes -> decoded instruction -> state transition -> matched trace -> recovered program/input result`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
