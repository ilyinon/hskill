# auth-sec: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Which identity transition? | Locate session issuance, token verification, object permission, browser trust, or federation mapping. |
| Evidence of the claimed outcome | Separate model text/status from authenticated principal and protected state. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| User is authenticated but another tenant record appears | Object policy rather than failed login | Keep identity fixed and route to IDOR/BOLA. |
| Cross-origin request succeeds in a CLI | HTTP access or browser-readable credentials | Route to CORS only after checking browser send/read constraints. |

## Interpret failure and finish the task

An authentication tool failure requires a valid baseline; it is not evidence about object permission. Select the earliest unresolved trust edge rather than following the whole broad-assessment flow.

Track `observed principal/operation -> actual trust decision -> one specialist -> requested proof`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

Recovery details belong in [authentication](../../authbypass-authentication-flaws/SKILL.md); token trust and object permissions have their own branches.
