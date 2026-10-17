# Worked case: the target rejects the relayed authentication binding

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied relay trace without contacting any service.

```text
owned origin produces authentication exchange
relay reaches test target; binding requirement is enabled
target trace: binding mismatch, no authenticated session
normal direct bound authentication as the owned principal succeeds
no protected target operation from relay supplied
```

**First approach and failure.** Calling the captured exchange a relay success skipped the target acceptance gate.

**Revised approach.** Correlate the target rejection and absence of a session. The supplied coercion/capture milestone does not reach target capability.

**Independent controls.** The direct bound baseline validates normal target authentication under a different valid path; it does not prove the relay worked.

**Completed result and limits.** No accepted relay in this trace. Other protocols, configurations and credential-based remote actions remain separate questions.
