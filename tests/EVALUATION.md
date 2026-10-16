# Behavioral evaluation

The fixtures are small, synthetic offline artifacts. The suite includes source
reviews, authorization controls, HTTP responses, a real minimal ELF, a one-packet
PCAP, and an altered PNG. All files needed by each case are checked in. No live
target, real credential, external account, compiler, or provider is required.

`eval_cases.json` contains the requests, artifact paths, and grading rubrics.
The evaluator must not receive the rubric before producing its answer. The
runner prepares blind inputs and checks result integrity; semantic grading is
performed by a human or an independent agent after the answer is preserved.
Unit tests exercise selected reviewed Python fixtures and arithmetic helpers.
ELF and PCAP files are parsed statically, never executed.

## Prepare a blind run

From the repository root, using a new output directory:

```sh
python3 scripts/eval_skills.py validate
python3 scripts/eval_skills.py prepare --output /tmp/hack-blind-001
```

Use `--case jwt-direct-control` to select one case; repeat `--case` for several.
The exported case folders contain only `request.md` and raw artifacts. `run.json`
records case IDs and input digests. Existing run directories are not overwritten.

For each case, give the evaluating agent the skill entry point at
`skills/hack/SKILL.md`, the exported request, and its artifact folder. Start a
fresh context per case for controlled comparisons. Keep model/settings and tool
availability fixed. Do not provide `eval_cases.json`, prior answers, or another
candidate's conclusions. Limit actions to the supplied offline task.

Preserve each answer and its actual file-read log. Record repeated reads; when
only a range was read, record its inclusive line numbers. Keep generated answers
and grades outside `skills/` and the fixture collection.

## Grade after the answer is preserved

```sh
python3 scripts/eval_skills.py template \
  --run /tmp/hack-blind-001/run.json \
  --output /tmp/hack-grades-001.json
```

Fill the template using the rubric in `tests/eval_cases.json`:

- `label`, `revision`, `reviewer`: identify the candidate, source snapshot, and
  grader. Include the settings in `model` so comparisons can reject differences.
- `context_mode`: `fresh-per-case` or `shared-session`. A shared-session review
  can find defects, but is not an isolated per-case context benchmark.
- `answer_file`: preserved answer path, absolute or relative to the grades file.
- `criteria`: `pass`, `fail`, or `ungraded` for every named criterion. Grade the
  reasoning and observed boundary, not a phrase match.
- `finding`: `reported`, `not_reported`, or `not_applicable`. Use the case's
  expected finding classification; `ungraded` leaves the result incomplete.
- `notes`: explain the verdict and any missing evidence.
- `read_files`: actual repository-relative reads, in order. A string records a
  whole file. A range is `{"path": "skills/hack/SKILL.md", "start_line": 8,
  "end_line": 20}`. If the log is incomplete, report that limitation rather than
  presenting an estimated log as measured telemetry.

The template records both raw-input and rubric digests. Do not edit those values
to make different fixtures appear comparable.

```sh
python3 scripts/eval_skills.py report \
  --results /tmp/hack-grades-001.json \
  --output /tmp/hack-report-001.json
```

Add `--tokens` with `tiktoken` installed to count the recorded text reads. Ranges
and repeated reads are included; binary content is counted separately. These
counts exclude tool-output formatting, images, other prompts, and model
reasoning. They do not measure total model usage. A first token count may
download the encoding table.

The report preserves answer/read hashes, missing or ungraded cases, false
positives and false negatives for the designated finding cases. It rejects
changed fixtures, changed rubrics, missing answers, or missing criterion grades.

## Compare candidates

```sh
python3 scripts/eval_skills.py compare \
  /tmp/hack-report-before.json /tmp/hack-report-after.json
```

Comparison requires the same model/settings label, context mode, complete grades,
case set, input digests, and rubric digests. Compare conclusion quality first,
then unnecessary reads and file-text tokens. Report suite coverage; passing this
small corpus does not validate every technique or software version.

## Maintain fixtures and verification records

Add a minimal artifact that distinguishes the intended behavior from a plausible
false positive or missed issue. Include a baseline/control when it changes the
conclusion. Keep dates, account identities, packet structure, and other relevant
facts in the artifacts. A request mentioning an absent source file is incomplete.

`skills/hack/verification.json` records selected primary sources, review dates,
tested environments, test IDs, and limitations. `source-reviewed` means the claim
was checked against a source; `offline-tested` means only the named local test
was run. A tested toy model does not certify a production library, CLI recipe,
provider, or historical CVE. Record new validation dates after actually checking
the claim, not when moving or reformatting text.
