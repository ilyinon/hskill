# lattice-crypto-attacks technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 4. COPPERSMITH'S METHOD

### 4.1 Univariate Case

Given f(x) ≡ 0 (mod N) with small root |x₀| < X, find x₀.

**Bound**: X < N^(1/d) where d = degree of f.

```python
# SageMath — built-in small_roots
N = ...
R.<x> = PolynomialRing(Zmod(N))
f = x^3 + a*x^2 + b*x + c  # known polynomial
roots = f.small_roots(X=2^100, beta=1.0, epsilon=1/30)
```

**Parameters**:
- `X`: upper bound on the root
- `beta`: N = p^beta (beta=1.0 for modular root of N itself; beta=0.5 for root mod unknown factor p ≈ √N)
- `epsilon`: smaller = better results but slower (try 1/30 to 1/100)

### 4.2 Stereotyped Message Attack (RSA)

```python
# SageMath
n, e, c = ...  # RSA parameters
known_msb = ...  # known upper portion of message

R.<x> = PolynomialRing(Zmod(n))
f = (known_msb + x)^e - c

# x represents the unknown lower bits
X = 2^(unknown_bit_count)
roots = f.small_roots(X=X, beta=1.0)
if roots:
    m = known_msb + int(roots[0])
```

### 4.3 Partial Key Exposure (Factor p)

Known MSBs of p: `p = p_known + x` where x is small.

```python
# SageMath
n = ...
p_known = ...  # known upper bits of p

R.<x> = PolynomialRing(Zmod(n))
f = p_known + x
roots = f.small_roots(X=2^unknown_bits, beta=0.5)
# beta=0.5 because p ≈ √n
if roots:
    p = p_known + int(roots[0])
    q = n // p
```

### 4.4 Multivariate Coppersmith (Howgrave-Graham)

For f(x, y) ≡ 0 (mod N):
- No polynomial-time algorithm guaranteed
- Heuristic methods work in practice
- Used in Boneh-Durfee for RSA small d

```python
# SageMath — Boneh-Durfee
# e*d ≡ 1 (mod phi) where phi = (p-1)(q-1)
# Rewrite: e*d = 1 + k*((n+1) - (p+q))
# Let x = k, y = (p+q), both small relative to n

R.<x, y> = PolynomialRing(ZZ)
A = (n + 1) // 2
f = 1 + x * (A + y)  # mod e

# Build shift polynomials and construct lattice
# Apply LLL to find small (x₀, y₀)
```

---

## 5. HIDDEN NUMBER PROBLEM (HNP) — DSA/ECDSA NONCE RECOVERY

### 5.1 Problem Statement

Given: signatures (rᵢ, sᵢ) where nonces kᵢ have known bias (leaked MSBs or LSBs).

DSA equation: `s = k⁻¹(H(m) + xr) mod q`

Rearranged: `k = s⁻¹(H(m) + xr) mod q`

If partial bits of k are known: reduces to CVP on a lattice.

### 5.2 Attack Setup

```python
# SageMath
def ecdsa_nonce_attack(signatures, q, known_bits, bit_position='msb'):
    """
    signatures: list of (r, s, hash, known_nonce_bits)
    q: curve order
    known_bits: number of known bits per nonce
    """
    n = len(signatures)

    # Build lattice
    B = 2^(q.nbits() - known_bits)  # bound on unknown part
    M = matrix(QQ, n + 2, n + 2)

    for i in range(n):
        r_i, s_i, h_i, a_i = signatures[i]
        t_i = Integer(inverse_mod(s_i, q) * r_i % q)
        u_i = Integer(inverse_mod(s_i, q) * h_i % q)

        M[i, i] = q
        M[n, i] = t_i
        M[n+1, i] = u_i - a_i  # a_i = known nonce bits

    M[n, n] = B / q
    M[n+1, n+1] = B

    # LLL reduction
    L = M.LLL()

    # Find row containing the private key x
    for row in L:
        x_candidate = Integer(row[n] * q / B) % q
        # Verify x_candidate against one signature
        if verify_private_key(x_candidate, signatures[0], q):
            return x_candidate

    return None
```

### 5.3 Practical Nonce Bias Sources

| Source | Leaked Bits | Required Signatures |
|---|---|---|
| MSB bias (always 0) | 1 bit | ~100 signatures |
| k generated with wrong length | Variable | ~50 signatures |
| Timing side channel | 1-4 bits | 20-100 signatures |
| Insecure PRNG | Many | Few |
| Reused nonce (k₁ = k₂) | All | 2 signatures |

For **reused nonce** (simplest case):

```python
def ecdsa_reused_nonce(r, s1, s2, h1, h2, q):
    """Recover private key when nonce k is reused."""
    # s1 - s2 = k⁻¹(h1 - h2) mod q  (since r is same)
    k = ((h1 - h2) * inverse_mod(s1 - s2, q)) % q
    x = ((s1 * k - h1) * inverse_mod(r, q)) % q
    return x, k
```

---

## 6. KNAPSACK / SUBSET SUM ATTACKS

### 6.1 Low-Density Attack

Knapsack: given weights a₁,...,aₙ and target S, find x₁,...,xₙ ∈ {0,1} such that Σxᵢaᵢ = S.

**Density** d = n / max(log₂ aᵢ). If d < 0.9408, lattice attack works.

```python
# SageMath
def knapsack_lattice(weights, target):
    """Solve subset sum via LLL lattice attack."""
    n = len(weights)

    # Build lattice (Lagarias-Odlyzko style)
    N = ceil(sqrt(n) / 2)  # scaling factor
    M = matrix(ZZ, n + 1, n + 1)

    for i in range(n):
        M[i, i] = 1
        M[i, n] = N * weights[i]
    M[n, n] = N * target

    # Alternative: CJLOSS embedding
    M2 = matrix(ZZ, n + 1, n + 2)
    for i in range(n):
        M2[i, i] = 1
        M2[i, n + 1] = N * weights[i]
    M2[n, n] = 1
    M2[n, n + 1] = N * (-target)

    L = M2.LLL()

    # Look for short vector with entries in {0, 1, -1}
    for row in L:
        if all(v in (0, 1) for v in row[:n]):
            solution = list(row[:n])
            if sum(solution[i] * weights[i] for i in range(n)) == target:
                return solution

    return None
```

---

