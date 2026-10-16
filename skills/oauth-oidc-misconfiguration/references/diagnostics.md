# OAuth/OIDC: locate the broken binding edge

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Observed grant/response flow and code path | Map authorize, callback, token exchange, and local account resolution. |
| Transaction binding | Establish state, session-held PKCE verifier, required challenge method, nonce where applicable, and one-time code behavior. |
| Verified provider identity | Inspect trusted issuer, token audience/signature, and the provider subject before local account linking. |
| Linking policy | Determine whether a local account lookup uses issuer+subject, an email, a client ID, or another mapping. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| No state parameter | Missing protection or a correctly enforced alternative binding | Trace the actual session/PKCE/nonce mechanism; compare same-session and foreign-code controls. |
| Foreign code rejected | Transaction binding works for that comparison | Inspect subsequent local identity lookup if the requested audit covers it; upstream safety does not prove downstream binding. |
| Same sub value appears at two providers | Legitimate issuer-local identifiers | Check whether the application keys identity by the pair (iss, sub); compare two owned provider identities. |
| Email maps to an existing account | Intended verified linking or unsafe automatic merging | Inspect verified-email/provider policy and required local authorization; matching text alone does not prove account ownership. |
| Callback error before exchange | Expired/reused code, redirect mismatch, provider error, or binding rejection | Identify the failed stage using a valid baseline. A tool/code lifetime failure does not isolate the intended defense. |

## Close the requested task

Track `request/session → grant → verified provider identity → local account → permitted action`. Choose the first unproved edge that can change the requested conclusion. A complete source lookup can support a local identity-collision finding; it does not demonstrate an entire provider takeover. For a fix, preserve both owned providers' legitimate identities without implicit linking. [RFC 8725 issuer/subject validation](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.8) is relevant to the final identity pair.
