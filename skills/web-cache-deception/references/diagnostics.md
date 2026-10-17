# web-cache-deception: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual key and partition | Record path/query normalization, identity/cookie partition, Vary and cacheability. |
| Independent reader | Use a clean separate test principal and an owned private marker with a unique key. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Authenticated response is a HIT | Private partition or shared cached bytes | Inspect key/partition and a clean second identity. |
| Marker appears only in priming response | Reflection or shared contamination | Check clean subsequent request without the priming input. |

## Interpret failure and finish the task

A cache miss or timeout is not disclosure. Cache-control headers alone do not prove the effective key; origin and cache behavior must be distinguished.

Track `prime request -> effective cache key/partition -> stored representation -> clean reader -> protected bytes`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
