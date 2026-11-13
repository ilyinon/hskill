# waf-bypass-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Attributed enforcement layers | Distinguish WAF block, application validation, backend execution and cache responses. |
| Exact transformation chain | Compare raw/normalized values for the observed content type and sink. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Modified request gets 200 | Block page changed, app received data, or real sink effect | Trace application parser and original vulnerability proof. |
| Filter and app disagree | A normalization mismatch or unrelated branch | Compare same input at both stages with an inert marker. |

## Interpret failure and finish the task

A WAF tool/parser failure is not target behavior. Passing a filter does not establish the original injection; vendor fingerprints and generic encoding tables are hypotheses.

Track `wire representation -> WAF interpretation -> application interpretation -> actual sink -> bounded policy effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Verify the application fix independently of the filter

Treat the WAF as one control in front of application validation. Inspect the application consumer and add a local regression for the corrected behavior. Compare the edge and application logs by request ID, and verify a normal input still works. A WAF event alone does not establish that the application received or processed the request.
