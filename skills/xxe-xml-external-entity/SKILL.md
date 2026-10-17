---
name: xxe-xml-external-entity
description: >-
  XXE playbook. Use when XML, SVG, OOXML, SOAP, or parser-driven imports may resolve external entities, files, or internal network resources.
---

# Xxe Xml External Entity

## Working approach

- Identify the server-side XML parser, configuration, resolver, entry format, and reflection/egress path
- Compare a harmless internal entity with a controlled external marker
- Separate entity resolution, file disclosure, SSRF, and extension execution.

## Evidence and limits

Server-side entity or related XML resource processing crosses the intended file/network boundary with attributable evidence.

Serving an SVG/XML file is not itself XXE; a callback does not prove file read, and XInclude/XSLT require their own enabled processing paths.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CLASSIC XXE PAYLOAD; 2. ATTACK SURFACE DISCOVERY; 3. OOB (OUT-OF-BAND) XXE — CRITICAL; 4. XXE FILE READ TARGETS; 5. SVG XXE (file upload context); 6. OFFICE FILE XXE (docx/xlsx/pptx); 7. SOAP ENDPOINT XXE; 8. XXE → SSRF CHAIN; 9. XInclude ATTACK | [Read](./references/01-classic-xxe-payload.md) |
| 10. PROTOCOL HANDLERS IN XXE; 11. BYPASSING DEFENSES; 12. QUICK DETECTION CHECKLIST; 13. LOCAL DTD INJECTION (BLIND XXE AMPLIFICATION); 14. ADDITIONAL OOB EXFILTRATION CHANNELS; 15. DTD NESTING TRICKS — PARAMETER ENTITY CHAINING | [Read](./references/02-protocol-handlers-in-xxe.md) |
| 16. XXE IN NON-OBVIOUS FORMATS; 17. XXE VIA FILE UPLOAD; 18. ERROR-BASED XXE; 19. XSLT INJECTION CONNECTION TO XXE | [Read](./references/03-xxe-in-non-obvious-formats.md) |
| Advanced: XXE — Extended Scenarios & Real-World Cases | [Read](./SCENARIOS.md) |
