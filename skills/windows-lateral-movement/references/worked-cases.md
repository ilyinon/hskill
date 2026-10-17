# Worked case: the credential authenticates but the management action denies

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied remote-management trace.

```text
owned test credential accepted by target service as test-a
method policy: management endpoint requires group operators
effective test-a groups exclude operators
management action -> access denied; no owned action marker
allowed read-only status endpoint returns its ordinary status
```

**First approach and failure.** Treating service authentication as successful remote management skipped endpoint authorization.

**Revised approach.** Locate the group-based method denial and retain only the status capability. Do not switch to administrator credentials to prove a low-privilege path.

**Independent controls.** The accepted authentication and allowed status response establish working transport/credentials; the protected action remains denied under the fixed identity.

**Completed result and limits.** No management privilege crossing in this trace. Other protocols, tickets and target-side actions require their own evidence.
