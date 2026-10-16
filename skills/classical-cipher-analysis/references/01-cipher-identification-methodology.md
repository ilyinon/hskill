For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Classical Cipher Analysis — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert classical cipher identification and breaking techniques for CTF. Covers cipher identification methodology (frequency analysis, IC, Kasiski), monoalphabetic substitution, Caesar/ROT, Vigenere, Enigma, affine, Hill, transposition ciphers, Bacon/Polybius/Playfair, and XOR ciphers. Base models often skip the identification step and jump to the wrong cipher type, or fail to recognize encoded (base64/hex) ciphertext that needs decoding before analysis.

## 0. RELATED ROUTING

- [symmetric-cipher-attacks](../../symmetric-cipher-attacks/SKILL.md) when dealing with modern symmetric ciphers (AES/DES) rather than classical
- [hash-attack-techniques](../../hash-attack-techniques/SKILL.md) when the challenge involves hash-based constructions
- [lattice-crypto-attacks](../../lattice-crypto-attacks/SKILL.md) when knapsack-based ciphers are encountered

### Quick identification guide

| Observation | Likely Cipher | First Action |
|---|---|---|
| All uppercase letters, uneven frequency | Monoalphabetic substitution | Frequency analysis |
| All uppercase, flat frequency distribution | Polyalphabetic (Vigenere) | IC + Kasiski |
| Only A-Z shifted uniformly | Caesar/ROT | Brute force 25 shifts |
| Base64 alphabet (A-Za-z0-9+/=) | Base64 encoded (decode first) | Base64 decode |
| Hex string (0-9a-f) | Hex encoded (decode first) | Hex decode |
| Binary (0s and 1s) | Binary encoded | Convert to ASCII |
| Dots and dashes | Morse code | Morse decode |
| Raised/normal text pattern | Bacon cipher | Map to A/B, decode |
| 2-digit number pairs (11-55) | Polybius square | Grid lookup |
| Text appears scrambled (right letters, wrong order) | Transposition | Anagram analysis |
| Non-printable bytes XOR-like | XOR cipher | Single/repeating key XOR analysis |

---

## 1. CIPHER IDENTIFICATION METHODOLOGY

### 1.1 Step 1: Character Set Analysis

```python
def analyze_charset(ciphertext):
    """Identify encoding/cipher by character set."""
    chars = set(ciphertext.strip())

    if chars <= set('01 \n'):
        return "Binary encoding"
    if chars <= set('.-/ \n'):
        return "Morse code"
    if chars <= set('0123456789abcdef \n'):
        return "Hex encoding"
    if chars <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n'):
        if '=' in ciphertext or len(ciphertext) % 4 == 0:
            return "Base64 encoding"
    if chars <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZ \n'):
        return "Uppercase only — classical cipher"
    if all(c in '12345' for c in ciphertext.replace(' ', '').replace('\n', '')):
        return "Polybius square (digits 1-5)"

    return "Mixed charset — needs further analysis"
```

### 1.2 Step 2: Frequency Analysis

```python
from collections import Counter

def frequency_analysis(text):
    """Compute letter frequency distribution."""
    text = text.upper()
    letters = [c for c in text if c.isalpha()]
    total = len(letters)
    freq = Counter(letters)

    print("Letter frequencies:")
    for letter, count in freq.most_common():
        pct = count / total * 100
        bar = '#' * int(pct)
        print(f"  {letter}: {pct:5.1f}% {bar}")

    return freq

# English letter frequency (for comparison):
# E T A O I N S H R D L C U M W F G Y P B V K J X Q Z
# 12.7 9.1 8.2 7.5 7.0 6.7 6.3 6.1 6.0 4.3 4.0 2.8 ...
```

### 1.3 Step 3: Index of Coincidence (IC)

```python
def index_of_coincidence(text):
    """
    IC ≈ 0.065 → English / monoalphabetic substitution
    IC ≈ 0.038 → random / polyalphabetic cipher
    """
    text = [c for c in text.upper() if c.isalpha()]
    N = len(text)
    freq = Counter(text)

    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

# Interpretation:
# IC > 0.060 → monoalphabetic (Caesar, simple substitution, Playfair)
# IC ≈ 0.045-0.055 → polyalphabetic with short key (Vigenere key < 10)
# IC ≈ 0.038-0.042 → polyalphabetic with long key or random
```

### 1.4 Step 4: Kasiski Examination (for Polyalphabetic)

```python
from math import gcd
from functools import reduce

def kasiski(ciphertext, min_len=3):
    """Find repeated sequences and their distances → key length."""
    text = ''.join(c for c in ciphertext.upper() if c.isalpha())
    distances = []

    for length in range(min_len, min(20, len(text) // 3)):
        for i in range(len(text) - length):
            seq = text[i:i+length]
            j = text.find(seq, i + 1)
            while j != -1:
                distances.append(j - i)
                j = text.find(seq, j + 1)

    if not distances:
        return None

    # Key length is likely GCD of common distances
    common_gcds = Counter()
    for d in distances:
        for factor in range(2, min(d + 1, 30)):
            if d % factor == 0:
                common_gcds[factor] += 1

    print("Likely key lengths (by frequency):")
    for length, count in common_gcds.most_common(5):
        print(f"  Key length {length}: {count} occurrences")

    return common_gcds.most_common(1)[0][0]
```

---

## 2. MONOALPHABETIC SUBSTITUTION

### 2.1 Frequency Analysis Attack

```python
def solve_substitution(ciphertext, interactive=False):
    """Solve monoalphabetic substitution via frequency analysis."""
    freq = frequency_analysis(ciphertext)

    # English frequency order
    eng_order = "ETAOINSRHLDCUMWFGYPBVKJXQZ"
    cipher_order = ''.join(c for c, _ in freq.most_common())

    # Initial mapping (frequency-based guess)
    mapping = {}
    for i, c in enumerate(cipher_order):
        if i < len(eng_order):
            mapping[c] = eng_order[i]

    # Apply mapping
    result = ""
    for c in ciphertext.upper():
        result += mapping.get(c, c)

    return result, mapping

# Better approach: use automated solvers
# quipqiup.com — online substitution solver
# dcode.fr/monoalphabetic-substitution — with word pattern matching
```

### 2.2 Known Plaintext (Crib Dragging)

If part of the plaintext is known (e.g., "flag{" prefix):

```python
def crib_drag_substitution(ciphertext, known_plain, known_cipher):
    """Build partial mapping from known plaintext-ciphertext pair."""
    mapping = {}
    for p, c in zip(known_plain.upper(), known_cipher.upper()):
        mapping[c] = p

    # Apply partial mapping
    result = ""
    for c in ciphertext.upper():
        result += mapping.get(c, '?')

    return result, mapping
```

---

