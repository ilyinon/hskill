---
name: dotenv-set-key-injection
description: Audit Python applications that write user data to .env files or load those files into runtime environments. Check the installed python-dotenv version, configuration boundaries, and remediation.
---

# Audit .env write and load boundaries

1. Trace the supplied source from user-controlled input to the writer, exact file, loader, and process that receives the configuration. Record the installed version, write mode, and reload behavior.
2. The upstream [python-dotenv 1.2.3 release](https://github.com/theskumar/python-dotenv/releases/tag/v1.2.3) fixes the specific `set_key` backslash round-trip issue. Check the deployed copy and configuration before attributing a finding or calling it fixed.
3. Keep user preferences in application storage. Keep deployment configuration separate, and pass only required variables to child processes. Validate changes with benign settings in an isolated environment.

A configuration write, a parsed setting, and a process receiving that setting are separate observations. Report the last supported step and mark downstream impact unverified.

## References

- [Version and remediation](./references/legacy-playbook.md) for update and regression checks.
- [Diagnostics](./references/diagnostics.md) when a write, reload, or environment boundary is unclear.
- [Worked case](./references/worked-cases.md) for environment precedence and evidence limits.
