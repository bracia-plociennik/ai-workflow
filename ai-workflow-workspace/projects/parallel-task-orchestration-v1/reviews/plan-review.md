# Plan Review
- Date: 2026-10-03
- Subject: planning/phase-2-project-plan.md and tasks.md
- Baseline: 8a0eeef; clean tracked source.

## Findings Resolved Before Plan QA
- P2: proposed smoke/parallel.sh was not part of the dispatcher's exact five-file/group manifest. Replaced with dedicated Python behavioral tests called through supplemental core.sh IDs. Frozen regions, original inventory and public groups remain unchanged. Related source files explicitly included in task scopes.
- P3: draft changelog path .systems/ai/CHANGELOG.md does not exist. Corrected to .systems/ai/core/changelog.md.
- Coverage gaps: included check-validator-smoke-tests coverage index in PTO-001 and behavioral test helper/manifest in each affected task. New policy validator must be audited by existing Review Completeness Gate.

## Post-Fix Full Review
All seven tasks checked against architecture and owner decisions after corrections.
Every task has goal, explicit source write set, out-of-scope, DoD, predecessor, risk, start/end gate and pending implementation approval.
Task index has identical IDs/spec routes. Quality column is a planned Phase 5 path, not evidence of implementation.
Serial order is necessary because the same helper/contract/templates are extended in several tasks.
Tests are added with each implementation task; PTO-006 integrates and evaluates, not the first testing step.
No fixture/model/backend test is claimed executed by planning.

## Adversarial And Producer-Consumer Audit
- Early capability publication: PTO-006 only after lifecycle/integration; installed declaration separate from real backend/approval.
- Zero platform support: serial fallback; cannot claim operational native support without a safe approved smoke.
- One unit accepted vs task complete: cross-task formal gates and capture retained.
- Max-three budget creeping back in: removed; only verified capacity.
- Manifest helper executing arbitrary commands: forbidden; plan/read-only CLI and explicit bounded state transitions.
- New group silently omitting prior tests: fixed using existing supplemental core convention, exact uniqueness audit.
- Single writer paths overlap across tasks: serial execution and spec refresh, not concurrent authoring.
- Handoff copying runtime/approvals: privacy-safe concepts/evidence only.
- Task router -> spec -> local tests -> acceptance -> common QA -> capture mapping complete.
- No unresolved material planning findings after correction.
- Residual risk: platform support and actual speedup await implementation evidence; runtime drift requires pre-write revalidation.

## Router Correction And Fresh Review
- Scoped status consumer rejected planned future Phase 5 paths as missing evidence. Corrected Quality column to none until implementation produces the real report; kept Spec QA route in Notes.
- Re-reviewed all seven rows and full plan after this correction. Task scope, DoD, risk, dependency order and formal quality route are unchanged. Plan QA run 002 supersedes run 001 for the new index bytes; all downstream Spec QA must be refreshed.

## Final Consumer Audit Correction
P2: validation-scope.py inventories an explicit directory allowlist that excludes the proposed orchestration namespace. PTO-004 now explicitly includes the consumer edit, an AC and mutation/symlink/foreign-root tests. Only canonical sanitized metadata is eligible; worktrees/raw logs remain outside. Re-reviewed the whole plan after this additive consumer correction; no task reorder or authority expansion. Plan QA run 003 and all downstream Spec QA use the corrected inputs.
