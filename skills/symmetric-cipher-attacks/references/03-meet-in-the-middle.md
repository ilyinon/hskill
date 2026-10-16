# symmetric-cipher-attacks technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. MEET-IN-THE-MIDDLE

### 5.1 Double Encryption Attack

```
Double encryption: C = E_K2(E_K1(P))
Brute force: 2^(2n) expected
MITM:        2^(n+1) + storage for 2^n entries

Attack:
1. Encrypt P with all possible K1 → store (E_K1(P), K1) in table
2. Decrypt C with all possible K2 → check if D_K2(C) matches any entry
3. Match found → (K1, K2) recovered
```

```python
from itertools import product

def meet_in_the_middle(encrypt, decrypt, plaintext, ciphertext, keyspace_bits):
    """MITM attack on double encryption."""
    # Phase 1: build encryption table
    enc_table = {}
    for k1 in range(2**keyspace_bits):
        intermediate = encrypt(plaintext, k1)
        enc_table[intermediate] = k1

    # Phase 2: decrypt and look up
    for k2 in range(2**keyspace_bits):
        intermediate = decrypt(ciphertext, k2)
        if intermediate in enc_table:
            k1 = enc_table[intermediate]
            return k1, k2

    return None
```

---

## 6. DECISION TREE

```
Symmetric cipher challenge — what can you observe?
│
├─ Can you detect the mode?
│  ├─ Repeated input → repeated output blocks?
│  │  └─ Yes → ECB mode
│  │     ├─ Can control prefix → byte-at-a-time decryption
│  │     ├─ Can reorder blocks → cut-and-paste
│  │     └─ Can detect block boundaries → block alignment oracle
│  │
│  ├─ Error message differs for bad padding?
│  │  └─ Yes → Padding oracle (CBC)
│  │     └─ PadBuster or custom script
│  │
│  └─ Can modify ciphertext and observe effect?
│     └─ Next-block plaintext changes → CBC bit flipping
│
├─ Stream cipher or XOR?
│  ├─ Key reused on different messages?
│  │  └─ XOR ciphertexts → crib drag
│  │
│  ├─ Known plaintext-ciphertext pair?
│  │  └─ Recover keystream directly
│  │
│  ├─ Single-byte XOR key?
│  │  └─ Brute force 256 keys with frequency analysis
│  │
│  ├─ Repeating-key XOR?
│  │  └─ Hamming distance → key length → per-position crack
│  │
│  └─ LFSR-based?
│     └─ Berlekamp-Massey for state/polynomial recovery
│
├─ PRNG-based cipher?
│  ├─ LCG → truncated output lattice attack
│  ├─ Mersenne Twister → 624 outputs → full state recovery
│  └─ Custom PRNG → analyze period and state size
│
├─ Double / triple encryption?
│  └─ Meet-in-the-middle
│
└─ RC4 specifically?
   ├─ Single encryption → initial byte bias
   ├─ Many encryptions same key → statistical attack
   └─ IV prepended to key → FMS attack (WEP-like)
```

---

## 7. TOOLS

| Tool | Purpose |
|---|---|
| **PadBuster** | Automated padding oracle exploitation |
| **xortool** | Repeating-key XOR analysis (key length detection + cracking) |
| **CyberChef** | Quick XOR, encoding, block cipher operations |
| **SageMath** | LFSR/LCG analysis, lattice-based recovery |
| **pycryptodome** | AES/DES implementation for testing |
| **hashcat** | Brute force symmetric keys (GPU-accelerated) |
| **Custom Python** | All attacks above implementable in pure Python |
