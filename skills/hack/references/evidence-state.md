# Keep evidence valid across changes and resumptions

Use for a long task, changing inputs, or a context handoff. Keep a small working
record in the task's existing notes; a separate file is optional. Store necessary
facts and links to originals, not copied payload catalogs or sensitive values.

```text
goal: recover the requested bytes for r17 revision 5
sources:
  trace-a: capture.pcap, sha256 …, stream 3 packets 9–14, observed at t1
  config-a: supplied build-4.json, sha256 …, staging
claims:
  C1: frames contain r17 revision 4; observed; source trace-a
  C2: those frames satisfy current import; hypothesis; depends on C1, config-a
conditions: supplied member, tenant north, build 4; no current-build observation
open: consumer revision and issuer acceptance
next: inspect import manifest, then join contracts
completion: no requested value yet
```

A useful claim names its evidence location, conditions, status, and the claims it
depends on. Keep **observed fact**, **inference**, **hypothesis**, **contradicted**,
and **stale/needs recheck** distinct. Confidence words alone cannot replace a
missing dependency. Negative results also depend on the baseline, valid tool
operation, and tested conditions.

When an input changes, record a new source identity rather than overwriting the
old evidence. A file hash can identify bytes; it cannot prove the current live
configuration. Track the relevant build/session/object/time explicitly. Invalidate
only the claims whose required conditions or sources changed, then transitively
mark their dependants for recheck. Preserve still-valid historical observations.
If relevance is uncertain, mark that dependency unknown instead of silently
carrying the conclusion forward.

Example: a new build changes issuer validation. The captured token's issuer
remains an observed fact. The claim that the current consumer accepts that token,
and any impact inferred from acceptance, need a fresh check. An unrelated packet
length calculation does not become false because the build changed.

Before resuming after compaction or a handoff:

1. Recover the user's goal, scope, current result, earliest open dependency, and
   stop condition from the record.
2. Check source identities and the environment facts needed by that dependency.
   A missing artifact or unobserved environment is an explicit unknown.
3. Resume at the first affected edge. Reuse sound evidence instead of repeating
   every step or treating an old summary as a new observation.

Keep derived conclusions traceable to raw artifacts. An agent's previous answer,
a screenshot caption, or a note saying “verified” is not an independent source.
Do not fill missing observations with plausible text when saving a checkpoint.
