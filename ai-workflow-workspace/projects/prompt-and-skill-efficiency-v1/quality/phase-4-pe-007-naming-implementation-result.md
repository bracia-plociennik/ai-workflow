# Phase 4 PE-007 Continuation: Frozen Eval Naming

## Current State

- Work mode: full-project workflow maintenance; risk: high.
- Source: amended LOOP-003 specification, PE-007 exact-file approval and positive PE-007 recovery Spec QA.
- Tracked continuation scope: `.systems/scripts/check-naming` and additional cases in the already approved `.systems/scripts/check-validator-smoke-tests`. The original four-file LOOP-003 work remains unchanged unless an in-scope defect is found.
- DoD source: item 7 of the amended specification plus the original six conditions. No deadline/timebox by owner decision.
- Baseline: HEAD `6e483fdc26d309ef94d9690d0991fb45c417a3f5`; four approved tracked files modified, `check-naming` unchanged before PE-007's first write.

## Instruction Adherence Refresh

- Status: performed-targeted.
- Trigger: PE-007 changed the accepted tracked write set after the full-validator naming failure.
- Contracts refreshed: `AGENTS.md`, operating model, command routing, Phase 3 Spec QA, Phase 4, risk model, permissions, implementation slicing, instruction refresh, accepted amended spec, PE-007 and current naming/smoke scripts.
- Reviewed baseline: HEAD/worktree, five-file scope, current project status/task, failed full-validator marker and safe local test environment.
- Drift/conflict: none; PE-007 supersedes PE-006 only for the exact fifth-file correction and related smoke coverage.

## Implementation Slice Plan

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| L3b-1 | Recognize only marker-backed frozen eval inputs | `.systems/scripts/check-naming` | `fixture/**` and `runs/*/checkout/**` pass only under project-local eval with nonempty `freeze.md`; canonical and tracked names remain checked | path-boundary review, targeted naming checks | completed |
| L3b-2 | Guard allow and deny boundaries | `.systems/scripts/check-validator-smoke-tests` | frozen fixture and archived checkout pass; missing marker, canonical eval, unrelated workspace and tracked bad names fail for the expected reason | smoke IDs, outputs and full-current-diff review | completed |
| L4 | Formal quality closure | no further tracked write | all seven DoD conditions, semantic review, paired eval and explicit full validation | Phase 5 artifact and current validation markers | awaiting final validation and high-risk owner gate |

- Stop rule: no path outside the five approved tracked files, no modification of frozen inputs, no broad naming exemption, no reduced safety check, and no formal quality verdict from scripts alone. Scope or permission expansion returns to owner decision and Spec QA.

## Slice Execution Evidence

| Slice ID | Status | Files/Areas Changed | Checks Run Or Skipped | Acceptance Result | Residual Risk | Next Slice Or Stop Reason |
| --- | --- | --- | --- | --- | --- | --- |
| L3b-1 | completed | `.systems/scripts/check-naming` | `bash -n`, official naming validator and manual path-boundary review | Marker-backed raw eval fixture and archived checkout names are exempt; canonical eval and unrelated paths remain checked | Unusual fixture path shapes may require later evidence | L3b-2 |
| L3b-2 | completed | `.systems/scripts/check-validator-smoke-tests` | Positive frozen-input case and negative missing-marker, canonical-artifact and unrelated-path smoke IDs passed in the prior full run; current smoke rerun follows the final adversarial fix | Expected allow/deny behavior observed on synthetic fixtures | Full current run still needed after latest validator change | L4 |
| L4 | pending | none | Semantic full-diff review found and corrected a negated-retest validator bypass, then a safe-conditional false positive; full smoke rerun and formal Phase 5 remain | No quality verdict yet | Same-model synthetic eval showed no behavior gain; external validity limited | Full validation, review and owner gate |

## Plan Quality Contract

- Plan classification: implementation-capable.
- Artifact QA route: PE-007 recovery Spec QA, completed positively.
- Implementation quality route: formal `phase-5-quality` on all five files.
- Required verification: targeted naming boundary cases, smoke suite, semantic current-diff review, paired eval evidence and explicit full validation after semantic QA.
- Quality-ready criteria: all seven DoD conditions, no unresolved material finding, current instruction baseline, full validation success and owner approval for the high-risk quality gate.
- Blocking decision: none for the fifth-file write after PE-007; later high-risk quality approval remains owner-controlled.

## Owner Decision Checkpoint

- Interaction mode: interactive owner answer recorded.
- Decision state: clear for L3b implementation.
- Material decisions: PE-007.
- Questions asked: whether to expand the write set for frozen eval naming.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: none.
- Decision artifacts: `decisions/pe-007-loop-003-naming-fixture-scope.md`.
- Next route: L3b-1.

## Optional Knowledge Capture

- Capture recommended: yes, after formal quality.
- Target: project-memory.
- Reason: the frozen-eval naming boundary is a reusable validation lesson.
- Owner decision required: no for proposal.
- Owner decision: defer-to-distillation.
- Privacy/scope check: pass.
- Suggested entry title: Frozen eval inputs and naming validation.
- Suggested entry summary: Treat marker-backed eval fixture and archived checkout paths as raw inputs while preserving canonical artifact naming checks.
