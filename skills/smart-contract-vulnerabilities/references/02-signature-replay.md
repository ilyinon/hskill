# smart-contract-vulnerabilities technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 7. SIGNATURE REPLAY

### Missing Nonce

Reuse a valid signature to repeat the action (e.g., transfer) multiple times.

### Cross-Chain Replay

Same contract deployed on multiple chains with same address → signature valid on all chains. Must include `block.chainid` in signed message.

### EIP-712 Implementation Errors

| Error | Consequence |
|---|---|
| Missing `DOMAIN_SEPARATOR` with chainId | Cross-chain replay |
| Domain separator cached at deploy | Breaks after hard fork changing chainId |
| Missing nonce in struct hash | Signature replay |
| `ecrecover` returns `address(0)` on invalid sig | Passes `== address(0)` owner check |

---

## 8. SELF-DESTRUCT & FORCE-SEND ETH

`selfdestruct(recipient)` force-sends all contract ETH to recipient — bypasses `receive()` and `fallback()`, cannot be rejected.

Breaks contracts that rely on `address(this).balance` for logic (e.g., `require(balance == expected)`).

Post-EIP-6780 (Dencun): `selfdestruct` only sends ETH; code/storage deletion only if called in same tx as creation.

---

## 9. CREATE2 & DETERMINISTIC ADDRESS EXPLOITATION

`CREATE2` address = `keccak256(0xff ++ deployer ++ salt ++ keccak256(initCode))`.

| Attack | Method |
|---|---|
| Pre-fund exploitation | Predict address → send tokens/ETH before deployment → `selfdestruct` → redeploy different code at same address |
| Pre-approve exploitation | Predicted address gets token approvals → deploy malicious contract → drain approved tokens |
| Metamorphic contracts | `CREATE2` → `selfdestruct` → `CREATE2` with same salt but different `initCode` (pre-EIP-6780) |

---

## 10. FLASH LOAN ATTACK PATTERNS

```
Single transaction:
├── Borrow large amount (no collateral)
├── Manipulate state (price oracle, governance, etc.)
├── Extract profit from manipulated state
├── Repay loan + fee
└── Keep profit
```

Key: entire sequence must succeed atomically or the whole tx reverts.

---

## 11. SHORT ADDRESS ATTACK

EVM pads missing bytes in ABI-encoded calldata with zeros. If `transfer(address, uint256)` is called with a 19-byte address, the uint256 amount shifts left by 8 bits → multiplied by 256.

Mitigation: validate calldata length; modern Solidity compilers add checks.

---

## 12. TOOLS

| Tool | Purpose | Usage |
|---|---|---|
| Slither | Static analysis, vulnerability detection | `slither .` in project root |
| Mythril | Symbolic execution, path exploration | `myth analyze contract.sol` |
| Echidna | Property-based fuzzing | Define invariants, fuzz for violations |
| Foundry (Forge) | Test framework, fuzzing, gas analysis | `forge test --fuzz-runs 10000` |
| Hardhat | Development, testing, deployment | `npx hardhat test` |
| Certora | Formal verification | Write specs, prove/disprove properties |
| 4naly3er | Automated gas optimization + vuln report | CI integration |

---

## 13. DECISION TREE

```
Auditing a smart contract?
├── Is it a proxy pattern?
│   ├── Yes → Check storage layout collision (Section 5)
│   │   ├── Compare slot assignments between proxy and implementation
│   │   ├── Check for function selector collision
│   │   └── Verify initializer cannot be called twice
│   └── No → Continue
├── Does it make external calls?
│   ├── Yes → Check reentrancy (Section 1)
│   │   ├── State updated before call? → CEI pattern OK
│   │   ├── ReentrancyGuard present? → Check all entry points
│   │   ├── Cross-function state sharing? → Cross-function reentrancy risk
│   │   └── View functions read during callback? → Read-only reentrancy
│   └── No → Continue
├── Does it handle tokens/ETH?
│   ├── Yes → Check integer overflow (Section 2)
│   │   ├── Solidity < 0.8? → All arithmetic suspect
│   │   ├── unchecked{} blocks? → Verify no user-influenced values
│   │   └── Casting between uint sizes? → Truncation risk
│   └── Also check self-destruct force-send (Section 8)
├── Does it use signatures?
│   ├── Yes → Check replay (Section 7)
│   │   ├── Nonce included? → Verify incremented
│   │   ├── ChainId included? → Cross-chain safe
│   │   └── ecrecover result checked for address(0)? → OK
│   └── No → Continue
├── Does it use on-chain randomness?
│   ├── Yes → Predictable (Section 4)
│   │   └── Recommend Chainlink VRF or commit-reveal with bond
│   └── No → Continue
├── Does it interact with DeFi protocols?
│   ├── Yes → Load [defi-attack-patterns](../defi-attack-patterns/SKILL.md)
│   │   ├── Flash loan vectors
│   │   ├── Oracle manipulation
│   │   └── MEV exposure
│   └── No → Continue
├── Does it use CREATE2?
│   ├── Yes → Check deterministic address exploitation (Section 9)
│   └── No → Continue
└── Run automated tools (Section 12)
    ├── Slither for static analysis
    ├── Mythril for symbolic execution
    └── Echidna for fuzzing invariants
```
