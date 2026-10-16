# hash-attack-techniques technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 3. SHA-1 COLLISION

### 3.1 SHAttered Attack (2017)

First practical SHA-1 collision: two PDF files with same SHA-1.

- Complexity: ~2^63 SHA-1 computations
- Cost: ~$110K on GPU clusters (2017 prices)
- Tool: shattered.io provides the collision PDFs

### 3.2 SHA-1 Chosen-Prefix Collision (2020)

- Complexity: ~2^63.4 computations
- Practical for attacking PGP/GnuPG key servers
- Demonstrates SHA-1 is broken for collision resistance

### 3.3 Impact

```
SHA-1 should NOT be used for:
  ✗ Digital signatures
  ✗ Certificate fingerprints
  ✗ Git commit integrity (migration to SHA-256 in progress)
  ✗ Deduplication based on hash

SHA-1 is still OK for:
  ✓ HMAC-SHA1 (collision resistance not required)
  ✓ HKDF-SHA1 (PRF security suffices)
  ✓ Non-adversarial checksums
```

---

## 4. BIRTHDAY ATTACK

### 4.1 Generic Birthday Bound

```
For n-bit hash: expected collisions after ~2^(n/2) hashes

Hash     Bits    Birthday bound
MD5      128     2^64
SHA-1    160     2^80
SHA-256  256     2^128

CTF application: if hash is truncated to k bits,
collision in ~2^(k/2) attempts
```

### 4.2 Birthday Attack Implementation

```python
import hashlib
import os

def birthday_attack(hash_func, output_bits, max_attempts=2**28):
    """Find collision for truncated hash."""
    mask = (1 << output_bits) - 1
    seen = {}

    for _ in range(max_attempts):
        msg = os.urandom(16)
        h = int(hash_func(msg).hexdigest(), 16) & mask

        if h in seen and seen[h] != msg:
            return seen[h], msg  # collision!
        seen[h] = msg

    return None

# Example: find collision for first 32 bits of SHA-256
result = birthday_attack(hashlib.sha256, 32)
```

---

## 5. HMAC TIMING ATTACK

### 5.1 Vulnerable Comparison

```python
# VULNERABLE: early-exit string comparison
def verify_hmac(received, expected):
    return received == expected  # Python == compares left to right

# The comparison may short-circuit on first differing byte,
# leaking timing information
```

### 5.2 Attack Strategy

```python
import requests
import time

def hmac_timing_attack(url, data, hmac_len=32):
    """Byte-by-byte HMAC recovery via timing."""
    known = ""

    for pos in range(hmac_len * 2):  # hex chars
        best_char = ""
        best_time = 0

        for c in "0123456789abcdef":
            candidate = known + c + "0" * (hmac_len * 2 - len(known) - 1)
            times = []

            for _ in range(50):  # multiple samples for accuracy
                start = time.perf_counter_ns()
                requests.get(url, params={**data, "mac": candidate})
                elapsed = time.perf_counter_ns() - start
                times.append(elapsed)

            avg_time = sorted(times)[len(times)//2]  # median
            if avg_time > best_time:
                best_time = avg_time
                best_char = c

        known += best_char
        print(f"Position {pos}: {known}")

    return known
```

### 5.3 Constant-Time Comparison (Defense)

```python
import hmac

# SECURE: constant-time comparison
def verify_hmac_secure(received, expected):
    return hmac.compare_digest(received, expected)
```

---

## 6. MEET-IN-THE-MIDDLE (HASH)

### 6.1 Concept

Split hash computation into two halves, precompute one, match against the other.

```
Hash computation: H = f(g(x₁), h(x₂))

Precompute: table[g(x₁)] = x₁  for all x₁ in space₁
Search:     for each x₂ in space₂:
              if h(x₂) in table:
                found! (x₁, x₂)

Time:  O(2^(n/2)) instead of O(2^n)
Space: O(2^(n/2))
```

---

## 7. HASH PROOF-OF-WORK

### 7.1 Common CTF PoW Formats

```python
# Format 1: Find x such that SHA256(prefix + x) starts with N zero bits
import hashlib

def solve_pow_prefix(prefix, zero_bits):
    target = '0' * (zero_bits // 4)
    i = 0
    while True:
        candidate = prefix + str(i)
        h = hashlib.sha256(candidate.encode()).hexdigest()
        if h.startswith(target):
            return str(i)
        i += 1

# Format 2: Find x such that SHA256(x) ends with specific suffix
def solve_pow_suffix(suffix_hex, hash_func=hashlib.sha256):
    i = 0
    while True:
        h = hash_func(str(i).encode()).hexdigest()
        if h.endswith(suffix_hex):
            return str(i)
        i += 1
```

### 7.2 GPU-Accelerated PoW

```bash
# hashcat for SHA256 PoW
hashcat -a 3 -m 1400 --hex-charset \
  "0000000000000000000000000000000000000000000000000000000000000000:prefix" \
  "?a?a?a?a?a?a?a?a"
```

---

## 8. RAINBOW TABLES & SALTING

### 8.1 Rainbow Table Attack

```
Precomputed chain: password → hash → reduce → password₂ → hash₂ → ...
Lookup: given hash h, check if h appears in any chain
Time-memory tradeoff: less space than full table, more time than direct lookup
```

### 8.2 Salt Defeats Rainbow Tables

```
Without salt: H(password) — same password always produces same hash
With salt:    H(salt || password) — different salt per user

Rainbow tables are password-specific, not (salt+password)-specific
Each unique salt requires a separate table → infeasible
```

### 8.3 Modern Password Hashing

| Algorithm | Salt | Iterations | Memory-Hard | Recommended |
|---|---|---|---|---|
| MD5 | No | 1 | No | Never |
| SHA-256 | No | 1 | No | Never for passwords |
| bcrypt | Yes | Configurable | No | Yes |
| scrypt | Yes | Configurable | Yes | Yes |
| Argon2 | Yes | Configurable | Yes | Best choice |
| PBKDF2 | Yes | Configurable | No | Acceptable |

---

