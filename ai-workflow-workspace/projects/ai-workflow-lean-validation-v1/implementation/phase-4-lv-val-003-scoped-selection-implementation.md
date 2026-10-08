# Phase 4 Implementation: LV003

## Metadata

- Project: ai-workflow-lean-validation-v1
- Task ID: LV-VAL-003-scoped-selection
- Date: 2026-09-30
- Status: source implementation recorded; awaiting owner-approved formal quality
- Source baseline: 00708146b6859bf3f2452baf1a5ef918c178c48f
- Work mode: workflow-maintenance; formal project; Risk: high
- Authority: LV-DEC-002 and current owner resume; no commit or push requested.
- Source: accepted LV003 spec and recovery Spec QA.
- DoD source: task contract and V3-01..10; dependencies and nineteen-path ceiling unchanged.
- Instruction refresh: performed-full after resume; AGENTS, router/operating model, risk/permissions, workflow/autopilot/phase4, plan/spec, quality/validation and current state re-anchored.
- Distillation State: capture-state/lv-val-003-scoped-selection.md, pending-quality before source writes.

## Task Idea Validation

- Co zostaje: explicit checks, full CI/updater, source-bound timing and findings-first quality.
- Co poprawic: unconditional fast prelude, duplicate checks and cross-owner scans.
- Czego brakuje: strict scope snapshot, declared dependency graph, execution/coverage distinction and bounded runtime consumers.
- Blokery / decyzje: none within existing approved source ceiling; high-risk Phase 5 approval due after implementation evidence.
- Rekomendowany routing: sequential formal Phase 4, semantic quality closure and supporting full validation, then stop at owner gate.

## Implementation Slice Plan

| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | strict manifest and dependency registry | new lib/validation-scope.py, validation-checks.json | strict parse, cycle/unknown/path safety | V3 graph and snapshot probes | implemented; targeted verified |
| 2 | NUL-safe Git and owned runtime inventory | scope helper | staged/unstaged/rename/delete/newline/digest | V3-04..08 | implemented; targeted verified |
| 3 | normalized dispatch and honest coverage | validate-workflow | no fast prelude, per-scope dedup/timing, failures | V3-01..03/06/10 | implemented; targeted verified |
| 4 | bounded runtime consumers | naming/status/QA/distillation checks | owned roots, missing/escaping inputs reject | V3-07..09 | implemented; targeted verified |
| 5 | contracts, validators, smoke and QA | remaining approved policy/docs/templates/tests | semantic review then full, unchanged old smoke IDs | producer-consumer/adversarial matrices | implemented; isolated source full verified; formal runtime gate pending |

Stop on missing source, changed DoD, unsafe action, outside-ceiling consumer or source conflict; no silent scope expansion.

## Plan Quality Contract

- Plan classification: implementation-capable
- Implementation writes: yes, official repository only, exact spec ceiling
- DoD source: accepted LV003 specification
- Testable done conditions: V3-01..10 and two spec matrices; runtime checkpoint only with complete required scope
- Artifact QA route: phase-3-spec-qa, current PASS inspected before writes
- Implementation QA route: phase-5-quality
- Required verification: local probes, fresh full-current-diff adversarial/producer-consumer review, applicable full validation after semantic QA
- Residual risk: manifests cannot authorize sensitive reads or replace owner scope/semantic evidence; no speed promise
- Owner opt-out: none for QA; delivery no deadline/timebox by LV-DEC-001

## Slice Execution Evidence

- Nineteen source paths match the approved ceiling. No CI, updater, timing/comparison helper or outside-scope source edit.
- Eleven reproducible synthetic probe groups: dedup, projects, graph, git, freshness, ownership, paths, checkpoint, source, finish and consumers. Dispatch probes deliberately stub checks; consumer probes use the real naming/status/QA/distillation scripts.
- Targeted profile, routing, completion and contract-compliance checks passed; Bash syntax, Python syntax and git diff --check passed.
- Local review corrections: Bash 3.2 empty-array dispatch could end without executing checks; invocation now works on the local Bash and finish rejects status-zero incomplete execution. Strict runtime inventory rejects unreadable directories and sensitive direct-root Markdown names before reading payloads. Finish re-plans to reject altered eligibility claims.
- Actual project full validation stopped at QA evidence, exit 1, one failure completion marker. The final recorded run took 21 seconds and confirmed exactly three source-stale assessments after expected LV003 edits: recovery Spec QA (AGENTS), LV001 Quality (smoke runner), LV002 Quality (commands). Original hashes/verdicts are preserved. Fresh regression assessments are required; no hash-only PASS refresh.
- Isolated source-only full verification found inherited dispatcher environment leaking into copied smoke fixtures (update-workspace/naming assertions). This real integration regression was corrected inside the approved source ceiling. The smoke runner clears inherited mode/root/runtime routing only in its child process; individual fixture environments remain explicit. Both failing runs are preserved. Full post-fix source review and suite were repeated against the final source.
- A further full-current-diff review found tracked target-owned runtime was incorrectly classified as framework impact. The in-scope correction recognizes only present inputs inside selected canonical owned runtime roots. Deleted/missing inputs, raw supporting trees, unselected projects and real system source remain ineligible/full-required. The previous 568-second source run and closure became historical after this fix; no prior verdict was reused.
- Final isolated full after that correction: exit 0, one full completion marker, 553 seconds; smoke-all exit 0, one completion marker, 529 seconds. Forty check IDs and 674 unique smoke IDs. Exact comparison to lv002-final-reviewed-001.json found zero missing check/test IDs and fourteen additional scope tests. No speed improvement claim: source-only runtime differs from the actual LV002 baseline.
- Final source copy matched all nineteen approved changed/new paths byte-for-byte. Actual CI/updater and timing/comparison helper sources remain unchanged. Workspace is ignored/untracked. No source-only run is evidence of actual runtime completion.
- Real scoped invocation with duplicate check-validation-profiles ran it once, exit 0, coverage_result unverified and final_evidence_eligible false; its TSV retained the nine-column V2 timing contract. No manifest was supplied, so no checkpoint eligibility was claimed.
- Local probes after the final correction: eleven groups passed; Bash/Python syntax and diff checks passed. Profile/routing/completion/compliance checks passed.
- Formal high-risk Phase 5 approval remains pending; no Phase 6/7, LV004, source commit, push or formal implementation PASS.

## Producer-Consumer Audit

| Producer | Consumer | Mapping / boundary |
| --- | --- | --- |
| snapshot JSON | plan and finish | exact schema, duplicate-field rejection, canonical source/runtime identity, complete re-snapshot before/after |
| dependency registry | planner and profile validator | forty checks, typed scope, cycle/unknown rejection, required runtime consumers |
| normalized invocation list | Bash dispatch and timing | check/root/project tuple, distinct opaque ID per scope, existing timing nine-column schema unchanged |
| owned runtime inventory | naming/status/QA/distillation | repo/core and project roots only; raw supporting trees excluded; missing, escaping and sensitive owned inputs rejected |
| execution result | checkpoint guidance/template | requested/required/executed/skipped, coverage and final-evidence eligibility separate from formal PASS/permissions |
| legacy current QA artifacts | QA/state consumers | genuine freshness failures preserved; new source results do not retroactively validate historical evidence |

## Adaptive Verification And Adversarial Matrix

| Source shape | Expected state/output | Forbidden state | Failure behavior / evidence |
| --- | --- | --- | --- |
| duplicate explicit checks / shared dependencies | stable closure, one invocation per scope | fast prelude or duplicate execution | dedup/projects probes inspect actual dispatch output |
| staged rename, unstaged delta, newline untracked and deletion | NUL-safe complete Git inventory | dropped path or delete mistaken for unchanged | git probe binds old/new/index/base state |
| changed manifest/runtime/framework/registry | nonzero, ineligible | stale or fabricated complete coverage | freshness/finish probes; manual finish re-plan trace |
| missing/unreadable/symlink/foreign/sensitive source | stop before unauthorized payload | green check from ignored required evidence | paths/ownership probes; direct-root .env.md rejected |
| runtime-only checkpoint / source change | complete only with all deps and clean framework | iteration or source impact advertised as final scoped | checkpoint/source probes; repo active project must be included |
| tracked target-owned runtime | complete only inside selected canonical owned roots | tracked runtime mistaken for framework, or unrelated/deleted input eligible | checkpoint probe covers modified tracked status, deletion and unselected project with a custom workspace name |
| real owned consumers | invalid naming/status/QA/state rejected | unrelated project scanned or cross-project target read | consumers probe executes actual scripts |
| coverage policy wording | safe prohibition accepted; enablement rejected | scoped coverage grants formal PASS | three smoke cases, including safe prohibition plus unsafe exception |

## Quality Closure Readiness

- Semantic current-diff inspection: nineteen paths, DoD V3-01..10, runtime ownership, failure paths and timing producer-consumer contract reviewed.
- Instruction baseline: current; full refresh after resume/compaction, source baseline 0070814 plus current LV003 changes.
- Automated evidence role: supporting-only.
- Post-fix full-current-diff re-review: completed after the tracked-runtime correction, restarting from all nineteen current paths, accepted V3-01..10, unchanged CI/updater, failure/timeout integration, field mapping and negative-space boundary probes. No additional source defect observed. Runtime evidence freshness remains a known blocker, not a clean overall quality verdict.
- Reviewed nineteen-path source digest: 061bfbfe7582453e8e3c9e144622102d4d818a80edeb258b0ceeb4ee77e186c7; SHA-256 of sorted path/content-hash pairs encoded as JSON. Final verified copy byte-matched those paths.
- Formal gate eligibility: not yet eligible. High-risk owner approval and fresh predecessor/spec assessments remain pending.
- Residual risk: no Linux CI run, no performance improvement measured; source-only verification does not validate the private runtime.

## Evidence Locations

- Canonical implementation output: quality/phase-4-lv-val-003-scoped-selection-implementation-result.md.
- Isolated final full log: implementation/lv003-source-full-final.log.
- Historical 568-second full run, superseded by the tracked-runtime correction: implementation/lv003-source-full-post-fix.log.
- Actual final runtime failure log: implementation/lv003-actual-runtime-full-final.log; the earlier failure log is historical.
- Failed integration attempts: implementation/lv003-source-full-inherited-env-failure.log and lv003-source-full-parent-workspace-failure.log.
- Scoped timing evidence: implementation/lv003-scoped-final-timing.tsv.
- Reproducible targeted probes: implementation/lv003-scope-probes.py.
- Owner queue and preserved freshness blockers: escalations/lv003-quality-approval-and-freshness.md and LV-DEC-007.
