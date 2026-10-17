# Worked case: valid authentication leaves an object-policy question

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Choose the smallest relevant specialization for the supplied audit.

```text
signature verification passes; principal=test-a, tenant=A
GET invoice a1 -> 200, owner=A
same token, GET invoice b1 -> 200, owner=B
policy: invoices private to tenant; complete handler looks up only invoice ID
```

**First approach and failure.** Opening signing-key and algorithm recipes would test a boundary that already works in the supplied path.

**Revised approach.** Route directly to API authorization/BOLA and canonical IDOR reasoning. Keep principal A fixed and trace the missing tenant constraint on the returned invoice.

**Independent controls.** Own invoice and foreign-owner baseline establish representation and ownership; the same-token comparison isolates object policy.

**Completed result and limits.** The route and source-supported private-read finding are justified. No token forgery, write privilege, or full API coverage is inferred.
