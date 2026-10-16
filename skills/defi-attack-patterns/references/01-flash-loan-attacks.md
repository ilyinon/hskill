For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: DeFi Attack Patterns — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert DeFi exploitation techniques. Covers flash loan mechanics, oracle manipulation (spot vs TWAP), MEV extraction (sandwich, JIT, liquidation), precision loss attacks, governance exploits, bridge vulnerabilities, and token standard pitfalls. Base models often miss the single-transaction atomicity constraint of flash loans and the distinction between spot price and TWAP manipulation.

## 0. RELATED ROUTING

- [smart-contract-vulnerabilities](../../smart-contract-vulnerabilities/SKILL.md) for underlying Solidity vulnerability patterns (reentrancy, integer overflow, delegatecall)
- [deserialization-insecure](../../deserialization-insecure/SKILL.md) when targeting off-chain bridge relayer or indexer infrastructure

---

## 1. FLASH LOAN ATTACKS

### 1.1 Mechanism

Flash loans provide uncollateralized borrowing within a single transaction. The entire borrow → use → repay cycle must complete atomically; if repayment fails, the transaction reverts as if nothing happened.

| Provider | Max Amount | Fee |
|---|---|---|
| Aave V3 | Pool liquidity per asset | 0.05% (can be 0 for approved borrowers) |
| dYdX | Pool liquidity | 0 (uses internal balance manipulation) |
| Uniswap V3 | Pool liquidity per pair | 0.3% (swap fee tier) |
| Balancer | Pool liquidity | Protocol-configurable |

### 1.2 Price Oracle Manipulation

```
1. Flash borrow 100,000 WETH
2. Swap 100,000 WETH → TOKEN on AMM_A
   → TOKEN spot price on AMM_A skyrockets
3. On Lending_Protocol (reads AMM_A spot price as oracle):
   → Deposit small TOKEN collateral (valued at inflated price)
   → Borrow large amount of WETH against it
4. Swap TOKEN back → WETH on AMM_A (restore price)
5. Repay flash loan (100,000 WETH + fee)
6. Keep borrowed WETH from Lending_Protocol minus collateral cost
```

**Key insight**: protocols using AMM spot reserves (`getReserves()`) as price oracles are vulnerable. Must use TWAP or external oracle (Chainlink).

### 1.3 Liquidity Pool Drain via Reentrancy

Flash borrow → deposit into pool → trigger reentrancy during callback → withdraw more than deposited → repay loan.

Exploits the combination of flash loan capital with reentrancy in pool accounting logic.

### 1.4 Governance Flash Borrow

```
1. Flash borrow governance tokens
2. Create/vote on malicious proposal (if no snapshot or timelock)
3. Proposal passes instantly
4. Execute proposal (drain treasury, change admin, etc.)
5. Return governance tokens
```

Defense: snapshot-based voting (Compound Governor Bravo), timelocks, minimum proposal period.

---

## 2. PRICE ORACLE MANIPULATION

### 2.1 Spot Price vs TWAP

| Oracle Type | Manipulation Cost | Time Window |
|---|---|---|
| Spot price (`getReserves()`) | Single large swap (flash loanable) | Same transaction |
| TWAP (Time-Weighted Average) | Sustained multi-block manipulation | Multiple blocks (expensive) |
| Chainlink aggregator | Compromise ≥ majority of oracle nodes | Practically infeasible |

### 2.2 AMM Manipulation Flow

```
Normal state: Pool has 1000 ETH + 1,000,000 USDC → price = 1000 USDC/ETH

Attack:
├── Swap 9000 ETH into pool
│   Pool now: 10000 ETH + 100,000 USDC (constant product)
│   Spot price: 10 USDC/ETH (crashed 100x)
├── Dependent contract reads this price
│   → Liquidates positions at wrong price
│   → Or allows cheap borrowing against ETH collateral
├── Swap back: buy ETH with USDC
│   Price restores to ~1000 USDC/ETH
└── Net profit = value extracted from dependent contract - swap slippage - fees
```

### 2.3 Chainlink Oracle Staleness

```solidity
(, int price, , uint updatedAt, ) = priceFeed.latestRoundData();
// Missing checks:
// 1. price > 0
// 2. updatedAt != 0
// 3. block.timestamp - updatedAt < HEARTBEAT
// 4. answeredInRound >= roundId
```

If oracle is stale (network congestion, L2 sequencer down), price can be hours old → arbitrage against stale price.

**L2 Sequencer Risk**: If Arbitrum/Optimism sequencer is down, Chainlink prices freeze. When it comes back, prices jump → mass liquidations at wrong prices.

---

## 3. MEV (MAXIMAL EXTRACTABLE VALUE)

### 3.1 Sandwich Attack

```
Mempool observation: victim submits swap TOKEN_A → TOKEN_B with slippage 1%

Front-run:  Buy TOKEN_B (increase price)
Victim tx:  Swap executes at worse price (within slippage tolerance)
Back-run:   Sell TOKEN_B (profit from price impact)

Profit = victim's price impact - gas costs × 2
```

### 3.2 JIT (Just-In-Time) Liquidity

```
1. Observe large pending swap in mempool
2. Provide concentrated liquidity in the exact price range (Uniswap V3 tick)
3. Victim's swap executes → JIT LP earns majority of fees
4. Remove liquidity immediately after swap
5. Profit = fee earned - gas - impermanent loss (minimal for single block)
```

### 3.3 Liquidation MEV

```
1. Monitor lending protocols for positions approaching liquidation threshold
2. When price oracle updates → position becomes liquidatable
3. Front-run other liquidators → execute liquidation
4. Receive liquidation bonus (typically 5-15% of collateral)
5. Sell collateral for profit
```

### 3.4 MEV Protection Mechanisms

| Mechanism | How It Works |
|---|---|
| Flashbots Protect | Sends tx to private mempool; only block builder sees it |
| MEV Blocker | RPC endpoint that routes through MEV-aware relayers |
| Cow Protocol (batch auction) | Batch matching eliminates ordering advantage |
| Encrypted mempools | Threshold encryption; decrypt only at block build time |
| MEV-Share | User captures portion of MEV extracted from their tx |

---

## 4. PRECISION LOSS EXPLOITATION

### 4.1 Rounding Errors in Token Calculations

Solidity has no floating point. Integer division truncates:

```
shares = depositAmount * totalShares / totalAssets
```

If `totalAssets` is very large relative to `depositAmount * totalShares`, result rounds to 0 → depositor gets no shares but pool keeps the deposit.

### 4.2 First Depositor / Vault Inflation Attack

```
1. Attacker deposits 1 wei → receives 1 share
2. Attacker donates 1,000,000 tokens directly to vault (not via deposit)
3. Vault state: 1,000,001 tokens, 1 share
4. Victim deposits 999,999 tokens:
   shares = 999,999 * 1 / 1,000,001 = 0 (integer truncation)
5. Victim gets 0 shares; attacker owns 100% of vault (now 2,000,000 tokens)
6. Attacker withdraws all
```

**Defenses:**
- Mint dead shares on first deposit (OpenZeppelin ERC4626 offset)
- Require minimum initial deposit
- Internal accounting with virtual offset

### 4.3 Dust Attack via Precision Truncation

Repeated small operations where each truncation loses 1 wei. Accumulate across thousands of operations → material loss.

---

