# Application Evidence Bank: Tailored Bullet Points, Pitches & Technical Interview Bank

## 1. Role-Tailored CV Bullet Points

### A. Backend & API Engineering Roles (Python, Node.js, TypeScript, PostgreSQL)
- **SJ Consulting (Commercial Deliverable):** Architected full-lifecycle education and testing platform on Supabase PostgreSQL (12 migrations, >130KB schema) and 8 Deno Edge Functions, implementing HMAC-SHA512 Paystack payment webhook validation and anti-cheat CBT state machines.
- **Finsa Directus Backend:** Designed and bootstrapped enterprise Directus 11 + PostgreSQL 15 + Redis backend featuring a 1,641-line relational snapshot across 13 custom collections, 10 granular RBAC policies, and an auto-generated `@finsa/directus-client` TypeScript SDK.
- **Disciplr Backend (Open Source):** Remediated CWE-798 (Hardcoded Credentials) vulnerability by eliminating insecure JWT fallback secrets, engineering deterministic fail-closed process termination for production environments (+347 lines diff).
- **RouteDock (Fastify Runtime):** Patched a high-concurrency stream reply hijacking bug in Fastify payment adapters on settled pass-through routes, preventing unhandled stream exceptions under concurrent micropayment traffic (#311).
- **MarketPadi (FastAPI):** Built modular asynchronous Python backend using FastAPI, SQLAlchemy, and Alembic, implementing multi-profile role schemas (Buyers, Vendors, Admins) and phone-based OTP authentication services.

---

### B. Infrastructure & Distributed Systems Roles (Rust, Systems, Docker, Linux)
- **Rescue (Solana & TEE):** Engineered confidential liquidation dark pool executing inside Intel TDX Trusted Execution Environments (TEE) via MagicBlock Ephemeral Rollups; validated MEV sandwich protection via 7 empirical hardware probes returning Anchor error 3007 on unauthorized public state reads.
- **RugRoll (High-Frequency State Loops):** Designed a sub-10ms decentralized game loop on Solana Ephemeral Rollups with gasless 1-click session keys; optimized Cargo build profiles (`opt-level = "z"`, single codegen unit) to bypass cloud builder RAM constraints.
- **Sentinel (Autonomous Node Infrastructure):** Engineered sub-18ms Stage 1 deterministic rules engine in TypeScript/Hono enforcing an 8-rule threat taxonomy (T1–T8) over incoming autonomous agent execution quotes, verified across 24 automated unit tests.
- **Credence Contracts (Metering & Gas Profiling):** Authored 1,316 lines of deterministic boundary and recovery test suites in Rust/Soroban (`cost.rs`), benchmarking CPU instruction and memory byte resource ceilings to guarantee atomic rollback during out-of-gas states.
- **Low-Level Systems (ALX):** Implemented custom memory allocation routines, pointer arithmetic algorithms, and POSIX process management in C adhering to strict Betty style and Valgrind memory-leak standards.

---

### C. Web3 & Protocol Engineering Roles (Solana Anchor, Soroban, Sui Move, SP1 zkVM)
- **Harvest (Solana Covered-Call Vaults):** Architected covered-call vault protocol on Solana Devnet (`34Y7acmqWosmkfPJjqRUQzrHFdxmxpQezLSvgD9bLJJo`) with Pyth Hermes oracle feeds, Token-2022 compatibility, and an autonomous TypeScript keeper daemon for automated epoch rollovers.
- **Mizan (SP1 zkVM & Sukuk Tokenization):** Developed Succinct SP1 RISC-V zero-knowledge circuit verifying DocuSign PDF PKCS#7 RSA/SHA-256 signatures and SEC Rule 501(a) accreditation without disclosing PII; deployed EVM Solidity verifier contracts resolving 32-byte ABI alignment challenges.
- **RouteDock (Soroban Smart Contracts):** Hardened Soroban agent vaults against front-running vulnerabilities by migrating mutable `initialize` routines into atomic contract constructor instantiations (#313).
- **Stellar-iPredict (Optimistic Oracles):** Authored 1,388-line end-to-end integration test suite in TypeScript/Soroban verifying the complete optimistic oracle lifecycle: bond collateralization, challenge dispute windows, slashing mechanics, and settlement resolution (#541).
- **Ackee School of Solana (Season 8):** Graduated from intensive Solana security fellowship; built PDA-based tipping protocol (`tip_project`) with Anchor account constraint validations, checked arithmetic, and reproducible Docker compilation.

---

### D. Fintech & High-Assurance Systems Roles
- **Paystack Webhook Settlement (SJ Consulting):** Engineered idempotent payment processing pipeline with cryptographic signature verification (HMAC-SHA512), dynamically unlocking candidate subscription tiers and recording audit trails.
- **x402 Micropayment Protocol (SolanaGuard):** Integrated HTTP 402 payment-required protocol with on-chain Solana micropayment settlement for real-time AI security scans.
- **PostgreSQL Performance Optimization (SJ Consulting):** Resolved complex nested JSONB subquery aggregation bottlenecks and refactored RPCs to `SECURITY INVOKER`, reducing student dashboard network roundtrips to a single sub-50ms query.

---

## 2. The 20-Second Pitch Bank (Elevator Summaries)

### Rescue (Confidential Dark Pool)
> *"On public blockchains, when a borrower is liquidated, predatory bots front-run the transaction and siphon value. Rescue moves liquidations into a private Intel hardware enclave where bot contracts literally cannot see the debt state, eliminating MEV entirely and returning fair market value to borrowers."*

### RugRoll (Sub-10ms State Machine)
> *"Blockchains are traditionally too slow for fast multiplayer action. RugRoll proves Solana can run sub-10ms real-time game loops inside Ephemeral Rollups with gasless session keys, settling balances back to L1 without users ever having to sign popups for each tick."*

### Mizan (Zero-Knowledge Accredited Investor Verification)
> *"Right now, investing in restricted assets like Sukuk bonds requires emailing passports and tax returns to strangers. Mizan lets an investor prove in zero-knowledge that DocuSign verified their accredited status using an SP1 RISC-V circuit, settling directly on an EVM contract without revealing a single line of private data."*

### SJ Consulting (High-Assurance Commercial Platform)
> *"I architected the backend for a commercial education platform using Supabase PostgreSQL and Deno Edge Functions. It handles university admission probability calculations, anti-cheat CBT exams with server-side scoring, realtime peer duels, and automated Paystack payment processing."*

---

## 3. Technical Interview Deep Dives (STAR Method)

### Question 1: "Tell me about a complex security vulnerability you identified and resolved."
- **Context:** While contributing to the open-source `Disciplr` backend (`#1652`), I audited the OAuth and JWT authentication middleware.
- **Problem:** The codebase was falling back to a default, hardcoded secret string (`'secret'`) if the `JWT_SECRET` environment variable was missing or empty. In production, this would allow an attacker to forge valid admin session tokens without compromising the host server.
- **Action:** I authored a comprehensive fix (+347 lines diff). First, I implemented deterministic fail-closed validation: if `NODE_ENV === 'production'` and `JWT_SECRET` is missing, empty, or fails entropy thresholds (minimum 32 characters), the server process immediately exits with a fatal error code during bootstrap. Second, I authored unit test suites asserting that the application fails to boot without credentials and verifying that tokens signed with the legacy fallback are strictly rejected with 401 Unauthorized.
- **Result:** The pull request eliminated CWE-798 vulnerabilities across all downstream production deployments and established automated CI security assertions.

---

### Question 2: "How do you design database schemas and APIs for high-concurrency financial operations?"
- **Context:** In building the SJ Consulting commercial backend on Supabase PostgreSQL, I had to support thousands of concurrent students taking time-limited CBT exams while processing Paystack payment webhooks.
- **Architecture & Design:**
  1. **Idempotent Webhooks:** Designed the Paystack webhook handler with HMAC-SHA512 verification and unique transaction reference constraints. If Paystack retries an event, the database idempotently logs the attempt without double-crediting student subscription tiers.
  2. **Security Invoker RPCs:** Initial stored procedures used `SECURITY DEFINER`, creating potential privilege escalation vectors. I refactored them to `SECURITY INVOKER`, ensuring that all queries strictly respect PostgreSQL Row-Level Security (RLS) policies.
  3. **Aggregation Optimization:** The candidate dashboard previously made 5 separate API calls to load profiles, exam attempts, and admission metrics. I unified these into a single stored procedure (`get_candidate_dashboard`), resolving nested JSONB subquery bottlenecks and delivering all student data in a single sub-50ms database roundtrip.

---

### Question 3: "Describe a challenging systems constraint you encountered and how you overcame it."
- **Context:** During the development of RugRoll and Rescue on Solana Anchor, our build environment was constrained by cloud container memory limits (Codespaces with limited RAM).
- **Problem:** The Rust compiler (`rustc`) and `anchor build` with LLVM optimization passes frequently exceeded available RAM, triggering Linux Out-Of-Memory (`OOMKilled`) termination on cargo builds.
- **Action:** Rather than throwing expensive cloud hardware at the problem, I analyzed the Cargo compilation graph. In `Cargo.toml`, I configured a custom release profile:
  - Set `codegen-units = 1` to reduce parallel memory overhead.
  - Used `opt-level = "z"` (optimizing for binary size rather than raw instruction pipelining, which dramatically reduces intermediate AST representation size).
  - Configured `lld` linker flags and stripped debug symbols via `strip = true`.
- **Result:** Cargo compilation memory footprint dropped by over 60%, allowing clean, deterministic Anchor program builds to complete reliably within containerized cloud environments.
