# Worked case: the fetch uses the pinned validated address

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess an offline check/use trace under an explicit peer-pinning contract.

```text
first DNS answer=192.0.2.20, allowed by supplied test policy
later authoritative answer=198.51.100.30, disallowed by that policy
fetch contract: connect to the validated pinned IP
connection trace: peer=192.0.2.20; no connection to later answer
```

**First approach and failure.** Treating the changed authoritative answer as the fetched destination skipped the actual use-time peer.

**Revised approach.** Correlate validation and connection records. Pinning keeps the supplied request on the validated address; the proposed check/use mismatch is absent.

**Independent controls.** A deliberately unpinned teaching trace would need a second lookup and a different peer. Host validation and browser-origin rules remain separate controls.

**Completed result and limits.** No destination-policy violation in this trace. No production resolver, private address, browser or network was contacted.
