# PTO-006/007 Protocol-Only Release Scope

- Date: 2026-10-04
- Decision ID: PTO-D06-protocol-only-release
- Classification: high-impact
- Status: approved scope direction, implementation conditional on Plan QA and Spec QA
- Owner source: Zaplanuj zmiane scope PTO-006/007 dla niedostepnego izolowanego backendu, bez oslabienia safety. Po PASS kontynuuj implementation range do phase 8.
- Prior evidence: reviews/pto-006-native-backend-preflight.md; approved bounded test made zero worker calls after failed isolation preflight
- Chosen scope: installed protocol, conservative schema-2 discovery, offline compatibility/integration checks, honest offline measurements and one AI System handoff
- Deferred: native operational verification and native/model performance evaluation; not completed by simulation
- Impact: PTO-006 AC6 is explicitly replaced before writes; protocol-only release can finish, native execution remains unavailable until independently verified
- Alternative: retain original native-test prerequisite and remain stopped; not selected by requested scope-change continuation
- Source write sets: original eight PTO-006 and six PTO-007 paths only; no new executor, adapter, API client or sandbox settings
- Safety: no dispatch without authentic isolation/capacity and approval; capabilities/worker evidence cannot grant authority; serial fallback does not secretly spawn a worker
- Delivery: no deadline or timebox
- Phase 5: prior conditional high-risk acceptance remains applicable only after all revised AC and actual semantic review
- Phase 8: explicitly requested after accepted Quality, Phase 6 and required checkpoints; no final-owner-yes
- Commit/push: not authorized
- Cross-system impact: yes, one final privacy-safe handoff to AI System; no counterpart changes

## Task Idea Validation
- Co zostaje: all authority, isolation, single-writer, integrated QA and phase gates
- Co poprawic: release DoD must not demand an unavailable runtime while falsely advertising support
- Czego brakuje: conservative installed capability handshake, compatibility tests and documentation of deferred verification
- Blokery/decyzje: scope direction resolved; Plan QA/Spec QA must confirm boundaries before source writes
- Routing: active-plan Plan Fix Loop and Spec Fix Loops for006/007, then implementation-range

## Implementation Slice Plan
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-006-S1 | Conservative capability discovery | original capability/coordinator/runtime files | schema1 parity, schema2 opt-in, no authorization | actual output and malformed-source tests | planned |
| PTO-006-S2 | Compatibility and offline measurement | original validator/tests/smoke/manifest files | full negative cases, three paired samples, old IDs preserved | tests and measured limits | planned |
| PTO-006-S3 | Current integrated Quality and capture | owning evidence | revised six AC and predecessors current | formal phase5, phase6 and cadence checkpoint | planned |
| PTO-007-S1 | Concise guidance and handoff | original six docs plus ignored handoff | actual capability/limitations and five counterpart answers | claim-to-source audit | planned |
| PTO-007-S2 | Common final Quality and capture | owning evidence | current full diff, all AC, privacy and source checks | phase5, phase6 and final checkpoint | planned |
| PTO-008-final | Owner-requested technical final check | owning evidence | complete included tasks, honest deferral, no owner yes | phase8 awaiting-owner-final-yes | planned |

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: revised PTO-006 AC1..6 and unchanged PTO-007 AC1..5
- Testable done conditions: schema1 compatibility, closed schema2 capability, no implicit operational/permission inference, all offline regressions, three paired samples and truthful handoff
- Artifact QA route: phase-2-plan-qa and phase-3-spec-qa for006/007 before source writes
- Implementation QA route: formal phase-5-quality per task with findings-first review, AC compliance and failure paths
- Required verification: producer-consumer/adversarial review, actual synthetic filesystem checks, public CLI behavior, full supporting validation and source/runtime freshness
- Quality-ready criteria: no unresolved P0/P1/material P2, current complete evidence, no unverified native claim
- Residual risk: native isolation/performance unverified; this release is not a functioning native dispatcher
- Owner opt-out: none for quality; existing no deadline/timebox remains
- Next route: Plan QA and Spec QA, then approved source writes only upon accepted artifacts
