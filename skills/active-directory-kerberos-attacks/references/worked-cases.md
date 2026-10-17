# Worked case: the ticket names a different service

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Diagnose the first failed edge of a supplied ticket-use attempt.

```text
ticket client=test-a; server=HTTP/app-one.example.invalid
requested service=HTTP/app-two.example.invalid
service trace: wrong service principal, no authenticated session created
matching app-one control accepts ticket as test-a
no app-two ticket or key supplied
```

**First approach and failure.** Retrying the same imported ticket with privilege-changing options ignores the service-principal mismatch.

**Revised approach.** Compare ticket server and requested service first. The app-two authentication prerequisite is absent; do not infer an authorization bypass from cache import.

**Independent controls.** The matching app-one acceptance validates the supplied ticket path but grants only test-a there. Each service action still needs its own permission evidence.

**Completed result and limits.** The app-two attempt failed before authentication. No impersonation, password recovery or domain-level capability is established.
