# LIKE wildcard oracle: recipes and budget

All requests run under one fixed principal/session. Fix every other search
parameter between probes; one variable at a time.

## Predicate matrix (candidates, verify per target)

| Predicate | Typical SQL | Use |
|---|---|---|
| `attr_cont` | `LIKE '%v%'` | prefix/middle match; works when the stored format has anchors you control with `%` |
| `attr_start` | `LIKE 'v%'` | cleanest prefix oracle: `prefix + guess + '%'` |
| `attr_end` | `LIKE '%v'` | suffix/backward extraction |
| `attr_matches` | case-sensitive `LIKE` (PostgreSQL) | removes case ambiguity on hex values |

Legacy Ransack-era endpoints may accept the flat form (`?user_email_cont=`)
instead of or in addition to `q[...]`. Ransack allows grouping with
`q[_and][]` / `q[_or][]` when a single predicate is filtered out. Older gems and
raw `LIKE` bindings pass `%` and `_` from the value unescaped; current releases
of Ransack, Django `contains`/`startswith`, and similar helpers escape them —
treat version tables as candidates and confirm with one positive control.

## Extraction loop (fixed-format digest, presence oracle)

For a 32-char hex digest and a prefix oracle:

1. Anchor on a value you can verify on a public column first (own username):
   confirm hits/non-hits behave as expected, then confirm `%` and `_` in a value
   change matching (`a%` matches, a random 6-char prefix does not).
2. For each position, try the alphabet (`0-9a-f`; add `A-F` only if case matters):
   `q[user_password_digest_start]=<known_prefix><guess>%`
   Keep the first hit; if two guesses hit, the oracle is unsound — stop and
   re-check case handling and pagination noise.
3. `_` pins unknown lengths/positions (`digest_start=543dc_____…`), which
   distinguishes "starts with" from "contains somewhere".
4. Finish with the full value and a direct check: `…_start=<full_hex>%` must
   return exactly the target row (count-based oracle: same count as any single
   row).
5. Take the recovered digest offline. A hash of the final candidate must equal
   the digest before anything is called a credential.

Cost: an alphabet of 16 averages ~8.5 probes per character (~300 requests for a
32-char hex digest). Prefer a response-count oracle if the endpoint returns
counts, and halve probes with a binary split (`[0-7]`-style classes only work if
`_` or ranges survive; plain LIKE has no character classes, so measure first).
Respect rate limits; back off instead of switching accounts or identities.

## Controls that must hold

- Positive on public column: own known value matches, prefix of it matches.
- Negative: random same-format prefix of the same length returns nothing.
- Unfiltered baseline differs from a false-pattern response (not all-equal).
- Final exact value returns exactly the expected row set.
- Case variant behaves per the measured collation (documented, not assumed).

## Remediation checks

For a code-audit or fix-verification task, confirm independently: sensitive
columns absent from `ransackable_attributes` (every searched model, not just the
one in the report), search gems updated to escaping releases, digests/tokens
never on searchable models, and search endpoints rate-limited per principal.
One fixed model does not certify its siblings.
