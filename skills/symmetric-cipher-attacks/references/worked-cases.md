# Worked case: state recovered, generator installed at the wrong index

Synthetic CPython MT19937 task: [624 observations](./examples/input.json). Inverse helpers are in [Block Cipher Attacks](../BLOCK_CIPHER_ATTACKS.md), section 5. No network or cryptographic service is involved.

**Goal.** Predict the next three full 32-bit outputs after the observed window. The input states all 624 observations are consecutive `getrandbits(32)` words from one instance.

**First approach.** Untemper the words, then install them with index 0. The next generated word repeats the first observed word. This is evidence that the installation starts at the old window, not proof that inverse tempering failed.

**Revised approach.** Keep the recovered words and install a CPython version-3 state tuple with index 624. The next request advances the generator from the end of the recovered block. The supplied construction's continuation is `731620334, 2389502510, 1369359274`.

**Independent check.** `test_solving_examples.SolvingExamples.test_mt_state_index_and_withheld_continuation` first verifies the old-window symptom, then checks 20 future words against an independently advanced standard-library generator. It uses the reviewed inverse helpers rather than assuming a recovered list predicts automatically.

**Completed result.** Correct next-output prediction under the exact full-output/order/state-layout contract. No original seed is recovered. Truncated outputs, floats, gaps, mixed instances, and cryptographic RNGs require different reasoning. A real observation list cannot prove its own provenance; that premise must come from the task or independent evidence.
