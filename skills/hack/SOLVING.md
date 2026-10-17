# Choosing the next useful action

Use the relevant section when a task stalls, evidence is ambiguous, or capabilities
must be combined. Topic diagnostics supply concrete branches; ordinary work does
not require another full workflow.

## Define what completes this task

| Requested task | Completion evidence |
|---|---|
| Code audit | Actual source path, required policy, missing/effective control, and bounded impact. |
| Fix/debug | Addressed failure mechanism, working legitimate case, and a regression control for the failed assumption. |
| Authorized lab/puzzle | Requested value, prediction, marker, or local effect independently checked under the supplied construction. |
| Capture/artifact analysis | Recovered bytes/events tied to format/stream locations, with explicit gaps and attribution limits. |

Tie completion to the user's request. An intermediate still needs its remaining
prerequisites; sufficient source evidence can complete an audit without production
execution. A requested proof need not expand into additional impact.

## Choose a discriminating check

Record necessary facts with source/packet/request locations; separate assumptions
and unknowns. Choose a small permitted check whose predicted outcomes distinguish
the leading explanations. Resolve a prerequisite or earliest uncertain edge before
repeating payloads testing the same assumption. Use a known-good baseline so wrong
format or a broken tool cannot masquerade as a negative.

For changing inputs or context resets, keep a compact
[evidence state](references/evidence-state.md). For a consequential conclusion
with a plausible competing explanation, use a targeted
[refutation pass](references/refutation.md).

## Interpret failure before retrying

| Failure type | What it supports | Next action |
|---|---|---|
| Setup/tool failure before the operation | Operation untested | Correct syntax/version/representation or use equivalent inspection. |
| Missing technique prerequisite | Technique inapplicable under observed conditions | Choose a compatible method; keep unrelated boundaries open. |
| Valid controlled negative | Tested path failed under those conditions | Update the hypothesis or conclude within scope. |
| Missing/noisy evidence | Outcome unknown | Obtain the smallest missing fact or state the limit. |

Change one causal dimension at a time. Retry when a new hypothesis predicts an
informative outcome. Equivalent failures do not justify unbounded search; one
malformed attempt does not establish class-wide safety.

## Join capabilities toward the goal

Keep a compact `capability → required condition → next effect` chain, with evidence
or an unknown on each edge. Select the earliest unresolved edge needed by the goal.
Readable bytes are not automatically accepted identity; a word list is not a
prediction; control transfer is not a working process effect.

Check [edge contracts](references/chain-contracts.md) when individually proven
steps may not compose. Use [staged progress](references/staged-progress.md) for
long tasks with delayed evidence or failed tools. If an edge needs unavailable
access or an unapproved action, retain the partial result and limit; reuse existing
authorization and clarify only genuine blockers.

A fix must preserve valid behavior. When a working proof's cause or repair is
unclear, [minimize the reproducer](references/minimization.md) with its control.

## Transfer mechanisms from worked cases

Read a case matching the unresolved mechanism. Extract why the first attempt was
uninformative, what observation changed the approach, and how the result was
independently checked. Re-establish prerequisites instead of copying the answer.
Synthetic examples verify supplied models, not every runtime or configuration.
