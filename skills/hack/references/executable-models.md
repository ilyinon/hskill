# Make a fragile reasoning step executable

Use for arithmetic, state transitions, ordering, or constraints whose manual
derivation is error-prone. Model the smallest mechanism that changes the answer,
using reviewed local code or a suitable available solver. Ordinary clear cases
do not need a model.

Record inputs, state, transition rule, desired invariant, and excluded behavior.
Keep integer widths, encoding, resets, identity and timing assumptions explicit.
Before using model predictions, replay an observed or supplied case and a
discriminating control. A mismatch means the abstraction or input mapping needs
repair; do not tune expected outputs merely to pass.

The self-contained [ledger model](../scripts/hack_ledger_model.py) illustrates
delivery versus operation identity on a fresh synthetic ledger. It supports three
explicit policies and checks at-most-once credit **per operation**. Run from this
skill's directory with the [example data](../assets/ledger-example.json):

```sh
python3 scripts/hack_ledger_model.py --input assets/ledger-example.json
```

Exit 0 means the named invariant holds in that trial; 1 means a model violation;
2 means invalid input and no trial. The example deliberately returns 1. This is
data-only simulation; no callbacks or payment provider are invoked. The model is
also the canonical implementation used by the repository's staged callback lab.

Compare the violating trace, a valid single operation, and multiple legitimate
operations. A policy that rejects everything can satisfy an upper-bound invariant
while failing the user's task. Check legitimate completion as a separate
obligation. Preserve the concrete counterexample and the invariant it violates.

Use [metamorphic checks](metamorphic-checks.md) to challenge generalization beyond
one example. For another system, supply its own observed transition rules: do
not transfer this ledger's semantics to a browser, concurrent process, or service.
Sequential enumeration cannot establish a real scheduler's behavior. A solver's
unsatisfiable result proves only the encoded constraints; check translation and
scope before promoting it to a system-level conclusion.

When reporting, distinguish raw observations, model assumptions, generated
predictions, and any separately verified system effect. Keep the input and model
version with the result so a later environment change can invalidate dependent
claims without erasing historical evidence.
