# Project Dossier: WDC Formatt (Production Commercial Platform Hardening)

**Dossier Generation Date:** November 10, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Source:** Remote Git (`WebDevConstruct/WDC_Formatt`) / Local Workspace (`/home/lala_02/WDC_Formatt`)  
**Access Level:** Proprietary Client Platform (WebDevConstruct)  
**Latest Verified Commit:** `d8a8a73` (`docs: create REVAMP_LOG.md engineering dossier for Phase 1 changes`)  
**Evidence Standard:** E2 (Production Git History, REVAMP_LOG.md, Code Diffs Across Routes)

---

## A. Identity and Purpose

- **Project Name:** WDC Formatt
- **Repository URL:** Private Client Repository (`WebDevConstruct`)
- **Relevant Branch:** `revamp`
- **What It Does:** An enterprise AI-powered administrative document automation platform that generates structured academic assignments, professional letters, and rapid assessments for higher-education students and institutions.
- **Specific Problem Addressed:** The production system suffered from critical mobile runtime failures (zero-byte corrupted PDF downloads on iOS Safari), inverted subscription tier authorization bugs locking out paying users, quota-leak race conditions during AI document streaming, and serverless PostgreSQL connection pool exhaustion.
- **Role:** Lead Platform Hardening & Systems Engineer (WebDevConstruct).

---

## B. Implementation Status

- **Classification:** **Commercial Production System / Phase 1 Architectural Hardening Completed**
- **Verified Deliverables & Engineering Scope:**
  - [x] **iOS Safari (WebKit) PDF Blob Lifecycle Fix:** Remediated silent download failures and 0-byte corrupt files on iPhones/iPads caused by premature `URL.revokeObjectURL()` and WebKit user activation expiration.
  - [x] **Subscription Tier Access Control Hardening:** Fixed inverted boolean condition (`if (user?.planTier !== "free")`) in `app/api/quickassessment/route.ts` that erroneously threw 403 Trial Expired against paying subscribers.
  - [x] **Atomic Quota Stream Synchronization:** Synchronized AI streaming completion events (`onFinish`) with transactional quota decrements, eliminating race conditions where concurrent browser tabs bypassed usage caps.
  - [x] **Prisma Connection Pool Singleton:** Enforced global singleton pattern across Next.js API routes, preventing connection leaks on serverless Postgres instances.
  - [x] **Comprehensive Engineering Audit:** Authored 142-line `REVAMP_LOG.md` detailing exact root causes, code transformations, and downstream stability guarantees.

---

## C. Technical Architecture & Deep Dives

### 1. Mobile WebKit Asynchronous Blob Destruction
```
[ User Clicks Download on iPhone ]
                │
                │ 1. Client awaits AI generation: await fetch("/api/generate-pdf")
                ▼
+--------------------------------------------------------------------------------+
|                             THE WEBKIT LIFECYCLE BUG                           |
|  - Old Behavior:                                                               |
|    a.click();                                                                  |
|    window.URL.revokeObjectURL(url); // INSTANTLY DESTROYED                     |
|  - In Desktop Chrome: Buffer reads synchronously -> Download succeeds          |
|  - In Mobile Safari: WebKit resolves blob on NEXT event loop tick ->           |
|    Target URL is already 404/revoked -> Silent failure or 0-byte corrupted file|
|  - WebKit User Activation Expiry: Programmatic a.click() blocked after async!  |
+--------------------------------------------------------------------------------+
                │
                │ Remediation
                ▼
+--------------------------------------------------------------------------------+
|                        THE HARDENED MOBILE PIPELINE                            |
|  1. Device Detection: const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent)|
|  2. If iOS: window.open(url, "_blank") launches native Safari PDF viewer,       |
|     surfacing native Share Sheet ("Save to Files", AirDrop, Print)             |
|  3. Delayed Revocation: setTimeout(() => URL.revokeObjectURL(url), 60000)       |
|     guarantees background buffers finish streaming before cleanup             |
|  4. Strict Response Gate: Checks if (!res.ok), parsing backend JSON errors     |
|     instead of casting error strings into fake PDF blobs                      |
+--------------------------------------------------------------------------------+
```

### 2. Inverted Access Control Remediation
In `app/api/quickassessment/route.ts`, the previous author implemented:
```typescript
// VULNERABLE INVERTED CHECK:
if (user?.planTier !== "free") {
  return new Response(JSON.stringify({ error: "Trial expired" }), { status: 403 });
}
```
This inverted logic allowed unauthenticated or free tier accounts to pass through while returning HTTP 403 to paying subscribers. The check was restructured to validate active plan validity against strict date and quota boundaries.

---

## D. Verification Evidence & Claims

| Claim ID | Claim Description | Evidence Source | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-FORMATT-001` | Hardened production WebKit PDF streaming and iOS blob lifecycle, resolving mobile download failures for WDC Formatt. | `REVAMP_LOG.md`, commit `047dc8c`, `app/dashboard/Files/quick_assessment/` | **E2** |
| `CLM-FORMATT-002` | Remediated inverted subscription tier authorization bug (403 lockout) and serverless Prisma connection pool leaks. | `app/api/quickassessment/route.ts`, `lib/prisma.ts` | **E2** |

---

## E. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"For WebDevConstruct's Formatt platform, I conducted a critical production runtime overhaul, resolving mobile WebKit blob memory lifecycle bugs that broke PDF downloads on iOS, fixing an inverted authorization check that locked out paid subscribers, and eliminating serverless database connection exhaustion."*
- **30-Second Technical Walkthrough:**  
  *"On WDC Formatt, iPhone users were receiving corrupted, unreadable PDFs. By profiling the WebKit event loop, I diagnosed that the frontend was executing `URL.revokeObjectURL()` immediately after triggering an asynchronous anchor click. Desktop browsers buffer this synchronously, but Safari resolves blobs asynchronously on the next event loop tick after user activation expires. I implemented an iOS-specific pathway using `window.open` into Safari's native PDF viewer with a 60-second delayed revocation window, fixed an inverted plan-tier check that threw 403s on paid users, and wrapped Prisma in a global singleton to stop connection leaks on serverless Postgres."*