# csp-bypass-advanced: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Every effective policy | Separate enforced and report-only headers/meta policies for the actual document. |
| Actual resource/script path | Record sink, nonce/hash source, ancestor/worker context and browser outcome. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| One policy allows a source | Another enforced policy may still block it | Evaluate the resource against the full enforced set. |
| Violation report appears | Attempt blocked, report-only observation, or unrelated resource | Correlate directive, disposition and actual execution marker. |

## Interpret failure and finish the task

A failed test harness does not test CSP. A report-only policy does not replace an enforced policy; a permitted source does not establish that an injection can reach it.

Track `injection/sink -> all enforced policies -> permitted load/execution -> observed bounded effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
