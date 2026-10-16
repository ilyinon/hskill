For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: RSA Attack Techniques — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert RSA attack techniques for CTF and authorized security assessments. Covers factorization attacks, small exponent exploits, lattice-based approaches (Wiener/Boneh-Durfee/Coppersmith), broadcast attacks, common modulus, padding oracles, and fault attacks. Base models often suggest attacks that don't match the given parameters or miss the correct attack selection based on what's known.

## 0. RELATED ROUTING

- [lattice-crypto-attacks](../../lattice-crypto-attacks/SKILL.md) for deep lattice theory behind Coppersmith/Boneh-Durfee
- [hash-attack-techniques](../../hash-attack-techniques/SKILL.md) when RSA signature forgery involves hash weaknesses
- [symmetric-cipher-attacks](../../symmetric-cipher-attacks/SKILL.md) when RSA protects a symmetric key (hybrid encryption)

### Advanced Reference

Also load [RSA_ATTACK_CATALOG.md](../RSA_ATTACK_CATALOG.md) when you need:
- Detailed SageMath/Python implementation for each attack
- Step-by-step mathematical derivation
- Edge cases and failure conditions per attack

### Quick attack selection

| Given / Observable | Attack | Tool |
|---|---|---|
| Small n (< 512 bits) | Direct factorization | factordb, yafu, msieve |
| e = 3, small message | Cube root | gmpy2.iroot |
| Multiple (n, c) same small e | Hastad broadcast | CRT + iroot |
| Very large e or very small d | Wiener / Boneh-Durfee | SageMath, RsaCtfTool |
| Partial p knowledge | Coppersmith small roots | SageMath |
| Same n, different e | Common modulus | Extended GCD |
| Multiple n values | Batch GCD (shared factor) | Python/SageMath |
| Padding error oracle | Bleichenbacher | Custom script |
| LSB parity oracle | LSB oracle attack | Custom script |
| Fault in CRT computation | RSA-CRT fault | Single faulty signature |

---

## 1. FACTORIZATION ATTACKS

### 1.1 Direct Factorization (Small n)

```python
from sympy import factorint

n = 0x...  # small modulus
factors = factorint(n)
p, q = list(factors.keys())
```

**When**: n < ~512 bits, or known to be in factordb.

### 1.2 Fermat's Factorization

Works when p and q are close together: |p - q| is small.

```python
from gmpy2 import isqrt, is_square

def fermat_factor(n):
    a = isqrt(n) + 1
    while True:
        b2 = a * a - n
        if is_square(b2):
            b = isqrt(b2)
            return (a + b, a - b)
        a += 1
```

### 1.3 Pollard's p-1

Works when p-1 has only small prime factors (B-smooth).

```python
from gmpy2 import gcd

def pollard_p1(n, B=2**20):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
    d = gcd(a - 1, n)
    if 1 < d < n:
        return d
    return None
```

### 1.4 Batch GCD (Multiple n share a factor)

```python
from math import gcd
from functools import reduce

def batch_gcd(moduli):
    """Find shared factors among multiple RSA moduli."""
    product = reduce(lambda a, b: a * b, moduli)
    results = {}
    for i, n in enumerate(moduli):
        remainder = product // n
        g = gcd(n, remainder)
        if g != 1 and g != n:
            results[i] = (g, n // g)
    return results
```

---

## 2. SMALL EXPONENT ATTACKS

### 2.1 Cube Root Attack (e = 3, small m)

If m^e < n (no modular reduction occurred), simply take the e-th root.

```python
from gmpy2 import iroot

c = 0x...  # ciphertext
e = 3
m, exact = iroot(c, e)
if exact:
    print(f"Plaintext: {bytes.fromhex(hex(m)[2:])}")
```

### 2.2 Hastad Broadcast Attack

Same message encrypted with same small e under different moduli (n₁, n₂, ..., nₑ).

```python
from sympy.ntheory.modular import crt
from gmpy2 import iroot

# e = 3, three ciphertexts under three different n
n_list = [n1, n2, n3]
c_list = [c1, c2, c3]

# CRT: find x such that x ≡ ci (mod ni) for all i
r, M = crt(n_list, c_list)
m, exact = iroot(r, 3)
assert exact
```

### 2.3 Related Message Attack (Franklin-Reiter)

Two messages related by a known linear function: m₂ = a·m₁ + b. Same n and e.

```python
# SageMath
def franklin_reiter(n, e, c1, c2, a, b):
    R.<x> = PolynomialRing(Zmod(n))
    f1 = x^e - c1
    f2 = (a*x + b)^e - c2
    return Integer(n - gcd(f1, f2).coefficients()[0])
```

---

## 3. LARGE e / SMALL d ATTACKS

### 3.1 Wiener's Attack (Continued Fractions)

When d < n^(1/4) / 3, the continued fraction expansion of e/n reveals d.

```python
def wiener_attack(e, n):
    """Recover d when d is small via continued fractions."""
    cf = continued_fraction(e, n)
    convergents = get_convergents(cf)

    for k, d in convergents:
        if k == 0:
            continue
        phi_candidate = (e * d - 1) // k
        # phi(n) = n - p - q + 1 → p + q = n - phi + 1
        s = n - phi_candidate + 1
        # p, q are roots of x^2 - s*x + n = 0
        discriminant = s * s - 4 * n
        if discriminant >= 0:
            from gmpy2 import isqrt, is_square
            if is_square(discriminant):
                return d
    return None

def continued_fraction(a, b):
    cf = []
    while b:
        cf.append(a // b)
        a, b = b, a % b
    return cf

def get_convergents(cf):
    convergents = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    for a in cf:
        h_prev, h_curr = h_curr, a * h_curr + h_prev
        k_prev, k_curr = k_curr, a * k_curr + k_prev
        convergents.append((h_curr, k_curr))
    return convergents
```

### 3.2 Boneh-Durfee Attack (Lattice-Based)

Extends Wiener: works when d < n^0.292. Uses lattice reduction (LLL/BKZ).

**Use SageMath implementation** — see [lattice-crypto-attacks](../../lattice-crypto-attacks/SKILL.md) for theory.

---

