# Worked case: the verified assertion is not the consumed assertion

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Audit a supplied identity-node trace without constructing a signature-wrapping payload.

```text
signature verifier returns verified element ID=trusted-1, subject=test-a
consumer trace chooses first Assertion ID=extra-2, subject=test-b
extra-2 has no verified signature reference
policy: consume only the verified assertion from the trusted IdP
```

**First approach and failure.** Stopping at signature_valid=true overlooked the identity node selected afterward.

**Revised approach.** Compare element identities, then pass the verified node directly to identity extraction or reject mismatches. Do not reselect identity by a fresh broad document search.

**Independent controls.** A single verified trusted-1 assertion must still map test-a; an unused unsigned extra node must never replace it. Reject duplicate/ambiguous identifiers as required by the actual parser profile.

**Completed result and limits.** The supplied source/trace supports a signature-to-consumer binding flaw. No cryptographic forgery, real SAML parser exploit, or IdP takeover has been executed.
