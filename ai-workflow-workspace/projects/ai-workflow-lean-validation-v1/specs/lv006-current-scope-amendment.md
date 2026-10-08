# LV006 Current Specification Amendment

## Sources And Authority

Read with specs/phase-3-lv-qa-006-integration-specification.md; this amendment resolves its historical pending approval/dependency claims for current execution. Effective plan: preserved base plus planning/lv005-deferral-plan-amendment.md. Current Plan QA: quality/recovery-phase-2-plan-qa.md. Source baseline a7d66c7, clean branch. Owner source/high-risk authority LV-DEC-002/008, shared impact yes LV-DEC-004, scope disposition LV-DEC-010.

## Dependency Status

LV001-LV004 have separate accepted formal quality and completed capture, linked in tasks.md; source-bound current assessments remain verified rather than inheriting planning-era outcomes. LV005 is owner-deferred; its failed isolated-context preflight and original promotion gate are preserved. No behavioral grade or instruction-efficiency result is needed for the excluded scope, and none can be claimed.

## Scope And DoD

Retain original LV006 five-path ceiling: .systems/ai/core/commands.md, AGENTS.md, HUMANS.md, README.md, .systems/ai/core/changelog.md. Only necessary integration documentation within that ceiling may change. No edits are required just to consume this amendment. Additional correctness changes need owning task/spec fix loops.

Testable done conditions:
1. Included LV001-LV004 evidence resolves to the same current sources/inputs, without historical verdict selection.
2. Full/CI/updater still execute all current smoke IDs; independent groups do not waive complete final coverage.
3. Measurement conclusions state baseline/source/population differences; no incomparable timing-based speed claim.
4. LV005 remains visibly deferred and undistilled; its unmet gates are not waived or treated as implementation findings resolved.
5. Full-current-diff semantic QA and adversarial producer-consumer/failure traces precede explicit full supporting validation.
6. Single handoff describes only accepted included changes and deferred scope; no AI System edit.
7. Phase 6, final Phase 7 and owner-triggered Phase 8 remain separate gates; no push or final-owner-yes.

## Implementation Slice Plan

| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| LV006-1 | audit current task/source and exclusion provenance | ignored review and source inventory | every included dependency current; LV005 excluded explicitly | source/input identities, task/decision mapping | planned |
| LV006-2 | reconcile only necessary integration guidance | original five-path ceiling, only if needed | no outside-ceiling writes or unsupported benefit | reviewed diff, DoD compliance | planned |
| LV006-3 | verify coverage and eligible measurement conclusions | synthetic checks and ignored comparison evidence | 694 IDs retained; unequal populations cannot prove speed gain | comparison rejection/manual trace and failure evidence | planned |
| LV006-4 | formal quality and downstream capture readiness | ignored quality/status and one handoff later | genuine semantic QA before explicit full; fresh evidence | formal Phase 5, later Phase 6/7 | planned |

Before any source write: repeat targeted instruction/HEAD/input check and create/update LV006 pending-quality state. Today's readiness is not that write or its quality closure.

## Tests And Adaptive Matrix

Retain original V6-01..07. V6-02 compares only manifest-compatible runs, otherwise records inconclusive. V6-06 verifies LV005 disposition and distinct later capture/final approval.

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| base plan plus approved amendment | included 001-004/006; deferred 005 | honest task/status/handoff | deferred converted to done or behavioral success | stop for reconciliation | targeted QA/status/state checks | owner disposition -> plan/index -> Spec QA |
| 660-case baseline and 694-case current source | unequal comparison populations | no full speed claim | lower wall equals benefit | report incomparable/inconclusive | comparison rejection in execution | manifest identity -> comparison eligibility |
| complete current coverage or missing assertion | all declared current IDs required | valid full evidence or failure | subset/early-zero success | nonzero and fix loop | full suite and ID audit in execution | dispatcher -> owned group -> exact ledger -> completion |

## Failure Paths, Edge Cases And Uncertainty

Missing/stale dependency, extra consumer, failed full, changed source after QA: stop, owning fix loop and fresh affected QA. A deferred future task may retain open findings without blocking acceptance of its explicitly excluded source scope; it must remain visible in final evidence. No silent promotion. Model runtime issue is not investigated further in LV006. Current full timings are not comparable by ID count alone. Linux CI is not yet executed, no remote success asserted.

## Implementation Gate

- DoD complete and testable: yes
- Required user decisions resolved: yes for included source scope
- Dependencies: current accepted LV001-LV004 outputs plus LV-DEC-010; excluded LV005 is not a source prerequisite
- Can enter implementation: only after fresh composite Spec QA and task-scoped pre-write/state check; stop after readiness for this request

## Plan Quality Contract

- Plan classification: implementation-capable
- DoD source: composite LV006 spec and effective amended plan
- Testable DoD / acceptance conditions: seven done conditions, V6-01..07 and matrix above
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after whole composite spec review
- Implementation Quality Closure route: phase-5-quality
- Required verification: included-task regression, failure/edge traces, producer-consumer/adversarial current-diff review, then explicit full
- Quality-ready criteria: evidence complete and no included-scope unresolved material findings
- Owner opt-out: none for QA
- Not-applicable reason: none
- Blocking decision: none within accepted ceiling
- Next route: Spec QA then readiness-only stop

Delivery: inherited LV-DEC-001 no deadline/timebox. Quality floor, permissions and approvals unchanged. Capture decision: record disposition/readiness now; actual task Phase 6/7 remains later.
