# Runtime Dependency Scope Fix

- Date: 2026-10-05
- Work mode: workflow-maintenance
- Risk: high; bounded change to a filesystem validation boundary
- Source: owner's instruction to fix the upstream checker, preserve the dependency symlink, update the named installation and rerun Phase8
- Baseline: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05
- Co zostaje: strict owned roots, evidence validation, schema1 and rejection of other links
- Co jest slabe: dependency links stop runtime inventory before capture records are checked
- Czego brakuje: explicit non-evidence dependency-directory classification
- Blokery / decyzje: no implementation decision missing; no final-owner-yes or publication inferred
- Recommended routing: upstream workflow-maintenance, local committed-source update, fresh target Phase7/8

## Plan Quality Contract

- Plan classification: implementation-capable
- Implementation writes planned: yes
- DoD source: owner instruction and current scoped inventory contract
- Testable DoD: prune only project-relative quality/artifacts/node_modules without traversal; print its exclusion; reject all other runtime links and every evidence reference into the excluded directory; invalid capture/QA still fails; preserve the target symlink; pass regressions and full workflow validation; use official updater and reassess target Phase7/8
- Artifact QA route: global-quality-review-stance
- Artifact QA trigger: pre-write acceptance/safety review
- Implementation Quality Closure route: global-quality-review-stance
- Required verification: adversarial scope probes, all runtime consumer regressions, full validator with all smoke groups, py_compile, diff check, live target checks after update
- Quality-ready criteria: no unresolved blocker in changed code, complete tests, current review, no hidden exclusions
- Owner opt-out: none for quality
- Blocking decision: none for implementation
- Residual risk: updating the target also brings its five missing upstream commits; fresh integration review is required

## Delivery Constraints

- Mode: owner-opt-out; continuing the accepted unbounded remediation
- Deadline: none
- Time budget: none
- Must-have outcome: safe inventory and fresh target assessment
- Cutline: no general ignore-symlink option, arbitrary exclusion list, package installation or schema migration
- Quality floor: all regression and full-profile checks, no skipped smoke groups

## Implementation Slice Plan

| slice id | goal | expected files/areas | acceptance check | evidence required | status |
| --- | --- | --- | --- | --- | --- |
| S1 | classify the single non-evidence dependency directory | validation-scope.py, qa-evidence.py, validation-profiles.md | no traversal, explicit diagnostic and blocked evidence references | code and adversarial review | complete |
| S2 | exercise safety and consumer behavior | tests/runtime-dependency-scope.py, smoke/core.sh, smoke/manifest.json | allowed dependency links coexist with real invalid-state failures | regression outputs | complete |
| S3 | validate, capture, locally commit and install | maintenance/capture evidence and official updater | full QA and preserved target link | actual exit codes and source identities | pending |
| S4 | refresh the named target's evidence | target project Phase7/8 and affected current QA | scoped checks eligible and history retained | current source-bound reports | pending |

## State And Authority

- State record required: yes
- State record path: ai-workflow-workspace/repo/capture-state/runtime-dependency-scope-fix.md
- State: pending-quality
- Cross-system impact: yes; install AI Workflow in the named AI System target, no AI System product-source change
- Handoff: ai-workflow-workspace/external-memory/memory/2026-10-05-runtime-dependency-scope-ai-system-handoff.md
- Instruction refresh: performed-full; upstream AGENTS, risk/permissions, slicing, delivery, quality, validation and updater contracts refreshed; clean dedicated branch
- Skills used: none; available domain skills do not match this Python validator correction
- Model recommendation: frontier/high reasoning; filesystem boundary and high-impact QA; non-blocking
- Stop rule: unknown source change, external effect, weakened evidence validation or scope growth requires reassessment

## Execution Evidence

Initial full validation exited 1 at check-status-consistency: three pre-existing project assessments bind an older changelog.md. Owner decision requested before any historical-artifact remediation. Full source and smoke verification remain required; no formal PASS is claimed for this maintenance record.

Owner approved byte-preserving history and new compatibility assessments for the
three named upstream projects. Twenty-one source-bound reports require refresh;
all original owning-project inputs match, and the deferred LV005 FAIL remains.
New tests are supplemental: all frozen smoke bodies/assertions remain unchanged.

### Current Verification And Stop

- Fixed dependency regression: passed; all four runtime consumers exercised, with rejection of invalid state and evidence references. The live target scoped distillation probe passed using the changed helper, before installation.
- Exact current-source isolated fixture: full profile passed, exit 0, 784 seconds; all five smoke groups passed, no skips. Source fixture parity was verified for all 475 selected files. This is product-source evidence, not full QA of the actual upstream runtime.
- Three owner-approved projects: 21 distinct current compatibility assessments created after semantic scope review; original report bytes and one original approval retained under their history directories. Deferred LV005 stays FAIL. Status and original owner decisions are unchanged; no new final-owner-yes is granted.
- Actual upstream check-status-consistency: exit 0. Actual check-qa-evidence and check-distillation-state: exit 1 on source-stale assessments of parallel-task-orchestration-v1.
- Actual upstream full profile: exit 1 at check-qa-evidence after 26 seconds. Twenty-one additional assessments and their bound historical approval require separately approved preservation and reassessment. No artifact of that fourth project has been changed.
- Owner subsequently approved preservation and compatibility re-review of the fourth project, followed by local commit/update/Phase7/8 after green QA. Twenty current PTO assessments were semantically reviewed and reissued, with 20 byte-identical originals and the original bound approval retained in history. The older recovery assessment is historical and unchanged. Original PTO status/owner decisions are unchanged; native operations/performance stay unverified. The earlier count of 21 additional items includes the bound approval, not 21 QA assessments.
- Actual upstream full QA is running again. No source commit, push, target update, activation or final-owner-yes has occurred.
- Target installation preflight identifies workflow-source-bound evidence in ai-system-integrity-and-efficiency-v2 and parallel-project-orchestration-v1. Separate owner decision requested before changing their private reports. These are target-owned runtime, not updater source writes.
- Target WEP supporting regressions repeated without source changes: focused editorial v2 46 tests, exit 0; integrated work-evidence 181 tests, exit 0, using the previously approved isolated dependencies. Real independent replay remains deferred.
- Official updater dry-run succeeded against the local dedicated branch; actual update was not attempted. Nested target installation remains on main at its original baseline.
- Existing dependency symlink is preserved. This remediation does not install packages or traverse the dependency target.

### Final Source Review And Target Preflight, 2026-10-05

- Actual upstream full profile completed with exit 0 after 754 seconds. All five smoke groups passed; 759 registered cases, including the one supplemental dependency regression; no skips. The earlier failed runs remain historical attempts, not current verdicts.
- Source review: no blockers found in the six changed source files. This is advisory maintenance review, not formal project Phase 5 or final owner acceptance. Detailed evidence: quality/runtime-dependency-scope-source-review.md under this repo namespace.
- Owner approved history preservation and new compatibility assessments for the two target projects only if scope/results are unchanged. That condition fails on the current target branch before updating Workflow: ai-system-integrity-and-efficiency-v2 has 15 changed inputs; parallel-project-orchestration-v1 has 12 missing and 20 changed inputs. Owning-project inputs match; the mismatches are target-source baselines, not rewritten task evidence.
- Example missing product source: .systems/ai/core/orchestration-compatibility.md. The target is codex/work-evidence-planning at 4f26727c9e1e8565db155905a16e114fcfcaf3dc, whereas the PPO final report assessed 297b6a971f272f9636d50eaf66d0f01cbc35a8ce. A Workflow-only update cannot supply missing AI System product files.
- Stop before actual target update or reissuing these two reports. No new target PASS, archival, branch integration, Phase 7/8 or final-owner-yes is inferred. A separate owner decision is needed to reconcile the approved target baseline while preserving existing WEP edits.
- S3 source verification complete; local source commit authorized, installation blocked at preflight. S4 remains pending. Capture remains pending-quality for the whole work unit because installed integration and target phase reassessment are not complete.
- Local source commit completed: a9a5c40, fix: exclude supporting runtime dependencies from evidence; exactly six reviewed source files. Upstream working tree clean, no push. Post-commit official updater dry-run exit 0 (result skipped, no fetch/merge/validation). Target nested clone remains unchanged; its dependency symlink inode and destination were rechecked unchanged.

## Cross-system Impact
- Owner decision: yes
- Counterpart: ai-system
- Handoff artifact: ai-workflow-workspace/external-memory/memory/2026-10-05-runtime-dependency-scope-ai-system-handoff.md

## Contract Compliance
- Work mode: workflow-maintenance
- Work mode compliance: pass for the approved narrow source and artifact scope
- Knowledge capture: required
- Capture target: repo-distillation and technical handoff
- Reason: reusable evidence/inventory boundary and explicitly authorized installation
