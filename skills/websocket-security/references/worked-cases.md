# Worked case: the socket opens but a foreign topic is denied

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied channel trace with two owned test tenants.

```text
A handshake -> 101, principal=A
A subscribes topic A/private -> ack allowed, A marker frame
same socket subscribes B/private -> error forbidden; no B frames
B own socket/topic -> B marker
policy: private topics restricted to owner
```

**First approach and failure.** Calling the successful handshake a topic-access bypass skipped the message-level decision.

**Revised approach.** Compare authorization and delivered frames on the same A connection. The foreign-topic denial is effective under the supplied policy.

**Independent controls.** Both owner baselines establish the topics exist; a denied ack plus no protected frames is stronger than status alone. Other message actions need independent checks.

**Completed result and limits.** No topic isolation flaw in this trace. Browser-origin hijacking, unrelated message types and server execution remain unassessed.
