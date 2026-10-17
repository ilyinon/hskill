# nosql-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Query language and decoded types | Trace JSON/form decoding, type checks, ODM casting and actual query construction. |
| Intended predicate | Separate caller data values from operators/aggregation stages and access policy. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Operator-looking JSON is rejected | Type policy before query or database parser behavior | Locate the rejection stage and try a valid string baseline. |
| An object reaches a query field | Intentional filter API or unintended structure control | Compare the declared contract and final predicate. |

## Interpret failure and finish the task

A malformed JSON error did not test database operators. A Mongo-style operator is not meaningful for every NoSQL backend, and an accepted filter may be a permitted feature.

Track `wire representation -> decoded type -> query predicate -> selected protected data/action`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
