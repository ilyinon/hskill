# classical-cipher-analysis technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. HILL CIPHER

Matrix-based cipher: `C = K · P mod 26` where K is an n×n key matrix.

### 6.1 Known-Plaintext Attack

```python
import numpy as np

def crack_hill(known_plain, known_cipher, n=2):
    """Recover Hill cipher key from known plaintext-ciphertext (mod 26)."""
    # Convert to numbers
    P = [ord(c) - ord('A') for c in known_plain.upper()]
    C = [ord(c) - ord('A') for c in known_cipher.upper()]

    # Build matrices (need at least n pairs of n-grams)
    P_matrix = np.array(P[:n*n]).reshape(n, n).T
    C_matrix = np.array(C[:n*n]).reshape(n, n).T

    # K = C · P⁻¹ mod 26
    # Need modular matrix inverse
    from sympy import Matrix
    P_mat = Matrix(P_matrix.tolist())
    C_mat = Matrix(C_matrix.tolist())

    P_inv = P_mat.inv_mod(26)
    K = (C_mat * P_inv) % 26

    return K
```

---

## 7. TRANSPOSITION CIPHERS

### 7.1 Rail Fence

```python
def rail_fence_decrypt(ciphertext, rails):
    """Decrypt rail fence cipher."""
    n = len(ciphertext)
    # Build the zigzag pattern
    pattern = []
    for i in range(n):
        row = 0
        cycle = 2 * (rails - 1)
        pos = i % cycle
        row = pos if pos < rails else cycle - pos
        pattern.append((row, i))

    pattern.sort()

    # Fill in characters
    result = [''] * n
    ci = 0
    for _, orig_pos in pattern:
        result[orig_pos] = ciphertext[ci]
        ci += 1

    return ''.join(result)

# Brute force all rail counts
for rails in range(2, 20):
    print(f"Rails {rails}: {rail_fence_decrypt(ct, rails)[:50]}")
```

### 7.2 Columnar Transposition

```python
def columnar_decrypt(ciphertext, key):
    """Decrypt columnar transposition given key word."""
    n_cols = len(key)
    n_rows = -(-len(ciphertext) // n_cols)  # ceiling division

    # Determine column order from key
    order = sorted(range(n_cols), key=lambda i: key[i])

    # Calculate column lengths (some may be shorter)
    full_cols = len(ciphertext) % n_cols
    if full_cols == 0:
        full_cols = n_cols

    # Split ciphertext into columns (in key order)
    columns = [''] * n_cols
    pos = 0
    for col_idx in order:
        col_len = n_rows if col_idx < full_cols else n_rows - 1
        columns[col_idx] = ciphertext[pos:pos + col_len]
        pos += col_len

    # Read off row by row
    plaintext = ''
    for row in range(n_rows):
        for col in range(n_cols):
            if row < len(columns[col]):
                plaintext += columns[col][row]

    return plaintext
```

---

## 8. XOR CIPHER

### 8.1 Single-Byte XOR

See [symmetric-cipher-attacks](../../symmetric-cipher-attacks/SKILL.md) Section 4.2 for full implementation.

### 8.2 Multi-Byte XOR (xortool)

```bash
# Automatic key length detection and cracking
xortool ciphertext.bin -l 5        # try key length 5
xortool ciphertext.bin -b          # brute force key length
xortool ciphertext.bin -c 20       # assume most common char is space (0x20)
```

### 8.3 Known Plaintext XOR

```python
def xor_known_plaintext(ciphertext, known_plain, offset=0):
    """Recover XOR key from known plaintext at given offset."""
    key_fragment = bytes(
        c ^ p for c, p in zip(ciphertext[offset:], known_plain)
    )
    print(f"Key fragment: {key_fragment}")

    # If repeating key, infer full key from fragment
    return key_fragment
```

---

## 9. SPECIAL CIPHERS

### 9.1 Bacon Cipher

Binary encoding using two typefaces (A=normal, B=bold/italic).

```python
BACON = {
    'AAAAA': 'A', 'AAAAB': 'B', 'AAABA': 'C', 'AAABB': 'D',
    'AABAA': 'E', 'AABAB': 'F', 'AABBA': 'G', 'AABBB': 'H',
    'ABAAA': 'I', 'ABAAB': 'J', 'ABABA': 'K', 'ABABB': 'L',
    'ABBAA': 'M', 'ABBAB': 'N', 'ABBBA': 'O', 'ABBBB': 'P',
    'BAAAA': 'Q', 'BAAAB': 'R', 'BAABA': 'S', 'BAABB': 'T',
    'BABAA': 'U', 'BABAB': 'V', 'BABBA': 'W', 'BABBB': 'X',
    'BAAAA': 'Y', 'BAAAB': 'Z',
}

def decode_bacon(text):
    """Decode Bacon cipher: uppercase=B, lowercase=A (or similar mapping)."""
    binary = ''.join('B' if c.isupper() else 'A' for c in text if c.isalpha())
    result = ''
    for i in range(0, len(binary) - 4, 5):
        chunk = binary[i:i+5]
        result += BACON.get(chunk, '?')
    return result
```

### 9.2 Polybius Square

```
    1 2 3 4 5
  ┌──────────
1 │ A B C D E
2 │ F G H I/J K
3 │ L M N O P
4 │ Q R S T U
5 │ V W X Y Z

"HELLO" = "23 15 31 31 34"
```

### 9.3 Playfair

5×5 grid cipher encrypting digraphs.

```
Key: "MONARCHY" → grid:
  M O N A R
  C H Y B D
  E F G I/J K
  L P Q S T
  U V W X Z

Rules:
  Same row → shift right: HE → FE → "GF"
  Same col → shift down
  Rectangle → swap columns
```

---

