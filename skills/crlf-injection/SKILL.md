---
name: crlf-injection
description: >-
  CRLF injection playbook. Use when user input reaches HTTP response headers, Location redirects, Set-Cookie values, or log files where carriage-return/line-feed characters can split or inject content.
---

# CRLF injection

## Working approach

Trace representation changes into actual wire bytes or log records; verify which downstream parser accepts a new boundary.

## Evidence and limits

A separately parsed benign header/message/log marker establishes only that boundary. Session fixation, shared-cache effects and script execution need their own evidence.

## References

- For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md).
- For a complete change of approach and independent controls, read the [worked case](./references/worked-cases.md).
- For matching recipes, tools and detailed variants, read the relevant section of the [technical playbook](./references/legacy-playbook.md). Establish its actual parser, runtime or workflow prerequisites first.
