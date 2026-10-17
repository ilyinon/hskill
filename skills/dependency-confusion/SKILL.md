---
name: dependency-confusion
description: >-
  Supply-chain testing via package-manager dependency confusion: when internal package names resolve to attacker-controlled public registries, leading to malicious install and script execution. Use for npm/pip/gem/Maven/Composer/Docker manifest review and authorized red-team supply-chain exercises.
---

# Dependency Confusion

## Working approach

- Identify ecosystem, package name, registry routing, constraints, lockfiles, and resolver behavior
- Distinguish namespace exposure from actual public-package selection
- Reproduce resolution with inert fixtures in a private local registry setup.

## Evidence and limits

The resolver selects an unintended source for the protected dependency under the target configuration.

A public name or higher version alone is insufficient; scoped registries, pinning, lockfiles, and version ranges matter, and publishing is a separate authorized action.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. CORE CONCEPT; 2. AFFECTED ECOSYSTEMS; 3. RECONNAISSANCE; 4. EXPLOITATION; 5. TOOLS | [Read](./references/01-quick-start.md) |
| 6. DEFENSE; 7. DECISION TREE | [Read](./references/02-defense.md) |
