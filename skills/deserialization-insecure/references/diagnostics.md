# deserialization-insecure: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual reconstruction API | Trace format decoding into safe data parsing or object/class reconstruction. |
| Reachable classpath and filters | Pin runtime, allowed classes and invoked hooks before using a gadget recipe. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Base64 decodes to JSON | Transport wrapper or object deserialization | Inspect the next parser call and object construction. |
| A gadget payload errors | Wrong format/classpath/filter or harmless rejection | Locate the failure stage using a benign valid message. |

## Interpret failure and finish the task

A magic prefix or parser exception is not gadget invocation. An absent required class makes that chain inapplicable; a dangerous reconstruction API still needs its own reachable-input analysis.

Track `untrusted bytes -> decoder -> reconstruction API -> allowed objects/hooks -> observed bounded effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
