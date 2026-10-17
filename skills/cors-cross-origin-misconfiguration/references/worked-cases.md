# Worked case: the wildcard does not expose the credentialed response

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret a supplied browser-policy trace without using real cookies.

```text
request Origin=https://reader.example.invalid, credentials=include
supplied trace: eligible cookie sent; server body=OWNED-PRIVATE
response ACAO=*, ACAC=true
browser trace: CORS exposure rejected; response body unavailable to script
policy: unrelated origins must not read private body
```

**First approach and failure.** Calling curl-visible bytes a browser leak skipped the final exposure gate.

**Revised approach.** Trace dispatch and exposure independently. The server generated private bytes, but the supplied credentialed browser read is blocked by the wildcard origin response.

**Independent controls.** A matching allowed origin with explicit ACAO and ACAC is the positive exposure control. A write endpoint would require separate CSRF analysis because requests may still be sent.

**Completed result and limits.** No private cross-origin read is demonstrated for this trace; no global CORS or CSRF safety claim follows.
