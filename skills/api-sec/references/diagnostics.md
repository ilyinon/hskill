# api-sec: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Observed failure stage | Separate discovery, credential verification, object selection, and business state. |
| Requested deliverable | Choose one concrete boundary rather than opening every API playbook. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| A valid JWT accompanies a foreign object read | Token forgery or missing object authorization | Keep the valid token fixed and inspect owner checks. |
| Schema lists privileged fields | Discovery or a reachable write policy | Trace a binding/update path before selecting a mass-assignment test. |

## Interpret failure and finish the task

A token appearing in the request does not make every API issue a JWT flaw. If the handler never executes, restore the correct route/method before diagnosing its policy.

Track `observed API operation -> failed boundary -> matching specialist -> bounded result`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

Use [API authorization](../../api-authorization-and-bola/SKILL.md) for this boundary; [JWT validation](../../jwt-oauth-token-attacks/SKILL.md) applies when token trust itself is in question.
