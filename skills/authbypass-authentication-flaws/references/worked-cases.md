# Worked case: the pending session is accepted by the protected handler

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Audit the supplied MFA transition without guessing codes.

```text
correct password -> session={user: test-a, stage: pending}
MFA completion requires valid code; no valid code supplied
complete /private handler checks session.user only
pending session + /private -> 200, OWNED-PRIVATE
policy: /private requires stage=complete
```

**First approach and failure.** Testing wrong codes proves rejection at MFA completion but misses a protected handler that accepts the pending state.

**Revised approach.** Keep the pending session and inspect the final authorization predicate. Requiring stage=complete before returning private data repairs the demonstrated edge.

**Independent controls.** Anonymous request remains denied; pending session is denied after repair; a supplied complete session still reads its own private marker.

**Completed result and limits.** A source-supported MFA enforcement gap is established for this handler. No OTP prediction, other-account takeover, or deployed behavior is claimed.
