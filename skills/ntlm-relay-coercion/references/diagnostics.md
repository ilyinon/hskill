# ntlm-relay-coercion: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Originating identity and target protocol | Record coercion path, authenticated principal, destination and permitted capability. |
| Target binding requirements | Inspect signing, channel binding/EPA and exact acceptance stage for this service. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Authentication exchange is captured | Coercion/capture or a target-accepted relay | Check the target session and protected operation. |
| Target requires binding/signing | This relay path may fail while direct valid authentication still works | Inspect the exact protocol rejection, not a generic reachability result. |

## Interpret failure and finish the task

A captured challenge/response is not a successful relay or recovered password. A transport/tool failure before authentication leaves the target binding test incomplete.

Track `originating authentication -> relay transport -> target binding checks -> accepted identity -> authorized capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review the receiving service's binding policy

Inventory where NTLM is still accepted and whether the receiving service requires signing, channel binding, or extended protection as applicable. Record effective settings and approved exceptions by service. Use authentication telemetry and a supported administrative validation to confirm expected clients continue to work after hardening.
