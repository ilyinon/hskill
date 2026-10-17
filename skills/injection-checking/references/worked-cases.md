# Worked case: the sink is a text node, not a template compiler

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Route an observed markup string without manufacturing an injection.

```text
response: application/json, {message: "<b>owned</b>"}
complete consumer: node.textContent = JSON.parse(body).message
no template compilation or innerHTML consumer supplied
policy: show the message literally
```

**First approach and failure.** Calling the raw angle brackets XSS or SSTI relied on input appearance rather than the final sink.

**Revised approach.** Trace the textContent assignment. It fulfills the supplied literal-text contract; if a rendering review is requested, use XSS context diagnostics without payload spraying.

**Independent controls.** A plain message and the markup string must both remain literal text. JSON presence alone would be insufficient without the complete consumer.

**Completed result and limits.** No injection is supported on this path. The router selects a context review rather than claiming execution or whole-app safety.
