For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Hash Attack Techniques — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert hash attack techniques for CTF and security assessments. Covers length extension attacks, MD5/SHA1 collision generation, meet-in-the-middle hash attacks, HMAC timing side channels, birthday attacks, and proof-of-work solving. Base models often incorrectly apply length extension to HMAC or SHA-3, or fail to distinguish between identical-prefix and chosen-prefix collisions.

## 0. RELATED ROUTING

- [rsa-attack-techniques](../../rsa-attack-techniques/SKILL.md) when hash weaknesses affect RSA signature schemes
- [symmetric-cipher-attacks](../../symmetric-cipher-attacks/SKILL.md) when hash is used in key derivation
- [classical-cipher-analysis](../../classical-cipher-analysis/SKILL.md) when analyzing hash-like constructions in classical ciphers

### Quick attack selection

| Scenario | Attack | Tool |
|---|---|---|
| `H(secret \|\| msg)` known, extend message | Length extension | HashPump, hash_extender |
| Need two files with same MD5 | Identical-prefix collision | fastcoll |
| Need specific MD5 prefix match | Chosen-prefix collision | hashclash |
| Byte-by-byte HMAC comparison | Timing attack | Custom script |
| Find any collision | Birthday attack | O(2^(n/2)) |
| Proof of work: find hash with leading zeros | Brute force | hashcat, Python |

---

## 1. LENGTH EXTENSION ATTACK

### 1.1 Vulnerable vs Non-Vulnerable

| Hash | Vulnerable | Why |
|---|---|---|
| MD5 | Yes | Merkle-Damgard construction |
| SHA-1 | Yes | Merkle-Damgard construction |
| SHA-256 | Yes | Merkle-Damgard construction |
| SHA-512 | Yes | Merkle-Damgard construction |
| SHA-3 / Keccak | No | Sponge construction |
| HMAC-* | No | Double hashing prevents extension |
| SHA-256 truncated | No (if truncated) | Missing internal state bits |
| BLAKE2 | No | Different construction |

### 1.2 Attack Mechanism

```
Given:   MAC = H(secret || original_message)
Known:   original_message, len(secret), MAC value
Compute: H(secret || original_message || padding || extension)
         WITHOUT knowing the secret!

How: The MAC value IS the internal hash state after processing
     (secret || original_message || padding).
     Initialize hash with this state, continue hashing extension.
```

### 1.3 Padding Calculation (MD5/SHA)

```python
def md5_padding(message_len_bytes):
    """Calculate MD5/SHA padding for given message length."""
    bit_len = message_len_bytes * 8

    # Pad with 0x80 + zeros until length ≡ 56 (mod 64)
    padding = b'\x80'
    padding += b'\x00' * ((55 - message_len_bytes) % 64)

    # Append original length as 64-bit little-endian (MD5)
    # or big-endian (SHA)
    padding += bit_len.to_bytes(8, 'little')  # MD5
    # padding += bit_len.to_bytes(8, 'big')    # SHA

    return padding
```

### 1.4 Tool Usage

```bash
# HashPump
hashpump -s "known_mac_hex" \
         -d "original_data" \
         -k 16 \            # secret length
         -a "extension_data"

# Output: new_mac, new_data (original + padding + extension)

# hash_extender
hash_extender --data "original" \
              --secret 16 \
              --append "extension" \
              --signature "known_mac_hex" \
              --format md5
```

### 1.5 Python Implementation

```python
import struct

def md5_extend(original_mac, original_data_len, secret_len, extension):
    """
    Perform MD5 length extension attack.
    original_mac: hex string of H(secret || original_data)
    """
    # Parse MAC into MD5 internal state (4 × 32-bit words, little-endian)
    h = struct.unpack('<4I', bytes.fromhex(original_mac))

    # Calculate total length after padding
    total_original = secret_len + original_data_len
    padding = md5_padding(total_original)
    forged_len = total_original + len(padding) + len(extension)

    # Continue MD5 from saved state with extension
    # (requires MD5 implementation that accepts initial state)
    from hashlib import md5
    # Most stdlib md5 doesn't expose state setting
    # Use: hlextend library or custom MD5

    import hlextend
    sha = hlextend.new('md5')
    new_hash = sha.extend(extension, original_data, secret_len,
                          original_mac)
    new_data = sha.payload  # includes original + padding + extension

    return new_hash, new_data
```

---

## 2. MD5 COLLISION ATTACKS

### 2.1 Identical-Prefix Collision (fastcoll)

Two messages with same prefix but different content, producing identical MD5.

```bash
# Generate collision pair
fastcoll -p prefix_file -o collision1.bin collision2.bin

# Result: MD5(collision1.bin) == MD5(collision2.bin)
# Files differ in exactly 128 bytes (two MD5 blocks)
```

### 2.2 Chosen-Prefix Collision (hashclash)

Two messages with different chosen prefixes, appended with computed suffixes to collide.

```bash
# hashclash (Marc Stevens)
./hashclash prefix1.bin prefix2.bin

# Result: MD5(prefix1 || suffix1) == MD5(prefix2 || suffix2)
```

### 2.3 UniColl (Single-Block Near-Collision)

Produces two messages differing in a single byte within one MD5 block, with same hash.

```
Application: forge two PDF/PE files with same MD5
  - File 1: benign content
  - File 2: malicious content
  - Same MD5 hash
```

### 2.4 Collision Applications

| Application | Technique | Impact |
|---|---|---|
| Certificate forgery | Chosen-prefix | Rogue CA certificate (proven in 2008) |
| Binary substitution | Identical-prefix + conditional | Two executables, same MD5, different behavior |
| PDF collision | UniColl | Two PDFs showing different content |
| Git commit collision | Chosen-prefix (SHAttered for SHA1) | Two commits with same hash |
| CTF: bypass MD5 check | fastcoll | Two different inputs accepted as same |

### 2.5 CTF MD5 Collision Tricks

```php
// PHP: md5($_GET['a']) == md5($_GET['b']) && $_GET['a'] != $_GET['b']

// Method 1: Array trick (not real collision)
?a[]=1&b[]=2  // md5(array) returns NULL, NULL == NULL

// Method 2: Real collision (fastcoll output, URL-encoded binary)
?a=<collision1_urlencoded>&b=<collision2_urlencoded>

// Method 3: 0e magic hashes (loose comparison ==)
// md5("240610708") = "0e462097431906509019562988736854"
// md5("QNKCDZO")   = "0e830400451993494058024219903391"
// PHP: "0e..." == "0e..." is TRUE (both evaluate to 0 as floats)
```

---

