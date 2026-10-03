# Project Dossier: SJ Consulting Education Platform

## 1. Executive Summary
- **Project Name:** SJ Consulting Backend Platform (Admission & CBT Engine)
- **Role & Ownership:** Lead Backend & Systems Architect (Commercial Client Deliverable via WebDevConstruct)
- **Production Status:** Production-Ready Client Platform / Staging Tested with Live Supabase Backend & Paystack Webhooks
- **Primary Tech Stack:** Supabase (PostgreSQL 15+), Deno / TypeScript Edge Functions, Paystack Payments API, Row-Level Security (RLS), Realtime WebSockets, TypeScript Client SDK
- **Core Engineering Significance:** Full-lifecycle educational platform engine featuring an automated UNILAG admission probability calculator, secure CBT (Computer Based Test) examination engine with anti-cheat state machines, real-time peer-to-peer duels, automated Paystack payment webhook processing, and CEO-governed staff deliverables & payroll workflows.

---

## 2. Architecture & System Design

```
+----------------------------------------------------------------------------------------------------+
|                                    Frontend / Client Applications                                   |
|                          (Web / Mobile via @sj-consulting/client-sdk)                               |
+-------------------------------------------------+--------------------------------------------------+
                                                  |
                         HTTPS API Requests / RPC | Realtime Subscriptions (Duels, Leaderboards)
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                     Supabase Edge Infrastructure                                    |
|                                                                                                    |
|  +--------------------+  +--------------------+  +--------------------+  +-----------------------+  |
|  |   auth-login       |  | cbt-start-session  |  |    cbt-submit      |  |   paystack-webhook    |  |
|  | (Custom sync/auth) |  | (Anti-cheat/trial) |  | (Server-side score)|  | (HMAC-SHA512 verify)  |  |
|  +--------------------+  +--------------------+  +--------------------+  +-----------------------+  |
|                                                                                                    |
|  +--------------------+  +--------------------+  +--------------------+  +-----------------------+  |
|  |  create-peer-duel  |  |   join-peer-duel   |  |   account-migrate  |  |     admin-content     |  |
|  |  (PvP matchmaker)  |  |   (Slot locks)     |  |   (Legacy sync)    |  |  (RBAC media/content) |  |
|  +--------------------+  +--------------------+  +--------------------+  +-----------------------+  |
+-------------------------------------------------+--------------------------------------------------+
                                                  |
                            Service Role / RLS Session Connection
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                 Supabase PostgreSQL 15 Database                                   |
|                                                                                                    |
|  +--------------------------------+  +--------------------------------+  +----------------------+  |
|  |    Admission Calculation Engine|  |       CBT Engine Tables        |  |  Enterprise Workflows|  |
|  |  - UNILAG aggregate scoring    |  |  - cbt_questions / options     |  |  - staff_deliverables|  |
|  |  - O-Level grade conversions   |  |  - cbt_sessions (server timing)|  |  - payroll_runs      |  |
|  |  - Catchment/merit cutoffs     |  |  - cbt_submissions & logs     |  |  - CEO sign-off auth |  |
|  +--------------------------------+  +--------------------------------+  +----------------------+  |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  |                          High-Performance Stored Procedures (RPCs)                          |  |
|  |  - get_candidate_dashboard(): Aggregates profile, admission status, CBT stats in 1 roundtrip |  |
|  |  - calculate_admission_probability(): Deterministic O-Level + UTME + Post-UTME computation    |  |
|  |  - Security: SECURITY INVOKER enforcement preventing RLS privilege escalation                 |  |
|  +----------------------------------------------------------------------------------------------+  |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Key Components & Implementation Details

### A. Admission Scoring & Prediction Engine
- **Mathematical Specification:** Implemented exact university admission scoring algorithm combining JAMB UTME scores (scaled to 50%), O-Level grades (A1=4.0, B2=3.6, B3=3.2, C4=2.8, C5=2.4, C6=2.0 across 5 core subjects = 20%), and Post-UTME examination (30%).
- **Cutoff Matching:** Evaluates candidates against dynamic Merit, Catchment, and Educationally Less Developed State (ELDS) cutoffs seeded for UNILAG faculties (`20260928000001_seed_unilag_2025_2026_requirements.sql`).

### B. High-Assurance CBT Engine
- **Session State Machine:** `cbt-start-session` enforces strict concurrency limits, checks active subscription tiers (or free trial quotas), randomizes question sets server-side without leaking answer keys to the client, and records `started_at` timestamps in PostgreSQL.
- **Server-Side Grading & Anti-Cheat:** `cbt-submit` verifies that submission timestamps fall within the allotted duration plus grace windows. Grades answers entirely within the Edge function using cryptographic answer comparisons, preventing client-side score manipulation.

### C. Financial & Webhook Processing (`paystack-webhook`)
- **Cryptographic Signature Verification:** Verifies incoming `x-paystack-signature` using HMAC-SHA512 with the secret key before processing any transaction payload.
- **Idempotency & State Sync:** Guarantees idempotent transaction recording. Successfully verified payments upgrade candidate profiles to premium status, unlocking unlimited CBT attempts, peer duels, and detailed admission analytics.

### D. Realtime Peer Duels
- **Multiplayer Matchmaking:** Edge functions `create-peer-duel` and `join-peer-duel` manage concurrent room state, question synchrony, and score broadcasts over Supabase Realtime channels.

### E. Corporate Operations & CEO-Governed Payroll
- **Deliverables & Payroll:** Commit `42af5cf` introduced departmental deliverables tracking and CEO-governed payroll approvals. Implemented database triggers and strict RLS policies ensuring that staff deliverables cannot be marked as payable without CEO cryptographic/session sign-off.

---

## 4. Security & Performance Engineering

1. **Security Invoker Fixes (`20261001000004_fix_dashboard_rpc_security_invoker.sql`):**
   - Refactored high-performance RPC functions from `SECURITY DEFINER` to `SECURITY INVOKER` to guarantee that PostgreSQL RLS policies cannot be bypassed through procedural execution contexts.
2. **Elimination of Nested Aggregation Bottlenecks:**
   - In `20261001000003_fix_nested_agg_dashboard_rpc.sql`, resolved a complex PostgreSQL JSONB aggregation bug where nested subqueries caused query planning degradation, reducing candidate dashboard load time from multiple network requests to a single optimized sub-50ms database call.
3. **Strict Input Sanitization:**
   - Authored `frontend-integration/lib/sanitize.ts` providing rigorous XSS defense and payload sanitization across all client-submitted text.

---

## 5. Verification Evidence & Artifacts

- **Local Path:** `/home/lala_02/SJ_consulting`
- **Git Commit Highlights:**
  - `42af5cf`: `feat(admin): add department deliverables tracking and CEO-governed staff payroll workflows`
  - `5cf6cb1`: `feat(cbt): enforce CBT Premium subscription check and free trial limits in cbt-start-session`
  - `d5f395e`: `feat(integration): wire complete CBT session, profile onboarding, subscriptions, and duels to SDK and README`
  - `5fd9bce`: `feat(sdk): add CBT session, profile, migration, subscription, and realtime duel score to client SDK`
- **Migrations:** 12 SQL migration files in `supabase/migrations/` totaling over 130,000 bytes of tested relational schema.
- **Edge Functions:** 8 production Deno Edge Functions in `supabase/functions/`.
