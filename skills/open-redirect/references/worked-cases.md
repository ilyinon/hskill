# Worked case: the external text is inside a same-origin query value

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Determine the effective target of a supplied redirect.

```text
base=https://app.example.invalid
Location=/continue?next=https://other.example.invalid/owned
supplied navigation trace stops at https://app.example.invalid/continue?next=...
complete /continue handler displays next as text and never redirects
policy: navigation remains on app.example.invalid
```

**First approach and failure.** Calling the external-looking substring an open redirect skipped the outer URL and final handler.

**Revised approach.** Resolve the Location and trace the complete continuation consumer. Navigation stays on the app host; external text remains data.

**Independent controls.** A normal relative Location provides the baseline. A true external Location would be a different candidate requiring effective navigation evidence.

**Completed result and limits.** No external navigation in this path. Token leakage, SSRF and other continuation consumers are not established.
