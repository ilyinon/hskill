# Worked case: a display string does not add an envelope recipient

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied mail-generation trace without sending messages.

```text
owned intended recipient=test-a@example.invalid
user subject includes literal text "Bcc: test-b@example.invalid"
serialized Subject remains one field; parsed Bcc absent
envelope recipients=[test-a@example.invalid]
no delivery to test-b in supplied test transport log
```

**First approach and failure.** Calling the Bcc-looking text an extra delivery relied on a UI string instead of the header parser and envelope.

**Revised approach.** Compare the parsed field list and recipient log. The supplied serializer kept the text in Subject and the envelope retained only the intended recipient.

**Independent controls.** A normal subject produces the same one-recipient envelope; independently compare a valid two-recipient teaching message to understand what recipient evidence would look like.

**Completed result and limits.** No recipient/header injection is shown. Real mail-client rendering, authentication alignment and delivery outside this trace remain untested.
