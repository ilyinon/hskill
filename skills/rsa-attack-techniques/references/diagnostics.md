# rsa-attack-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact RSA construction | Record n,e,c, padding/encoding, related moduli and oracle/fault prerequisites. |
| Candidate proof | Verify factors and original modular relation, then message encoding and independent constraints. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Exponent is small | Raw message power may still wrap modulo n | Check the no-wrap condition before taking an integer root. |
| Two moduli are present | Shared factor, same modulus or unrelated keys | Use exact gcd/equality evidence rather than an attack label. |

## Interpret failure and finish the task

A nonperfect integer root disproves only the no-wrap root route for that input. Raw textbook arithmetic does not automatically apply to OAEP/PSS profiles.

Track `RSA parameters/construction -> applicable relation -> factors/plaintext -> original modular and format checks`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
