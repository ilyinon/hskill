# Worked case: the copy changes one target prototype, not every object

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied object-copy observation.

```text
parsed input has an own __proto__ key with object value {case: owned}
copy trace: Object.assign({}, input) invokes target prototype setter
result.case=owned; result has no own case key
unrelated fresh {} has no case property
no security-sensitive consumer supplied
```

**First approach and failure.** Calling the parsed JSON alone global Object.prototype pollution overstated both the write mechanism and its scope.

**Revised approach.** Trace the copy operation and compare target inheritance with the unrelated object. The demonstrated change is the copied target prototype, not all objects.

**Independent controls.** Check own-property descriptors and target prototype identity; use an isolated instance and discard it after the comparison.

**Completed result and limits.** A target-prototype mutation is supported under the supplied trace. Global pollution and gadget/RCE effects require additional evidence.
