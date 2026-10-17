# Worked case: an own-property guard stops an inherited option

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied pollution-to-consumer chain.

```text
teaching source: shared prototype has mode=unsafe-marker
consumer: if hasOwn(options, mode) use options.mode; otherwise use safe
options={} -> mode safe
options own mode=safe -> mode safe
no other consumer is reachable in the supplied path
```

**First approach and failure.** Calling the prototype marker a completed gadget ignored the hasOwn gate.

**Revised approach.** Trace the guarded lookup. The primitive exists, but the consumer deliberately avoids inherited mode; classify the chain break rather than searching unrelated gadgets automatically.

**Independent controls.** Use fresh isolated state, an own safe option and inherited-only marker; verify the actual selected mode rather than just property lookup in the console.

**Completed result and limits.** No consumer-policy violation from this chain. The mutation source may still need repair; other call sites and execution effects remain unproved.
