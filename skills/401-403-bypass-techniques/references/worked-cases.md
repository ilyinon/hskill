# Worked case: a successful response is the login shell

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Decide whether a path variant exposed the private test report.

```text
low session + /reports/r1 -> 403
same session + /reports/r1/ -> 200, text/html, <title>Sign in</title>
owner session + /reports/r1 -> 200, application/json, {marker: OWNED-R1}
unknown path -> 200, text/html, <title>Sign in</title>
```

**First approach and failure.** Calling the 200 a bypass ignored the authorized representation and the wildcard fallback.

**Revised approach.** Compare the variant with both the owner report and nonexistent-path control. The variant matches the fallback and contains no report marker.

**Independent controls.** Keep session, report ID, and method fixed; the owner baseline proves what a report looks like, while the unknown path explains the generic page.

**Completed result and limits.** No private-report access is established by this variant. Other routes and forbidden actions remain untested; an HTTP status change alone is insufficient.
