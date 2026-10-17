# saml-sso-assertion-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact signed identity object | Track which element ID is signature-verified and which node supplies consumed identity. |
| Federation profile | Establish issuer, audience, recipient, time and solicited/unsolicited request rules. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| An unsigned assertion is present | Unused extra node or identity consumed without verification | Compare the verified element reference with the consumed element ID. |
| Missing InResponseTo | Permitted unsolicited flow or broken request binding | Read the configured profile and replay/freshness checks before reporting. |

## Interpret failure and finish the task

XML parse rejection did not test signature/identity binding. A valid signature on one node says nothing about another node the application actually consumes.

Track `validated document/signature -> exact assertion -> issuer/profile checks -> local account -> protected capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
