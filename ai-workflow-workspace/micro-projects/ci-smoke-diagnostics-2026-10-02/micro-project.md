# CI Smoke Diagnostics Portability

- Work mode: workflow-maintenance
- Risk: medium
- Baseline: main, f73891b, clean
- Owner approval: implement accepted repair, QA/full validation, then commit/push if successful
- Cross-system impact: not-applicable; upstream-specific diagnostic assertion repair, no execution contract change
- Distillation State: repo/capture-state/ci-smoke-diagnostics-2026-10-02.md

## Task Idea Validation

- Co zostaje: fail-closed policy helper, expected exit code 1, full smoke coverage.
- Co poprawic: assertion must use the helper diagnostic instead of version-specific rg stderr.
- Czego brakuje: portable and negative assertion regressions.
- Blokery / decyzje: none; no settings, policies or unrelated workflow changes.
- Rekomendowany routing: scoped workflow-maintenance fix.

## Implementation Slice Plan

| Slice | Goal | Files | Acceptance check | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Stable diagnostic and adversarial assertion cases | smoke/common.sh, smoke/core.sh | Both rg formats accepted; missing marker/wrong status rejected | All five isolated regressions passed | completed |
| 2 | Preserve inventory | smoke/manifest.json | Existing IDs and frozen regions unchanged; new IDs uniquely owned | 695 existing IDs unchanged; exactly 5 supplemental core IDs added; manifest verified | completed |
| 3 | Review, full validation, commit/push | tracked scope above only | Fresh findings-first review and full validation pass | Semantic review and full validation complete; 3218aa7 committed and pushed; remote CI running | completed |

## Definition of Done

- Missing-source rejection uses the exact helper-owned diagnostic and exit code 1.
- Short and long rg diagnostics both pass the real smoke assertion.
- Missing helper marker and exit codes 0/2 are rejected.
- Existing test IDs, ownership and frozen regions remain unchanged.
- Semantic current-diff review has no unresolved material findings.
- Full validation succeeds before commit/push; remote CI is checked afterward.

## Plan Quality Contract

- Implementation writes: yes, three tracked smoke files only.
- DoD source: accepted CI diagnostic repair plan and conditions above.
- Artifact QA route: global-quality-review-stance.
- Implementation QA route: global-quality-review-stance.
- Required verification: assertion regressions, manifest audit, core/quality smoke groups, explicit full validation.
- Residual risk: local tests simulate both rg formats; real Linux CI must confirm portability.
- Quality-ready criteria: all done conditions and no unresolved material findings.
- Blocking decision: none.
- Next route: execute slices, semantic review, full validation, commit/push.

## Semantic Quality Review

- Owner intent / plan / scope / DoD compliance: aligned; only the three planned smoke files changed.
- Findings/blockers in implementation: none found after complete current-diff review.
- Formal gate eligibility: not-applicable; advisory workflow-maintenance closure, no formal implementation PASS.
- Review baseline: f73891b plus current three-file diff.
- Instruction refresh: performed-full after context compaction; current AGENTS, routing, operating model, risk, permissions, slicing, capture and quality contracts reviewed.
- Post-fix full re-review: completed; no implementation edits after this review.
- Evidence role: supporting-only.
- Producer-consumer audit: helper emits the stable marker and sets fail=1; run_must_fail requires exit 1 and an anchored exact marker; manifest maps each new ID to core.
- Adversarial matrix: both rg formats accepted; missing marker rejected; marker with exit 0/2 rejected; restoring the old version-dependent expectation is caught by the short-format regression.
- Failure-path trace: rg exit 2 -> helper fail=1 -> caller exit 1 -> smoke assertion accepts only exact helper diagnostic plus status 1.
- Frozen-region / coverage audit: all 674 frozen IDs, 110 external assertions, 34 nested assertions, existing supplemental IDs, ownership and region hashes preserved.
- Full validation: explicit full profile passed on the byte-identical current-source fixture, all 700 smoke IDs; smoke duration 615s, full duration 648s, exit 0.
- Remaining verification: remote Linux CI after publishing.

## Validation Environment Notes

- Full run with local ignored runtime stopped on stale historical QA fingerprints in two already-existing closed projects (changelog.md and smoke/core.sh inputs). Historical evidence was not rewritten or bypassed.
- CI-equivalent source snapshot contains all 439 selected tracked current-worktree inputs with matching SHA-256 values and no private ignored runtime.
- First isolated sandbox run stopped when the smoke supervisor could not use ps. The full run was restarted with the required local process-inspection permission.
- Workspace artifacts remain ignored; no global memory, client repository, policy helper or Actions workflow changes.

## Quality Closure And Commit Readiness

- Findings: none in the scoped implementation.
- Blockers: none for publishing the CI source repair; unrelated local historical runtime fingerprints remain stale.
- DoD: source repair, portable/negative regressions, preserved inventory and full source validation satisfied; remote confirmation pending publication.
- Review Completeness Gate: complete, current, advisory-only; policy helper unchanged, assertion failure paths and producer-consumer mapping reviewed.
- Adaptive verification: long/short stderr -> helper marker plus exit 1 -> accepted; missing marker or exit 0/2 -> rejected; old assertion mutation -> regression caught.
- Contract compliance: warning only for the explicitly separate ignored historical runtime; workflow-maintenance scope, risk and owner authority aligned.
- Cross-system impact: not-applicable; no substantive system execution contract upgrade.
- Knowledge capture: no separate phase-6 artifact required; repair evidence and lesson are captured here and in permanent regression tests.
- Distillation disposition: not-applicable, no additional reusable knowledge beyond the existing stable-diagnostic portability lesson captured in regression tests.
- Instruction refresh: performed-targeted for commit readiness; baseline and write set unchanged.
- Validation scope: full tracked-source CI-equivalent snapshot; not a claim that local historical runtime QA is fresh.

## Publication Evidence

- Commit: 3218aa7861215ab06f0d6f40797be25f3f728565
- Subject: fix: make smoke failure diagnostics portable
- Push: origin/main, fast-forward from f73891b.
- Git status: clean, main synchronized with origin/main.
- Tracked workspace files: none.
- Remote CI: https://github.com/bracia-plociennik/ai-workflow/actions/runs/36986843550 ; failed on a separate workspace bare remote HEAD fixture. Original diagnostics and core/policy/quality/skills groups passed.

## Owner-Approved Fixture Fix Loop

- Scope expansion: smoke/workspace.sh and smoke/manifest.json; only two bare-remote initial branch declarations.
- Evidence: remote HEAD points at an empty default branch after pushing main; clone has no checked-out AGENTS.md.
- Preflight: implicit bare HEAD fails under init.defaultBranch=master and succeeds under main; explicit initial-branch=main succeeds under both.
- DoD: both fixture remotes explicitly use main; original 700 IDs and assertions unchanged; frozen-region behavior audit complete; targeted fixtures tested under both defaults; full validation forced to master passes; subsequent Linux CI checked.
- Slices: fixture branch declarations -> manifest/behavior audit -> targeted master/main checks -> semantic review -> full master-default run -> commit/push.
- Quality closure: current for expanded scope after fresh full-current-diff review and full master-default validation.
- Handoff: not-required; fixture-only repair, no execution contract change.

## Fixture Fix Loop Review

- Current-diff review: no findings or blockers in the two-statement repair.
- Owner intent / DoD / scope: aligned; bootstrap/update product scripts and host Git configuration unchanged.
- Producer-consumer trace: explicit main creates refs/heads/main as bare HEAD; push populates that ref; clone checks out AGENTS.md; existing bootstrap and dirty/origin/approval/workspace-preservation assertions remain unchanged.
- Assertion/behavior audit: both modified frozen regions differ only in the git init argument; their line counts, all command/outcome contracts, all 700 test IDs, 110 outside assertions and 34 nested assertions are identical to 3218aa7.
- Targeted verification: all existing bootstrap/update tests in both affected regions passed under default master and main.
- Adversarial evidence: original implicit bare HEAD reproduces the missing checkout under master; explicit main succeeds under both configurations.
- Post-fix full re-review: completed, current; no source edit after review.
- Full validation: passed with master forced through process-local Git config, all 700 smoke IDs; smoke 595s, full 624s, exit 0.
- Harness correction: first master-default run stopped because its live log was inside the snapshot and changed source identity. The source-drift guard behaved correctly; log moved outside the source root, no product/test changes made, full run restarted.
- Automation evidence role: supporting-only; semantic current-diff review, targeted master/main checks, behavior audit and full validation complete.
- Final scoped verdict: no findings or blockers found; ready for owner-authorized commit/push.
- Contract compliance: workflow-maintenance, medium, approved two-file scope; unrelated ignored historical QA remains outside this source repair.
- Capture decision: evidence recorded here; no separate formal phase-6 record required for fixture-only repair.

## Final Remote Confirmation

- Second commit: a758bb45e4e7e639d0b65e0189d776ea5176d50d
- Subject: fix: set explicit main branch in bare smoke fixtures
- Push: origin/main, fast-forward from 3218aa7.
- CI: https://github.com/bracia-plociennik/ai-workflow/actions/runs/36989456124 ; success, validate job 6m33s.
- All job steps passed: full validation, strict naming, whitespace.
- Review baseline: 3218aa7..a758bb4, unchanged reviewed source; no further tracked edits.
- Final scoped QA: no findings or blockers found; all accepted source repair conditions satisfied.
- Remaining out-of-scope items: stale historical QA fingerprints in local ignored runtime; non-blocking Actions/Ubuntu migration notices.
- Workspace artifacts: local-only/ignored, never staged.
