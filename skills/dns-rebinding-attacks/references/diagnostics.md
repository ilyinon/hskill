# dns-rebinding-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Which client and resolution path? | Separate browser origin behavior from a server check/use destination decision. |
| Connection address and host policy | Correlate validation answer, actual selected peer, cache/pinning and application Host checks. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Authoritative answer changes | Resolver/client may retain the old address or re-resolve | Inspect the actual connection peer at use time. |
| TTL is zero | A hint to caches, not an observed destination change | Correlate the second lookup and request, rather than assuming it occurred. |

## Interpret failure and finish the task

A DNS timeout is setup/evidence failure, not rebinding success. A changed DNS record alone does not establish that a protected address was contacted.

Track `controlled name -> validation resolution -> use-time peer -> destination/origin policy -> protected response/action`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
