# macos-process-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual launch context | Record OS/build, architecture, responsible process, environment and signing/entitlements. |
| Boundary-specific checks | Separate loader environment, writable search paths, XPC peer authorization and process-memory permissions. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| DYLD variable is present in a shell | It may be stripped/ignored in the target launch context | Inspect the actual target environment and loader decision. |
| A dylib path is missing | Search-path candidate, not accepted foreign code | Check writable location and code-signature/library-validation prerequisites. |

## Interpret failure and finish the task

A local loader error did not establish cross-process execution. A debug/instrumented launch is a different threat model from a protected release process.

Track `controlled launch/input -> actual loader/IPC context -> signing/peer policy -> attributed process effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
