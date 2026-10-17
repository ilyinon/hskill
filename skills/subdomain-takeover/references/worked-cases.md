# Worked case: a stale record fails the domain-binding prerequisite

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Classify supplied stale-DNS evidence without attempting a resource claim.

```text
name=old.example.invalid -> provider resource old-17
resource status=missing
supplied provider contract: custom-domain binding requires a fresh TXT ownership token
no control of example.invalid DNS and no valid TXT proof supplied
```

**First approach and failure.** Treating the missing resource as a completed takeover ignored the required domain-binding proof.

**Revised approach.** Record stale DNS but keep takeover unsupported under the supplied contract. The next useful evidence is whether the exact provider workflow really enforces ownership, not an unapproved registration attempt.

**Independent controls.** Distinguish resource creation from binding this custom domain. A different provider without this control would require a new applicability review.

**Completed result and limits.** Stale configuration is supported; claimable domain control is not. No real provider behavior or registration was tested.
