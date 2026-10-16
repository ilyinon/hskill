# Worked case: sound callback binding, wrong local identity

Synthetic post-verification lookup: [input](./examples/input.json), [model](./examples/model.py). The input explicitly assumes token and transaction validation already succeeded; it does not simulate an identity provider.

**Goal.** Check that two owned identities at different providers remain separate local users.

**First approach.** Inspecting only state/PKCE or replaying a foreign code would test an upstream edge already guaranteed by this fixture. No missing-state finding follows from these artifacts.

**Revised hypothesis.** Provider A and provider B legitimately use the same subject string `42`. The broken lookup ignores issuer and returns the first matching subject. The validated B/42 callback therefore resolves to `alice-local`, although B/42 belongs to `bob-local`. This is a complete identity-mapping failure in the supplied lookup.

**Repair and controls.** Resolve by the exact trusted `(iss, sub)` pair. A/42 must still map to Alice, B/42 to Bob, and an unknown pair to no local account. `test_solving_examples.SolvingExamples.test_provider_subject_pair_preserves_local_identity` verifies all three results. Linking two local accounts requires its separate explicit policy.

**Completed result.** A source-demonstrated provider-subject collision and a checked mapping repair. Code exchange, browser feasibility, session creation, and provider acceptance are premises, not newly observed facts. The useful change of approach was moving to the next unproved binding edge, not repeating an unrelated state-parameter probe.
