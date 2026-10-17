---
name: insecure-source-code-management
description: >-
  Source control and artifact exposure (.git, .svn, .hg, backups, .env). Use when recon finds VCS paths, 403 on hidden dirs, or backup/config leaks during authorized testing.
---

# Source-control artifact exposure

## Working approach

Compare returned artifact bytes with a nonexistent-path control. Recover only the required in-scope material and inspect reconstructed content as untrusted data.

## Evidence and limits

Status codes alone do not prove a repository. Keep authentic metadata, source reconstruction, sensitive exposure and live credential validity as separate claims.

## References

- For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md).
- For a complete change of approach and independent controls, read the [worked case](./references/worked-cases.md).
- For matching recipes, tools and detailed variants, read the relevant section of the [technical playbook](./references/legacy-playbook.md). Establish its actual parser, runtime or workflow prerequisites first.
