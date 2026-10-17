# Worked case: 95 percent accuracy is the majority baseline

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied membership-inference claim without querying a model.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Using raw accuracy alone calls the always-majority rule an inference success.

**Revised approach.** Compare the majority baseline: also95%. TPR=0/50=0; specificity=950/950=1; balanced accuracy=(0+1)/2=0.5.

**Independent controls.** Inspect the confusion matrix and an independently held-out, balanced evaluation if actual signal is claimed. The metric does not establish data provenance by itself.

**Completed result and limits.** This classifier shows no useful positive membership signal beyond the supplied baseline. General model privacy is not certified; no model or training data was accessed.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_membership_accuracy_against_majority_baseline`. This is not a product/runtime exploit test.
