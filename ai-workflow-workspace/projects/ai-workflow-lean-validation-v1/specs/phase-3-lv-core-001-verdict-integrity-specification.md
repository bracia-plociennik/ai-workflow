# Phase 3 Specification: LV001

## Metadata

- Project: ai-workflow-lean-validation-v1.
- Task/package ID: LV-CORE-001-verdict-integrity.
- Task/package name: Trustworthy smoke and QA verdicts.
- Date: 2026-09-29.
- Readiness: owner approved high-risk source work; fresh Spec QA and readiness transition remain required before implementation.
- Baseline: f362ce3 plus staged, conflict-free merge of fetched origin/main 1b45483 on codex/ai-workflow-lean-validation-v1. Pre-LV001 merged source diff SHA-256: 16ac8b1002c6f29ff8f05a5950747c6e927cee22f884fe4e590022bb7d14e14c.

## Sources

- Project plan: planning/phase-2-project-plan.md; Plan QA: quality/phase-2-plan-qa.md.
- Architecture: architecture/phase-1-architecture.md and its Architecture QA.
- Intake: intake/phase-0-repo-intake.md; decisions: decisions/lv-decisions.md; context.md.
- Existing dependency outputs: current repository source and accepted planning artifacts.

## Task Contract

- Goal: Reject false smoke success and select only a coherent current QA assessment.
- Scope: Smoke outcome API; current-run QA parsing, templates and status consumers; compatibility and recovery diagnostics.
- Out of scope: No historical rewrites, automatic legacy registration, broad smoke partition or timing optimization.
- Definition of Done: Reserved infrastructure exits cannot pass policy tests; expected failures match status and diagnostic; current QA has one matching run/baseline/evidence/gate; ambiguous or stale assessment fails; valid V1 and permitted legacy remain supported.
- Dependencies: none beyond Spec QA and high-risk source approval.
- Risk type: high; formal workflow-maintenance.
- Main risk: false confidence, coverage loss or unintended authority change.
- Start condition: LV-DEC-002, current source baseline, accepted Spec QA and predecessor quality evidence.
- End condition: testable task DoD, semantic findings-first Phase 5, applicable explicit full validation and no unresolved material findings; later capture follows phase rules.
- Requires user decision before implementation: yes.

## Proposed Write Set

- .systems/scripts/check-validator-smoke-tests
- .systems/scripts/check-qa-evidence
- .systems/scripts/check-status-consistency
- .systems/scripts/lib/qa-evidence.py (new)
- .systems/ai/core/full-qa-verification.md
- .systems/ai/core/status.md
- .systems/ai/templates/workflow/phase-{1-architecture-qa,2-plan-qa,2-packaging-qa,3-spec-qa,5-quality,8-final-check}.template.md
- .systems/ai/examples/projects/EXAMPLE/quality/ (only matched updated examples)
- .systems/scripts/check-full-qa-verification
- .systems/scripts/check-review-completeness-gate

These paths are the proposed task ceiling, not current write permission. Brace expressions enumerate only named sibling files. New helpers are explicitly marked new. Any additional source consumer discovered at pre-write must be reconciled in this spec and Spec QA before editing.

## Dependency Status

- No predecessor implementation dependency; current source inspected.
- Source approval/base: LV-DEC-002 approved. Branch chosen and origin/main merged without conflict; merge remains uncommitted until task quality gate.
- Canonical main introduced explicit QA result selection in `check-qa-evidence` and five negative/positive smoke cases. LV001 must preserve those checks and route V2 through one typed current-assessment reader rather than returning to broad prose `PASS` matching.
- No source or timing/eval outcome is assumed.

## Interface And Implementation Slices

1. Inventory negative smoke calls and all after-call assertions before touching outcomes. Replace implicit any-nonzero acceptance with an explicit expected-status and diagnostic contract. Preserve existing IDs. Capture stdout/stderr per case; diagnostics are specific to the intended rejection, not just the word error.
2. Add a stdlib QA reader shared by check-qa-evidence and status assessment where required. New reports use a versioned current-run block and unique run identity; validate structured values before enforcing existing completeness rules. Retain the merged main result-selection behavior for existing V1 and negative final-check evidence.
3. Update all six formal QA templates and their corresponding EXAMPLE QA reports atomically with consumers. Do not rewrite real closed workspace reports. Add smoke and parser unit fixtures, then full-current-diff review.

## Current QA Schema

New marker: QA verification contract full-qa-verification-v2. Exactly one top-level Current QA Run section contains Run ID, Artifact kind, Project/task identity, Assessed source HEAD, Assessed worktree digest, Input artifacts (relative path plus SHA-256), Verdict and Gate Decision. That section owns the required completeness/evidence/findings subsections. Other runs live only under Historical Runs and cannot supply missing current fields.
The parser recognizes Markdown headings outside fenced blocks, rejects duplicate keys/current sections and invalid enums, and produces one structured assessment. Verdict must match Gate Decision and task/phase identity. Source HEAD alone is insufficient for dirty worktrees; the digest covers staged/unstaged/untracked in-scope inputs without hashing the assessment file into itself.
Assessment reports are contained in the owning project/example quality root. Assessed input references carry an explicit root kind (workflow-source, approved-target-source, owning-project-evidence) and relative path; canonicalize against that allowlist. System source hashes are allowed without permitting arbitrary filesystem reads. Reject cross-project borrowing, traversal and escaping symlinks. Hash only explicit approved non-secret inputs; sensitive/unapproved discoveries remain metadata-only and block eligibility rather than authorizing content reads.
Input artifact hashes bind to the assessed version, not blindly to latest HEAD after unrelated commits. At phase progression compare the intended scope's current fingerprint to that assessment. Unrelated changes cannot make historical reports invalid, but changed assessed inputs invalidate current eligibility.
Status consumers resolve the same current assessment. A fabricated later PASS with older or unrelated evidence fails.
Single-run V1 keeps V1 completeness checks. Unmarked registered pre-V1 retains exact path/hash admission. Ambiguous V1 multi-run records remain immutable and report recovery-required; they cannot silently become V2 or enter a registry to bypass missing evidence.

## Planned Tests

| ID | Input | Expected state/output |
| --- | --- | --- |
| V1-01 | intended policy error code + matching diagnostic | negative test succeeds |
| V1-02 | 0, wrong diagnostic, or wrong nonzero code | negative test fails |
| V1-03 | 124/126/127/130/143 or crash/signal under ordinary rejection | infrastructure failure, never successful rejection |
| V1-04 | explicitly declared timeout test returning 124 and marker | succeeds only for declared timeout contract |
| V1-05 | completed V2 run with matching input identities/evidence/gate | eligible for its own phase only |
| V1-06 | historical FAIL plus complete current assessment | history preserved; only current assessment evaluated |
| V1-07 | component PASS but current FAIL; duplicate current block; missing verdict | ineligible, precise reason |
| V1-08 | later PASS with stale input digest or evidence owned by another run | stale/mismatch, never eligible |
| V1-09 | heading-like text inside code fence | not a current-run selector |
| V1-10 | missing/unreadable file, traversal/symlink, invalid schema enum | fail closed, no report mutation |
| V1-11 | valid V1 and exact registered pre-V1; byte-changed registry input | preserve valid admission; changed fingerprint rejected |
| V1-12 | safe prohibition, unsafe enablement, compound contradiction | unchanged policy boundaries; unsafe cases rejected by relevant policy checks |

## Adaptive Verification Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Process status and diagnostic | expected rejection or infrastructure failure | accurate smoke/timing result | timeout counted as policy success | nonzero suite failure | V1-01..04 | policy rejection then missing-command trace |
| Versioned Markdown QA | one typed current assessment | scoped gate eligibility | mixed-run evidence | block with recovery reason | V1-05..12 | valid current run then stale-input failure |

## Specific DoD And Stop Conditions

Every current negative test has an explicit expected failure contract; reserved statuses cannot be admitted accidentally. Consumer outputs agree for each supported artifact kind.
Stop if legacy ambiguity would require altering closed runtime evidence or changing final owner approvals; that is a separate recovery task, not a parser shortcut.
Rollback: retain immutable legacy inputs; revert only the new source adapter through approved change, never reintroduce known smoke false positives as an optimization.

## Potential Errors

Wrong rejection status accepted; multi-run QA evidence mixed; hashing assessment output recursively.

## Edge Cases

Reserved exit statuses, fenced headings, deleted inputs, relative-root aliases and symlink escape.

## Assumptions

Current single-run V1 remains supported; ambiguous history stays immutable.

## Blocking Uncertainties

None for this conditional specification: design and stop rules are explicit. Execution remains blocked by LV-DEC-002 and the Dependency Status section; predecessor source changes require fresh Spec QA.

## Non-Blocking Uncertainties

Actual runtime cost and future compatibility details are measured during implementation; no performance gain is assumed. Discovery outside the proposed write set stops for spec reconciliation.

## User Decisions

LV-DEC-001 resolved the delivery opt-out. LV-DEC-002 requires source execution/base approval. LV-DEC-003 governs LV005 model runs. LV-DEC-004 governs later commit/handoff. Planning approval resolves none of these future gates.

## Implementation Gate

- DoD complete and testable: yes.
- Dependencies satisfied or explicitly gated: yes, explicitly gated above.
- Required user decisions resolved: yes for LV001; LV005 eval and later shared impact are separately approved.
- Can enter implementation: after fresh Spec QA and run readiness transition, not from this spec alone.
- Blocking reason: fresh Spec QA of the merged source baseline and explicit readiness `ready` remain pending.
- Gate invalidation: changed predecessor interfaces, approved scope, source or evidence requires spec refresh and fresh Spec QA.

## Plan Quality Contract

- Plan classification: implementation-capable.
- DoD source: accepted project context, architecture and LV001 task contract.
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
