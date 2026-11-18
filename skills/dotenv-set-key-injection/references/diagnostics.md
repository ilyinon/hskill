# .env audit: decisions from evidence

Trace `user field → writer → file → loader → effective configuration`. Record the
last supported step. Use [version and remediation](./legacy-playbook.md) for
the upstream fix and checks after mitigation.

| Observation | What to distinguish | Smallest useful check |
|---|---|---|
| Source writes user data to a configuration file | Deployment input or application-only storage | Trace the exact path and show which loader, if any, reads that file. |
| The lockfile lists a fixed release | Fixed dependency in use or a different deployed copy | Compare the installed or vendored package with the lockfile and inspect the actual writer. |
| Parsed settings differ from process settings | Existing environment value, no reload, or a different file | Compare the loader inputs and the effective value of the same harmless setting in two clean runs. |
| Parent and helper read different settings | Filtered child environment or a separate settings reader | Inspect the launch configuration and compare the allowed setting names at that boundary. |
| The preference still works after the redesign | Separation is effective or both stores are still written | Confirm that the preference is saved and the deployment configuration stays unchanged. |

A file change does not establish that a loader used it. A parsed key does not
establish process behavior. Do not infer child or production impact from a
configuration-only check.
