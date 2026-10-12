# EM-COMPAT-002-compatibility Specification
## Source And Scope
Owner-approved compatibility plan and decisions/2026-10-08-compatibility-scope.md.
Source-bound capability contract 1; projection schema 2 with chronological unique attempt IDs, unit ID, stable cause ID and optional progress fingerprint.
Three consecutive unproductive attempts block the unit, shared claims and transitive dependents. New verified progress can reset only that cause counter, never existing Spec/Quality/run budgets. Resume retains history.
Schema 1 remains readable as legacy without verified recovery; fresh schema 2 is required before future execution claiming the new guard.
No dispatch, approval verification, native eval, target edits or automatic installation.
## Implementation Slice Plan
| Slice ID | Goal | Expected areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| COMPAT-1 | capability and recovery contract | execution-modes/autopilot/templates | source pin and schema review | producer-consumer map | pending |
| COMPAT-2 | pure capability/recovery inspection | inspector, validator | malformed/legacy/limits fail-safe | deterministic tests | pending |
| COMPAT-3 | regressions and counterpart integration | tests, smoke, manifest | tamper and recovery scenarios | frozen harness manifest/results | pending |
| COMPAT-4 | integrated QA and capture | docs/handoff/project evidence | current review then full validation | formal quality, distillation/checkpoint, Phase 8 | pending |
- DoD source: accepted compatibility plan and this specification.
- Stop rule: new scope/risk/permission or counterpart source drift invalidates affected evidence before continuation.
## Definition Of Done
1. Exact capability contract/mapping/behaviors and current relative non-symlink source pins validated.
2. Schema 2 enforces stable-cause per-unit recovery with unique attempts, new-vs-repeated evidence and persisted stricter budgets.
3. Legacy inspection does not attest new recovery or approvals.
4. Stalled units/dependents/shared resources are blocked; independent approved units continue.
5. Deterministic regressions and frozen actual counterpart adapter scenarios pass without source mutations.
6. Semantic/adversarial producer-consumer review, full validation and fresh formal Quality are complete.
7. Existing outgoing handoff, Phase 6/7 and technical Phase 8 are refreshed; no final-owner-yes or push.
Implementation Quality evaluates implementation conditions 1-5, semantic review and final-source validation in 6, and readiness of the handoff/capture/final-check inputs. Delivery condition 7 remains mandatory after Quality and is evaluated at the separately authorized technical Phase 8. Phase 5 does not claim that downstream capture or final check already happened; this sequencing clarification does not remove any delivery condition.
## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: this specification and owner scope decision
- Testable done conditions: seven numbered conditions above
- Artifact QA route: phase-3-spec-qa
- Implementation Quality Closure route: phase-5-quality
- Required verification: pure state/capability tests, policy tamper smoke, actual frozen counterpart harness, failure-path review, full validation
- Quality-ready criteria: no unresolved P0/P1/material P2, source-bound evidence current
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none
- Next route: phase-4-implementation
- Residual risk: source-bound synthetic compatibility is not installed rollout or proof of model adherence; declared progress needs coordinator verification.
