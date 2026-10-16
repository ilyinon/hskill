# classical-cipher-analysis technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 10. DECISION TREE

```
Unknown ciphertext — how to identify and break?
│
├─ Step 1: Check encoding
│  ├─ Base64 alphabet with padding? → Decode first, then re-analyze
│  ├─ Hex string? → Convert to bytes, re-analyze
│  ├─ Binary (01)? → Convert to ASCII
│  ├─ Morse (.-/)? → Decode Morse
│  └─ Printable text? → Continue to Step 2
│
├─ Step 2: Character set
│  ├─ Only letters (A-Z)?
│  │  ├─ Compute IC
│  │  │  ├─ IC ≈ 0.065 → Monoalphabetic
│  │  │  │  ├─ Uniform shift in freq? → Caesar → brute force 25
│  │  │  │  ├─ Random-looking mapping? → Simple substitution → frequency analysis
│  │  │  │  └─ Digraph patterns? → Playfair → digraph analysis
│  │  │  │
│  │  │  ├─ IC ≈ 0.04-0.05 → Polyalphabetic
│  │  │  │  ├─ Kasiski → find key length
│  │  │  │  └─ Per-position frequency → crack Vigenere
│  │  │  │
│  │  │  └─ IC ≈ 0.038 → Very long key or one-time pad
│  │  │     └─ Look for key reuse or weak key generation
│  │  │
│  │  └─ Letters appear scrambled (right freq, wrong order)?
│  │     └─ Transposition
│  │        ├─ Rail fence → brute force rail count
│  │        └─ Columnar → try common key lengths
│  │
│  ├─ Numbers (digit pairs)?
│  │  ├─ Pairs in range 11-55 → Polybius square
│  │  └─ Numbers mod 26 → numeric substitution
│  │
│  ├─ Mixed case with pattern?
│  │  └─ Upper/lower encodes binary → Bacon cipher
│  │
│  └─ Non-printable bytes?
│     └─ XOR cipher
│        ├─ Single-byte key → brute force 256
│        ├─ Repeating key → xortool / Hamming distance
│        └─ Known plaintext → direct key recovery
│
└─ Step 3: Apply specific attack
   ├─ Substitution → quipqiup.com / frequency analysis
   ├─ Caesar → dcode.fr / brute force
   ├─ Vigenere → Kasiski + per-column Caesar
   ├─ Affine → brute force 312 combinations
   ├─ Hill → known-plaintext matrix attack
   ├─ Transposition → pattern analysis + brute force
   └─ XOR → xortool / crib dragging
```

---

## 11. TOOLS

| Tool | Purpose | URL/Usage |
|---|---|---|
| **CyberChef** | Universal encoding/cipher Swiss army knife | gchq.github.io/CyberChef |
| **dcode.fr** | 200+ cipher solvers online | dcode.fr |
| **quipqiup** | Automated substitution cipher solver | quipqiup.com |
| **xortool** | XOR cipher analysis and cracking | `pip install xortool` |
| **RsaCtfTool** | RSA + some classical cipher support | GitHub |
| **Ciphey** | Automated cipher detection and decryption | `pip install ciphey` |
| **hashID** | Identify hash types | `pip install hashid` |
| **Python** | Custom frequency analysis and scripting | All attacks above |

### CyberChef Recipes (Common)

```
ROT13:               ROT13
Caesar brute force:   ROT13 (with offset slider)
Base64 decode:        From Base64
Hex decode:           From Hex
XOR:                  XOR (key as hex/utf8)
Vigenere:             Vigenère Decode
Morse:                From Morse Code
```
