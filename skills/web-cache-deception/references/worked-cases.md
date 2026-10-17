# Worked case: the cache is partitioned by identity

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied HIT trace before reporting cross-user leakage.

```text
teaching key=(normalized path, authenticated user ID)
A /account/style.css -> HIT, body=A-private
B same path -> MISS, origin body=B-private; then B HIT contains B-private
anonymous same path -> own partition, login page
no A-private bytes in B/anonymous responses
```

**First approach and failure.** Calling A's HIT a shared-cache leak assumed the key omitted identity.

**Revised approach.** Inspect the actual partition and compare clean readers. The supplied key separates identities, so this path does not expose A's bytes to B.

**Independent controls.** Use unique keys and compare body markers after priming. Report-only cache labels or browser-local caches cannot substitute for a shared-reader observation.

**Completed result and limits.** No cross-user cache disclosure in this trace. Other keys, normalization rules, query exclusions and poisoning paths remain untested.
