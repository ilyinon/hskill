---
name: unauthorized-access-common-services
description: >-
  Unauthorized access playbook for common exposed services. Use when Redis, Rsync, PHP-FPM, AJP/Ghostcat, Hadoop YARN, H2 Console, or similar management interfaces are exposed without authentication.
---

# Unauthorized Access Common Services

## Working approach

- Identify the service, version, exposure, identity, and effective permissions
- Select its specific read-only protocol check
- Separate unauthenticated reachability from sensitive read/write/administrative capability before considering a permitted follow-on.

## Evidence and limits

The unchanged unauthenticated or low-privilege principal obtains a protected service capability contrary to policy.

An open port, banner, PONG, or management UI alone does not establish every command or RCE; ACLs, filesystem access, modules, and version restrictions matter.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. DISCOVERY — PORT SCANNING; 2. REDIS (PORT 6379); 3. RSYNC (PORT 873); 4. PHP-FPM / FASTCGI (PORT 9000); 5. GHOSTCAT — AJP (PORT 8009) — CVE-2020-1938 | [Read](./references/01-discovery-port-scanning.md) |
| 6. HADOOP YARN RESOURCEMANAGER (PORT 8088); 7. H2 DATABASE CONSOLE; 8. QUICK REFERENCE; 9. REVERSE PROXY MISCONFIGURATION | [Read](./references/02-hadoop-yarn-resourcemanager-port-8088.md) |
| Advanced: PORT / SERVICE EXPLOITATION MATRIX | [Read](./PORT_SERVICE_MATRIX.md) |
