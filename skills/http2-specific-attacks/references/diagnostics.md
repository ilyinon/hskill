# http2-specific-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Negotiated and backend protocols | Verify H2 on this connection and whether any H1 translation actually exists. |
| Boundary evidence | Capture stream IDs, serialized backend requests and benign follow-up association. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| An invalid pseudo-header yields an error | Normal H2 rejection or downstream ambiguity | Locate whether a backend request was emitted. |
| H2 is supported | Direct H2 service or H2-to-H1 frontend | Inspect topology before using H1 framing recipes. |

## Interpret failure and finish the task

A local H2 tool/ALPN failure did not test the server parser. A protocol error without a forwarded ambiguous request is not smuggling.

Track `H2 stream -> frontend validation/translation -> backend message boundary -> controlled follow-up effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review the protocol boundary defensively

Identify where HTTP/2 is terminated and whether the origin receives a translated HTTP/1.1 request. Compare the configured header and message-length validation at each hop. Verify in a local decoder or configuration test that invalid messages never reach the origin adapter. [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.html)
