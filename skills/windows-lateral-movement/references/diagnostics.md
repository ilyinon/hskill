# windows-lateral-movement: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Credential type, target and transport | Record the current identity, service authentication and allowed management method. |
| Method-specific authorization | Inspect remote logon rights, endpoint ACLs, UAC filtering and the actual action identity. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| SMB authentication succeeds | Credential validity, not management execution | Inspect authorization for the chosen service/action. |
| A remote method denies | Rights/endpoint policy, transport setup or credential problem | Use the acceptance stage and effective token to locate the first failed edge. |

## Interpret failure and finish the task

A credential accepted by one service is not universal remote execution. Signing/relay conditions and direct valid-credential use are different paths.

Track `usable credential -> service reachability -> authentication -> method/action permission -> attributed destination effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review administrative pathways and logon evidence

Inventory which managed identities may use remote administration and from which hosts. Review permissions and effective firewall rules for the approved channels. Correlate source, destination, logon type, and service or process event before claiming that a remote action ran.
