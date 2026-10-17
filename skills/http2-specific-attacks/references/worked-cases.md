# Worked case: the invalid stream never reaches the backend

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret the supplied frontend/backend trace without sending traffic.

```text
client connection negotiates h2
invalid test stream 3 -> frontend rejects before translation
backend request count for stream 3=0
valid stream 5 -> exactly one backend request; correct response on stream 5
no shared-user connections in this teaching trace
```

**First approach and failure.** Calling the unusual stream error desynchronization skipped the missing backend message.

**Revised approach.** Follow stream 3 to the rejection point and use stream 5 as a working forwarding baseline. No parser-boundary disagreement is shown.

**Independent controls.** Count translated requests and correlate stream/response IDs, not timing alone. Resource exhaustion and other stream features require separate bounded tests.

**Completed result and limits.** No smuggling from this candidate under the supplied trace. H2 support and protocol errors do not establish an exploitable downgrade path.
