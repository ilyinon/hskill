# ORM search injection: decisions from evidence

Read when a search probe is ambiguous or a parameter appears dead. Use only the
rows matching the current observation.

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| `q[attr_cont]` returns the full list | Predicate ignored, unknown column silently dropped, or allowlist excludes the column | Test the same predicate on a column that demonstrably filters. Parameter accepted on a public column isolates the allowlist. |
| Any value returns the same rows | All-equal responses (filtered-out search), cache, or a broken page | Compare against the unfiltered request and a random pattern on a verified column. All-equal responses are a dead sink, not a match. |
| `%` in the value matches everything | Wildcard pass-through (oracle), or the app strips `%` and searches empty string | A random same-length literal prefix must return fewer rows than `%`. Empty-pattern equivalence means stripped metacharacters. |
| Prefix guess hits, but two different guesses hit at one position | Case-insensitive collation, pagination noise, or an unsound oracle | Measure case behavior with one A/a pair; switch to counts instead of presence, and pin one case class before continuing. |
| Responses stop after N requests | Rate limit, WAF, or lockout | Record the boundary, slow to the last working cadence, and keep the same principal. Identity-switching to evade limits changes the test population. |
| SQL error on a quote in the value | Structure-level SQLi elsewhere in the same query | Stop the LIKE-oracle plan; re-enter via the SQLi skill with the error as the sink observation. Do not mix the two claims. |
| Digest prefix works, digest crack is slow/failed | Strong password; digest recovered but credential not | Report the searchable-digest finding with its own impact (verification oracle, cross-service password reuse checks), and mark credential impact unverified. |

## Evidence chain to close

Map `parameter → predicate/column allowlist → wildcard pass-through → per-position
hits → full recovered value → offline candidate matching the digest → authentication
or platform verdict`. Each arrow is a separate reported observation; the report may
stop early with the later steps marked unverified. Never present a prefix hit or an
uncracked digest as a compromised account.
