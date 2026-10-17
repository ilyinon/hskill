# Worked case: the issued certificate maps to the requester only

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied certificate identity trace.

```text
owned requester=test-a; certificate issuance succeeds
certificate display name includes test-b
supplied mapping contract binds authenticated requester ID, not display name
mapping log=test-a; service identity=test-a
protected test-b operation remains denied
```

**First approach and failure.** Calling the display name a successful impersonation ignored the actual trusted identity binding.

**Revised approach.** Trace the certificate through mapping and the service action. The requester retains its own identity under the supplied contract.

**Independent controls.** A normal test-a certificate and the display-name variant must map consistently; an issued certificate not accepted by a service is a separate chain failure.

**Completed result and limits.** No test-b impersonation in this teaching trace. Real CA policy, patch state, issuance authorization and other mapping paths remain unvalidated.
