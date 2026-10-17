# Behavioral evaluation

The fixtures are small, synthetic offline artifacts. The suite includes source
reviews, authorization controls, HTTP responses, a real minimal ELF, a one-packet
PCAP, a segmented TCP capture, and an altered PNG. All files needed by each case are checked in. No live
target, real credential, external account, compiler, or provider is required.

`eval_cases.json` contains the requests, artifact paths, and grading rubrics.
The evaluator must not receive the rubric before producing its answer. The
runner prepares blind inputs and checks result integrity; semantic grading is
performed by a human or an independent agent after the answer is preserved.
Unit tests exercise selected reviewed Python fixtures and arithmetic helpers.
ELF and PCAP files are parsed statically, never executed.

The suite has 44 cases. Ten `solve-*` cases transfer the diagnostic reasoning to
new data or preconditions rather than repeating the published worked answers.
They include already-enforced defenses, a partial-refund policy that permits
multiple legitimate operations, an already-aligned stack, withheld generator
continuation, and TCP reassembly with retransmission. A correct outcome can be
a supported finding, a controlled rejection of a hypothesis, or a concrete
non-finding result. Do not treat every task as vulnerability reporting.

For numeric and capture tasks, the evaluator may write its own reviewed offline
arithmetic or parser. It must not execute supplied fixture programs. Preserving
the actual result is required; describing a possible method alone does not
complete a task that asks for numbers or recovered bytes.

Sixteen `extend-*` cases broaden the transfer checks to path components,
forwarded authority, duplicate binding, separate XML/transform resource gates,
accepted certificate identity, unknown admission, direct versus relayed service
access, telemetry health, finite-word recovery, tiny raw RSA, bit extraction,
process lifetimes, membership metrics, tool authority, callback ordering, and a
known-topic route. Several deliberately reverse the worked case's conclusion.

All 102 topic/router entries have conditional diagnostics and a worked case.
Material coverage is recorded in `skills/hack/solving_coverage.json`; it is not
runtime coverage. The 15 new `test_extended_solving.py` tests execute only the
named arithmetic/state contracts from inert JSON. Supplied product traces in
other examples were not observed by running those products.

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

## Evaluate tasks with progressive evidence

Three additional cases in `staged_cases.json` exercise an export chain, a build
change, and callback reproducer reduction. They combine incomplete artifacts,
supplied setup failures, alternative explanations, and final concrete results.
The runner replays finite synthetic observations and executes one reviewed small
refund-ledger model. It does not emulate a real API, browser, deployment, payment
provider, or product runtime. Fixture code and payload catalogs are never run.

The host starts one fresh session per case:

```sh
python3 scripts/staged_eval.py validate
python3 scripts/staged_eval.py start \
  --case release-export --session /tmp/hack-staged-001
```

Other IDs: `changing-build`, `callback-reproducer`. Give the evaluator only
`task/request.md`, `task/artifacts/`, the skill entry point, the session path, and
the trusted runner command. Do not supply `staged_cases.json`, its implementation,
unit tests, `staged_rubrics.json`, or sibling sessions. Future observations are
not in the exported task; the implementation and grading data are host resources.
This separation avoids accidental answer disclosure; it is not an adversarial
filesystem sandbox. Use a restricted worker filesystem if isolation is required.

The request supplies an action menu. The evaluator writes a call file such as:

```json
{"action": "inspect-client", "arguments": {}}
```

```sh
python3 scripts/staged_eval.py act \
  --session /tmp/hack-staged-001 --input /tmp/call-001.json
python3 scripts/staged_eval.py status --session /tmp/hack-staged-001
python3 scripts/staged_eval.py finish \
  --session /tmp/hack-staged-001 --answer /tmp/answer-001.md
```

Each accepted `act` call consumes one simulated action, including a tool error or
unknown result. An unrecorded input has no known outcome; do not generalize it to
a rejection by the real system. Invalid CLI invocations and other agent actions
are not counted. `repeated_inputs` counts identical calls, not wasted work: a
repeat after a changed environment can be necessary. Review the trace to classify
uninformative actions, and do not penalize a discriminating negative check.

History, raw observations, published artifact versions, and the submitted answer
are preserved. `status` replays the recorded history and checks input identity
and preserved artifacts; a changed scenario requires a fresh session. It does
not execute an agent's inferred claims or automatically invalidate their notes.
The evaluator must maintain and revise its own dependencies. Use one writer per
session; this local harness is not a concurrent service or tamper-proof audit log.

`finish` copies the answer and writes `report.json` with hashes, observations,
outcome counts, action budget, and **pending** grading. It can preserve a partial
answer when the budget is exhausted. It never marks an answer correct.

After preserving the answer, a human or independent reviewer reads
`staged_rubrics.json`. Save `pass`, `fail`, or `ungraded` for every criterion with
supporting answer/trace locations, plus a list of unnecessary actions with reasons.
Record the scenario input digest, answer hash, actual skill-read log, model and
settings, context mode, and limitations alongside the grades. Use honest unknown
values for metadata the runtime does not expose. Do not invent measured read
telemetry or model identity. Completion requires every criterion to pass; an
ungraded case is incomplete. Review reasoning, not matches to preferred wording.

Compare candidates only under the same scenario digest, action menu, budget,
model/settings and fresh per-case context. Compare completion and false claims
before action cost or recorded file-text tokens. Report the tiny sample size;
three successful synthetic tasks do not establish a general quality gain or
validate a live target. The existing static-case `compare` command does not
accept staged reports.

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
