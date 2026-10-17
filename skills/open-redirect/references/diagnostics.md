# open-redirect: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Redirect sink and normalization | Identify which component resolves relative URLs and how destination policy is enforced. |
| Effective navigation target | Capture resolved scheme/host/port, not just a reflected string. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Location contains an external URL as a query value | Same-origin navigation or actual external destination | Parse the effective outer URL. |
| External redirect works | Navigation flaw or an independently exploitable token/fetch chain | Validate each later trust edge before increasing impact. |

## Interpret failure and finish the task

A 3xx without a resolved destination is incomplete evidence. A parser rejection is a valid control for that representation, not proof of all URL-parser behavior.

Track `caller destination -> normalization -> policy -> actual navigation -> independently demonstrated chain effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
