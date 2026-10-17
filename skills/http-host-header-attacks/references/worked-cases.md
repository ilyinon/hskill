# Worked case: the URL builder consumes an untrusted forwarded host

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Audit a supplied reset-link artifact without sending mail or using credentials.

```text
direct peer=192.0.2.50, not a trusted proxy
Host=app.example.invalid passes Host allowlist
X-Forwarded-Host=other.example.invalid
complete builder trusts forwarded host without peer validation
owned local mail fixture URL=https://other.example.invalid/reset?token=OWNED-INERT
policy: reset URLs must use configured app origin
```

**First approach and failure.** Stopping at the Host allowlist missed the different authority consumed by the link builder.

**Revised approach.** Trace the actual absolute-URL source. Use a configured canonical origin for this link or enforce the real trusted-proxy/stripping contract before honoring forwarded authority.

**Independent controls.** Without the forwarded header the owned link uses app origin; with the same direct peer it must remain canonical after repair. Inspect the local emitted artifact, not only an HTTP reflection.

**Completed result and limits.** A protected-link origin-policy flaw is supported in the supplied model. No email was sent, live token used, account taken over or arbitrary server fetch demonstrated.
