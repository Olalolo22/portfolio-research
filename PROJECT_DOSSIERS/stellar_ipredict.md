# Project Dossier: Stellar-iPredict (Optimistic Prediction Market Protocol)

## 1. Executive Summary
- **Project Name:** Stellar-iPredict
- **Upstream Repository:** `Stellar-iPredict/Stellar-iPredict`
- **Contributor Fork:** `Olalolo22/Stellar-iPredict`
- **Contribution Model:** Core Open-Source Contributor (Integration Testing, Oracle Lifecycle Verification, Fail-Closed Security, Contract Upgrade Engineering)
- **Primary Tech Stack:** Rust (Soroban Smart Contracts), TypeScript / Node.js, Jest / Vitest, PostgreSQL (Drizzle ORM)
- **Core Engineering Significance:** Engineered the comprehensive 1,388-line end-to-end integration test suite verifying the complete optimistic oracle lifecycle (bond deposits, assertion windows, challenge disputes, slashing, and market settlement) and enforced fail-closed API route authorization.

---

## 2. Verified Contributions & PR Highlights

### A. Full Optimistic Oracle Lifecycle E2E Suite (`#541`)
- **Scope:** In prediction markets, the oracle resolution state machine is the highest-risk surface. Incorrect dispute timing or slashing logic leads to permanent fund drain.
- **Code Change (`test/issue-541-oracle-lifecycle-e2e`):**
  - Commit `eac30e5`: `test(e2e): add end-to-end test covering full optimistic oracle lifecycle (#541)`
  - Added +1,388 lines of rigorous integration tests in `markets.integration.test.ts`.
  - Tested:
    1. Market creation and liquidity initialization.
    2. Proposer bond commitment.
    3. Dispute window countdown and optimistic finalization.
    4. Malicious assertion challenge and disputer bond matching.
    5. Disputer victory / proposer slashing and collateral redistribution.
  - Commit `d8f8edf`: Fixed migration numbering sequence (renumbering market sort migration to `0029`), synchronized Drizzle schema snapshots, and updated dependency boundaries.

### B. Fail-Closed API Route Authentication Registry (`#548` / `#756`)
- **Scope:** Prevent unauthenticated API access to backend oracle and market management routes.
- **Code Change (`test/route-auth-registry-548`):**
  - Commit `1df5caa`: `test(backend): assert API route authentication registry and fail-closed enforcement (#548) (#756)`
  - Added architectural tests ensuring every newly registered API route defaults to fail-closed authentication unless explicitly whitelisted in a public route manifest.

### C. Contract Upgrade & Storage Compatibility Standards (`#538`)
- **Code Change (`docs/issue-538-contract-upgrade-storage-compatibility`):**
  - Commit `594bde1`: `docs(contracts): document upgrade procedure and storage compatibility rules (#538)`
  - Authored Soroban storage layout compatibility guidelines to prevent contract data corruption during WASM bytecode migrations.

---

## 3. Engineering Evidence & Traceability

- **Local Path:** `/home/lala_02/Stellar-iPredict`
- **Remote Fork:** `https://github.com/Olalolo22/Stellar-iPredict.git`
- **Key Branches:**
  - `test/issue-541-oracle-lifecycle-e2e` (+1,388 lines diff)
  - `test/route-auth-registry-548` (Fail-closed route enforcement)
  - `docs/issue-538-contract-upgrade-storage-compatibility`
