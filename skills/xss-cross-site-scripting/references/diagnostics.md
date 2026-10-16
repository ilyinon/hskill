# XSS: trace the final parser and rendering context

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Complete input-to-render path | Identify server serialization, client decoding, and the actual DOM/template sink. |
| Context at the final insertion | Separate HTML text, attribute, URL, JavaScript, CSS, and inert JSON data. |
| Applied encoding/sanitization | Read how it matches that context; a filter name is not the transformation. |
| Claimed effect | Distinguish reflected text, parsed markup, executable behavior, and account/business impact. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| One route escapes markup correctly | Effective local protection; a separate renderer may differ | Trace only reachable alternate sinks supported by source or captures. Do not keep varying payloads against the same correctly encoded text sink. |
| JSON contains literal markup | Inert JSON data or a later unsafe HTML sink | Inspect the consuming code: textContent and innerHTML have different semantics. |
| Markup becomes an element | HTML injection; execution still depends on context and defenses | Demonstrate only the parsed-content claim until a browser-feasible executable path is established. |
| Filter rejects a string | Working control for that transformation or an untested alternate path | Identify the sink/context and valid baseline before choosing a different representation. |
| Scanner or browser harness fails | Navigation, tooling, CSP, sandbox, or actual rejection | Separate harness failure from rendering and execution evidence; no whole-class conclusion follows. |

## Close the requested task

Track `untrusted data → transformations → final sink → parsed/executed effect → requested impact`. A code audit can identify an unsafe reachable sink without executing a browser payload. For a fix, encode for the actual context or use a text sink, then preserve allowed text rendering. Do not label an inert-markup parser test as script execution. [textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent) documents the text-insertion distinction.
