# memory-forensics-volatility: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Acquisition and symbol context | Preserve hash, OS/build, symbol compatibility, capture time and acquisition gaps. |
| Object identity and time basis | Use process object/create time, not PID/name alone; align network/module timeline evidence. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Process list is empty | Wrong symbols/plugin, acquisition gap or no recovered objects | Establish a compatible known-good artifact baseline. |
| A connection shares a PID with a suspicious name | PID reuse or same process instance | Compare creation/lifetime and object identifiers before attribution. |

## Interpret failure and finish the task

A plugin/symbol error did not prove absence of a process. RWX, a familiar name or one scanning hit is not malware without corroborated behavior.

Track `image provenance -> compatible parsing -> process instance/time -> correlated artifacts -> bounded incident conclusion`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
