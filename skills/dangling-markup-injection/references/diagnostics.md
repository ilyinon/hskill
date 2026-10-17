# dangling-markup-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Precise HTML insertion and following bytes | Locate the parser state, quotation boundaries and sensitive marker position. |
| Actual parser and outbound policy | Inspect repaired DOM and the exact attempted/sent resource URL. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| An unclosed tag is reflected | Parser repairs it, ignores it, or consumes following bytes | Inspect the actual resulting attribute/DOM. |
| Resource request occurs | Only attacker text or protected following content | Compare sent URL bytes against the owned marker and policy. |

## Interpret failure and finish the task

A CSP-blocked request does not show transmission. Parsed markup alone is not a data leak, and success in a different browser/parser is a different applicability condition.

Track `HTML insertion -> parser state -> captured following bytes -> permitted outbound request -> protected marker crossing`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
