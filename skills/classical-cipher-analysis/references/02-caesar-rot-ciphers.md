# classical-cipher-analysis technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 3. CAESAR / ROT CIPHERS

### 3.1 Brute Force

```python
def caesar_bruteforce(ciphertext):
    """Try all 25 shifts, score by English frequency."""
    results = []
    for shift in range(26):
        decrypted = ""
        for c in ciphertext:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                decrypted += chr((ord(c) - base - shift) % 26 + base)
            else:
                decrypted += c

        # Chi-squared scoring against English frequency
        score = chi_squared_score(decrypted)
        results.append((shift, score, decrypted))

    results.sort(key=lambda x: x[1])
    return results[0]  # best match

def chi_squared_score(text):
    """Lower score = closer to English."""
    expected = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
        'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
        'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
        'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
        'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2, 'Q': 0.1, 'Z': 0.1,
    }
    text = text.upper()
    letters = [c for c in text if c.isalpha()]
    total = len(letters)
    if total == 0:
        return float('inf')

    freq = Counter(letters)
    score = sum(
        (freq.get(c, 0) / total * 100 - expected.get(c, 0)) ** 2 / max(expected.get(c, 0.1), 0.1)
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )
    return score
```

### 3.2 ROT13 and ROT47

```python
import codecs

# ROT13 (letters only)
rot13 = codecs.decode(ciphertext, 'rot_13')

# ROT47 (ASCII 33-126)
def rot47(text):
    return ''.join(
        chr(33 + (ord(c) - 33 + 47) % 94) if 33 <= ord(c) <= 126 else c
        for c in text
    )
```

---

## 4. VIGENERE CIPHER

### 4.1 Full Attack Workflow

```
Step 1: Confirm polyalphabetic (IC ≈ 0.04-0.05)
Step 2: Find key length (Kasiski + IC per period)
Step 3: For each key position, solve as single Caesar cipher
Step 4: Assemble key → decrypt
```

### 4.2 IC-Based Key Length Detection

```python
def find_vigenere_key_length(ciphertext, max_key=20):
    """Use IC to find Vigenere key length."""
    text = [c for c in ciphertext.upper() if c.isalpha()]
    results = []

    for kl in range(1, max_key + 1):
        # Split text into kl columns
        columns = [[] for _ in range(kl)]
        for i, c in enumerate(text):
            columns[i % kl].append(c)

        # Average IC across columns
        avg_ic = sum(
            index_of_coincidence(''.join(col)) for col in columns
        ) / kl

        results.append((kl, avg_ic))
        print(f"  Key length {kl:2d}: IC = {avg_ic:.4f}")

    # Key length with IC closest to 0.065
    best = max(results, key=lambda x: x[1])
    return best[0]
```

### 4.3 Per-Position Frequency Attack

```python
def crack_vigenere(ciphertext, key_length):
    """Crack Vigenere given known key length."""
    text = [c for c in ciphertext.upper() if c.isalpha()]
    key = ""

    for pos in range(key_length):
        column = ''.join(text[i] for i in range(pos, len(text), key_length))
        # Solve as Caesar cipher
        shift, score, _ = caesar_bruteforce(column)
        key += chr(shift + ord('A'))

    # Decrypt
    plaintext = ""
    ki = 0
    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[ki % key_length]) - ord('A')
            base = ord('A') if c.isupper() else ord('a')
            plaintext += chr((ord(c) - base - shift) % 26 + base)
            ki += 1
        else:
            plaintext += c

    return key, plaintext
```

---

## 5. AFFINE CIPHER

### 5.1 Definition

`E(x) = (a·x + b) mod 26` where gcd(a, 26) = 1.

Valid a values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25 (12 values).

### 5.2 Brute Force (312 combinations)

```python
def crack_affine(ciphertext):
    """Brute force affine cipher: 12 × 26 = 312 combinations."""
    valid_a = [a for a in range(1, 26) if gcd(a, 26) == 1]

    for a in valid_a:
        a_inv = pow(a, -1, 26)
        for b in range(26):
            plaintext = ""
            for c in ciphertext.upper():
                if c.isalpha():
                    y = ord(c) - ord('A')
                    x = (a_inv * (y - b)) % 26
                    plaintext += chr(x + ord('A'))
                else:
                    plaintext += c

            score = chi_squared_score(plaintext)
            if score < 50:  # reasonable English
                print(f"a={a}, b={b}: {plaintext[:50]}...")
```

### 5.3 Known Plaintext

```python
def affine_from_known(plain1, cipher1, plain2, cipher2):
    """Recover (a, b) from two known plaintext-ciphertext pairs."""
    p1, c1 = ord(plain1) - ord('A'), ord(cipher1) - ord('A')
    p2, c2 = ord(plain2) - ord('A'), ord(cipher2) - ord('A')

    # c1 = a*p1 + b, c2 = a*p2 + b
    # c1 - c2 = a*(p1 - p2) mod 26
    diff_p = (p1 - p2) % 26
    diff_c = (c1 - c2) % 26

    if gcd(diff_p, 26) != 1:
        return None

    a = (diff_c * pow(diff_p, -1, 26)) % 26
    b = (c1 - a * p1) % 26
    return a, b
```

---

