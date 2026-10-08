# PTO-002 Current-Diff Advisory Quality Review

- Date: 2026-10-03
- Baseline: HEAD 8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1 and reviews/pto-002-source-snapshot.json.
- Work mode: formal project, high-risk workflow-maintenance.
- Result: no unresolved material technical findings after fresh post-fix review.
- Formal gate eligibility: awaiting human acceptance for PTO-002. No formal PASS
  or permission for PTO-003 follows from this advisory record or green scripts.

## Findings And Blockers
- Resolved technical findings: Unicode parent alias collision; subtree hardlink
  alias collision; symlink ancestors of repository/manifest; Unicode combining
  order normalization. Exact candidate/reservation regressions cover the fixes.
- Resolved runtime evidence gaps: task index uses canonical `done`, unfinished
  Phase 4 does not prematurely route to Quality, and canonical Phase 4 result
  routers now reference the actual detailed implementation evidence.
- Remaining decision: high-risk Phase 5 owner acceptance for this task.
- No known in-scope bug or direct regression remains after the current review.

## Intent / Plan / Spec Compliance
- Compliance status: aligned.
- Compared owner request, accepted architecture/plan, task index, eight-path
  allocation spec, current code/diff and AC1..AC5.
- No scope creep, underbuild, overbuild or wrong-problem implementation identified.
- No native dispatch, model eval, transport, state mutation, capability publication,
  new public smoke group, source commit or AI System change is included.

## Definition Of Done Validation
| DoD | Evidence | Assessment |
| --- | --- | --- |
| AC1 | Strict exact JSON fields, identity/types, DAG and unsafe path regressions | satisfied |
| AC2 | Deterministic Kahn/priority order; whole-pool capacity and active reservation tests | satisfied |
| AC3 | Read/write/prefix/case/Unicode conflicts; subtree hardlinks fail closed; resources exclusive by default | satisfied |
| AC4 | Zero capacity/ready work, serial singleton, dynamic four-slot selection, failed/submitted not complete | satisfied |
| AC5 | CLI JSON/human; invalid input exit 2/no payload; fixture bytes/inventory unchanged; execution_authorized false | satisfied |

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Four disjoint units, known four slots | validated DAG and one parent slot | four proposals, no authority | fixed two/three cap or dispatch | no execution | capacity and CLI tests | template keys -> validate -> ordered candidates -> accumulated slots -> JSON |
| Submitted or stale predecessor | blocked dependent | reason, no dependent selected | accepted from done/prose/stale hash | blocked proposal | chain/diamond/cross-task tests | predecessor state -> digest check -> rejected_candidates |
| Colliding canonical/Unicode paths or reserved resource | exclusive overlap retained | omit conflicting candidate | two writers on alias/ancestor or reused running reservation | serialize or reject unsafe tree | prefix, Unicode and resource regressions | normalize parent -> overlap with reservation -> reject candidate |
| Symlink/hardlink/FIFO/malformed bytes | invalid input, no safe proposal | CLI exit 2, empty stdout | read FIFO or follow linked ancestors | reject before unsafe content read | path/special/UTF-8/schema tests | physical components/type -> reject -> stderr, no writes |
| Unknown checkpoint/capacity/isolation | conservative blocked/serial | explicit observed limit/reason | fourth parent task or inferred isolation | retain reservations | checkpoint/unknown tests | parent set accumulates across selected units -> slot exhaustion |

## Review Completeness Gate
- Status: complete for advisory technical review; formal approval is pending.
- Cross-contract consistency: aligned.
- Risk/work mode compatibility: aligned.
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes.
- Negative-space / adversarial review: completed.
- Policy-boundary adversarial matrix: completed for retained PTO-001 changes;
  37 cases and all active consumers, shared helper unchanged.
- Producer-consumer field audit: completed; all run/unit keys and types mapped
  into strict validation, CLI proposal fields into JSON/human output and smoke
  helper/coverage index/manifest into the existing five-group runner.
- Required-field mapping: complete for PTO-002, not future result/attempt schemas.
- Automated evidence role: supporting-only.
- Post-fix full re-review: completed, all 23 current project source paths and
  all eight PTO-002 paths including additive shared integration reviewed.
- Instruction refresh: performed-full after continuity restoration, then targeted.
- Instruction baseline: current.
- Reviewed baseline: current HEAD and exact source hashes in the snapshot.
- Closure freshness: current after final normalization fix and full source freeze.

## Evidence Reviewed
- Parent: 25 full offline tests, including subprocess wrapper and read-only checks.
- Independent sidecar: 24 focused tests, 17 type/container mutations, six
  combining-order variants, in-process CLI/type/budget/error probes. Sidecar did
  not execute subprocess wrapper or broad scripts; parent covered those.
- Core source run: current full includes core result pass, duration 66 seconds.
- Full project-scoped validation: result pass, exit 0, duration 656 seconds;
  all five groups, smoke 622 seconds, 741 IDs. Actual completion marker observed.
- Old 703 smoke records retained unchanged, frozen 674 IDs unchanged, no old ID
  removed; verify-manifest passed. No source edit occurred during full validation.
- PTO-001 current formal regression reassessment preserves its original history
  and corrects bindings for the three additive shared smoke files.

## Limits And Residual Risk
- Finite Unicode/filesystem/policy coverage, not a proof against malicious host
  mutation or TOCTOU. Dispatch must re-observe actual state under later preflight.
- The bounded metadata scan rejects unsupported hardlinks/special/linked subtrees
  and large access inventories. Prefer precise access sets; no partial safety claim.
- Native isolation/capacity, lifecycle mutation, acceptance/integration, performance
  and capability publication belong to later tasks and were not exercised here.
- No skipped applicable PTO-002 check; future native verification is not a current
  task completion claim. Remote state/CI was not queried; no publication is authorized.

## Knowledge Capture
- Capture state: pending-quality, is_distilled false for PTO-002.
- Target: phase-6-distillation only after accepted formal Quality.
- Cross-system impact: yes, one final privacy-safe handoff after completed project.
- Commit needed: no, current evidence is ignored/local-only; source commit not authorized.
- Push allowed: no.
