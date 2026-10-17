# Worked case: the small exponent wraps, but a second modulus reveals a shared factor

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Recover the integer message in a complete tiny textbook-RSA lab.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Taking the ordinary cube root of23 does not yield an integer plaintext; small e alone does not establish m^e<n.

**Revised approach.** Compute gcd(55,85)=5, so p=5,q=11. phi=40, d=27, and 23^27 mod55=12. Verify 12^3 mod55=23 and 12 mod5=2.

**Independent controls.** Check p*q=55, e*d mod40=1 and the original ciphertext equation independently. Do not report an approximate root as decrypted bytes.

**Completed result and limits.** The supplied lab integer is12. This is a tiny raw-RSA example, not evidence against modern padded implementations or any deployed key.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_raw_rsa_shared_factor_and_original_equation`. This is not a product/runtime exploit test.
