# binary-protection-bypass: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact artifact and runtime | Pin architecture/build, loaded mappings and enabled loader/hardware protections. |
| Available primitive versus protection | Identify read/write/control-flow capability and which specific gate blocks it. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Tool prints NX/PIE/RELRO label | Static metadata or observed runtime enforcement | Inspect relevant headers/mappings and the actual operation. |
| Executable code segment exists | Normal program text, not executable attacker-writable data | Compare the controlled buffer mapping and transfer outcome. |

## Interpret failure and finish the task

A checksec/parser error leaves the label unknown. A crash at an address is not a mitigation bypass; static metadata alone cannot prove the runtime effect.

Track `exact artifact -> runtime protection -> available primitive -> relevant mapping/target -> bounded observed effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
