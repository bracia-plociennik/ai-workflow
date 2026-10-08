# Phase 5 Quality: PSE-CORE-001 Conditional Instruction Router

## Metadata

- Project: `prompt-and-skill-efficiency-v1`
- Task/package ID: `PSE-CORE-001-conditional-instruction-router`
- Date: `2026-09-25`
- Implementation/spec under review: root `AGENTS.md`; accepted CORE-001 specification and Phase 4 result.
- Workflow phase: `phase-5-quality`
- Result: `PASS`, with high-risk owner approval recorded in `decisions/pe-004-core-quality-and-cross-system-handoff.md`.
- QA verification contract: `full-qa-verification-v1`

## Definition Of Done Validation

| DoD Item | Result | Evidence |
| --- | --- | --- |
| Shorter unconditional read-first list and explicit conditional routes | PASS | The complete one-file diff has 31 insertions and 68 deletions; four always-on core policies remain, with task/phase/risk/domain routes. |
| Mandatory authority, risk, permissions, approvals, skills, QA and phase behavior retained | PASS | Full-diff contract mapping and 10/10 paired GPT-6 Sol High synthetic cases found no missed mandatory policy, forbidden action or false formal quality verdict. |
| Directly observed reduction in irrelevant explicit contract reads | PASS | Frozen-rubric JSONL grading: development 11 to 5, holdout 17 to 7, total 28 to 12; one mixed case increased from 1 to 3. |
| Mandatory root instruction autoload coverage | PASS | Candidate SHA-256 `eab833e37b454578891d7e36cc8f9a4fedf52ed1251dcd73b887f19e8e8330e2`, 32,567 bytes; no CLI truncation warning in 10 candidate cases. Baseline at 34,969 bytes warned at 32,768. |
| Exact approved tracked write set | PASS | `git diff --name-only` lists only `AGENTS.md`; bytes match the evaluated v4 candidate. |
| Semantic QA and applicable validation | PASS | Findings-first current-diff review against current `origin/main`, `git diff --check`, paired grading and a fresh full validation on the default environment with a successful completion marker. |

## Intent / Plan / Spec Compliance

- Result: `PASS`
- Owner instruction reviewed: `yes`; CORE-only implementation, then explicit high-risk quality, phases 6 and 7, and local commit.
- Accepted plan reviewed: `yes`; amended Plan QA and PE-003 defer SKILL-002 and LOOP-003.
- Accepted spec reviewed: `yes`; CORE-001 specification and accepted Spec QA.
- Scope/out-of-scope reviewed: `yes`; only root `AGENTS.md` tracked; no skill or script edit.
- Acceptance criteria reviewed: `yes`; read efficiency, autoload safety, mandatory-policy retention and one-file scope.
- Compliance status: `aligned`
- Wrong problem solved: `no`
- Owner instruction mismatch: `no`
- Accepted plan mismatch: `no`
- Accepted spec mismatch: `no`
- Acceptance criteria gap: `no`
- Scope creep: `no`
- Underbuild: `no`
- Overbuild: `no`
- Evidence: accepted spec, PE-002/003/004, Phase 4 result, controlled eval traces, current `AGENTS.md` diff and fresh full validation result.

## Review Completeness Gate

- Cross-contract consistency: `aligned`; root router keeps existing contract and phase authority.
- Risk/work mode compatibility: `aligned`; high-risk full-project workflow maintenance with human quality approval.
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: `yes`.
- Negative-space / adversarial review: `completed`; read-only security, skill review near miss, mixed UI/blockchain, formal architecture QA, tiny docs and completion routes checked.
- Automated evidence role: `supporting-only`
- Post-fix full re-review: `completed`; entire current `AGENTS.md` diff reviewed after candidate v4 promotion, the late capture-state evidence repair and fast-forward to canonical `origin/main`.
- Reviewed baseline: `e8b99e8` (`origin/main`), branch `codex/prompt-and-skill-efficiency-core-001`, only tracked diff `AGENTS.md`, SHA-256 `eab833e37b454578891d7e36cc8f9a4fedf52ed1251dcd73b887f19e8e8330e2`.
- Instruction refresh: `performed-full` on resume; targeted at quality closure.
- Instruction baseline: `current`
- Closure freshness: `current`
- Policy-boundary adversarial matrix: `completed`; no changed route enables an approval, risk, QA, source-authority or write bypass.
- Producer-consumer field audit: `completed`; no runtime schema field changed, and each changed root trigger retains a named core or phase consumer.
- Producers/consumers reviewed: `AGENTS.md` against `command-routing.md`, `operating-model.md`, `risk-model.md`, `permissions.md`, `workflow.md`, quality, skills, capture and update contracts.
- Required-field mapping: `complete`
- Evidence: full tracked diff against `e8b99e8`, accepted spec and decisions, Phase 4 result, paired case traces, new validator completion marker, and scoped capture-state record.

## Adaptive Data / Integration Verification Matrix

- Applicability: `not-applicable`
- Not-applicable reason: `Instruction routing text only; no data model, parser, integration, persisted state or executable entrypoint changed. Policy-route and producer-consumer audits cover the relevant risk.`

## Edge Cases And Regression Review

| Case | Result | Evidence |
| --- | --- | --- |
| Small documentation work | covered | One-slice route retained; irrelevant reads reduced in controlled case. |
| Security review | covered | Read-only risk and permission boundary retained; no automatic fix. |
| Skill review near miss | covered | Candidate loads active skill-creator guidance. |
| Formal architecture QA | covered | Missing design evidence still blocks formal phase acceptance. |
| Mixed UI/blockchain work | covered with cost warning | Mandatory guidance retained, but one holdout case used two additional irrelevant reads. |
| Completion, status and target update routes | static review | Changed root routing still points to unchanged detailed contracts; no target repository touched. |

## Findings

### Bugs In Scope

- None found in the current `AGENTS.md` diff after findings-first review.

### Resolved Process Finding

- The scoped Distillation State producer record was missing at the first implementation write. It now exists as `pending-quality`; the original timing violation remains documented and cannot be retroactively erased. The current Phase 5 and Phase 6 consumers have a canonical record.

### Warnings And Skipped Checks

- Candidate has about 201 bytes of headroom before the observed CLI instruction truncation threshold; future expansion needs autoload verification.
- Earlier full runs failed intermittently while Git copied bare-clone fixture objects, including with `/private/tmp`; the exact operating-system cause is unproven. Canonical `origin/main` replaced the affected bare-clone fixture setup with `git init --bare` and `git push`. After a non-destructive fast-forward, the full profile passed in the default environment. No smoke-runner edit was made in this CORE scope.
- Synthetic command traces do not reveal every OS-level file open or prove token savings. There is no product build for a root policy text change.
- Skipped check affects quality verdict: `no`; no required check was skipped. Controlled behavioral cases, semantic review and a fresh default-environment full validation cover the accepted DoD.

## Quality Gate

- Intent / Plan / Spec Compliance PASS: `yes`
- Review Completeness Gate PASS: `yes`
- Cross-contract consistency aligned: `yes`
- Risk/work mode compatibility aligned: `yes`
- Negative-space / adversarial review complete or not applicable: `yes`
- Automated evidence treated as supporting-only: `yes`
- Post-fix full re-review complete or not required: `yes`
- Instruction baseline current: `yes`
- Closure freshness current: `yes`
- Policy-boundary adversarial matrix complete or not applicable: `yes`
- Producer-consumer field audit complete or not applicable: `yes`
- Required-field mapping complete or not applicable: `yes`
- 100% DoD satisfied: `yes`
- No known bug in scope: `yes`
- No regression in changed/direct paths: `yes`
- Edge cases covered or explicitly rejected: `yes`
- Explicit evidence attached: `yes`
- Quality result: `PASS`
- Required next phase: `phase-6-distillation`

## Distillation State

- Work ID: `PSE-CORE-001-conditional-instruction-router`
- State after quality closure: `ready`
- Quality artifact: this file.
- Source implementation artifact: `quality/phase-4-pse-core-001-conditional-instruction-router-implementation-result.md`
- Privacy/scope check: `pass`; only synthetic/system evidence.
- Residual risk: the late original state-producer write remains a disclosed process deviation.

## Delivery Constraints QA

- Constraint source: owner-approved no-deadline/no-timebox decision in the accepted specification.
- Deadline/timebox status: `owner-opt-out`
- Delivered scope: CORE-001 `AGENTS.md` router only.
- Deferred scope: SKILL-002 and LOOP-003.
- Quality floor preserved: `yes`
- Overrun decision: no deadline/timebox applies.
- Evidence: project status, accepted spec and PE-003.

## Validation Execution Record

- Semantic QA result: aligned with owner intent and full CORE-001 DoD.
- Findings/blockers: none unresolved in the approved tracked scope; process and temp-fixture warnings disclosed above.
- Product checks: 10/10 controlled paired synthetic cases; no product code changed.
- Workflow script applicability: applicable for high-impact workflow router confidence.
- Targeted workflow commands: `git diff --check`, paired JSONL grader and `.systems/scripts/validate-workflow --profile full --progress summary --explain`.
- Script evidence role: `supporting-only`
- Final verdict: formal quality approval as recorded in PE-004, with the quality gate above satisfied.

## Evidence

- Command: `cmp AGENTS.md /private/tmp/pse-core-001-candidate-v4-AGENTS.md` exited 0.
- Command: `git diff --check` exited 0; `git diff --name-only` listed only `AGENTS.md`.
- Command: controlled JSONL grading observed irrelevant reads 28 baseline versus 12 candidate across 10 matched cases.
- Command: `.systems/scripts/validate-workflow --profile full --progress summary --explain` exited 0 and emitted `AI_WORKFLOW_VALIDATE_COMPLETE profile=full result=pass exit_code=0 duration_seconds=552`; the smoke suite emitted `AI_WORKFLOW_SMOKE_COMPLETE group=all result=pass exit_code=0 duration_seconds=518`.
- Manual-checks: owner intent, CORE spec, full current diff against `e8b99e8`, authority and risk routes, DoD, policy adversarial cases and producer-consumer routes reviewed after fast-forward. The evaluated `AGENTS.md` checksum remained unchanged.
- Artifacts-reviewed: Phase 4 result, PE-002/003/004, controlled eval metadata and scoped Distillation State.

## Gate Decision

- Result: PASS.
- Can-proceed: true, to `phase-6-distillation` for CORE-001 only.
- Owner approval: explicit high-risk Phase 5 authorization in the current instruction, recorded in PE-004.
- Project closure: no; SKILL-002 and LOOP-003 remain deferred.
- Push authorization: no.

## Owner Decision Checkpoint

- Interaction mode: none.
- Decision state: clear for CORE-001 quality and capture.
- Material decisions: PE-002, PE-003 and PE-004.
- Questions asked: cross-system impact was answered yes.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: observe future full runs for intermittent fixture failures; the canonical fixture change is now present.
- Decision artifacts: `decisions/pe-004-core-quality-and-cross-system-handoff.md`.
- Next route: `phase-6-distillation`.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: controlled router evaluation and scope boundaries are useful for later project tasks.
- Owner decision required: no; phase-6 was explicitly requested.
- Owner decision: capture-now.
- Privacy/scope check: pass.
- Suggested entry title: Conditional instruction router evaluation.
- Suggested entry summary: Use paired direct-read traces and autoload checks before promoting a conditional root router; green validators remain supporting evidence.
