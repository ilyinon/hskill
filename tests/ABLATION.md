# Measure the contribution of one optional reference

Use a paired blind run when deciding whether a reasoning module improves task
completion. `ablation_eval.py` prepares jobs and aggregates explicit semantic
grades; it never invokes a model, target, or fixture program. This is a maintainer
workflow and is not loaded by the runtime skill.

## Prepare frozen inputs

From the repository root, choose a new directory outside the checkout:

```sh
python3 scripts/ablation_eval.py prepare \
  --module hack/references/backward-planning.md \
  --case reason-backward-artifact \
  --repeats 2 --seed 17 --output /tmp/hack-ablation-001
```

Each pair gets identical raw task inputs and skill snapshots except for the
selected reference. The control replaces only that file with a neutral stub.
Entry files, frontmatter, UI metadata, other references, helpers and assets remain
identical. This measures access to that reference's guidance, not removal of the
entire capability. A control may still solve the task or discover the helper
through another route. No canonical repository file is modified.

The seed randomizes neutral condition codes and dispatch order; it is not a model
sampling seed. Use `--repeats 1` for a workflow smoke test. More repetitions help
expose variability, but a small paired sample is not statistical proof.

Give each solver only its `workers/trial-NNN` directory. Start a separate fresh
context for every job with no prior task, answer or rubric exposure. Keep model,
complete inference settings, tool permissions/availability, budgets and prompt
construction fixed. Include those facts in the declared environment fingerprint.
Do not provide the host manifest, source repository, tests, sibling workers or
expected answers. Snapshot separation is not a hostile-filesystem sandbox; use
restricted workers when stronger isolation is needed.

The 47 static cases include three `reason-*` transfer tasks with values outside
the instructional examples: backward artifact construction, a calibrated ledger
model, and argument-contract recovery. Their rubrics remain host-only. They are
withheld from runtime instructions, not claimed to be unknown to model training.

## Preserve outputs before grading

Each solver writes `answer.md` and `reads.json` in its own worker. Reads are actual
skill paths, optional inclusive ranges and repetitions, using the same form as
the static evaluator. Do not infer a read from an answer mentioning a concept.
Solver calculations and output files go beside these files, outside `skills/`
and `task/`. A failed job without an answer/read log leaves the experiment
incomplete; do not fabricate those records to enable comparison.

```sh
python3 scripts/ablation_eval.py seal \
  --experiment /tmp/hack-ablation-001 --output /tmp/hack-ablation-grades.json
```

Sealing checks the frozen inputs and preserves answer/read hashes in a grading
template. Grade with the case's rubric after sealing. The template identifies
case/repetition without revealing condition roles. Keep the full/control mapping
hidden from the grader until grades and reasons are saved. Blinding is procedural,
not guaranteed by the local filesystem.

Fill every criterion with `pass`, `fail` or `ungraded`. Fill `finding` using
`reported`, `not_reported`, `not_applicable` or `ungraded`; wrong classification
cannot pass all criteria. Record unsupported factual claims and unnecessary
actions as reviewed nonnegative counts, with evidence in `notes`. A useful
negative check or recheck after changed conditions is not wasted work.

Declare the actual `model_id`, complete `settings`, `settings_complete`,
`tools_fingerprint`, and unique fresh `context_id` for each job. An environment
fingerprint should cover system/tool conditions and limits as well as available
tools; unchanged script names do not establish identical capabilities. If the
runtime does not expose exact metadata, preserve that uncertainty and leave
settings incomplete. A repeated unknown label is not a controlled environment.

## Review the paired result

```sh
python3 scripts/ablation_eval.py report \
  --grades /tmp/hack-ablation-grades.json \
  --output /tmp/hack-ablation-report.json --tokens --require-comparable
```

`--tokens` uses optional `tiktoken` and the cached o200k_base table. Counts cover
recorded file text, including ranges and repeats, not total session usage.
Read logs and environment metadata are supplied records, not automatic telemetry.

Changed inputs, rubrics, answers or read logs are rejected. Missing grades,
unknown environment metadata, different environments or reused/shared contexts
produce `controlled_comparable:false` with no pair deltas. `--require-comparable`
also returns exit 2 after preserving the diagnostic report. Unit tests use clearly
labeled fictional metadata to exercise bookkeeping; that is not a model result.

Assess completion and false claims before unnecessary actions and context cost.
Report whether the full reference was actually read; no exposure gives no
evidence of instructional benefit. Inspect disagreements against raw artifacts.
Keep an improvement only when its intended behavior is supported, and retain
limitations. The tool does not automatically select a winning skill or certify
a general gain from a tiny sample.
