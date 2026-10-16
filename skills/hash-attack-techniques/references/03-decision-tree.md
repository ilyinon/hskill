# hash-attack-techniques technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 9. DECISION TREE

```
Hash-related challenge — what's the scenario?
│
├─ Have H(secret || message), need to extend?
│  ├─ Hash is MD5/SHA1/SHA256/SHA512?
│  │  └─ Yes → Length extension attack
│  │     └─ Need: MAC value, original message, secret length
│  │        └─ Tool: HashPump or hash_extender
│  │
│  └─ Hash is SHA3/HMAC/BLAKE2?
│     └─ Length extension doesn't work
│        └─ Look for other vulnerabilities
│
├─ Need two inputs with same hash?
│  ├─ MD5?
│  │  ├─ Same prefix → fastcoll (seconds)
│  │  ├─ Different prefixes → hashclash (hours)
│  │  └─ CTF PHP loose comparison → 0e magic hashes
│  │
│  ├─ SHA-1?
│  │  └─ SHAttered (expensive, use precomputed if possible)
│  │
│  └─ SHA-256+?
│     └─ No practical collision attack
│        └─ Look for logic flaws instead
│
├─ Need to forge HMAC?
│  ├─ Timing side channel available?
│  │  └─ Byte-by-byte timing attack
│  │
│  ├─ Key is short/weak?
│  │  └─ Brute force key with hashcat
│  │
│  └─ No weakness?
│     └─ HMAC is secure — look elsewhere
│
├─ Hash is truncated (short output)?
│  └─ Birthday attack — collision in 2^(bits/2)
│
├─ Proof of work?
│  └─ Brute force with parallel computation
│     ├─ Python multiprocessing for < 28 bits
│     ├─ hashcat/GPU for > 28 bits
│     └─ Optimize: pre-increment string, avoid re-encoding
│
└─ Password hash cracking?
   ├─ No salt → rainbow tables (pre-computed)
   ├─ Known salt → hashcat / John the Ripper
   └─ Memory-hard (Argon2/scrypt) → limited by memory, slow brute force
```

---

## 10. TOOLS

| Tool | Purpose | Usage |
|---|---|---|
| **HashPump** | Length extension attack | `hashpump -s MAC -d data -k secret_len -a extension` |
| **hash_extender** | Length extension (multiple algorithms) | `hash_extender --data D --secret L --append E --sig MAC` |
| **fastcoll** | MD5 identical-prefix collision | `fastcoll -p prefix -o out1 out2` |
| **hashclash** | MD5 chosen-prefix collision | `hashclash prefix1 prefix2` |
| **hashcat** | Password/hash cracking (GPU) | `hashcat -m MODE -a ATTACK hash wordlist` |
| **John the Ripper** | Password cracking (CPU/GPU) | `john --wordlist=rockyou.txt hashes.txt` |
| **CyberChef** | Quick hash computation and encoding | Web-based |
