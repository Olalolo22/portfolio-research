# Project Dossier: Aegis Ledger (Confidential USDC Payroll on Solana)

**Dossier Generation Date:** October 3, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Path:** [`/home/lala_02/aegis-ledger`](file:///home/lala_02/aegis-ledger)  
**Remote URL:** [`git@github.com:Olalolo22/aegis-ledger.git`](https://github.com/Olalolo22/aegis-ledger)  
**Active Production Branch:** [`feat/colosseum-usdc-payroll`](file:///home/lala_02/aegis-ledger) (+5 commits ahead of `feature/zero-trust-refactor`)  
**Target Program / Platform:** Solana (Colosseum Eternal Track)  
**Evidence Standard:** **E1 (Dual-Rail Settlement Code, CSV Batch Engine, MagicBlock TEE Client)**

---

## A. Identity and Purpose

- **Project Name:** Aegis Ledger
- **Repository URL:** [`https://github.com/Olalolo22/aegis-ledger`](https://github.com/Olalolo22/aegis-ledger)
- **Active Working Branch:** `feat/colosseum-usdc-payroll`
- **What It Does:** Confidential, non-custodial USDC payroll protocol for Solana organizations, DAOs, and crypto-native teams. Solves the dual challenge of corporate transparency and employee privacy by implementing a **dual-rail settlement architecture**:
  1. **Instant Rail (MagicBlock TEE / Intel TDX):** Sub-50ms execution inside hardware enclaves for bulk organizational payroll (10–50+ contributors) with zero client-side WASM lag.
  2. **Shielded Rail (Cloak ZK):** Client-side Groth16 zero-knowledge proving for sovereign, mathematically un-linkable transactions.
  3. **Compliance Layer:** Scoped viewing keys enabling certified CPA auditors to inspect payroll books without exposing employee salary details on public block explorers.
- **Specific Problem Addressed:** When Web3 companies pay contributors on public Solana, wallet addresses, payment amounts, and salary intervals are visible to competitors, headhunters, and malicious actors on Solscan. Conversely, fully dark mixers are banned by compliance auditors.
- **Target Context:** Built for **Colosseum Eternal** ($250k track).

---

## B. Implementation Status & Branch Evolution

- **Classification:** **Implemented, Verified in Prototype, and Benchmarked**
- **Branch Evolution Across 4 Distinct Milestones:**
  1. **Milestone 1 — Single-Rail ZK Prototype (`feature/zero-trust-refactor` / `main`, May 15, 2026):**  
     Relied strictly on client-side Groth16 WASM proving in the browser (~30s/payment).
  2. **Milestone 2 — Strategic Positioning & Architecture Overhaul (`magic-mvp`, Sept 3, 2026):**  
     Authored [`MASTER_STRATEGY_DOSSIER.md`](file:///home/lala_02/aegis-ledger/MASTER_STRATEGY_DOSSIER.md) (+165 lines) and [`ROADMAP_SPEC.md`](file:///home/lala_02/aegis-ledger/ROADMAP_SPEC.md) (+117 lines), establishing the triad architecture (TEE + ZK + Viewing Keys).
  3. **Milestone 3 — Dual-Rail Settlement & Batch Importer ([`feat/colosseum-usdc-payroll`](file:///home/lala_02/aegis-ledger), Sept 24, 2026):**  
     **+1,553 lines of code added**, integrating MagicBlock Private Ephemeral Rollups and drag-and-drop CSV batch ingestion.

---

## C. Technical Architecture

```mermaid
flowchart TD
    subgraph ADMIN ["Corporate Payroll Administrator"]
        CSV["Drag-and-Drop CSV Importer (src/components/CsvImporter.tsx)"]
        SWITCH["Dual-Rail Selector (src/components/PayrollTerminal.tsx)"]
    end

    subgraph TEE_RAIL ["Rail A: High-Throughput TEE (devnet-tee.magicblock.app)"]
        ENCLAVE["MagicBlock Intel TDX Hardware Enclave"]
        SUB50["Sub-50ms Slot Execution (<1s Batch)"]
        MEMO["TEE Confidential Note Commitments"]
    end

    subgraph ZK_RAIL ["Rail B: Pure Cryptographic Privacy (Cloak ZK)"]
        WASM["Browser Groth16 WASM Prover"]
        R1CS["128,480 R1CS Constraints"]
        SNARK["192-byte zk-SNARK Proof"]
    end

    subgraph AUDIT ["Audit & Compliance Layer"]
        VIEW["Scoped Merkle Viewing Keys"]
        CPA["CPA Accountant / Tax Auditor Inspection"]
    end

    CSV --> SWITCH
    SWITCH -->|Bulk Payroll (10-50+ payees)| TEE_RAIL
    SWITCH -->|Single Sensitive Transfer| ZK_RAIL
    TEE_RAIL --> AUDIT
    ZK_RAIL --> AUDIT
```

---

## D. Engineering Depth & Key Implementations

1. **Hardware Enclave Client ([`src/lib/magicblock.ts`](file:///home/lala_02/aegis-ledger/src/lib/magicblock.ts)):**
   - Implemented `buildTeeBatchPayload` constructing batched transactions with 64-character cryptographic note commitments.
   - Routes bulk payments directly to the MagicBlock TEE RPC (`https://devnet-tee.magicblock.app`), eliminating the 30-second client-side Groth16 proving barrier.
2. **Enterprise Drag-and-Drop CSV Importer ([`src/components/CsvImporter.tsx`](file:///home/lala_02/aegis-ledger/src/components/CsvImporter.tsx)):**
   - 341 lines of TypeScript implementing client-side CSV parsing, Solana public key format validation, duplicate address detection, and total payroll allocation summaries.
3. **Dual-Rail Terminal UI ([`src/components/PayrollTerminal.tsx`](file:///home/lala_02/aegis-ledger/src/components/PayrollTerminal.tsx)):**
   - Interactive terminal UI exposing live step-by-step logs for both TEE enclave delegation (`TEE_LOG_STEPS`) and Groth16 constraint satisfaction (`ZK_LOG_STEPS`).
4. **Browser Runtime Hardening ([`src/hooks/usePayrollSigner.ts`](file:///home/lala_02/aegis-ledger/src/hooks/usePayrollSigner.ts)):**
   - Handled ed25519 on-curve validation, Buffer polyfills, and fail-closed state management for Web3 wallet providers.

---

## E. Claims Ledger Entries

| Claim ID | Claim Description | Source / Evidence | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-AEGIS-001` | Designed and implemented dual-rail confidential settlement architecture combining MagicBlock TEE and Cloak ZK. | [`src/lib/magicblock.ts`](file:///home/lala_02/aegis-ledger/src/lib/magicblock.ts), [`src/components/PayrollTerminal.tsx`](file:///home/lala_02/aegis-ledger/src/components/PayrollTerminal.tsx) | **E1 (Direct)** |
| `CLM-AEGIS-002` | Built enterprise CSV batch importer with client-side pubkey format and duplicate validation. | [`src/components/CsvImporter.tsx`](file:///home/lala_02/aegis-ledger/src/components/CsvImporter.tsx) | **E1 (Direct)** |
| `CLM-AEGIS-003` | Resolved client-side Groth16 WASM proving bottlenecks by shifting bulk payroll to sub-50ms TEE enclave slots. | [`src/lib/magicblock.ts:L7-13`](file:///home/lala_02/aegis-ledger/src/lib/magicblock.ts) | **E1 (Direct)** |
| `CLM-AEGIS-004` | Authored complete Colosseum Eternal positioning dossier and technical roadmap specification. | [`MASTER_STRATEGY_DOSSIER.md`](file:///home/lala_02/aegis-ledger/MASTER_STRATEGY_DOSSIER.md), [`ROADMAP_SPEC.md`](file:///home/lala_02/aegis-ledger/ROADMAP_SPEC.md) | **E2 (Docs)** |

---

## F. Limitations & Trade-Offs

1. **Hardware Enclave Trust Assumptions (TEE vs ZK):**  
   MagicBlock TEE provides sub-second speed for bulk batches, but relies on Intel TDX hardware isolation assumptions. Cloak ZK provides pure mathematical trustlessness, but imposes a ~30-second client-side proving penalty per batch. Aegis explicitly presents this as a configurable trade-off to the administrator.
2. **Devnet Validator State:**  
   The TEE rail requires active connectivity to MagicBlock's devnet TEE validator (`MTEWGuqx...`).

---

## G. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"Aegis Ledger is a confidential USDC payroll protocol on Solana that uses a dual-rail architecture — MagicBlock TEE for sub-second bulk batches and Cloak ZK for mathematical privacy — allowing organizations to disburse salaries privately with certified auditability."*
- **30-Second Technical Overview:**  
  *"Paying corporate payroll on public Solana exposes salary details on Solscan, while pure ZK in the browser takes 30 seconds per proof, creating terrible UX for 50-person payrolls. On the `feat/colosseum-usdc-payroll` branch, I resolved this by engineering a dual-rail settlement engine. Administrators drag and drop an employee CSV. For bulk runs, transactions execute inside a MagicBlock Intel TDX hardware enclave at sub-50ms speeds with note commitments. For single sensitive transfers, users can toggle to client-side Cloak Groth16 proving. Scoped Merkle viewing keys ensure CPAs can audit the books for tax compliance."*
