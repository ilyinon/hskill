# Worked case: a sibling directory passes a textual root-prefix check

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Audit a supplied file-root guard using an owned marker.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Checking the prefix without a path-component boundary accepts the sibling directory.

**Revised approach.** Compare canonical ancestry: export-old is not a child of export. Constrain the actual opened resource to the intended root using the platform appropriate canonical/handle-based design.

**Independent controls.** /srv/export/inside.txt remains readable; the sibling marker must deny; a genuinely missing in-root file remains a lookup failure rather than a policy proof.

**Completed result and limits.** A root-containment file-read flaw is supported by the supplied path model. Symlink races, OS-specific APIs, includes and execution remain untested.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_canonical_path_components_not_text_prefix`. This is not a product/runtime exploit test.
