# Project Dossier: Artemis Telemetry Link (Rust Systems Datalink & Failsafe Prototype)

**Dossier Generation Date:** November 10, 2026  
**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  
**Repository Source:** Remote GitHub (`Olalolo22/artemis-telemetry-link`) / Local Workspace (`/home/lala_02/artemis-telemetry-link`)  
**Access Level:** Public / Open Source  
**Latest Verified Commit:** `b8fa571` (`docs: calibrate README and Cargo.toml tone to honest systems prototype`)  
**Evidence Standard:** E2 (Complete Rust Implementation, 30 Passing Unit & Integration Tests, Architecture Specs)

---

## A. Identity and Purpose

- **Project Name:** Artemis Telemetry Link
- **Repository URL:** [`https://github.com/Olalolo22/artemis-telemetry-link`](https://github.com/Olalolo22/artemis-telemetry-link)
- **Relevant Branch:** `main`
- **What It Does:** A high-assurance vehicle systems software prototype in Rust modeling binary datalink framing, lossy RF link quality estimation, HMAC-SHA256 command authentication, and deterministic failsafe state machines for autonomous unmanned platforms (UAV / UGV).
- **Specific Problem Addressed:** Unmanned platforms operating over contested or lossy RF links suffer from 15% to 30% packet loss, multipath bit-flips, and intermittent radio link dropouts. Naive vehicle software can execute corrupted packets, suffer airborne disarms from unauthenticated commands, or enter unrecoverable failsafe deadlocks. Artemis implements a zero-panic, memory-safe communication and flight mode supervisor in pure Rust.
- **Intended Domain:** Defense tech, robotics, embedded flight controllers, companion computer daemons.

---

## B. Implementation Status

- **Classification:** **Implemented and Verified Rust Systems Prototype**
- **Verified Components:**
  - [x] **Binary Datalink Framing Codec:** Sync words (`0xAA55`), monotonic sequence numbering, packet length bounds validation, and CRC-16-CCITT integrity verification.
  - [x] **HMAC-SHA256 Command Authentication:** MAVLink 2 style message signing utilizing 128-bit truncated HMAC-SHA256, session isolation, and temporal replay rejection windows.
  - [x] **RF Link Quality Estimator:** Real-time sliding-window tracker calculating Packet Delivery Ratio (PDR), detecting sequence gaps, managing sequence rollovers (wrapping at `u16::MAX`), and recording bit-flip CRC rejections.
  - [x] **Deterministic Safety State Machine (FSM):** Enforces strict airborne safety invariants: rejects in-flight disarm commands without touchdown confirmation, enforces ground hold guards, monitors heartbeat timeouts, and preserves pre-loss flight modes upon link reconnection.
  - [x] **Automated Test Suite:** 30 passing unit and property-based integration tests (`cargo test`).

---

## C. Technical Architecture

```
[ Ground Control Station (GCS) ]
               │
               │ 1. Serializes Telemetry / Command with 0xAA55 Sync Word
               │ 2. Appends Monotonic Sequence + CRC-16-CCITT
               │ 3. Signs Payload with HMAC-SHA256 (Truncated 128-bit)
               ▼
~~~~~~~ LOSSY RF CHANNEL (15-30% Packet Loss / Multi-Path Interference) ~~~~~~~
               │
               ▼
[ Artemis Vehicle Daemon (Rust) ]
               │
               ├───▶ [ Datalink Decoder ]: Checks 0xAA55, Validates Bounds, Computes CRC-16
               │        └── Failure? Drop packet & increment CRC rejection counter
               │
               ├───▶ [ Authenticator ]: Checks HMAC-SHA256 & Sequence Replay Window
               │        └── Failure? Drop packet & emit Security Violation event
               │
               ├───▶ [ Link Quality Estimator ]: Updates PDR (Packet Delivery Ratio)
               │        └── PDR < 20% or Heartbeat > 3.0s? Emit LinkLoss signal
               │
               ▼
[ Deterministic Failsafe State Machine (FSM) ]
  - State: InFlight / AutonomousMission
  - Inbound Command: DISARM? -> REJECTED (Invariant: Disarm prohibited while airborne)
  - Event: LinkLoss? -> Transitions to ReturnToHome (RTH)
  - Event: LinkRecovered? -> Restores pre-loss mission mode seamlessly
```

---

## D. Verification Evidence & Claims

| Claim ID | Claim Description | Evidence Source | Confidence |
| :--- | :--- | :--- | :---: |
| `CLM-ARTEMIS-001` | Built zero-panic binary datalink codec in Rust with CRC-16-CCITT, monotonic sequence tracking, and bounds checks. | `src/codec.rs`, 30 passing cargo tests | **E2** |
| `CLM-ARTEMIS-002` | Engineered HMAC-SHA256 command authentication and anti-replay window for unmanned vehicle command links. | `src/auth.rs`, commit `c4b8954` | **E2** |
| `CLM-ARTEMIS-003` | Implemented deterministic vehicle safety state machine with airborne disarm protection and flight mode restoration. | `src/fsm.rs`, commit `22f9981` | **E2** |

---

## E. Interview-Ready Talking Points

- **One-Sentence Pitch:**  
  *"Artemis Telemetry Link is a systems software prototype in Rust that hardens unmanned vehicle communications across lossy RF channels using binary framing, HMAC-SHA256 anti-replay command verification, and a deterministic failsafe state machine that prevents airborne disarms."*
- **30-Second Technical Walkthrough:**  
  *"When a drone or rover flies through RF interference, dropped packets and corrupted bytes can cause erratic movements or allow unauthenticated attackers to hijack the vehicle. I built Artemis in pure Rust to solve this. Every packet is framed with a `0xAA55` sync word, CRC-16-CCITT, and a truncated 128-bit HMAC-SHA256 signature to reject replayed or injected commands. A sliding-window estimator tracks the Packet Delivery Ratio in real time. If the link drops for over 3 seconds, a deterministic state machine triggers Return-to-Home, strictly rejecting any airborne disarm command until touchdown sensors register ground contact."*
