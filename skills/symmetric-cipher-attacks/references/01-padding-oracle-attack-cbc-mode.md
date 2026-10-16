For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Symmetric Cipher Attacks — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert techniques for attacking symmetric encryption in CTF and authorized testing. Covers CBC padding oracle, CBC bit flipping, ECB detection and exploitation, stream cipher key reuse, LFSR/LCG state recovery, RC4 biases, and meet-in-the-middle attacks. Base models often confuse ECB and CBC attack strategies or fail to set up byte-at-a-time ECB decryption correctly.

## 0. RELATED ROUTING

- [rsa-attack-techniques](../../rsa-attack-techniques/SKILL.md) when symmetric key is protected by RSA
- [hash-attack-techniques](../../hash-attack-techniques/SKILL.md) when HMAC or hash-based authentication is involved
- [lattice-crypto-attacks](../../lattice-crypto-attacks/SKILL.md) for LCG/LFSR state recovery via lattice methods

### Advanced Reference

Also load [BLOCK_CIPHER_ATTACKS.md](../BLOCK_CIPHER_ATTACKS.md) when you need:
- Detailed attack scripts with full Python implementations
- Step-by-step byte-at-a-time ECB walkthrough
- PadBuster usage and custom padding oracle scripts
- LCG/LFSR recovery implementation

### Quick attack selection

| Observable Behavior | Likely Weakness | Attack |
|---|---|---|
| Same plaintext → same ciphertext (block-aligned) | ECB mode | Cut-and-paste / byte-at-a-time |
| Padding error distinguishable | CBC padding oracle | Decrypt without key |
| Can modify ciphertext, affects next block | CBC mode, no integrity check | Bit flipping |
| Key reused with XOR/stream cipher | Two-time pad | XOR ciphertexts together |
| Predictable PRNG output | LCG or LFSR | State recovery |
| Double encryption used | 2DES-like | Meet in the middle |

---

## 1. PADDING ORACLE ATTACK (CBC MODE)

### 1.1 Mechanism

CBC decryption: `P_i = D_K(C_i) ⊕ C_{i-1}`

If the server reveals whether padding is valid (PKCS#7), we can decrypt any block by manipulating the previous ciphertext block.

### 1.2 Attack Steps

```
Target: decrypt block C_i (with unknown plaintext P_i)

For byte position b = 15 down to 0 (last byte first):
  padding_value = 16 - b
  
  For guess = 0x00 to 0xFF:
    Construct modified C'_{i-1}:
      - Bytes 0..b-1: original C_{i-1} bytes
      - Byte b: guess
      - Bytes b+1..15: calculated to produce correct padding
    
    Send (C'_{i-1} || C_i) to oracle
    
    If oracle says "valid padding":
      intermediate_byte[b] = guess ⊕ padding_value
      plaintext_byte[b] = intermediate_byte[b] ⊕ original_C_{i-1}[b]
```

### 1.3 Python Implementation

```python
def padding_oracle_attack(ciphertext, block_size, oracle):
    """
    oracle(ct) returns True if padding is valid, False otherwise.
    ciphertext includes IV as first block.
    """
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext = b""

    for block_idx in range(1, len(blocks)):
        prev_block = bytearray(blocks[block_idx - 1])
        curr_block = blocks[block_idx]
        intermediate = [0] * block_size
        decrypted = [0] * block_size

        for byte_pos in range(block_size - 1, -1, -1):
            padding_val = block_size - byte_pos

            for guess in range(256):
                modified = bytearray(block_size)
                modified[byte_pos] = guess

                for j in range(byte_pos + 1, block_size):
                    modified[j] = intermediate[j] ^ padding_val

                test_ct = bytes(modified) + curr_block
                if oracle(test_ct):
                    if byte_pos == block_size - 1:
                        # Verify it's not a false positive (padding 0x02 0x02)
                        check = bytearray(modified)
                        check[byte_pos - 1] ^= 1
                        if not oracle(bytes(check) + curr_block):
                            continue

                    intermediate[byte_pos] = guess ^ padding_val
                    decrypted[byte_pos] = intermediate[byte_pos] ^ prev_block[byte_pos]
                    break

        plaintext += bytes(decrypted)

    return plaintext
```

### 1.4 Tools

```bash
# PadBuster
padbuster http://target/decrypt?ct= CIPHERTEXT_HEX 16 -encoding 0
padbuster http://target/decrypt?ct= CIPHERTEXT_HEX 16 -encoding 0 -plaintext "admin=true"
```

---

## 2. CBC BIT FLIPPING

### 2.1 Concept

Flipping bit at position j in C_{i-1} flips the same bit at position j in P_i (and corrupts all of P_{i-1}).

```
Original:  P_i[j] = D_K(C_i)[j] ⊕ C_{i-1}[j]
Modified:  P'_i[j] = D_K(C_i)[j] ⊕ C'_{i-1}[j]
                    = P_i[j] ⊕ (C_{i-1}[j] ⊕ C'_{i-1}[j])
```

### 2.2 Practical Example

```python
def cbc_bitflip(ciphertext, block_size, target_byte_pos, old_value, new_value):
    """
    Flip byte in plaintext block N+1 by modifying ciphertext block N.
    target_byte_pos: absolute position in plaintext (0-indexed).
    ciphertext excludes the IV; target must be in block 1 or later.
    To modify plaintext block 0, modify the separately held IV instead.
    """
    if target_byte_pos < block_size:
        raise ValueError("Target block 0 requires modifying the separate IV")
    if target_byte_pos >= len(ciphertext):
        raise ValueError("Target position is outside the ciphertext")
    ct = bytearray(ciphertext)
    block_num = target_byte_pos // block_size
    byte_in_block = target_byte_pos % block_size

    # Modify previous block (block_num - 1) to flip target byte
    modify_pos = (block_num - 1) * block_size + byte_in_block

    # XOR to cancel old value and set new value
    ct[modify_pos] ^= old_value ^ new_value
    return bytes(ct)

# Example: flip "admin=0" to "admin=1"
# If "admin=0" is at byte position 22 (block 1, byte 6):
modified_ct = cbc_bitflip(ciphertext, 16, 22, ord('0'), ord('1'))
```

---

