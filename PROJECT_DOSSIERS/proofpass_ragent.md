# Project Dossier: ProofPass & Ragent (ZK Compliance & Agent Marketplace)

## 1. Executive Summary
- **Projects:** ProofPass (`ProofPass`) & Ragent (`Ragent`)
- **Role & Ownership:** Lead Architect & Protocol Engineer
- **Tech Stack:**
  - **ProofPass:** Rust, Succinct SP1 zkVM, Groth16, Soroban Smart Contracts, Next.js
  - **Ragent:** Node.js / TypeScript, FastAPI / Python, Smart Contracts, Vercel Serverless, Agent Coordinator
- **Core Engineering Significance:**
  - **ProofPass:** Zero-knowledge accreditation credentialing system verifying DocuSign PDF signatures in SP1 zkVM and settling Groth16 zk-SNARK verification on Stellar/Soroban. Direct technological precursor to Mizan.
  - **Ragent:** Decentralized AI agent procurement and orchestration marketplace featuring autonomous coordinator daemons, task escrow contracts, and dynamic worker bidding.

---

## 2. Key Technical Implementations

### A. ProofPass: Soroban ZK Investor Gating
- **ZK Circuit & Verifier:** Implemented `sp1-zk-accredited-investor` circuit generating Groth16 SNARK proofs (`proof.json`, `groth16_vk.bin`) over investor attestations (`attestation.pdf`).
- **On-Chain Settlement:** Deployed `soroban-zk-investor-gate` smart contract verifying SNARK proofs on Stellar testnet to gate restricted investment pools without exposing PII.

### B. Ragent: Agent Coordinator & Task Lifecycle
- **Autonomous Agent Daemon:** Engineered the `coordinator/` runtime managing task assignment, state transitions, heartbeat liveness monitoring, and verifiable delivery attestations.
- **Production Debugging:** Solved critical serverless runtime issues documented in `vercel_debugging_log.md` and authored autonomous external agent integration roadmap (`ROADMAP.md`).

---

## 3. Engineering Evidence & Traceability

- **Local Paths:**
  - `/home/lala_02/ProofPass`
  - `/home/lala_02/Ragent`
- **ProofPass Key Artifacts:** `IMPLEMENTATION_PLAN.md`, `groth16_vk.bin`, `proof.json`, `soroban-zk-investor-gate`
- **Ragent Key Artifacts:** `coordinator/`, `contracts/`, `DEMO_SCRIPT.md`, commit `f8cce71` (`docs(roadmap): add autonomous external agents implementation plan`)
