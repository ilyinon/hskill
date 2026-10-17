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
python3 scripts/eval_skills.py validate
python3 scripts/staged_eval.py validate
python3 -m unittest discover -s tests -v
```

The default structural check is offline and uses the standard library. Installing
PyYAML enables full frontmatter parsing. With `tiktoken` installed, use
`python3 scripts/check_skills.py --tokens` for an entry budget review (currently
1,600 tokens, a maintenance threshold rather than a platform limit). The first
token count may download the encoding table; ordinary checks do not need it.
Token counts cover file text only, not total model usage.

`tests/test_reference_examples.py` checks selected mathematical examples.
`tests/test_eval_fixtures.py` checks reviewed offline source models and binary
artifact structure. `tests/test_solving_examples.py` checks the ten self-contained
worked models, including the failed approach and independent controls. These
tests do not validate every exploit or version table. `test_extended_solving.py`
checks 15 additional inert arithmetic/state contracts from canonical per-topic
JSON data; it does not run product runtimes or skill payload catalogs.

Use the blind preparation and grading workflow in [tests/EVALUATION.md](tests/EVALUATION.md)
after changing routing or evidence rules. Its 44 cases include real local
artifacts; expected outcomes stay outside the evaluating agent's context.
Preserve answers, read logs, input/rubric digests, settings, and grading reasons.
The ten `solve-*` and sixteen `extend-*` transfer cases change values or
preconditions from the worked cases. Keep those differences meaningful: include working defenses and valid
alternatives so copying an example's fix cannot pass. Grade task completion,
not just vulnerability classification.

For tasks with delayed evidence, use the three staged cases described in
[tests/EVALUATION.md](tests/EVALUATION.md). Keep final-answer grading separate
from runner bookkeeping. Add meaningful alternative explanations and legitimate
controls; a model must be able to refute the tempting hypothesis. Unknown inputs
in a finite recording are untested, not controlled negatives. Preserve original
sources and invalidate dependent conclusions when relevant conditions change.
Keep the five shared complex-task references behind conditional `SOLVING.md`
links rather than copying them into every specialist entry.

For diagnostic references, connect prerequisites and observed failures to the
smallest distinguishing check. Separate setup errors, unmet preconditions,
controlled negative results, and inconclusive evidence. Link intermediate
capabilities to the requested result. Worked cases should show a real first
failure, why the revised approach follows, and a control independent of the
claimed success. Do not turn the case's fix into a universal rule. Mark supplied
teaching traces as supplied, rather than implying a browser, kernel, provider or
other product was executed. Keep real test pointers next to executed models and
update `skills/hack/solving_coverage.json` when adding a topic or named check.
Topic routers should teach the next boundary decision without duplicating all
of their specialist references.

For overlapping subjects, choose a canonical home for the technique and link to
it from adjacent workflows. API credential/proxy handling belongs in
`api-auth-and-jwt-abuse`, JWT signing/key/claim validation in
`jwt-oauth-token-attacks`, and OAuth/OIDC transaction binding in
`oauth-oidc-misconfiguration`. Category routers are optional for ambiguous tasks.
Use task-oriented reference names and index labels; keep compatibility paths
when existing links need them.

Record source review and actual offline validation separately in
`skills/hack/verification.json`. Supply the checked version/configuration and
limitations. A verification record must not imply that an untested library or
CLI command was executed.

## Continuous checks and token review

The GitHub Actions workflow runs offline checks on Python 3.9 and full YAML/token
checks on Python 3.13. It does not call an agent API or contact a test target.
Optional check dependencies are pinned in `requirements-check.txt`.

```sh
python3 scripts/check_skills.py --tokens --strict --baseline tests/token_baseline.json
```

The reviewed baseline covers entry files and references. Existing-file growth
above both 64 tokens and 15% triggers review; a new reference over 2,000 tokens
also triggers review. Entry files retain the 1,600-token review threshold.
`--strict` makes warnings fail CI. These are maintenance choices: inspect whether
growth improves the skill, then intentionally refresh the baseline when justified:

```sh
python3 scripts/check_skills.py --tokens --strict --json tests/token_baseline.json
```

Keep the baseline update reviewable beside the content change. The CI summary
shows per-document token changes; it is not a behavioral quality score.
