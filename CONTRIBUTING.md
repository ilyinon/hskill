# Maintaining the skill collection

Keep `skills/hack/SKILL.md` as the small entry point. Read its role or technical
routes only when the current task needs them. Specialized `SKILL.md` files should
explain what to inspect, how to choose a method, what proves the claim, and which
false positives to rule out. Put detailed recipes and catalogs in linked
references; do not require reading every reference before starting.

When editing a technique:

- Preserve its useful prerequisites, examples, and failure cases. Fix incorrect
  examples rather than shortening them into an unsupported assertion.
- Distinguish a candidate, an observation, and a demonstrated security impact.
  Keep the principal and relevant controls fixed when testing a boundary.
- Treat version and vendor tables as candidates until checked against primary
  documentation and the target version. Record sources near corrected claims.
- Keep all references reachable and update relative links after moving content.
  Never split a fenced example across files.

Run from the repository root with Python 3.9 or later:

```sh
python3 scripts/check_skills.py
python3 -m unittest discover -s tests -v
```

The default structural check is offline and uses the standard library. Installing
PyYAML enables full frontmatter parsing. With `tiktoken` installed, use
`python3 scripts/check_skills.py --tokens` for an entry budget review (currently
1,600 tokens, a maintenance threshold rather than a platform limit). The first
token count may download the encoding table; ordinary checks do not need it.
Token counts cover file text only, not total model usage.

`tests/test_reference_examples.py` checks selected mathematical examples without
contacting a target. It does not validate every exploit or version table.
`tests/eval_cases.json` contains behavioral regression cases: run raw scenarios
without exposing their expected behavior, then compare routing, proof, stopping,
and context loaded against those expectations. Recheck affected scenarios after
changing routing or evidence rules; record missing artifacts as limitations.
