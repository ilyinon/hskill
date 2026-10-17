# Worked case: literal escape text is not a new header

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Determine whether the supplied response creates an extra HTTP field.

```text
input value text=alpha%0D%0AX-Case: owned
complete contract: no percent decoding; serializer emits this literal value
raw wire: X-Label: alpha%0D%0AX-Case: owned\r\n

parser fields: X-Label only; no X-Case field
```

**First approach and failure.** Finding the marker in a screenshot or header value confused text with a field boundary.

**Revised approach.** Inspect the wire and parsed field list. The percent characters remain data in one header value under this contract.

**Independent controls.** Compare an ordinary label and a parser fixture with two genuinely separated benign fields; only the latter has a distinct X-Case key. Do not send that fixture to a target.

**Completed result and limits.** No header-splitting proof from this path. A real decoder/narrowing mismatch would need its own trace; cache sharing, session fixation and body execution remain separate claims.
