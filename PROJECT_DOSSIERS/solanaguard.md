# Project Dossier: SolanaGuard (Autonomous Token Intelligence & Risk Agent)

**Dossier Generation Date:** October 3, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Source:** Remote GitHub (`Olalolo22/TG-ct-auto-checker`)  
**Access Level:** Public Repository (Inspected via GitHub API)  
**Latest Verified Commit:** `2026-05-21T08:03:47Z` (`docs: add detailed SolanaGuard README with architecture, status and roadmap`)  
**Evidence Standard:** E1 (Code & Architecture Spec) / E2 (Commit Records)

---

## A. Identity and Purpose

- **Project Name:** SolanaGuard 🛡️ (Internal Repo: `TG-ct-auto-checker`)
- **Repository URL:** [`https://github.com/Olalolo22/TG-ct-auto-checker`](https://github.com/Olalolo22/TG-ct-auto-checker)
- **Relevant Branch:** `main`
- **What It Does:** Autonomous on-chain agent monitoring newly launched Raydium liquidity pools on Solana, scanning smart contract code and liquidity parameters for rug-pull vulnerabilities using multi-modal AI models, generating visual risk cards and vocal audio alerts, and broadcasting findings directly to Telegram channels—entirely self-funded via on-chain `x402` micropayments.
- **Specific Problem Addressed:** High-velocity memecoin launches on Solana (e.g., Raydium, Pump.fun) are plagued by malicious rug-pulls, mint authority traps, and liquidity draining. Retail traders lack the time and technical tooling to parse contract state in seconds. Most alert bots are centralized and require off-chain subscriptions.
- **Context & Hackathon:** Built for the **OOBE Protocol × AceData Cloud Hackathon** (Target Category: *Ace Data Cloud Usage / x402 Facilitator*).

---

## B. Implementation Status

- **Classification:** **Implemented and Verified in Prototype / Hackathon Submission**
- **Verified Components:**
  - [x] **Autonomous Discovery Engine:** Listens to Solana Raydium pool creation transactions via RPC / Synapse Sentinel agent.
  - [x] **Risk Analysis Pipeline:** Sends token metadata and contract bytecode to Claude 3 Haiku for heuristic vulnerability scanning (liquidity lock, mint authority, freeze authority, top holder concentration).
  - [x] **Multi-Modal Generation Layer:**
    - Generates a visual trading / risk scorecard via Flux image generation API.
    - Generates a vocal threat alert voice note MP3 via Fish Audio TTS API.
  - [x] **On-Chain Micropayment Integration (`x402`):** Implements HTTP 402 / payment-required flows where agent service costs and downstream API calls are authenticated and settled on-chain via Solana micropayments.
  - [x] **Automated Telegram Broadcaster:** Posts multi-modal alert packages (analysis text, image card, audio alert) directly into subscriber Telegram channels without manual intervention.

---

## C. Technical Architecture

### The Autonomous Multi-Modal Loop
```
[ Raydium Pool Launch on Solana ]
               │
               ▼
[ Synapse Sentinel / RPC Discovery ]
               │
               ▼
   [ Claude 3 Haiku Scanner ] ──(Risk Score & Heuristics)
               │
         ┌─────┴────────────────────────┐
         ▼                              ▼
[ Flux Image Generation ]      [ Fish Audio TTS ]
(Visual Threat Card PNG)       (Voice Warning MP3)
         │                              │
         └──────────────┬───────────────┘
                        ▼
         [ Telegram Broadcast Bot ]
                        ▲
                        │
       [ x402 On-Chain Micropayments ]
```

---

## D. Engineering Depth & Key Learnings

1. **Protocol Micropayments (`x402` Facilitator):**
   - Implemented autonomous agent payment loops where API requests trigger HTTP 402 Payment Required challenges that the agent signs and settles on-chain, proving practical experience with machine-to-machine economic settlement.
2. **Multi-Modal Pipeline Orchestration:**
   - Coordinated asynchronous dependencies across text analysis (LLM), graphic synthesis (Flux), audio generation (Fish Audio), and messaging networks (Telegram), handling failure retries across external AI providers.
3. **Solana Token Security Heuristics:**
   - Evaluated critical Solana SPL token risk factors: mint authority non-revocation, freeze authority retention, LP token non-burn/lock, and holder clustering.

---

## E. Claims Ledger Entries

| Claim ID | Claim Description | Evidence Source | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-SOLGUARD-001` | Built SolanaGuard: autonomous Solana token intelligence agent monitoring Raydium pool launches for rug-pull vulnerabilities. | `Olalolo22/TG-ct-auto-checker:README.md`, `src/` | **E1 / E2** |
| `CLM-SOLGUARD-002` | Integrated multi-modal AI pipeline synthesizing text heuristics, Flux visual cards, and Fish Audio vocal alerts. | `package.json`, `src/` | **E1 / E2** |
| `CLM-SOLGUARD-003` | Implemented x402 on-chain payment flow for machine-to-machine agent API settlement during the OOBE x AceData Hackathon. | `README.md`, `src/` | **E1 / E2** |

---

## F. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"SolanaGuard is an autonomous agent that monitors Raydium pool launches, conducts automated multi-modal risk assessments using Claude 3 and Flux, broadcasts vocal and visual alerts to Telegram, and self-funds its operations through on-chain x402 micropayments."*
- **30-Second Technical Overview:**  
  *"During the OOBE x AceData Cloud Hackathon, I built an end-to-end token security agent. The challenge was making an agent that operates autonomously without recurring credit card charges. I wired an RPC listener for new Raydium liquidity pairs, streamed contract state to Claude 3 Haiku for freeze and mint authority auditing, piped the output into Flux for scorecard generation and Fish Audio for audio alerts, and monetized the execution loop using the x402 HTTP micropayment protocol on Solana."*
