---
name: ai-ml-security
description: >-
  AI/ML security playbook. Use when assessing model supply chain attacks (pickle RCE, poisoned weights), adversarial examples, model poisoning, model stealing, data privacy attacks (membership inference, model inversion), and autonomous agent security risks.
---

# Ai Ml Security

## Working approach

- Identify model artifacts, loaders, training/inference data, serving APIs, and agent tools
- Separate deserialization, adversarial behavior, privacy inference, and tool-authority hypotheses
- Test on controlled artifacts with a baseline and a relevant control.

## Evidence and limits

Reproducible model or system behavior violates the specified integrity, confidentiality, or tool-authorization boundary.

A harmful-looking response, a low-confidence membership guess, or a generic jailbreak is not proof of system execution or data extraction.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. MODEL SUPPLY CHAIN ATTACKS; 2. ADVERSARIAL EXAMPLES; 3. MODEL POISONING | [Read](./references/01-model-supply-chain-attacks.md) |
| 4. MODEL STEALING / EXTRACTION; 5. DATA PRIVACY ATTACKS; 6. LLM-SPECIFIC SECURITY (Cross-ref); 7. AGENT SECURITY; 8. TOOLS & FRAMEWORKS | [Read](./references/02-model-stealing-extraction.md) |
| 9. DECISION TREE | [Read](./references/03-decision-tree.md) |
