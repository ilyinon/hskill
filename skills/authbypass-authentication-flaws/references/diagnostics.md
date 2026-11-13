# authbypass-authentication-flaws: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Session state machine | Identify anonymous, primary-authenticated, MFA-pending, and fully authenticated states. |
| Final enforcement | Trace both session issuance and authorization at the protected handler. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| OTP endpoint returns success | Delivery/format acceptance or completed second factor | Inspect session assurance state and protected operation. |
| Pending session token exists | Expected temporary capability or an overprivileged session | Compare a protected action under the same pending session. |

## Interpret failure and finish the task

Wrong OTP format or an expired transaction does not isolate MFA enforcement. A denied protected action may be an effective control even if token naming is confusing.

Track `credentials -> pending identity -> required factor -> session assurance -> protected capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Verify complete authentication state

Model anonymous, pending, fully authenticated, and expired sessions explicitly. Check protected handlers require the fully authenticated state and that reset or second-factor transitions expire and consume their pending record. Include a normal login and a direct handler call with a pending session in the application test.
