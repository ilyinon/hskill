# Worked case: the destination loopback is on the forwarding host

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Diagnose an offline forwarding trace.

```text
client host=C; forwarding host=F
contract: F opens destination connection to 127.0.0.1:8080
intended service runs on C:8080, not F
trace: tunnel established; F loopback connection refused
owned service on F:9090 answers its marker in a separate allowed control
```

**First approach and failure.** Treating an established tunnel as a path to C's loopback service confused the host that resolves/opens the destination.

**Revised approach.** Identify F as the destination socket origin. Choose an already permitted destination reachable from F or correct the direction if authorized and needed.

**Independent controls.** The F:9090 marker validates forwarding without claiming the original service is reachable. A local listening socket alone is not end-to-end proof.

**Completed result and limits.** The first failing network edge is diagnosed. No new route, target access, UDP support or remote service authority is inferred.
