# Worked case: the malformed request is rejected before forwarding

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret a supplied request-framing observation.

```text
candidate request has conflicting framing metadata
frontend trace: reject 400, close connection, backend bytes forwarded=0
fresh valid request on a new isolated connection -> one backend request/one response
no mismatched follow-up association supplied
```

**First approach and failure.** Calling the 400 or closed connection a successful desync skipped the absence of backend input.

**Revised approach.** Locate the frontend rejection. This candidate did not establish a parser disagreement; the valid request confirms the forwarding path works under normal syntax.

**Independent controls.** Preserve exact wire length and connection IDs. A different ambiguous candidate would need its own byte-boundary and benign follow-up evidence.

**Completed result and limits.** No smuggling is supported by this trace. Other translation paths and resource behavior remain untested.
