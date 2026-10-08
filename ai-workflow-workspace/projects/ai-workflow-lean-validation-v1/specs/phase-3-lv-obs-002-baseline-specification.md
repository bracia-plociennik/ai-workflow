# Phase 3 Specification: LV002

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Task/package ID: LV-OBS-002-baseline.
- Task/package name: Precise durable cost baseline.
- Date: 2026-09-29.
- Readiness: dependency resolved; fresh Spec QA required before implementation.
- Baseline: 62090f482d47351a162c6558c2bfd8c1a1f9e1f0; clean tracked checkout.

## Sources

- Project plan: planning/phase-2-project-plan.md; Plan QA: quality/phase-2-plan-qa.md.
- Architecture: architecture/phase-1-architecture.md and its Architecture QA.
- Intake: intake/phase-0-repo-intake.md; decisions: decisions/lv-decisions.md; context.md.
- Existing dependency outputs: LV001 formal Quality PASS, accepted Phase 6 distillation, and commits `fa5eac1`/`62090f4`.

## Task Contract

- Goal: Measure complete valid executions before optimizing coverage selection or partition.
- Scope: Monotonic timing, compatibility-safe metadata, local comparison tool and three post-correctness baseline runs.
- Out of scope: No speed claims from counts, benchmarks before LV001 quality, network, telemetry payloads or source optimization.
- Definition of Done: Three complete comparable baseline runs frozen; timing success/failure preserved; wall-clock separate from children/setup; median, range and noise rule documented; raw records remain private and durable.
- Dependencies: LV001.
- Risk type: high; formal workflow-maintenance.
- Main risk: false confidence, coverage loss or unintended authority change.
- Start condition: LV-DEC-002, current source baseline, accepted Spec QA and predecessor quality evidence.
- End condition: testable task DoD, semantic findings-first Phase 5, applicable explicit full validation and no unresolved material findings; later capture follows phase rules.
- Requires user decision before implementation: no new decision; approved LV-DEC-002 controls source writes.

## Proposed Write Set

- .systems/scripts/validate-workflow
- .systems/scripts/check-validator-smoke-tests
- .systems/scripts/lib/validation-timing.py (new)
- .systems/scripts/report-validation-comparison (new)
- .systems/scripts/check-validation-observability
- .systems/ai/core/validation-observability.md
- .systems/ai/core/commands.md
- README.md

These paths are the proposed task ceiling, not current write permission. Brace expressions enumerate only named sibling files. New helpers are explicitly marked new. Any additional source consumer discovered at pre-write must be reconciled in this spec and Spec QA before editing.

## Dependency Status

- LV001: formal Quality PASS and Phase 6 distillation inspected. Source `validate-workflow`, smoke runner, timing consumer and validation-observability contract inspected at current HEAD. Rerun Spec QA before dependent writes.
- Source approval/base: LV-DEC-002 resolved for the six-task range on `codex/ai-workflow-lean-validation-v1`.
- No LV002 timing/eval outcome is assumed.

## Interface And Implementation Slices

1. Add a stdlib monotonic timing helper and instrument top-level checks, smoke tests and shared setup with perf_counter_ns or monotonic_ns. Preserve process exit/timeout/signal behavior and exactly-one completion protocol.
2. Keep the first five TSV columns compatible (command/check_id, group, duration_seconds, result, profile); append schema-version, run-id, record-kind and parent-id only with a versioned header and updated in-repo consumers. Completion duration can remain backward-compatible while raw measurements gain precision.
3. Add a local comparison report command accepting baseline and candidate manifests. No raw command outputs, prompts, absolute client paths or secrets in telemetry.
4. After LV001 semantic/Phase 5 evidence and this instrumentation review, execute three complete full monolith runs on one frozen revision/environment and input tree. Record representative small-task, artifact-QA, checkpoint, skill and validator paths. Execution is later, not this planning-range.

## Baseline Manifest And Comparison

Manifest records revision, source digest, OS/runtime versions, profile, selected scope fingerprint, test/assertion inventory fingerprint, run ID, expected/performed checks, completion status, setup regime and raw timing paths. Runtime artifacts must be synthetic or privacy-reviewed and identical across comparisons. Baseline and candidate code revisions are expected to differ only by the reviewed change; each source digest must match its own frozen manifest. Reject unexplained changes within a run, not the intentional baseline-to-candidate revision difference. Coverage identity and input equivalence are separate from code identity.
Distinguish wall-clock record from child durations. Do not sum full smoke duration plus each smoke test. Shared setup remains a separate accounted interval.
Three same-environment valid runs are the minimum. Record all failures and infrastructure aborts separately; never substitute short failed runs for complete measurements. If baseline cannot finish validly, block optimization and route the precise existing defect.
Candidate run order alternates against baseline when feasible to limit warm-cache/time drift. Do not flush system caches or change global settings.
Predeclared conservative improvement rule per path: all candidate valid durations below all baseline valid durations and median gain above 5 percent; otherwise inconclusive and collect more evidence only with an explicit local plan. This is a screening rule, not statistical certainty. Report median, min/max, paired differences and coverage identity.
For scoped paths compare the same declared scope and required check/assertion coverage, not unrelated global work excluded by design. Report removed unrelated work separately. Full-to-full comparisons require exact full coverage equivalence.

## Planned Tests

| ID | Input | Expected state/output |
| --- | --- | --- |
| V2-01 | sub-second checks and nested smoke | positive precise durations, non-double-counted wall-clock |
| V2-02 | failed/timeout/interrupted child | original exit propagated; incomplete run preserved |
| V2-03 | source not matching its own manifest, or incompatible environment/input/scope | incomparable, no speed verdict |
| V2-04 | missing test record or duplicate identity | incomplete/invalid |
| V2-05 | overlapping timing ranges or median-only small improvement | inconclusive |
| V2-06 | three complete equivalent runs with separated durations | qualified improvement with limitations |
| V2-07 | existing five-column reader/header handling | compatibility or explicit version error, not silent column drift |
| V2-08 | unsafe output path, unwritable sink or conflicting schema file | fail with clear diagnostic; no tracked overwrite |
| V2-09 | telemetry inspection | no raw content, credentials or private runtime data |

## Adaptive Verification Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| process intervals and nested run IDs | typed timing records | wall-clock plus attribution | child/parent double count | invalid comparison | V2-01..04 | one complete run and timeout |
| baseline/candidate manifests | comparable or incomparable | qualified improvement/inconclusive | partial run advertised faster | withhold speed claim | V2-03..09 | matching pair then coverage mismatch |

## Specific DoD And Stop Conditions

Freeze and retain the post-correctness instrumented baseline before LV003 or LV004 alters execution. No numeric speed promise is an acceptance dependency. Correctness work survives a measured slowdown.
Timing paths must be canonicalized, reject escaping symlinks and tracked targets, and never truncate an existing unrelated report. Output files stay in ignored project evidence or approved tmp; project evidence holds durable copies, not only ephemeral tmp links.

## Potential Errors

Nested timing double counted; failed short runs called faster; unrelated source drift hidden.

## Edge Cases

Sub-second checks, signal exit, unwritable output, changed candidate revision with stable test inputs.

## Assumptions

Instrumentation uses current Python stdlib and preserved lifecycle; no timing result assumed.

## Blocking Uncertainties

None after fresh Spec QA: design and stop rules are explicit. If review finds an interface or write-set mismatch, stop for spec fix before tracked writes.

## Non-Blocking Uncertainties

Actual runtime cost and future compatibility details are measured during implementation; no performance gain is assumed. Discovery outside the proposed write set stops for spec reconciliation.

## User Decisions

LV-DEC-001 resolved the delivery opt-out. LV-DEC-002 approved source execution/base for LV001-LV006. LV-DEC-003 governs LV005 synthetic model runs. LV-DEC-004 approved one later handoff. Fresh Spec QA is still required for this changed artifact.

## Implementation Gate

- DoD complete and testable: yes.
- Dependencies satisfied or explicitly gated: yes; LV001 Quality PASS and Phase 6 are recorded.
- Required user decisions resolved: yes for the accepted LV002 source scope.
- Can enter implementation: only after a fresh Spec QA PASS and readiness audit.
- Blocking reason: fresh Spec QA and run-scoped readiness pending.
- Gate invalidation: changed predecessor interfaces, approved scope, source or evidence requires spec refresh and fresh Spec QA.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: accepted project context, architecture and LV002 task contract.
- Testable DoD / acceptance conditions: task DoD plus the concrete test/matrix cases in this specification.
- Artifact QA route: phase-3-spec-qa.
- Artifact QA trigger: after complete spec review, before any execution approval/readiness.
- Implementation Quality Closure route: phase-5-quality.
- Required verification: targeted regression tests, manual representative success/failure trace, adversarial policy matrix, producer-consumer audit, fresh full-current-diff review, then explicit full profile for source changes.
- Quality-ready criteria: complete coherent spec; runtime correctness is not claimed until implemented and checked.
- Owner opt-out: none for QA.
- Not-applicable reason: none.
- Blocking decision: LV-DEC-002 for source execution; LV-DEC-004 before commit/handoff.
- Next route: phase-3-spec-qa, then stop at planning-range boundary.

## Delivery Constraints

- Mode: owner-opt-out.
- Deadline: none.
- Time budget: none.
- Timezone: Europe/Warsaw.
- Owner override: LV-DEC-001; explicit no-deadline/no-timebox for this project.
- Must-have outcome: preserve safety and coverage while reducing unnecessary validation cost.
- Should-have scope: measured workflow ergonomics improvements.
- Stretch scope: none.
- Explicitly deferred scope: automatic changed-file inference, cache, production changes.
- Quality floor: semantic QA, DoD, evidence, approvals and complete required coverage.
- Cutline rule: retain monolith if equivalence is inconclusive; defer LV005 promotion if behavioral evidence is inconclusive.
- Overrun checkpoint: no calendar limit; stop on material scope/permission conflict, infrastructure blocker or retry limit.

## Model Recommendation

- Recommended: GPT-5.6 Sol High.
- Reason: contract-preservation, parser and failure-path reasoning; advisory inherited guidance, not an assertion about current model availability.
- Criticality: high for future implementation.
- Current model known: no.
- Blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued.
- Decision state: clear.
- Material decisions: none blocking this planning phase; implementation gates remain explicit.
- Questions asked: none during running.
- Auto-resolved reversible decisions: kebab-case artifact names and sequential artifact writes.
- Optional owner refinements: none.
- Decision artifacts: decisions/lv-decisions.md.
- Next route: next declared planning phase only; stop before implementation.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: decision-artifact.
- Reason: preserve approved scope, safety boundaries and dependency gates.
- Owner decision required: no additional approval for requested planning artifacts.
- Owner decision: capture-now.
- Privacy/scope check: pass.
- Suggested entry title: Lean validation planning decisions.
- Suggested entry summary: current artifact and decisions/lv-decisions.md contain the planning evidence; no ad hoc global memory write.
