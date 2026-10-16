# Worked case: algorithm checks pass, recipient binding fails

Synthetic signed-token model: [input](./examples/input.json), [model](./examples/model.py). The fixture key and issuers are artificial. It is not a production JWT implementation.

**Goal.** Determine whether the reports receiver accepts only its intended tokens and repair the demonstrated defect.

**First approach.** Changing the payload without resigning or choosing `alg:none` is rejected. Those are useful controls for signature and algorithm policy. They do not exercise audience validation.

**Revised approach.** Inspect `report`: issuer is checked, but audience is used only when `enforce_audience=True`. Keep the preissued token's signature intact and supply the same trusted issuer's token intended for `invoices`. The broken receiver returns Alice and `report fixture`, violating its declared reports-only recipient policy. No signature forgery is demonstrated or required.

**Repair and independent check.** Enforce membership of `reports` in the normalized scalar/list audience. `test_solving_examples.SolvingExamples.test_valid_signature_is_not_recipient_authorization` confirms the legitimate reports token and a legitimate list audience still succeed; the validly signed foreign audience fails. It separately checks a modified payload and unsigned control.

**Completed result.** A receiver-policy defect and a focused regression check. Actual issuer infrastructure, production permissions, expiration, key rotation, and a complete JWT profile remain outside this minimal model. The returned fixture body supports the modeled capability claim; merely decoding the token would not.
