---
name: deserialization-insecure
description: >-
  Insecure deserialization playbook. Use when Java, PHP, or Python applications deserialize untrusted data via ObjectInputStream, unserialize, pickle, or similar mechanisms that may lead to RCE, file access, or privilege escalation.
---

# Deserialization Insecure

## Working approach

- Identify the actual wire format, decoder, runtime, dependency versions, and reachable entry
- Distinguish parsing from object instantiation and gadget invocation
- Use the smallest controlled side effect supported by the exact classpath/configuration.

## Evidence and limits

Untrusted serialized input reaches an unsafe reconstruction path and produces the claimed boundary violation.

Magic bytes, a parser error, or a gadget generator's output is not proof; gadget availability, allowlists, filters, and invocation context must match.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. TRAFFIC FINGERPRINTING — IS IT DESERIALIZATION?; 2. JAVA — GADGET CHAINS AND TOOLS | [Read](./references/01-traffic-fingerprinting-is-it-deserialization.md) |
| 3. PHP — unserialize AND PHAR; 4. PYTHON — PICKLE; 5. DETECTION METHODOLOGY; 6. DEFENSE AWARENESS; 7. QUICK REFERENCE — KEY PAYLOADS; 8. RUBY DESERIALIZATION | [Read](./references/02-php-unserialize-and-phar.md) |
| 9. .NET DESERIALIZATION; 10. NODE.JS DESERIALIZATION; RUBY DESERIALIZATION; .NET DESERIALIZATION | [Read](./references/03-net-deserialization.md) |
| NODE.JS DESERIALIZATION; 11. RUBY DESERIALIZATION; 12. .NET DESERIALIZATION; 13. NODE.JS DESERIALIZATION | [Read](./references/04-node-js-deserialization.md) |
| Advanced: Java Gadget Chains & Cross-Language Deserialization Deep Dive | [Read](./JAVA_GADGET_CHAINS.md) |
