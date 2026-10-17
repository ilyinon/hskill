# Worked case: a higher public version is outside the locked resolution

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess the supplied protected-package source decision without publishing or installing anything.

```text
teaching resolver contract: frozen lock selects exact name/version/source/integrity
lock: internal-widget 1.4, registry=private.example.invalid, hash=H1
public candidate: internal-widget 9.0, hash=H9
resolution trace: selected private 1.4/H1; missing locked artifact causes failure, no fallback
```

**First approach and failure.** Calling the version difference dependency confusion skipped the active frozen-lock contract.

**Revised approach.** Trace the protected package selection and fail-closed behavior. The public candidate is not eligible under this configuration.

**Independent controls.** Check the exact protected package rather than unrelated public dependencies. A failed private fetch must not silently switch sources in this contract.

**Completed result and limits.** No unintended selection is shown. This synthetic resolver trace does not certify a particular package-manager version; no package was published or lifecycle script executed.
