# Worked case: one permissive header cannot relax another

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret the supplied resource-decision trace.

```text
enforced P1: script-src 'self'
enforced P2: script-src 'none'
report-only P3: script-src https://cdn.example.invalid
candidate same-origin script: P1 allows, P2 denies; execution marker absent
```

**First approach and failure.** Selecting the most permissive directive or report-only header ignores the intersecting enforced policy.

**Revised approach.** Evaluate the candidate under P1 and P2 together. P2 denies it; P3 is observational and cannot grant execution.

**Independent controls.** Within the supplied policy evaluator, remove P2 in a separate offline control and P1 allows the same origin; preserve all policies when describing the real trace.

**Completed result and limits.** This candidate is blocked by the complete supplied policy. No CSP bypass or whole-application XSS safety is established; browser behavior was supplied, not executed here.
