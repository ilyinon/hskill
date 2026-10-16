# rsa-attack-techniques technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 9. TOOLS

| Tool | Purpose | Usage |
|---|---|---|
| **RsaCtfTool** | Automated RSA attack suite | `python3 RsaCtfTool.py --publickey pub.pem --uncipherfile flag.enc` |
| **SageMath** | Mathematical computation | Coppersmith, lattice attacks, polynomial arithmetic |
| **factordb.com** | Online factor database | Check if n is already factored |
| **yafu** | Fast factorization (SIQS/GNFS) | `yafu "factor(n)"` |
| **msieve** | GNFS factorization | Large n factorization |
| **gmpy2** | Fast Python integer library | `iroot`, `invert`, `gcd` |
| **pycryptodome** | RSA primitives | Key construction from factors |

### RsaCtfTool Quick Commands

```bash
# From public key
python3 RsaCtfTool.py --publickey pub.pem -n --private

# From parameters
python3 RsaCtfTool.py -n $N -e $E --uncipher $C

# Try all attacks
python3 RsaCtfTool.py --publickey pub.pem --uncipherfile flag.enc --attack all
```

### Decrypt After Factoring

```python
from Crypto.PublicKey import RSA
from gmpy2 import invert

p, q = ...  # factored
n = p * q
e = 65537
phi = (p - 1) * (q - 1)
d = int(invert(e, phi))

c = ...  # ciphertext as integer
m = pow(c, d, n)
plaintext = m.to_bytes((m.bit_length() + 7) // 8, 'big')
print(plaintext)
```
