# Project Dossier: RogueTrader (Pre-Trade Risk System for Sui)

**Dossier Generation Date:** November 10, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Source:** Remote GitHub (`Olalolo22/roguetrader`) / Local Workspace (`/home/lala_02/roguetrader`)  
**Access Level:** Public / Open Source  
**Latest Verified Commit:** `9ffcfee` (`docs: synchronize BLOG_POST.md with published Substack essay`)  
**Evidence Standard:** E1 (On-Chain Mainnet Account, Walrus Blobs, gRPC Balance Verification) / E2 (Complete Source Code, Benchmark Engine, Vercel Desk)

---

## A. Identity and Purpose

- **Project Name:** RogueTrader
- **Repository URL:** [`https://github.com/Olalolo22/roguetrader`](https://github.com/Olalolo22/roguetrader)
- **Live Deployment:** [`https://roguetrader.vercel.app`](https://roguetrader.vercel.app)
- **Published Essay:** [`https://olumide2956.substack.com/p/roguetrader-how-market-memory-influences`](https://olumide2956.substack.com/p/roguetrader-how-market-memory-influences)
- **Relevant Branches:** `main`, `landing-v9` (production), `mascot-v5` (locked fixture at commit `3030764`)
- **What It Does:** A deterministic Pre-Trade Risk System (PTRS) for Sui Mainnet that intercepts autonomous agent trading intents before execution, projects trade parameters against decentralized historical market memory stored on Walrus (`@mysten-incubation/memwal`), penalizes overconfident directional sizing during adverse liquidity regimes, and monetizes risk intelligence via HTTP 402 (`x402`) micropayments verified on-chain.
- **Specific Problem Addressed:** Stateless autonomous trading agents suffer from acute temporal myopia: they evaluate price action purely over narrow context windows (5 to 15 minute OHLCV candles). When entering crowded trades during liquidity vacuums, high borrow utilization on lending protocols (e.g., NAVI/Scallop), or epoch boundary oracle delays, stateless agents hallucinate 85% to 95% directional confidence right into liquidity traps. RogueTrader acts as an external pre-trade firewall, anchoring agent beliefs against persistent decentralized regime memory.
- **Intended Users:**
  1. Autonomous trading agents and solver networks operating on Sui DEXs (Cetus, DeepBook v3).
  2. DAO treasuries and automated vaults requiring pre-execution leverage governors.
  3. Algorithmic traders seeking historical market memory retrieval via standardized HTTP 402 endpoints.
- **Context & Tracks:** Built for the **Tatum x Walrus Sui Hackathon** (submitted across Track 1 / Track 2).

---

## B. Implementation Status

- **Classification:** **Fully Implemented, Deployed on Sui Mainnet & Live Production Desk**
- **Verified On-Chain & Storage Identifiers:**
  - **Sui Mainnet MemWal Account ID:** `0xf7bbb0464e0088b39df94354701fdeef69ccfd7e15b59964b1ac73c30c44e223`
  - **Sui Mainnet Package ID:** `0xe7c16fbea0560e7057e2bf7422feaa4fb313749fc69c9e9092fac7a33b81d7f5`
  - **x402 Micropayment Merchant Address:** `0xaff0ccba609e3d18b5f5cf6290f158736c6c788ed4074951d636b223a4824b4d`
  - **Verified Settlement Transaction Digest:** `5VGXV3D6nT8N3vw67LyJTXRQNkiLY8bLaJoAs1iqEJ2N`
  - **Minimum x402 Micropayment Gate:** 0.05 SUI (50,000,000 MIST)
  - **Walrus Mainnet Memory Blobs (15 Blobs Verified):**
    - `thAHmeWQNFkTOjN-sdmU7SVKuXI2jWpO3wzTXgjr6R0` (Oct 14: NAVI borrow squeeze, -8.2% cascade)
    - `1ZOLBULVD-pOR80s3qADLhBbPHmA6yVQ1rs7Y4QoiJM` (Oct 16: Low-crowding DeepBook absorption breakout)
    - `qlvh2ujy6cs7mTgjoWPK_k8OCcKdWE-2BNKWcMtKr5E` (Oct 18: Scallop borrow thin liquidity pool wick)
    - `BamlyvKWqCgUcjK_kQ2YiM94grCFrkl5u1f3fRYA2z8` (Oct 19: Sui epoch 512 transition oracle latency)
    - `gi3MnkJ1wY-f7nPs1ODkjnx7D0CJBdKixFqH1LoNxW0` (Oct 24: Retail euphoria spike & DeepBook bid-depth vacuum)
    - `u29gxoSNeyIB6DOBR-GL1rieV6O3lXFfwdfomb2ytHY` (Oct 25: DeepBook institutional bid absorption)
    - `kxziGvQVIZ25vsfvvMxZo9GSzdeQAhGJgL6Z-CAXBcs` (Oct 28: Stop-hunt liquidity sweep through bid vacuum)
    - `oceCZClMB-mLNKFGNhyAyqHPm7i-GiTaWeXdcddveAE` (Oct 30: Scallop 140% APY flash-loan deleverage spike)
    - `VyTfLjzJqL7MBYOufVlPBvD2WFs54HxoztDQHCxXdzk` (Nov 02: Clean trend continuation, low borrow crowding)
    - `F6pMrdzRAen9NQZzsADr7Lj8bUAr8WXzzy_9OwFwKHs` (Nov 04: Meme coin 86% borrow cascade liquidation)
    - `-geRj7clDG5AxtiNpmz35jpoRrUg0LcavGuLAYsnjoM` (Nov 06: Sui checkpoint congestion oracle delay)
    - `uCWoMfbtNImcsKdyhkHh5Yzql2z3ehK_v6HteE3KJIQ` (Nov 08: DeepBook v3 $8.2M wholesale wall absorption)
    - Plus 3 dynamic forward-commitment memories recorded live through the desk.

---

## C. Technical Architecture

```
[ Autonomous Trading Agent / User Intent ]
                 │
                 │ 1. Submits Proposed Trade (Size, Leverage, Asset, Thesis)
                 ▼
+--------------------------------------------------------------------------------+
|                       ROGUE TRADER PRE-TRADE RISK ENGINE                       |
+--------------------------------------------------------------------------------+
|                                                                                |
|  2. Real-Time Telemetry Ingestion (Tatum Gateway / RPC)                       |
|     - Fetches live SUI/USDC exchange rates & checkpoint metadata               |
|                                                                                |
|  3. Vector Similarity Memory Retrieval (Walrus / MemWal <400ms)                |
|     - Queries @mysten-incubation/memwal relayer across persistent blobs        |
|     - Computes cosine similarity against past adverse regime clusters          |
|                                                                                |
|  4. Probabilistic Belief Calibration (Brier Scoring Formula)                  |
|     - Applies Bayesian memory penalty: P_calibrated = P_raw * (1 - lambda * sim)|
|     - Compresses leverage: Leverage_max = 1 / (1 - P_calibrated)               |
|     - Enforces wipeout buffer: Wipeout_buffer = (1 / Leverage) - Margin_maint  |
|                                                                                |
|  5. Pre-Trade Intercept Decision                                               |
|     - SQUEEZE DETECTED: Clamps 3x leverage down to 2x (Buffer: 33.3% -> 50.0%) |
|     - CAPITAL PROTECTED: Calculates explicit avoided drawdown in USDC          |
+--------------------------------------------------------------------------------+
                 │
                 │ 6. Dispatches HTTP 402 Payment-Required Header
                 ▼
+--------------------------------------------------------------------------------+
|                   HTTP 402 ON-CHAIN MICROPAYMENT GATEWAY                       |
+--------------------------------------------------------------------------------+
|  7. Client signs and broadcasts 0.05 SUI transfer to merchant wallet           |
|  8. api/x402/check.ts inspects balanceChanges via SuiGrpcClient                |
|  9. Asserts recipient == 0xaff0cc... and net delta >= +50,000,000 MIST         |
| 10. Replay Attack Prevention: Caches claimed tx digests, returns 409 Conflict  |
| 11. Emits cryptographically verified receipt and unlocks full execution proof  |
+--------------------------------------------------------------------------------+
```

### Key Engineering Decisions

1. **Decoupled Asynchronous Memory Architecture:** Walrus blob commits require standard epoch/checkpoint finality. Rather than blocking millisecond trading executions on write latency, RogueTrader performs ultra-fast vector retrieval (<400ms) on indexed read pathways and dispatches memory persistence asynchronously.
2. **Deterministic On-Chain Verification Over Trust:** The x402 payment gate does not rely on third-party payment gateways. It communicates directly with official Sui Mainnet nodes via `@mysten/sui/grpc`, inspecting native `balanceChanges` structs to mathematically prove transfer execution before issuing access receipts.
3. **Replay Protection via In-Memory Digest Cache:** Every verified transaction digest is cached. Any attempt to replay a historical transaction digest to unlock multiple risk queries is rejected with HTTP `409 Conflict`.
4. **Brier Calibration Formula:**
   ```text
   Brier Score = (1/N) * sum((forecast_t - outcome_t)^2)
   ```
   Across the 12-regime empirical benchmark, uncalibrated agents registered an average Brier error of `0.6108` (severe overconfidence). RogueTrader's memory-anchored calibration compressed the Brier score to `0.1539`—a **74.8% error reduction** (and up to 72.6% peak leverage compression during the Oct 14 NAVI squeeze).

---

## D. Verification Evidence & Claims

| Claim ID | Claim Description | Evidence Source | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-ROGUETRADER-001` | Built and deployed Pre-Trade Risk System on Sui Mainnet with Walrus decentralized memory (`@mysten-incubation/memwal`). | Sui Mainnet Account `0xf7bbb...`, Package `0xe7c16...`, 15 Walrus Blobs | **E1** |
| `CLM-ROGUETRADER-002` | Implemented HTTP 402 micropayment gate with Sui gRPC `balanceChanges` on-chain verification and replay-attack cache. | `api/x402/check.ts`, verified tx digest `5VGXV3D6nT8N3vw67LyJTXRQNkiLY8bLaJoAs1iqEJ2N` | **E1** |
| `CLM-ROGUETRADER-003` | Reduced directional forecast Brier error from 0.6108 to 0.1539 (74.8% error reduction) across 12 empirical market regimes. | `src/services/agentEngine.ts`, `BLOG_POST.md` | **E2** |
| `CLM-ROGUETRADER-004` | Built full-stack production trading desk with live Tatum RPC telemetry, Ruled Bento Grid, and dynamic digest input. | [`https://roguetrader.vercel.app`](https://roguetrader.vercel.app), commit `9ffcfee` | **E2** |

---

## E. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"RogueTrader is a Pre-Trade Risk System on Sui that prevents autonomous agents from hallucinating high-confidence leverage into market squeezes by checking proposed trades against persistent Walrus regime memory, monetized via on-chain HTTP 402 micropayments."*
- **30-Second Technical Walkthrough:**  
  *"Stateless trading agents blow up because their context window only sees the last 15 minutes of candles; they can't remember that an 80% borrow rate on NAVI triggered an 8% cascade two weeks ago. RogueTrader intercepts trade intents pre-execution. It runs sub-400ms vector similarity lookups against 15 Walrus Mainnet memory blobs via MemWal, penalizes the agent's confidence score, and forces leverage down from 3x to 2x. To unlock the risk certificate, the agent settles an on-chain HTTP 402 micropayment in SUI, which our backend verifies via Sui gRPC by inspecting balance changes directly on the ledger."*
