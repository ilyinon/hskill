# Check whether capabilities compose

Use when a task needs two or more established capabilities. A proof of A and a
proof of B do not establish A → B unless A supplies what B actually accepts.

Write only the uncertain boundary, for example:

```text
producer: read export E through session S; observed in trace T:41–53
output: raw bytes, object r17 revision 4, tenant north, staging issuer
consumer: report import; requires decoded JSON revision 5, production issuer
status: broken at revision and issuer; representation conversion alone cannot fix it
next check: inspect the current import contract using the existing scoped session
```

Compare the dimensions that can change the outcome:

| Dimension | Typical non-composing evidence |
|---|---|
| Principal, session, authority | Reading a key does not establish its validity; admin proof does not transfer to the supplied member. |
| Object, tenant, namespace | A basename or display name is equal while the internal object or tenant differs. |
| Version, configuration, runtime | A local parser accepts bytes that the deployed build rejects; a gadget exists in another image. |
| Representation | Wire bytes, decoded text, canonical path, integer width, or endianness differ at the boundary. |
| Time, state, lifetime | A nonce has expired, a process restarted, a callback consumed the state, or the observation predates a configuration change. |
| Required effect | Reading, authenticating, scheduling, executing, and persisting are different effects. |

Mark an edge **supported**, **incompatible**, or **unknown** under stated
conditions. Unknown is not compatible. A mismatch can be resolved by an observed
adapter, mapping, or transition; record that transition and test its output at the
consumer. Do not invent a decoder, credential exchange, or namespace mapping.

Choose the earliest unresolved edge on a route to the requested result. If that
edge is disproved, retain its useful observations and try another supported route
within the existing scope. Do not discard the whole investigation or claim a
longer impact chain than the evidence supports. In a source audit, a complete
source-level contract may suffice; invoking the consumer is not always required.

For the final claim, cite the joining evidence as well as both endpoints. A
diagram of plausible arrows is a hypothesis until the needed joins are supported.
