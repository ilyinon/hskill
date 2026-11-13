# container-escape-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Namespace and privilege context | Record UID mapping, effective capabilities, mounts, runtime/kernel and control policy. |
| Host resource evidence | Identify the exact host-side object or authority the container could reach. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| id shows UID 0 | Container root or host-root mapping | Compare namespace/user mappings and the actual host operation. |
| Host-like path is mounted | Read-only data, scoped bind, or writable host control | Inspect mount flags and independently attributed resource access. |

## Interpret failure and finish the task

A denied syscall needs its errno and policy context; a helper crash is not an escape result. Historical cgroup/runtime recipes require the exact missing prerequisites.

Track `container principal -> namespace/mount/capability prerequisite -> host resource -> observed host-side effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review workload isolation

Inspect the rendered workload spec for host namespaces, host paths, runtime sockets, privileged mode, and added capabilities. Remove host-control mounts, restrict capabilities, and check that the expected seccomp policy and non-root settings apply to the running workload. In Kubernetes, review exceptions against the Restricted Pod Security Standard and verify admission with a permitted workload and a policy-rejected manifest in dry run. [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
