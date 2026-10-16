# Choosing the next useful action

Use the relevant section when a task stalls, a result is ambiguous, or several
capabilities must be combined. Topic diagnostics supply the concrete branches;
this document does not require another full workflow before ordinary work.

## Define what completes this task

| Requested task | Completion evidence |
|---|---|
| Code audit | Actual source path, required policy, missing/effective control, and bounded impact; no production proof is inherently required. |
| Fix/debug | The failure mechanism is addressed, the legitimate case still works, and a regression control exercises the failed assumption. |
| Authorized lab/puzzle | The requested recovered value, prediction, marker, or local effect passes an independent check under the supplied construction. |
| Capture/artifact analysis | Recovered bytes/events are tied to format/stream locations, with explicit gaps and attribution limits. |

Keep this criterion tied to the user's request. An interesting intermediate is
useful progress; a requested end result still needs its remaining prerequisites.
A sufficient requested proof can complete a task without additional impact.

## Choose a check that distinguishes explanations

Record only the facts needed now, with source/packet/request locations. Keep
assumptions and unknowns separate. For the leading explanations, identify which
small permitted check would produce different expected outcomes. Prefer a check
that resolves a prerequisite or the earliest uncertain edge over another payload
testing the same assumption. Use a known-good baseline so a broken tool or wrong
format does not masquerade as a negative result.

## Interpret a failed attempt before retrying

| Failure type | What it supports | Useful next action |
|---|---|---|
| Setup/tool failure before the intended operation | The operation was not tested | Correct syntax/version/representation or use an available equivalent inspection method. |
| Technique prerequisite absent | That technique is inapplicable under the observed conditions | Select a method whose prerequisites fit; keep unrelated boundaries open. |
| Valid controlled negative | The tested path/capability failed under those conditions | Update that hypothesis and choose another supported explanation or conclude within scope. |
| Missing/noisy evidence | The outcome remains unknown | Obtain the smallest missing fact if possible, otherwise state the limit. |

Change one causal dimension at a time. Retry when a new hypothesis predicts a
different informative outcome. Repeated equivalent failures do not justify an
unbounded search; a single malformed attempt does not establish class-wide safety.

## Combine intermediate capabilities toward the goal

For a multi-step task, keep a compact chain of `current capability → required
condition → next effect`, with evidence or an unknown marker on each edge. Select
the earliest unresolved edge that matters to the requested goal. Do not silently
promote readable bytes into accepted identity, a recovered word list into a
prediction, or a correct control transfer into a working process effect.

If an edge requires unavailable access, a different target, or an unapproved
action, preserve the partial result and its limit. Reuse existing authorization;
only genuinely missing blockers need clarification. A fix should preserve valid
behavior as well as reject the violating case.

## Use worked cases as mechanisms, not templates to copy

Read a case matching the unresolved mechanism. Extract why its first attempt was
uninformative, which observation changed the approach, and how the result was
independently checked. Re-establish its prerequisites in the current task. The
included synthetic examples verify their supplied models; they do not certify
every library, browser, runtime, or production configuration.
