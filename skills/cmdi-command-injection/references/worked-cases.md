# Worked case: no shell, but a filename becomes an option

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Locate the violated input contract without executing a command.

```text
teaching utility contract: --summary is an option unless after --
caller passes argv=[reporter, user_filename], shell=false
user_filename=--summary -> summary mode, no file operand
policy: caller may choose a filename, never reporter mode
normal owned.txt -> file mode
```

**First approach and failure.** A semicolon probe remains one literal argv item; it does not test option interpretation.

**Revised approach.** Trace the utility grammar. End option parsing before the filename with a supported -- delimiter, or enforce the utility-specific safe operand interface.

**Independent controls.** Ordinary filename still selects its file; --summary in the operand position is treated as a filename or rejected by filename policy, never as a mode change.

**Completed result and limits.** Argument/option injection is supported under the supplied utility contract. Shell execution, file disclosure and real reporter behavior are not demonstrated.
