# lattice-crypto-attacks technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 7. NTRU CRYPTANALYSIS

### 7.1 NTRU Lattice

```python
# SageMath
def ntru_lattice_attack(h, q, N):
    """
    Construct NTRU lattice for key recovery.
    h = public key polynomial (mod q)
    q = modulus
    N = dimension
    """
    # NTRU lattice:
    # | qI  0 |
    # | H   I |
    # where H is the circulant matrix of h

    H = matrix(ZZ, N, N)
    for i in range(N):
        for j in range(N):
            H[i, j] = h[(j - i) % N]

    M = block_matrix([
        [q * identity_matrix(N), zero_matrix(N)],
        [H, identity_matrix(N)]
    ])

    L = M.LLL()

    # Short vector in reduced basis = (f, g) private key
    for row in L:
        f = vector(row[:N])
        g = vector(row[N:])
        if f.norm() < q and g.norm() < q:
            return f, g

    return None
```

---

## 8. CONSTRUCTING ATTACK LATTICES — METHODOLOGY

### 8.1 General Recipe

```
1. Express the cryptographic problem as:
   "Find small x such that f(x) ≡ 0 (mod N)"
   or "Find x close to target t in some lattice L"

2. Choose lattice type:
   ├─ Polynomial lattice → Coppersmith-style
   ├─ Modular lattice → HNP-style CVP
   └─ Knapsack lattice → subset sum / CJLOSS

3. Determine dimensions:
   └─ More dimensions = better approximation but slower

4. Set scaling factors:
   └─ Balance the rows so short vector has roughly equal entries
   └─ Common: multiply by N/X where X is the root bound

5. Apply reduction:
   ├─ LLL first (fast, usually sufficient)
   └─ BKZ if LLL fails (increase block size: 20, 30, 40)

6. Extract solution:
   └─ Check reduced basis rows for valid solutions
```

### 8.2 Embedding Technique (CVP → SVP)

Transform CVP into SVP by embedding the target into the lattice:

```python
# SageMath
def cvp_to_svp(basis_matrix, target, scale=1):
    """Convert CVP to SVP via Kannan's embedding."""
    n = basis_matrix.nrows()
    m = basis_matrix.ncols()

    # Augment matrix
    M = matrix(ZZ, n + 1, m + 1)
    for i in range(n):
        for j in range(m):
            M[i, j] = basis_matrix[i, j]
        M[i, m] = 0

    for j in range(m):
        M[n, j] = target[j]
    M[n, m] = scale  # scaling factor (try 1, then adjust)

    L = M.LLL()

    # Look for row with last entry = ±scale
    for row in L:
        if abs(row[m]) == scale:
            return vector(target) - vector(row[:m]) * (row[m] // abs(row[m]))

    return None
```

### 8.3 Dimension Selection Guide

| Problem | Typical Dimension | Notes |
|---|---|---|
| Coppersmith univariate (degree d) | d × m where m ≈ 1/ε | Larger m = smaller root bound |
| HNP with n signatures | n + 2 | n ≥ known_bits_ratio × q_bits |
| Knapsack with n weights | n + 1 or n + 2 | Depends on density |
| LCG with n outputs | n + 1 | More outputs = easier |
| Boneh-Durfee | (m+1)(m+2)/2 | m = parameter depth |

---

## 9. DECISION TREE

```
Lattice approach needed — which construction?
│
├─ RSA-related?
│  ├─ Small unknown part of message → Coppersmith univariate
│  │  └─ Check: unknown_bits < n_bits / e
│  ├─ Partial factor knowledge → Coppersmith mod p
│  │  └─ Use beta=0.5, X=2^unknown_bits
│  ├─ Small private exponent d → Boneh-Durfee
│  │  └─ Check: d < N^0.292
│  └─ Multiple related equations → multivariate Coppersmith
│
├─ DSA/ECDSA-related?
│  ├─ Reused nonce → direct algebraic recovery (no lattice needed)
│  ├─ Partial nonce leakage → HNP → CVP lattice
│  │  └─ Need enough signatures: n ≥ q_bits / leaked_bits
│  └─ Nonce bias → statistical HNP → larger lattice
│
├─ Knapsack / subset sum?
│  ├─ Low density (d < 0.9408) → CJLOSS lattice attack
│  ├─ High density → lattice attack unlikely to work
│  └─ Super-increasing → greedy algorithm (no lattice needed)
│
├─ LCG / PRNG?
│  ├─ Full outputs known → algebraic recovery (no lattice)
│  ├─ Truncated outputs → CVP on recurrence lattice
│  └─ Unknown modulus → use GCD of output differences
│
├─ NTRU?
│  └─ Build circulant lattice → LLL/BKZ for short key vector
│
└─ Custom problem?
   ├─ Express as "find small root of polynomial mod N" → Coppersmith
   ├─ Express as "find lattice point close to target" → CVP
   ├─ Express as "find short vector in lattice" → SVP / LLL
   └─ If none fit → probably not a lattice problem
```

---

## 10. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---|---|---|
| Root bound too large | `small_roots()` returns empty | Reduce X, increase epsilon, verify bound satisfies Coppersmith criterion |
| Wrong scaling | LLL finds irrelevant short vector | Scale columns so target vector has balanced entries |
| Insufficient dimension | Solution not in reduced basis | Increase m parameter (more shift polynomials) |
| Wrong beta | Coppersmith doesn't find factor | beta=0.5 for half-size factor, beta=1.0 for full modulus |
| Too few signatures (HNP) | Lattice attack fails | Collect more signatures with nonce bias |
| BKZ block size too small | Solution not short enough | Increase block size (try 25, 30, 40) |
| Integer overflow | SageMath crashes | Use ZZ ring explicitly, avoid mixing QQ and ZZ |
