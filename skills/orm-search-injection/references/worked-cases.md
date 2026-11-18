# Worked case: admin digest extracted through a users search endpoint

Lab teaching case condensed from an authorized CTF run on a disposable Rails
app (GitLab-era Ransack search). The contract below is the supplied evidence.

**Goal.** Recover the sole admin user's password from the application database
via the web interface; the platform verifies submitted flags.

**Contract.**

```text
GET /users?q[user_username_cont]=gustav -> 1 row (public listing endpoint)
leaked advanced_search source: index builds a searchable column list,
  explicitly removing id and password_digest; the users controller's
  index action does not apply that removal
GET ...?q[user_password_digest_cont]=543dc% -> 1 row   (digest column searchable)
GET ...?q[user_password_digest_cont]=f9e8d7c6% -> 0 rows
```

**First approach and failure.** Treating the searchable `password_digest` column
alone as "the finding" skipped proof: no prefix had yet been shown to change the
result set, and a searchable column is a lead, not extraction.

**Revised approach.** Confirm the oracle on public columns (own username: known
value hits, random prefix misses, `%` matches). Then extract the 32-char digest
position by position with `q[user_password_digest_start]=<prefix><hex>%`,
16-probe alphabet, presence oracle; `_cont` was case-insensitive here, so a
single lowercase hex alphabet sufficed. Recovered
`543dc20bce20f799652e3ffdb8fd9d8a`. Cracked offline only after the full value
was fixed: a weak password hashed to it (`md5(candidate) == digest` computed
locally). Submitted the candidate, not the digest, as the flag.

**Independent controls.** A random same-length hex prefix returned nothing
(specificity). The full-value `…_start=<full>%` returned exactly one row (no
pagination noise). Local hashing showed the submitted candidate alone, and no
altered variant, reproduced the recovered digest, and the platform then returned
a `correct` verdict for that candidate.

**Completed result and limits.** Credential recovered and platform-confirmed.
No claim about the installed Ransack version (source audit was unavailable at
runtime); the same chain on another app must re-measure case sensitivity and
allowlist behavior, since current gems escape wildcards by default.
