# Project Dossier: The Last Pavilion (Real-Time Ephemeral Survival Arena on Solana)

**Dossier Generation Date:** November 10, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Source:** Remote GitHub (`Olalolo22/last-pavilion`) / Local Workspace (`/home/lala_02/last-pavilion`)  
**Access Level:** Public / Open Source  
**Latest Verified Commit:** `eec244c` (`fix(timing): synchronize 1:1 real-clock timer seconds, calibrate Council extinction to ~18s, label button +50 ENERGY (-10 INF)`)  
**Evidence Standard:** E1 (Deployed Program ID on Solana Devnet) / E2 (Anchor Smart Contract, Real-Time Tick Engine, Sound Synth)

---

## A. Identity and Purpose

- **Project Name:** The Last Pavilion
- **Repository URL:** [`https://github.com/Olalolo22/last-pavilion`](https://github.com/Olalolo22/last-pavilion)
- **Relevant Branch:** `main`
- **What It Does:** A high-frequency multiplayer survival arena built on Solana utilizing MagicBlock Private Ephemeral Rollups (PER). Eight distinct factions drain energy continuously toward zero in real time. Players allocate scarce Influence to sustain their favored faction; when any faction collapses, its extinction permanently accelerates the drain speed of all remaining survivors, triggering an escalating death-refund salvage mechanic.
- **Specific Problem Addressed:** Web3 games frequently suffer from multi-second transaction latency, clumsy wallet confirmation popups on every tick, and boring turn-based pacing. The Last Pavilion demonstrates sub-50ms real-time state machine mechanics inside Ephemeral Rollups where custody and round settlement guarantee trustless L1 state anchoring on Solana.
- **Context & Tracks:** Built for **MagicBlock Blitz 9 / Colosseum Crypto's World Fair**.

---

## B. Implementation Status

- **Classification:** **Deployed on Solana Devnet & Fully Functional Real-Time Game Loop**
- **Verified On-Chain & Deployment Identifiers:**
  - **Solana Devnet Program ID:** `38iyWaZXa4nAZZxGYEGA6GqXhWE5g1dPt9ht9iFcxo63`
  - **Framework Version:** Anchor 0.29.0
  - **Execution Architecture:** MagicBlock Private Ephemeral Rollup (PER)
- **Verified Components:**
  - [x] **Smart Contracts (Solana Anchor / Rust):** Manages nation account state, Influence debiting, decay rates, elimination events, and death refund pool accounting.
  - [x] **Real-Clock Synchronization Engine:** Synchronizes client and rollup state 1:1 against wall-clock timestamps, preventing visual drift and timing exploits.
  - [x] **Web Audio Synthesizer:** Built-in retro audio engine with Web Audio singleton management, preventing browser audio context exhaustion under high-frequency tick sound triggers.
  - [x] **Interactive HUD:** Live progress bars, 1-click intervention (+50 Energy for -10 Influence), death refund claims, and sound controls.

---

## C. Technical Architecture

```
[ 8 Nations in Arena: Velocity, Shadow, Vault, Flow, Commons, Forge, Council, Genesis ]
                                      │
                                      ▼
+--------------------------------------------------------------------------------+
|             REAL-TIME DECAY TICK STATE MACHINE (Ephemeral Rollup)              |
+--------------------------------------------------------------------------------+
|  1. Continuous Meter Drain: Base Rate = -λ * dt                                |
|  2. Player Intervention: Spends 10 Influence -> +50 Energy (1s cooldown)       |
|  3. Nation Extinction Trigger: Energy <= 0 -> Status = FALLEN                  |
|  4. Escalation Factor: Drain_rate = Base_rate * (1 + 0.25 * Fallen_count)      |
|  5. Salvage Pool: 30 Influence pooled to reward supporters who pivot           |
+--------------------------------------------------------------------------------+
                                      │
                                      ▼
+--------------------------------------------------------------------------------+
|                     SOLANA L1 SETTLEMENT (Anchor 0.29)                         |
+--------------------------------------------------------------------------------+
|  Program ID: 38iyWaZXa4nAZZxGYEGA6GqXhWE5g1dPt9ht9iFcxo63                    |
|  - Validates session state transitions                                         |
|  - Settles final winner and distributes round rewards                          |
+--------------------------------------------------------------------------------+
```

### Key Engineering Decisions

1. **1:1 Real-Clock Synchronization Over Blind Tick Loops:** In browser-based Web3 games, browser tab switching can freeze `requestAnimationFrame` or `setInterval`, causing desynchronization with the validator. The Last Pavilion anchors decay rates to monotonic wall-clock delta times (`Date.now()`), recalculating exact state dynamically upon tab refocus.
2. **Web Audio Singleton Context Management:** Browsers impose strict limits (typically 6) on simultaneous `AudioContext` instances. Creating contexts per sound effect quickly throws `DOMException: The number of hardware contexts provided has reached the maximum`. The codebase enforces a single persistent audio context dispatcher with synthesized oscillators.
3. **Escalating Drain Feedback Loop:** By multiplying decay speed inversely with the count of remaining nations, rounds naturally compress from 2 minutes down to high-intensity 15-second survival endgames.

---

## D. Verification Evidence & Claims

| Claim ID | Claim Description | Evidence Source | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-PAVILION-001` | Deployed real-time 8-nation survival game on Solana Devnet (`38iyWaZXa4nAZZxGYEGA6GqXhWE5g1dPt9ht9iFcxo63`) with Anchor 0.29 and Ephemeral Rollups. | Solana Devnet Explorer, `programs/` | **E1** |
| `CLM-PAVILION-002` | Engineered 1:1 real-clock monotonic synchronization and audio singleton engine avoiding browser thread lockups. | Commit `eec244c`, `commit 329ab0a`, `src/utils/audio.ts` | **E2** |
| `CLM-PAVILION-003` | Implemented escalating decay curve with death-refund salvage mechanics for MagicBlock Blitz 9. | `README.md`, `src/components/PavilionArena.tsx` | **E2** |

---

## E. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"The Last Pavilion is an on-chain real-time survival arena on Solana where 8 factions continuously drain toward extinction, demonstrating sub-50ms execution and escalating death-refund economics inside Ephemeral Rollups."*
- **30-Second Technical Walkthrough:**  
  *"Built for MagicBlock Blitz 9, The Last Pavilion solves the problem of sluggish Web3 gaming by running high-frequency gameplay inside an Ephemeral Rollup anchored to Solana Devnet. Eight competing philosophies drain energy every tick. Players spend Influence to boost their faction, but every time a nation dies, the remaining nations drain 25% faster. If your faction falls, you can claim a salvage refund from the death pool to back another survivor. The whole state machine runs at 60 fps using monotonic wall-clock delta sync and an audio singleton engine to prevent Web Audio browser crashes."*