# Worked case: liveness is public but protected reads require authentication

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied service transcript without issuing commands.

```text
policy: anonymous PING allowed; protected key reads require authentication
anonymous PING -> PONG
anonymous protected-read owned-test-key -> authentication required
authenticated owned test principal read -> OWNED marker
no write/admin operation supplied
```

**First approach and failure.** Calling PONG unrestricted service access ignored command-specific policy.

**Revised approach.** Compare liveness and protected-read stages under the same anonymous principal. The protected capability is denied in this trace.

**Independent controls.** The authenticated owner response establishes the test data exists; it does not turn anonymous liveness into a protected read.

**Completed result and limits.** No anonymous protected-read violation here. Other command ACLs and services remain uncovered, and execution is not inferred.
