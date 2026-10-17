# Worked case: the peer address breaks a forged identity claim

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess an identity-header hypothesis under the supplied trusted-proxy contract.

```text
trusted proxy peer = 192.0.2.10; only this peer may supply X-Test-User
request peer = 192.0.2.40; bearer principal = test-reader
with X-Test-User: test-admin -> principal test-reader, admin-read 403
without header -> principal test-reader, admin-read 403
configured trusted proxy with test-admin -> principal test-admin, admin-read 200
```

**First approach and failure.** Treating the header text as the effective identity skipped the peer trust check.

**Revised approach.** Trace extraction: the direct peer is outside the trusted proxy set, so bearer identity remains authoritative. The trusted-hop control establishes a distinct configuration branch.

**Independent controls.** Compare returned principal and protected action together. Do not swap to valid administrator credentials when testing the direct low-privilege request.

**Completed result and limits.** No direct-header authentication bypass in this model. Whether the proxy can be impersonated or its topology is deployed correctly requires separate evidence.
