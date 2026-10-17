# Worked case: an inherited ACE applies only to a different object class

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Determine whether the supplied permission path applies to the selected target.

```text
teaching ACL contract: ACE applies only to descendants of class=group
principal test-a is in delegated-team
candidate target server-1 has class=computer
ACE is visible as inherited metadata but class filter does not match
no other allow ACE or ownership path supplied
```

**First approach and failure.** Treating the graph label as an unqualified right on server-1 skipped the inherited object-class filter.

**Revised approach.** Evaluate the effective ACE against the actual computer object. This edge cannot authorize the proposed operation in the supplied model.

**Independent controls.** A descendant group object is the matching positive control under this contract; inspect denial and inherited scope without modifying directory state.

**Completed result and limits.** The proposed computer-object path is unsupported. This is a bounded ACL interpretation, not a full AD access-check emulator or live directory test.
