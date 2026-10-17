# Worked case: a scanner match loses its affected code path

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Prioritize the supplied inventory without turning fingerprints into findings.

```text
scope=portal.example.invalid read-only review
scanner: product family Q, historical issue candidate
supplied deployment manifest: affected optional module disabled
captured portal /api/export includes object IDs and member identity
auxiliary host in certificate is outside scope
```

**First approach and failure.** Following the candidate CVE before checking the module would spend effort on an absent prerequisite.

**Revised approach.** Mark that technique inapplicable to the supplied deployment; prioritize export object authorization from the actual captured operation.

**Independent controls.** Keep scanner output as provenance, the module configuration as applicability evidence, and the outside host as a scope note rather than a tested asset.

**Completed result and limits.** A justified testing plan and coverage limits are complete. This does not certify the portal or the historical product family.
