# http-host-header-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Authority sources and proxy chain | Trace Host, forwarded authority, trusted peers and the actual absolute-URL builder. |
| Protected downstream consumer | Locate reset/email links, cache keys, routing or fetch behavior beyond reflection. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Host allowlist passes | Other authority inputs may still control URL generation | Inspect the exact builder source after validation. |
| Foreign text is reflected | Display only or a protected emitted link/destination | Compare the actual output artifact and intended origin policy. |

## Interpret failure and finish the task

A proxy/HTTP parse error before the builder is not evidence of poisoning. A generated foreign link supports that boundary only; delivery, navigation and credential use are separate edges.

Track `untrusted authority -> trusted-hop/allowlist decision -> actual URL/router consumer -> protected artifact -> bounded impact`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
