# request-smuggling: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Connected parser pair and reuse | Identify exact frontend/backend parsing, protocol translation and connection sharing. |
| Boundary and association evidence | Capture consumed byte ranges and a benign follow-up request/response pair. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Ambiguous length request times out | Normal rejection, body wait, tool framing error, or desync | Inspect frontend/backend bytes and the isolated follow-up. |
| Conflicting headers appear | Candidate syntax or actual different boundaries | Compare which parser consumes what before claiming smuggling. |

## Interpret failure and finish the task

A timeout alone is inconclusive. If the frontend rejects before forwarding, the backend parser was not exercised; use isolated owned connections rather than shared-user queues.

Track `raw bytes -> frontend message boundary -> forwarded backend bytes -> backend boundary -> controlled follow-up association`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Verify framing policy at each hop

Align message validation between the edge and origin and prefer rejecting ambiguous framing before forwarding. In an offline parser or adapter test, check that a valid request is forwarded once and a rejected message sends no bytes to the next hop. Verify the connection is not reused after a framing error. [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html#section-6.3)
