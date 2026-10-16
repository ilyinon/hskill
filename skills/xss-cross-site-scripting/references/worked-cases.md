# Worked case: the primary renderer is safe, the legacy renderer is not

Synthetic HTML-text rendering: [input](./examples/input.json), [model](./examples/model.py). The input is harmless `<b data-case="owned">marker</b>` markup; no script is used.

**Goal.** Both routes must show the supplied value literally. Locate and repair a path violating that contract.

**First approach.** `main_page` escapes the string before inserting it into a paragraph. A proper HTML parse sees text, not a new `b` element. Repeated encodings against this same path do not establish a missing control.

**Revised approach.** The complete source also has `legacy_preview`, which concatenates the original string into a div. The same data is now parsed as a `b` element. This demonstrates a separate HTML-injection path, not an encoder bypass in `main_page`.

**Repair and independent check.** Encode this HTML-text insertion too. `test_solving_examples.SolvingExamples.test_alternate_html_text_sink_and_fix` compares parsed element structure for the safe path, the legacy path, and the fixed path, and confirms the original value survives as text after the fix. It uses Python's parser only for this simple inert HTML example.

**Completed result.** The literal-text contract is restored in both paths. No browser JavaScript execution, CSP bypass, attribute/URL-context safety, or deployed XSS impact is claimed. A later JSON-to-DOM consumer would need its own source trace; raw markup inside a JSON response alone is insufficient.
