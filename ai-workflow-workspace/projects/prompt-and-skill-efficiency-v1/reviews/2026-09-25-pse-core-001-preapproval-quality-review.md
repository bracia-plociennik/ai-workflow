# Preapproval Quality Review: PSE-CORE-001 Conditional Instruction Router

## Metadata

- Project: `prompt-and-skill-efficiency-v1`.
- Task: `PSE-CORE-001-conditional-instruction-router`.
- Date: `2026-09-25`.
- Workflow phase: `phase-5-quality`.
- Result: `blocked`; high-risk quality gate awaits owner approval. This is review evidence, not a formal gate verdict.
- Reviewed baseline: `7a904f736eaf029bea750c3a735cd53fa61ef4c0`, branch `codex/prompt-and-skill-efficiency-core-001`, only tracked modification `AGENTS.md`.

## Definition Of Done Validation

| DoD item | Review status | Evidence |
| --- | --- | --- |
| Shorter unconditional read-first and explicit task/phase/risk triggers | met | `AGENTS.md` current diff: 31 insertions, 68 deletions; read-first is four core policies plus conditional routes. |
| Mandatory authority, risk, approval, skill, QA and phase behavior retained | met in controlled scope | Manual full-diff review and 10/10 paired GPT-6 Sol High synthetic cases; no forbidden action or false formal gate verdict observed. |
| Directly observed reduction in irrelevant explicit contract reads | met for measured cases | Frozen rubric and completed JSONL command traces: development 11 to 5, holdout 17 to 7, total 28 to 12. One mixed case rose from 1 to 3. |
| Mandatory root instruction autoload coverage | met for tested CLI path | Candidate is 32,567 bytes, below observed 32,768-byte warning threshold; no truncation warning in 10 candidate stderr logs. Baseline was 34,969 bytes and warned about truncation. |
| No unapproved tracked write | met | `git status --short --branch` lists only modified `AGENTS.md`; candidate bytes match the isolated v4 file. |
| Semantic QA and applicable validation | met as review evidence; owner gate pending | Full-current-diff review; `git diff --check`; one complete full validation rerun passed with all smoke IDs. |

## Intent / Plan / Spec Compliance

- Owner instruction: run CORE-only implementation-range after renewed readiness, tracked write only `AGENTS.md`, no commit.
- Accepted plan/spec: CORE-001 conditional instruction router, PE-002 exact-file approval, PE-003 deferral of SKILL-002/LOOP-003, corrected Spec QA and amended Plan QA.
- Compliance status: `aligned` for implementation scope and measured DoD; no commit or push.
- Wrong problem, scope creep, underbuild, overbuild, or unapproved file: none found in current diff.
- Formal implementation quality approval: pending owner due to high-risk classification, independent of technical evidence.

## Review Completeness Gate

- Cross-contract consistency: `aligned`; root router still points to current core contracts, formal phases, skills, memory and stop conditions.
- Risk/work mode compatibility: `aligned`; formal project task is high-risk workflow-maintenance, not a micro-task.
- Source-of-truth, permissions, phase gates, artifact state, acceptance criteria: reviewed against root diff, CORE spec, Spec QA, PE-002/003 and current status.
- Negative-space / adversarial review: completed for read-only security, skill-review near miss, mixed UI/blockchain, formal architecture QA, local implementation loop, optional capture and short command routing. Batch/completion/status routes were checked statically in unchanged downstream sections; they were not separate paired CLI cases.
- Policy-boundary adversarial matrix: compared unconditional versus conditional routes for prompt injection, write approval, quality, source authority, owner decisions, autopilot and target clone update. No enabling exception found in changed text; smoke suite is supporting evidence.
- Producer-consumer field audit: `AGENTS.md` routes to detailed `.systems/ai/core/**` and phase contracts; no core schema, validator, template or runtime producer/consumer field changed. Each retained trigger has a named contract consumer.
- Automated evidence role: `supporting-only`; green scripts did not establish the semantic verdict.
- Post-fix full re-review: completed against the entire current tracked diff after v4 promotion; ignored Phase 4 evidence edits did not alter implementation or candidate text.
- Instruction refresh: performed-full on resume and pre-write; performed-targeted for quality closure.
- Instruction baseline: current root diff, `HEAD`, project status, accepted spec and decisions.
- Closure freshness: current for `AGENTS.md` SHA-256 `eab833e37b454578891d7e36cc8f9a4fedf52ed1251dcd73b887f19e8e8330e2`.

## Findings

- In-scope blockers or unresolved material findings in the `AGENTS.md` diff: none found by the current-diff review.
- Resolved process finding: the required scoped Distillation State record was absent at the first implementation write. The `pending-quality` record now exists under `capture-state/`; its late creation is disclosed in Phase 4 and cannot retroactively satisfy the original timing rule. Review the final state again before formal closure.
- Warning: candidate size leaves about 201 bytes before the observed CLI truncation threshold; a later expansion needs an autoload check.
- Warning: the first full run failed while a smoke fixture copied a Git object under the default macOS TMPDIR; the complete rerun with `TMPDIR=/private/tmp` passed. This is a validation-environment reliability concern outside the approved one-file change.
- Residual uncertainty: command-level trace does not expose every OS-level open; the 10 synthetic cases are not exhaustive paraphrase coverage or a statistical estimate of token savings.

## Commands And Manual Checks

| Evidence | Result | Role |
| --- | --- | --- |
| `cmp AGENTS.md /private/tmp/pse-core-001-candidate-v4-AGENTS.md` | exit 0 | Same bytes as evaluated candidate. |
| `git diff --check` | exit 0 | Whitespace check. |
| `python3 evals/grade-controlled-cli.py <baseline> <candidate>` | irrelevant reads 28 to 12 | Direct completed command telemetry; case relevance fixed before grading. |
| Local completion-loop fixture direct unit tests | 3 tests passed | Isolated behavior check. |
| `.systems/scripts/validate-workflow --profile full --explain` | first run exit 128 in temp Git fixture | Disclosed failed evidence; not counted as successful full validation. |
| `TMPDIR=/private/tmp .systems/scripts/validate-workflow --profile full --explain` | exit 0, full completion marker, 573 seconds | Supporting contract and smoke evidence. |
| Current `git diff -- AGENTS.md`, spec, PE-002/003 and 10 case outputs | reviewed | Intent, DoD, authority, policy boundary and regression assessment. |
| Scoped capture-state audit | late producer record repaired | Process finding remains documented; future state consumers now have a canonical per-work record. |

## Adaptive Data / Integration Verification Matrix

- Applicability: `not-applicable`.
- Reason: this one-file change alters instruction routing text, not a data model, parser, integration, state transition or executable entrypoint. The relevant adaptive control is the policy-route and producer-consumer audit above.

## Edge And Regression Review

- Tiny docs: one-slice scope, advisory closure, no formal verdict.
- Frontend/backend/blockchain: relevant domain skill/risk lens preserved in paired cases.
- Skill review near miss: active skill-creator loaded by candidate, addressing a baseline miss.
- Security review: read-only scope and P1 ownership concern retained; no auto-fix.
- Formal architecture QA: missing design evidence blocks formal phase acceptance.
- Mixed Web3/UI: no unauthorized backend or chain writes; extra irrelevant reads disclosed.
- Installation, batch, completion and target clone update: changed router still reaches the existing detailed contracts; no target repository was modified.

## Gate Decision

- Semantic review: no in-scope blocker found, with two warnings and stated coverage limits.
- Formal phase-5 quality approval: awaiting owner; the risk model and phase file reserve high-risk gate approval for the human owner.
- Next route: stop this autopilot as `awaiting-owner`. Do not run phase-6 distillation, phase-7 checkpoint, commit, push or phase-8 final check until the owner resolves the gate.

## Owner Decision Checkpoint

- Interaction mode: queued after stopping the run.
- Decision state: blocked.
- Material decision: approve or reject high-risk CORE-001 quality gate after reading this evidence and tracked diff.
- Questions asked during run: none.
- Auto-resolved reversible decisions: none.
- Optional refinements: consider a separate later validator-fixture reliability task; not part of the exact AGENTS-only write set.
- Decision artifacts: PE-002, PE-003, this quality review.
- Next route: owner quality decision, then phase 6 only if formal gate is approved.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: controlled routing eval and false-positive validator behavior are reusable project lessons, but formal distillation waits for quality approval.
- Owner decision required: no for a proposal; writes remain subject to phase permissions.
- Owner decision: not-requested.
- Privacy/scope check: pass; synthetic cases and system files only.
- Suggested entry title: Controlled instruction-router evaluation.
- Suggested entry summary: Freeze paired inputs and classify observed command-level reads; verify autoload size and behavioral boundaries before promoting a shorter router.
