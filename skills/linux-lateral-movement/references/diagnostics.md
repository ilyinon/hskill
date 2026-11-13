# linux-lateral-movement: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Credential/agent usability | Record actual socket access, key restrictions, agent availability and credential type. |
| Destination policy and scope | Identify the permitted host, authentication method and resulting remote capability. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| SSH_AUTH_SOCK path exists | Usable agent, stale path or denied socket | Inspect ownership/access and a supplied signer observation. |
| Authentication succeeds | Full session, forced command, file-only or other restricted capability | Inspect the destination policy and observed operation. |

## Interpret failure and finish the task

A stale socket or refused connection is a setup/prerequisite failure, not evidence of the target account policy. Credential readability alone does not prove remote access.

Track `current principal -> usable credential/agent -> target authentication -> destination restrictions -> actual capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review administrative trust between hosts

Map which principals and managed agents are permitted to access each host. Inspect SSH trust, agent forwarding, service accounts, and lateral authentication logs under the same account and time basis. Remove unused paths and validate approved administration still works. A successful login does not alone establish unauthorized privilege.
