For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Lattice-Based Cryptanalysis — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert lattice techniques for CTF and cryptanalysis. Covers LLL/BKZ reduction, Coppersmith's method (univariate and multivariate), Hidden Number Problem for DSA/ECDSA nonce recovery, knapsack attacks, and NTRU analysis. Base models often fail to construct the correct attack lattice (wrong dimensions, missing scaling factors) or misapply Coppersmith bounds.

## 0. RELATED ROUTING

- [rsa-attack-techniques](../../rsa-attack-techniques/SKILL.md) for RSA-specific attacks that use lattice methods (Coppersmith, Boneh-Durfee)
- [symmetric-cipher-attacks](../../symmetric-cipher-attacks/SKILL.md) for LCG state recovery via lattice
- [classical-cipher-analysis](../../classical-cipher-analysis/SKILL.md) when lattice methods apply to classical cipher analysis

### Quick application guide

| Problem Type | Lattice Technique | Key Parameter |
|---|---|---|
| RSA small roots | Coppersmith (LLL on polynomial lattice) | Root bound X < N^(1/e) |
| RSA small d | Boneh-Durfee (multivariate Coppersmith) | d < N^0.292 |
| DSA/ECDSA nonce bias | Hidden Number Problem → CVP | Bias bits known |
| Knapsack cipher | Low-density lattice attack | Density < 0.9408 |
| LCG truncated output | CVP on recurrence lattice | Unknown bits per output |
| Subset sum | LLL reduction on knapsack lattice | Element size vs count |
| NTRU key recovery | Lattice reduction on NTRU lattice | Dimension and key size |

---

## 1. LATTICE FUNDAMENTALS

### 1.1 Definitions

A **lattice** L is the set of all integer linear combinations of basis vectors:

```
L = { a₁·b₁ + a₂·b₂ + ... + aₙ·bₙ | aᵢ ∈ ℤ }
```

where b₁, ..., bₙ are linearly independent vectors in ℝᵐ.

**Key problems**:
- **SVP** (Shortest Vector Problem): Find the shortest non-zero vector in L
- **CVP** (Closest Vector Problem): Given target t, find v ∈ L closest to t
- **SVP is NP-hard** in general, but LLL finds an approximately short vector in polynomial time

### 1.2 Lattice Quality Metrics

```
Determinant: det(L) = |det(B)| where B is the basis matrix
Gaussian heuristic: shortest vector ≈ √(n/(2πe)) · det(L)^(1/n)
```

---

## 2. LLL ALGORITHM

### 2.1 What LLL Does

Takes a lattice basis B and produces a **reduced basis** B' where:
- Vectors are nearly orthogonal
- First vector is approximately short (within 2^((n-1)/2) factor of SVP)
- Runs in polynomial time: O(n^5 · d · log³ B) where d = dimension, B = max entry size

### 2.2 SageMath Usage

```python
# SageMath
M = matrix(ZZ, [
    [1, 0, 0, large_value_1],
    [0, 1, 0, large_value_2],
    [0, 0, 1, large_value_3],
    [0, 0, 0, modulus],
])

L = M.LLL()
# Short vectors in L reveal the solution
short_vector = L[0]  # first row is typically shortest
```

### 2.3 Python (fpylll)

```python
from fpylll import IntegerMatrix, LLL

n = 4
A = IntegerMatrix(n, n)
# Fill matrix A...
A[0] = (1, 0, 0, large_value_1)
A[1] = (0, 1, 0, large_value_2)
A[2] = (0, 0, 1, large_value_3)
A[3] = (0, 0, 0, modulus)

LLL.reduction(A)
print(A[0])  # shortest vector
```

---

## 3. BKZ (BLOCK KORKINE-ZOLOTAREV)

### 3.1 Comparison with LLL

| Property | LLL | BKZ-β |
|---|---|---|
| Quality | 2^((n-1)/2) approximation | 2^(n/(β-1)) approximation |
| Speed | Polynomial | Exponential in β |
| Block size | Fixed (2) | Configurable β |
| Best for | Quick reduction | High-quality reduction |

### 3.2 Usage

```python
# SageMath
M = matrix(ZZ, [...])
L = M.BKZ(block_size=20)  # β = 20

# fpylll
from fpylll import BKZ
BKZ.reduction(A, BKZ.Param(block_size=20))
```

Rule of thumb: start with LLL, increase to BKZ if needed. BKZ block size 20-40 is usually sufficient for CTF.

---

