# Project Plan

Order: EFF-001 baseline before tracked implementation; EFF-002 selection; EFF-004/005 history and producer; EFF-003 reuse; EFF-006 bounded route; EFF-007 refresh/preflight; integration review and full validation. No deadline/timebox. No handoff. Planning/spec QA precede writes. Each task uses slices and current-diff review; a combined integration Phase 5 checks the seven task DoDs. Capture/checkpoint follow, then technical Phase 8 awaiting owner.

## Implementation Slice Plan

| Slice | Goal | Areas | Acceptance | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| EFF-001 | Process timing | lib/execution-efficiency.py; tests/execution-efficiency.py | Record whole-process intervals; preserve unknowns, estimates and overlap semantics. | Three baseline and three candidate samples for each synthetic scenario; timings use monotonic clocks. | planned |
| EFF-002 | Validation applicability | validation-routing.md; validation-profiles.md; validate-workflow; lib/validation-checks.json | Explicit product/runtime/integration/environment check plan; no unrelated smoke for runtime-only closure. | Unknown coverage escalates; full/CI/update run fresh; runtime scope still validated by existing manifests. | planned |
| EFF-003 | Source-bound reuse | lib/execution-efficiency.py; validate-workflow | Authenticated completed receipts with source/dependency/argv/tool/environment/coverage bindings. | Tampered, failed, timeout, interrupted, changed and undeclared input records reject reuse or execute fresh. | planned |
| EFF-004 | Historical QA lifecycle | lib/qa-evidence.py; check-qa-evidence | Immutable explicit history admission with checksum, provenance and decision reference; no history PASS progression. | Historical reports validate integrity/schema independently of live input hashes; direct current PASS consumer rejects history. | planned |
| EFF-005 | Schema-driven quality producer | prepare-quality-record; lib/quality-record.py | Generate deterministic V2 QA from supplied reviewed sections and live approved inputs. | All QA kinds, Phase 8 and separate owner approval validate before no-clobber publication; no invented semantic verdict/approval. | planned |
| EFF-006 | Bounded defect | operating-model.md; risk-model.md; implementation-slicing.md | Add locally authorized low/medium reversible defect route with one compact work record. | Known consumers, DoD and regression proof required; prohibited impact or ambiguity rejects eligibility; scope growth reroutes. | planned |
| EFF-007 | Refresh and preflight | instruction-adherence-refresh.md; validation-observability.md; lib/execution-efficiency.py | Fingerprint actual opened contracts and scope/stage; selective full refresh checks current authority; environment checked early. | Resume with changed scope/source cannot silently continue; ps/tools/writable output fail before expensive checks. | planned |

## Plan Quality Contract

- Plan classification: implementation-capable
- DoD source: context.md and the accepted owner plan in this conversation.
- Testable DoD / acceptance conditions: seven capabilities work; current/history separation preserves bytes; producer validates supplied review; reuse rejects changed, incomplete or forged evidence; coverage preserved.
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: before the first write of each task.
- Implementation Quality Closure route: phase-5-quality
- Required verification: adversarial Python tests, producer-consumer audit, three comparable synthetic samples per scenario, existing smoke suite, explicit full validation.
- Quality-ready criteria: no unresolved P0/P1/material P2; all seven scope checks and regression evidence complete.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none
- Next route: specification QA, approved implementation slices, phase 5, phase 6, phase 7, owner-triggered phase 8 awaiting final-owner-yes.
