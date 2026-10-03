# Project Dossier: Persist (Temporal Access Control for Sui)

**Dossier Generation Date:** October 3, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Source:** Remote GitHub (`Olalolo22/Persist`)  
**Access Level:** Private Repository (Authenticated via GitHub API)  
**Latest Verified Commit:** Merge pull request #2 (`2026-06-27T09:16:56Z`)  
**Evidence Standard:** E1 (Direct Code & Docs in Repo) / E2 (Git History & Hackathon Submission Specs)

---

## A. Identity and Purpose

- **Project Name:** Persist
- **Repository URL:** [`https://github.com/Olalolo22/Persist`](https://github.com/Olalolo22/Persist) (Private)
- **Relevant Branch:** `main`
- **What It Does:** Temporal Access Control protocol on Sui. Creates cryptographically sealed data capsules — condition-gated, time-locked, encrypted via Seal, and stored permanently on Walrus — that unlock autonomously only when predefined on-chain conditions are satisfied.
- **Specific Problem Addressed:** Existing decentralized storage lacks native time- or condition-bound decryption without relying on centralized key custodians. If a user, autonomous agent, or organization disappears or fails to check in, there is no trustless mechanism on-chain to unlock vital keys, documents, or succession state without human intervention.
- **Intended Users:** 
  1. Autonomous AI agents requiring succession continuity and external memory failovers.
  2. DAOs requiring automated contingency execution upon governance stalemates.
  3. Individual users establishing non-custodial digital inheritance and emergency data release.
- **Context & Tracks:** Built for **Sui Overflow 2026** (submitted across both the **Walrus** and **Agentic Web** tracks).

---

## B. Implementation Status

- **Classification:** **Implemented and Verified in Prototype / Hackathon Submission**
- **Verified Components:**
  - [x] **Smart Contracts (Sui Move):** Located in `contracts/`. Implements capsule creation, time-lock thresholds, condition checking, and on-chain blob ID registration.
  - [x] **Walrus Storage Integration:** Three-layer integration architecture:
    1. Core permanent blob storage for Seal-encrypted payload data.
    2. Agent operational memory persistence (`MemWal`).
    3. Condition-release verification blobs.
  - [x] **Seal Encryption Integration:** Threshold encryption ensuring data remains completely sealed until the Move contract emits the verifiable condition-satisfaction signal.
  - [x] **Guardian Agent (`agent/`):** Autonomous agent monitoring liveness, attesting condition triggers, and managing capsule lifecycle.
  - [x] **Submission Specs:** Authored `SUBMISSION_WALRUS.md`, `SUBMISSION_AGENTIC.md`, and `ROADMAP.md`.

---

## B.1 Remote Branches & Iteration History on GitHub (6 Branches Audited)

The GitHub repository (`Olalolo22/Persist`) contains 6 distinct remote branches documenting the rapid iterative development for Sui Overflow 2026:

| Branch Name | Latest Commit | Date | Verified Engineering Scope & Features |
| :--- | :---: | :---: | :--- |
| **`main`** | `df270a66` | 2026-06-27 | Production submission freeze merging PR #2 (`nifemi-version`), integrating full Move contracts, Walrus storage, and agent specs. |
| **`overflow-v3`** | `ce4f0c06` | 2026-06-18 | **Agent Succession Engine & Telemetry:** Built agent succession UI, wired live state counters, and fixed build errors in the agent worker. |
| **`new-design-v4`** | `901f51ab` | 2026-06-24 | **Documentation Specification:** Finalized public and internal developer documentation, Walrus integration guides, and security assumptions. |
| **`nifemi-version`** | `fd558515` | 2026-06-21 | **Responsive UI & Animations:** Polished capsule creation drawers, unlock countdown modals, and responsive layout adjustments. |
| **`PersistDesignAid`** | `df2f0b92` | 2026-06-21 | **Landing Page Architecture:** Initial landing page build, purged unused configs, and established cohesive visual theme. |
| **`experiment-new-design`** | `4b08dc32` | 2026-06-20 | Exploratory design branch testing interactive capsule inspection views. |

---

## C. Technical Architecture

### Component Diagram & Flow
```
[ User / Autonomous Agent ]
         │
         │ 1. Encrypt payload via Seal (Threshold Crypto)
         ▼
[ Seal Encrypted Payload ] ────▶ [ Permanent Walrus Blob Storage ]
         │                                       ▲
         │ 2. Register Capsule (Blob ID + Condition)│
         ▼                                       │
[ Sui Move Smart Contract ]                      │ (Blob ID Reference)
         │                                       │
         │ 3. Condition/Heartbeat Met?           │
         ├─── Yes ───▶ Emit Decryption Key Event ┘
         └─── No  ───▶ Capsule Remains Sealed
```

### Key Engineering Decisions
1. **Separation of Storage from Access Condition:** Walrus provides permanent, immutable decentralized data storage, but Walrus does not enforce access control. By combining Walrus with Seal threshold encryption and Sui Move execution, Persist ensures data availability is decoupled from data accessibility.
2. **Autonomous Agent Continuity:** For the Agentic Web track, Persist implements a "Dead Man's Switch" for AI agents: if an agent's heartbeat stops, its memory state in Walrus is unlocked for successor agents, preventing catastrophic loss of autonomous operational context.

---

## D. Verification Evidence & Claims

| Claim ID | Claim Description | Evidence Source | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-PERSIST-001` | Designed and implemented "Temporal Access Control for Sui" combining Sui Move, Seal encryption, and Walrus storage. | `Olalolo22/Persist:README.md`, `contracts/` | **E1 / E2** |
| `CLM-PERSIST-002` | Built three-layer Walrus integration for Sui Overflow 2026 (Core storage, Agent memory extension, Succession triggers). | `SUBMISSION_WALRUS.md`, `agent/` | **E1 / E2** |
| `CLM-PERSIST-003` | Implemented autonomous Guardian Agent capable of condition attestation and memory recovery. | `agent/`, `SUBMISSION_AGENTIC.md` | **E1 / E2** |

---

## E. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"Persist is a temporal access control protocol built for Sui that creates cryptographically sealed, condition-gated capsules stored permanently on Walrus, ensuring trustless continuity for autonomous agents, DAOs, and digital inheritance."*
- **30-Second Technical Walkthrough:**  
  *"During Sui Overflow 2026, I built Persist across the Walrus and Agentic Web tracks. The core problem was that decentralized storage is publicly accessible, while private data requires access conditionality. I integrated Seal threshold encryption with Sui Move smart contracts and Walrus blob storage. Sensitive agent operational state or inheritance data is encrypted with Seal and written to Walrus. The Sui Move contract enforces condition validation (such as heartbeat timeouts or multi-sig triggers); once satisfied, the contract authorizes threshold key reconstruction, releasing the capsule trustlessly."*
