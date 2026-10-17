# Worked case: the parser closes the attribute before the marker

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Determine whether a supplied parser/network trace establishes leakage.

```text
inert following marker=OWNED-FOLLOWING
supplied repaired DOM: img.src=https://collector.example.invalid/owned
marker appears only in a separate text node
network trace: request URL ends /owned; marker absent
no target/browser execution performed in this case
```

**First approach and failure.** Calling any resource request a following-content leak skipped which bytes entered the attribute.

**Revised approach.** Compare DOM attribute and transmitted URL with the exact marker location. The supplied parser did not include the marker in the request.

**Independent controls.** A plain marker in visible text confirms its presence; the request trace confirms only the inert destination. Do not infer secret capture from malformed source alone.

**Completed result and limits.** No following-marker leak is demonstrated. Other contexts, CSP dispositions and browser versions require their own observations.
