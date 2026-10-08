# PTO-003 Current-Diff Quality Review

- Date: 2026-10-04
- Baseline: HEAD 8a0eeef and reviews/pto-003-final-source-snapshot.json, 25 source paths.
- Scope: eight approved PTO-003 paths and affected PTO-001/002 consumers.
- Owner high-risk acceptance: decisions/pto-quality-range-approval.md, conditional.
- Current verdict: no unresolved material findings; complete semantic review and
  fresh full supporting validation. Formal high-risk gate uses the accepted owner decision.

## Findings And Blockers
- Resolved P1: attempt could be replayed with changed run/project/coordinator.
  Preflight now freezes all originating identity fields; verifier compares them.
- Resolved P2: additional failed/skipped checks did not block readiness. All
  reported check outcomes now must pass, with findings/skips also preventing readiness.
- Parent review also added empty-directory/mode/deletion coverage, termination
  observation before inventory and frozen minimal-context paths.
- Resolved P2: worker root metadata was not inventoried. Preflight now binds
  root mode and device/inode; the verifier rejects drift before result inventory.
- Independent eight-path post-fix review found no remaining material findings.
- Fresh full run after the final root-metadata fix passed (645 seconds, exit 0).
- Native operational claims are out of PTO-003 completion; neither fake observations
  nor JSON constraints_verified are an authenticated OS sandbox.

## Intent / Plan / Spec Compliance
- Compliance status: aligned.
- Owner task, architecture, plan, AC1..AC5 and approved eight-path scope reviewed.
- No recursive workflow, transport, arbitrary executor, automatic worktree management,
  source commit/push, AI System source write or native capability advertisement.

## Definition Of Done Validation
| AC | Review evidence | Assessment |
| --- | --- | --- |
| AC1 | Task/slice/goal/DoD, approval/source snapshot, execution input/context/check/stop fields | satisfied |
| AC2 | Physical isolated cwd, exact observed writable root, actual file hashes; unverified constraints reject | satisfied for consistency checks; native authenticity remains external |
| AC3 | Exact attempt/run/coordinator binding; actual output/baseline/diff; structured evidence/findings/skips | satisfied |
| AC4 | Protected routers reject even allowlisted; actual unreported writes and modes fail | satisfied within observed enforcement boundary |
| AC5 | No create/copy/cleanup call; Git metadata unsupported fails closed | satisfied |

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Frozen minimal inputs and isolated fake workspace | parent-owned inventory/identity | verified submission, accepted false | native sandbox claim or task PASS | consistency only | protocol positive case | unit -> preflight -> frozen baseline -> actual diff -> verifier |
| Same source with foreign run/coordinator or changed DoD | origin mismatch retained | rejection | replay across execution pools | fail closed | replay and unit drift cases | origin captured -> current manifest mismatch -> exception |
| Omitted actual file, mode, directory or deletion | changed set from actual inventory | rejection | self-report overrides filesystem | fail closed | actual inventory cases | before map vs actual tree -> actual scope check |
| Required/additional failed or skipped check | submitted with disclosures | quality_ready false | green required subset hides failure | preserve failure | additional check cases | all structured outcomes -> readiness, not acceptance |
| FIFO, link, broad writable root or live worker | no safe inventory/dispatch | rejection before hashing | external or concurrent write claim | blocked | special/observation/termination cases | observed constraints/type -> reject without execution |

## Review Completeness Gate
- Status: complete; current source snapshot unchanged through the full run.
- Cross-contract consistency: aligned; predecessor regression review recorded separately.
- Risk/work mode compatibility: high formal project, accepted scope, no new authority.
- Policy-boundary adversarial matrix: retained 37 policy cases; lexical contract checker passes.
- Producer-consumer field audit: unit execution, observed preflight, attempt/result and
  supplemental smoke manifest exact fields reviewed. attempt_id and termination_verified
  are parent-owned additions, never worker authorization.
- Required-field mapping: complete for dispatch/result, not future lifecycle schemas.
- Post-fix full re-review: parent and independent reviewer complete across all eight paths.
- Instruction refresh: performed-full at continuity, targeted at write/closure.
- Instruction baseline: current.
- Reviewed baseline: exact source snapshot and current accepted inputs.
- Closure freshness: current, after final edit and full run; not stale result reuse.
- Automated evidence role: supporting-only.

## Evidence Reviewed
- Original 25 planner cases plus 12 filesystem protocol regressions pass.
- Manifest verification and check-parallel-task-orchestration pass.
- Earlier sandbox preflight failed on ps; the old escalated run was interrupted
  deliberately before fixing root metadata (exit 143, duration 256 seconds).
  Neither supplies complete full validation evidence.
- Full source freeze is checked against the snapshot; no source writes during the run.
- Independent reviews found three material findings; all fixed with regression tests.
- Full run: result=pass, exit_code=0, duration_seconds=645; 742 smoke IDs across
  all five groups. Authenticated source receipt: /tmp/pto-003-full-source.json.
  The private key is not published. This remains supporting, not semantic evidence.

## Residual Risk
No proof against malicious host, backend lying, write-and-restore, outside-root
effects or unobserved activity. Parent must independently verify actual backend
enforcement and termination. Git-backed workspace adapter is not implemented here.
Future lifecycle/integration/native capability and performance belong to PTO-004..006.

## Knowledge Capture
- Required: Phase 6 after formal Quality, then Phase 7 at third parent task.
- No durable System Insights write; one AI System handoff at program completion.
- Commit/push/final-owner-yes: not authorized.
