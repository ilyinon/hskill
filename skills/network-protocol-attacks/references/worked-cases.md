# Worked case: the receiver rejects the competing mapping

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret a supplied bounded naming/routing trace.

```text
owned peer initially maps test-gateway -> legitimate endpoint
competing response is captured on the segment
supplied receiver trace: reject untrusted mapping source; cache unchanged
subsequent owned marker traffic still goes to legitimate endpoint
```

**First approach and failure.** Calling a transmitted response interception ignored the receiver's rejection and unchanged routing.

**Revised approach.** Compare receiver state and the actual subsequent destination. Position and message delivery are established; redirection is not.

**Independent controls.** A trusted fixture mapping update changes the cache under the supplied contract; the untrusted variant does not. Preserve direction and endpoint attribution.

**Completed result and limits.** No peer redirection or interception in this trace. Other naming protocols, switches and receiver policies need separate evidence.
