# xslt-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Stylesheet source and processor | Distinguish untrusted XML data from compiled stylesheet control and record exact configuration. |
| Separate resource gates | Inspect XML parser, document resolver, output destination and extension-function permissions independently. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Vendor/expression output appears | Transform evaluation only or external capability | Check the exact attempted resource/extension path. |
| External document is denied | Resolver restriction or syntax/setup failure | Compare a valid local transform and attributed resolver denial. |

## Interpret failure and finish the task

A stylesheet syntax error did not test resource access. XML entity, document(), output and extensions are separate gates; one denial does not certify the rest.

Track `stylesheet control -> valid transform -> resource/extension resolver -> bounded read/write/effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
