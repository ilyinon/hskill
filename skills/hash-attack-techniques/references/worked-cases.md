# Worked case: the verifier is HMAC, not a keyed-prefix hash

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess applicability of a proposed length-extension method.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Identifying only the digest algorithm skipped the HMAC construction on which the proposed extension method does not operate.

**Revised approach.** Trace the verifier and classify the keyed-prefix length-extension recipe as inapplicable here. Preserve other hypotheses only if independent evidence supports them.

**Independent controls.** Compute the baseline and changed-message HMAC locally with a synthetic key if verification is needed; do not claim to have recovered a real secret.

**Completed result and limits.** No length-extension flaw in the supplied construction. Key strength, side channels, encoding ambiguity and other endpoints remain unassessed.

The independent baseline is [RFC4231 test case2](https://www.rfc-editor.org/rfc/rfc4231.html#section-4.3); it tests HMAC arithmetic, not a deployed verifier or side channel.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_hmac_rfc_vector_and_changed_message`. This is not a product/runtime exploit test.
