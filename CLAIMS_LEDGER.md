# Claims Ledger: Evidence Tiers & Master Claim Index

## 1. Evidence Tier Taxonomy

Every claim in this ledger is categorized into one of four strictly defined evidence tiers:
- **Tier E1 (Cryptographic & On-Chain Ground Truth):** Verified on-chain Program IDs, transaction signatures, deployed bytecode, live hardware probe responses, or live production deployments.
- **Tier E2 (Code & Commit Verified):** Verifiable in local source code, git commit logs, branch diffs, AST structures, or deterministic test suites.
- **Tier E3 (Design & Specification Verified):** Grounded in written architecture specifications, schema files, API contracts, or project RFCs.
- **Tier E4 (Unsubstantiated / Caveated):** Aspirational, mocked, or unverified claims that must **NOT** be stated without explicit qualification.

---

## 2. Master Claims Matrix

| Claim ID | Project | Engineering Domain | Claim Statement & Verified Metric | Evidence Tier | Primary Verification Reference |
|:---|:---|:---|:---|:---:|:---|
| **CLM-001** | Rescue | Confidential TEE / Solana | Deployed confidential liquidation dark pool on Solana Devnet (`ZnDqdjHjR1HuwyMehcfEGrxCt6QiCz58UW21VjbnGjf`) executed inside Intel TDX TEE via MagicBlock Private Ephemeral Rollups. | **E1** | Program ID verified; Anchor error 3007 MEV lock; 7/7 live hardware probes passed; Settlement tx `3oJ6Ufzq...` |
| **CLM-002** | Rescue | Protocol Security | Eliminated front-running and MEV sandwiching on liquidations by locking accounts inside confidential enclaves, rejecting public RPC state reads with Anchor error 3007. | **E1** | Probe #5 returned `AnchorError: 3007`; `programs/rescue/src/lib.rs` |
| **CLM-003** | RugRoll | High-Frequency Solana | Engineered sub-10ms crash game loop on Solana Devnet (`DSfJQMFV36ib2Kd4c9bSkV9M9ZWmhhVCjTb7hhtACwyS`) using Ephemeral Rollups and gasless 1-click session keys. | **E1** | Program ID verified; `feat/onchain-er` branch; Anchor tests passing; 3% house edge formula |
| **CLM-004** | RugRoll | Systems Optimization | Bypassed cloud builder RAM limitations during Anchor Cargo compilation via single-codegen-unit, `-C opt-level=z`, and lld linker flags. | **E2** | `Cargo.toml` profile configurations; commit `7ce4ec2` |
| **CLM-005** | Harvest | DeFi Options / Oracles | Architected covered-call vault protocol on Solana Devnet (`34Y7acmqWosmkfPJjqRUQzrHFdxmxpQezLSvgD9bLJJo`) with Pyth Hermes oracle feeds for tokenized equities (`AAPLx`, `NVDAx`, `TSLAx`). | **E1** | Program ID verified; `programs/harvest/src/lib.rs`; autonomous keeper daemon `scripts/keeper.ts` |
| **CLM-006** | Harvest | Token-2022 Integration | Implemented Token-2022 compatibility for synthetic yield-bearing share mints (`hShare`) with autonomous epoch rollover keepers. | **E2** | +1,780 lines on `design-v2`; `src/lib.rs` |
| **CLM-007** | Aegis Ledger | Confidential Payroll | Engineered dual-rail confidential USDC payroll platform on Solana combining MagicBlock TEE (<1s batches) and Cloak ZK proofs. | **E2** | Branch `feat/colosseum-usdc-payroll` (+1,553 lines); `src/components/CsvImporter.tsx`; ed25519 curve checks |
| **CLM-008** | Mizan | ZK Circuits / SP1 zkVM | Built Succinct SP1 RISC-V zero-knowledge circuit verifying DocuSign PDF PKCS#7 RSA/SHA-256 signatures and SEC Rule 501(a) accreditation without exposing PII. | **E2** | `sp1-sukuk-prover/program/src/main.rs`; regex pattern matching; document nullifier hash |
| **CLM-009** | Mizan | Smart Contracts / EVM | Deployed Solidity verifier contracts (`ZKSukukGate.sol`, `SukukToken.sol`, `SukukDistributor.sol`) on X Layer / Sepolia, resolving 32-byte EVM ABI proof alignment. | **E2** | Branch `fix/evm-sp1-proof`; `contracts/src/ZKSukukGate.sol` |
| **CLM-010** | Sentinel | Autonomous Agent Node | Built sub-18ms Stage 1 deterministic rules engine enforcing T1–T8 threat taxonomy over incoming A2MCP agent execution quotes. | **E2** | `sentinel-node/src/engine/rules.ts`; 24 passing unit tests; Hono API server |
| **CLM-011** | Sentinel | EVM Staking Bond | Implemented `SentinelBond.sol` on X Layer managing slashing bonds for autonomous agent verification nodes. | **E2** | `contracts/SentinelBond.sol`; `@sentinel/sdk` |
| **CLM-012** | Finsa | Enterprise CMS / Backend | Architected Directus 11 + PostgreSQL 15 + Redis enterprise backend with 1,641-line relational snapshot, 13 custom collections, and 10 granular RBAC roles. | **E2** | `snapshot.json` (1,641 lines); `@finsa/directus-client` TypeScript SDK; automated Railway deployment scripts |
| **CLM-013** | SJ Consulting | Commercial Fintech / CBT | Architected full-lifecycle education platform on Supabase PostgreSQL (12 migrations, >130KB schema) with 8 Deno Edge Functions and HMAC-SHA512 Paystack webhook validation. | **E2** | `supabase/migrations/`; `supabase/functions/paystack-webhook/`; `cbt-start-session`; commit `42af5cf` |
| **CLM-014** | SJ Consulting | Database Optimization | Refactored PostgreSQL stored procedures to `SECURITY INVOKER` and resolved nested JSONB aggregation bottlenecks, reducing dashboard load times to a single sub-50ms RPC. | **E2** | `20261001000004_fix_dashboard_rpc_security_invoker.sql`; `20261001000003_fix_nested_agg_dashboard_rpc.sql` |
| **CLM-015** | RouteDock | Smart Contract Security | Hardened Soroban agent vault by eliminating unauthenticated `initialize` front-running vulnerability, moving configuration into contract constructor (#313). | **E2** | Commit `f65324e`; `fix/issue-313-vault-constructor`; Rust type annotations |
| **CLM-016** | RouteDock | High-Concurrency Node.js | Fixed Fastify reply stream hijacking bug (#311) on settled pass-through routes, preventing unhandled stream exceptions under concurrent micropayment traffic. | **E2** | Commit `b9f4fd6`; `fix/issue-311-fastify-reply-hijack`; PR #498 merged to upstream |
| **CLM-017** | Stellar-iPredict | Protocol Verification | Authored complete 1,388-line end-to-end integration test suite verifying optimistic oracle proposal, dispute windows, bond slashing, and market resolution (#541). | **E2** | Commit `eac30e5` in `markets.integration.test.ts`; `test/issue-541-oracle-lifecycle-e2e` |
| **CLM-018** | Disciplr | Authentication Security | Remediated CWE-798 (Hardcoded Credentials) by eliminating insecure JWT fallback secrets, enforcing deterministic fail-closed process termination in production (#1652). | **E2** | Commit `94880da` in `fix/issue-1652-oauth-jwt-secret`; +347 lines diff |
| **CLM-019** | Credence | Smart Contract Metering | Authored 1,316-line boundary and recovery test suite in `cost.rs` asserting Soroban CPU instruction and memory byte metering limits for decentralized credit bonds (#1313). | **E2** | Commit `613b7294b` in `Credence-Contracts:test/issue-1313-cost-benchmark-boundary-recovery` |
| **CLM-020** | SolanaGuard | AI Security / x402 | Built real-time Solana transaction scanner with x402 on-chain micropayment settlement, Claude 3 Haiku risk analysis, and automated Telegram alerts. | **E2** | `TG-ct-auto-checker/src/`; x402 facilitator integration; Flux card generation |
| **CLM-021** | Persist | Decentralized Storage | Built multi-agent memory persistence platform on Sui Move with Walrus decentralized blob storage, Seal threshold encryption, and deterministic recovery. | **E2** | `contracts/persist/`; Walrus blob storage client; 6 git branches audited |
| **CLM-022** | School of Solana | Solana Certification | Completed Ackee Blockchain School of Solana Season 8, developing native instruction handlers, PDAs, and full Anchor capstone tipping protocol (`tip_project`). | **E2** | `School-of-Solana/program-Olalolo22`; `Ackee_001`; tasks 1–4 verified |
| **CLM-023** | HNG13 | Asynchronous Microservices | Passed multiple qualification rounds in HNG Internship Cohort 13, building high-throughput Python REST APIs and an autonomous Telex AI agent daemon. | **E2** | `HNG13_0`, `HNG13_1`, `HNG13_2`, `HNG13_3_Agent` |
| **CLM-024** | ALX | Low-Level Systems | Completed rigorous C systems engineering curriculum: manual memory management (`malloc`/`free`), pointer arithmetic, data structures, and POSIX process lifecycles. | **E2** | `alx-low_level_programming`; `alx-higher_level_programming`; Betty style compliance |

---

## 3. Disallowed & Caveated Claims (Tier E4 Guardrails)

The following claims are strictly prohibited from CVs and interviews unless explicitly qualified:
1. **DO NOT CLAIM:** "Sole creator/author of RouteDock or Stellar-iPredict."
   - *Truth:* Core open-source contributor. Authored critical security fixes, oracle test suites, and constructor hardening PRs to existing codebases.
2. **DO NOT CLAIM:** "Processed millions of dollars in live mainnet transactions for Rescue or Harvest."
   - *Truth:* Deployed and verified on Solana Devnet with real empirical TEE hardware probes and Pyth Hermes oracle feeds.
3. **DO NOT CLAIM:** "Invented the Intel TDX TEE architecture."
   - *Truth:* Pioneered application of MagicBlock Private Ephemeral Rollups to MEV-resistant dark pools and sub-10ms state loops.
