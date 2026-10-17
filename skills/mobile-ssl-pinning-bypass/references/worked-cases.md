# Worked case: the app traffic never reaches the configured proxy

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Diagnose the earliest failed edge before changing certificate checks.

```text
proxy listens for TCP on test endpoint
supplied app trace uses direct UDP transport; proxy capture empty
no certificate/pin check failure recorded
permitted ordinary TCP test client through proxy -> owned marker captured
```

**First approach and failure.** Treating an empty proxy capture as a pinning failure skipped transport selection.

**Revised approach.** Identify the app's actual transport and supported interception path. Establish an app-specific routed baseline before attributing any later TLS failure to pinning.

**Independent controls.** The TCP control validates only proxy readiness, not app routing. Preserve app process/connection attribution and separate mTLS/trust/pinning stages.

**Completed result and limits.** The missing transport edge is diagnosed; pinning was not tested by this attempt. No hook, certificate policy change or server flaw is claimed.
