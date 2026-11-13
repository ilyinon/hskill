# xxe-xml-external-entity: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual parser and enabled stages | Identify XML entry decoding, entity resolution, XInclude and transforms separately. |
| Attribution and byte effect | Trace the resolver request and returned owned marker, not mere upload or XML reflection. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Internal entity expands | Basic entity processing, not necessarily external loading | Inspect external resolver configuration and a controlled resource trace. |
| No callback arrives | Blocked resolver, egress, wrong parser or attribution gap | Use parser/config evidence and a valid parse baseline before concluding. |

## Interpret failure and finish the task

A malformed XML error did not test external loading. Serving an SVG as bytes does not prove a server parsed it; a resource request does not automatically prove file disclosure.

Track `entry bytes -> actual XML stage -> resource resolver -> returned/used marker -> requested boundary`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Verify the parser configuration

Identify the parser and every later processing stage that can resolve resources. Disable external DTDs and entities where the input contract does not need them and use a resolver that denies external I/O. Check schema imports and transforms separately if present. Use a recording resolver in tests and confirm normal documents still parse while external requests never reach the I/O layer. [OWASP XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
