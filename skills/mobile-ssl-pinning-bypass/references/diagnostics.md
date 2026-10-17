# mobile-ssl-pinning-bypass: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Working interception baseline | Record routing/proxy, protocol, TLS stack, trust store, mTLS and app build before hooks. |
| Actual pinning decision | Locate certificate/public-key check and compare its result with attributed app traffic. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Proxy sees no request | Routing/QUIC/DNS/mTLS/trust or pin rejection | Inspect the actual client transport and handshake stage. |
| Local hook returns success | Intended check may not be used by this stack | Correlate the same app connection and real trust outcome. |

## Interpret failure and finish the task

A proxy listener alone does not establish client routing. A local instrumentation success is an observation aid, not a server authentication flaw.

Track `app connection -> transport/proxy path -> TLS trust/pinning gate -> attributed request/response`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
