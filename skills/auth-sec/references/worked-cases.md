# Worked case: password reset delivery is not a completed takeover

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Route a password-reset observation to the missing verification step.

```text
owned account requests reset -> email queued
reset response reveals requestId but no bearer/reset credential
captured completion call requires token and account binding
no valid completion observation supplied
```

**First approach and failure.** Calling the queued email or requestId a takeover skipped the credential and session transition.

**Revised approach.** Choose authentication/recovery diagnostics, then inspect requestId use, token binding, lifetime, and final session issuance. Do not start JWT signing attacks merely because a session token is eventually used.

**Independent controls.** Compare a valid owned completion with a missing/foreign token only if that test is supplied or permitted; keep unsupplied completion unknown.

**Completed result and limits.** The correct next boundary is identified; account takeover is not established from this evidence.
