# recon-and-methodology: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Explicit permitted assets and actions | Record allowed hosts/ranges and distinguish passive clues from active tests. |
| Observation provenance | Keep capture time, identity, method, response type, and source of fingerprints. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Scanner labels a product/CVE | Heuristic fingerprint or actual affected component | Validate component/configuration and a reachable path. |
| Several names resolve to one address | Shared hosting, aliases, or related services | Deduplicate observations while retaining separate scope and host routing. |

## Interpret failure and finish the task

A timeout is unknown reachability, not absence. An old banner cannot establish an unpatched code path; prioritize evidence that changes the next permitted check.

Track `in-scope seed -> attributed surface -> reachability/configuration -> prioritized boundary -> explicit coverage record`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
