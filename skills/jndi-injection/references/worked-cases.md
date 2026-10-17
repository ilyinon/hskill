# Worked case: the naming request occurs but reconstruction is blocked

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound the conclusion from a supplied lookup trace.

```text
source permits caller-controlled naming lookup; policy allows only local names
owned test name -> outbound LDAP query attributed to application
returned reference -> factory blocked by configured filter
no local factory invocation or execution marker supplied
```

**First approach and failure.** Treating the LDAP callback as code execution skipped the explicitly blocked reconstruction step.

**Revised approach.** Report the supported outbound-lookup policy violation and locate the execution chain break. Restrict the naming source/provider as required by the local-only contract.

**Independent controls.** A permitted local-name lookup must remain valid; the external name should be rejected before lookup after repair. Do not silently reinterpret blocked reconstruction as successful execution.

**Completed result and limits.** A naming/destination-control finding is supported; RCE, credential exposure and arbitrary local class availability remain unproved.
