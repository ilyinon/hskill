# JWT: test each trust decision independently

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Required token kind, issuer, audience, algorithm | Read verifier policy and a known accepted token for this receiver. |
| Actual key selection and representation | Trace the configured key map/JWKS path; a public key or header value alone proves no confusion. |
| Identity and capability after acceptance | Inspect which principal the verifier returns and which protected operation follows. |
| Time/revocation profile | Establish required exp/nbf/leeway and token lifecycle before treating a profile choice as a universal flaw. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Changed claim or alg:none is rejected | Signature/algorithm control works | Test issuer, audience, token kind, or lifecycle only where the observed profile requires them. Do not conclude all trust decisions are correct. |
| Valid signature, wrong intended receiver | Missing audience check or an explicitly shared audience | Compare the receiver's policy and a preissued token for another owned client; preserve valid signatures. |
| Modified token decodes but is rejected | Normal signature protection or parser rejection | Establish an accepted baseline and the exact rejection stage; decoding is not acceptance. |
| Token accepted but endpoint denied | Authentication and authorization are separate | Inspect resulting claims/principal and the endpoint's permission decision before claiming privilege impact. |
| Offline tool fails to parse a token | Wrong format, encoding, JWE, or tool options | Identify the representation first; the server's trust policy has not been tested. |

## Close the requested task

Track `trusted issuer/key → valid signature → correct recipient/type → mapped principal → protected capability`. A success at one edge does not prove the rest. For a fix, retain legitimate scalar/list audiences and reject a validly signed foreign-recipient token. [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.9) describes recipient validation. The worked model deliberately omits other production requirements.
