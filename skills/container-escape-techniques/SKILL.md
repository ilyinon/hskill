---
name: container-escape-techniques
description: >-
  Container escape playbook. Use when operating inside a Docker container, LXC, or Kubernetes pod and need to escape to the host via privileged mode, capabilities, Docker socket, cgroup abuse, namespace tricks, or runtime vulnerabilities.
---

# Container Escape Techniques

## Working approach

- Record runtime/kernel version, namespaces, cgroup mode, mounts, capabilities, seccomp, and security modules
- Identify the exact host resource or privilege exposed
- Verify boundary crossing using minimal permitted host-side evidence.

## Evidence and limits

Access exceeds the container's intended namespace, filesystem, or host-control boundary.

UID 0 in a container, a mounted path, or a named capability alone is not host root; historical release_agent and runtime chains require exact conditions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. AM I IN A CONTAINER?; 2. PRIVILEGED CONTAINER ESCAPE; 3. CAPABILITY-BASED ESCAPE; 4. DOCKER SOCKET ESCAPE (/var/run/docker.sock); 5. CGROUP V1 RELEASE_AGENT ESCAPE; 6. CGROUP V2 / eBPF ESCAPE; 7. NAMESPACE ESCAPE | [Read](./references/01-am-i-in-a-container.md) |
| 8. RUNTIME VULNERABILITIES; 9. KUBERNETES POD ESCAPE; 10. TOOLS; 11. CONTAINER ESCAPE DECISION TREE | [Read](./references/02-runtime-vulnerabilities.md) |
| Advanced: Docker Escape Chains & Kubernetes Escape Paths | [Read](./DOCKER_ESCAPE_CHAINS.md) |
