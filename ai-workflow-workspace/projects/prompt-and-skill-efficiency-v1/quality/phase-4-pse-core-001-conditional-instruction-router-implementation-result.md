# Phase 4 Implementation: PSE-CORE-001 Conditional Instruction Router

## Current State

- Phase: `phase-4-implementation`; result: `completed; ready-for-quality`, not a formal quality verdict.
- Work mode: `full-project` workflow maintenance; risk: `high`.
- Source: accepted CORE-001 specification, artifact-level Spec QA, PE-002 exact-file approval and PE-003 CORE-only sequencing.
- Implementation scope: root `AGENTS.md` only as tracked candidate; ignored synthetic eval and phase runtime evidence may be written separately.
- DoD source: `specs/phase-3-pse-core-001-conditional-instruction-router-specification.md` and accepted plan.
- Delivery: owner opted out of deadline and timebox; DoD, QA and stop conditions unchanged.

## Instruction Adherence Refresh

- Status: performed-full.
- Trigger: resumed task after context compaction, separate implementation-range start, branch change and pre-write boundary.
- Contracts refreshed: root `AGENTS.md`; operating model, workflow, autopilot, phase-4, risk, permissions, DoD, implementation slicing, response, contract compliance and prompt injection; accepted plan/spec/QA/decisions.
- Reviewed baseline: clean branch `codex/prompt-and-skill-efficiency-core-001` at `7a904f736eaf029bea750c3a735cd53fa61ef4c0`, project/repo status, controlled snapshot and pre-write approval.
- Drift/conflict: none; the PE-003 plan amendment affects sequencing only, not CORE scope or DoD.

## Implementation Slice Plan

| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| CORE-S1 | Establish same-method CLI baseline and current instruction/read evidence | Ignored `evals/cli-runs/**`, frozen local synthetic copies | Baseline cases use fixed model, effort, flags, prompts, fixture hashes; completed command traces recorded or uncertainty marked | Per-case JSONL, metadata, classification, autoload warning/budget | completed |
| CORE-S2 | Design minimal conditional root router in isolated candidate | Isolated candidate `AGENTS.md` only; no tracked source yet | Static safety map preserves mandatory always-on rules, known triggers, validator-required strings and autoload prefix | Candidate diff and source/trigger map | completed; v4 selected |
| CORE-S3 | Run paired candidate cases and decide promotion | Ignored paired eval outputs; tracked `AGENTS.md` only if promotion evidence supports it | No mandatory behavior regression; lower directly observed irrelevant explicit reads; safe autoload coverage | Per-case and partition grading, command traces, missed-source and forbidden-action audit, promotion decision | completed; v4 promoted |
| CORE-S4 | Apply approved candidate, verify scope and hand off to phase-5 | Root `AGENTS.md` only if S3 promotes; ignored implementation result/status | Changed-files review and local checks; no hidden files or unresolved decision | Diff, checks/skips, residual risk and phase-5 route | completed; ready-for-quality |

Stop on evidence ambiguity, mandatory-policy or skill miss, unapproved file requirement, unsafe autoload coverage, fixture drift, external effect, or a false formal quality verdict. A slice plan does not grant approval. If direct read-efficiency cannot be demonstrated, do not promote the candidate or claim CORE complete.

## Slice Execution Evidence

- CORE-S1: `evals/cli-runs/core-001-002/baseline/` has 10/10 completed GPT-6 Sol High cases with JSONL traces and per-case metadata. Master fixture/status/intake SHA-256 values match `evals/controlled-baseline-manifest.md`. Baseline root `AGENTS.md` is 34,969 bytes and CLI reports truncation at 32,768 bytes.
- CORE-S2: isolated v1/v2 candidates were drafted only under `/private/tmp`; no tracked source changed. The v2 candidate is 32,611 bytes, has no autoload truncation warning in its tiny-doc case and passes `validate-workflow --profile standard` on a copied checkout. A missing `worktree-bootstrap.md` reference was caught and repaired before v2 tests. Experimental v3 separates planning from implementation and makes script/prompt-injection reads conditional; it is 32,731 bytes and passes the same standard structural validation.
- CORE-S3: completed direct-read command-path summary is in `evals/summarize-controlled-cli.py`, with frozen relevance rules in `evals/core-001-read-classification-rubric.md` and mechanical grading in `evals/grade-controlled-cli.py`. The parser was corrected for shell brace expansion, variable-driven `for` reads, and content-reading `rg` before final grading; no self-reported source list is counted as telemetry. V2 development cases read 94 distinct per-case core paths versus baseline 78, so v2 was rejected before holdout. V3 reached an irrelevant-read tie (11 versus 11), so it was also rejected. V2 exposed a dirty `AGENTS.md` in the synthetic checkout; v3/v4 use a Git index hint only inside disposable candidate copies to emulate a clean post-adoption view without a commit. V4 completed 10/10 matched cases at `evals/cli-runs/core-001-005/candidate/` with unchanged candidate SHA-256 `eab833e37b454578891d7e36cc8f9a4fedf52ed1251dcd73b887f19e8e8330e2`, exit 0, no AGENTS truncation warning, and matched prompt hashes. Rubric-irrelevant explicit core reads: development 11 baseline versus 5 v4; holdout 17 versus 7; total 28 versus 12. Manual review found no mandatory-skill, approval, scope, formal/advisory QA or source-authority regression in these cases. The candidate local completion-loop fixture changed only the clamp implementation and three direct tests passed. Telemetry covers observed completed command-level reads, not every OS file open; one mixed Web3/UI holdout case rose from 1 to 3 irrelevant reads, without a required-policy miss. No token-savings claim is made.
- CORE-S4: after restoring missing PE-002 ignored decision evidence from the owner's explicit AGENTS-only approval, a fresh pre-write check found passing Spec QA, isolated clean branch and exact one-file permission. The official root `AGENTS.md` is byte-identical to v4 (`cmp` exit 0); `git diff --stat` shows only `AGENTS.md`, 31 insertions and 68 deletions. Findings-first semantic diff review retained source-of-truth, prompt-injection data boundary, owner approval, formal phase gates, QA/quality, stop and write conditions. `git diff --check` passed. First full validation failed in the smoke fixture while copying a Git object under the macOS default TMPDIR; a complete rerun with `TMPDIR=/private/tmp` passed all validators and smoke IDs with one `AI_WORKFLOW_VALIDATE_COMPLETE profile=full result=pass exit_code=0` marker (573 s). This is supporting evidence; phase-5 must re-review the final state before a quality verdict.
- Post-implementation evidence repair: the required scoped Distillation State record was missing at the first write. It was created later at `capture-state/pse-core-001-conditional-instruction-router.md` as `pending-quality`, with the timing violation preserved as a finding. Quality must not assume this repair makes the original producer timing compliant.

## Evidence

- Artifacts-reviewed: accepted CORE specification, corrected Spec QA, PE-002 exact-file decision, PE-003 deferral, fresh implementation-range readiness, controlled baseline manifest and fixed rubric.
- Commands: `cmp AGENTS.md /private/tmp/pse-core-001-candidate-v4-AGENTS.md` exited 0; `git diff --check` exited 0; `git status --short --branch` lists only modified `AGENTS.md`.
- Commands: `python3 evals/grade-controlled-cli.py` with frozen baseline/candidate run roots reported 28 versus 12 irrelevant explicit reads; direct isolated clamp fixture tests reported three passing tests.
- Commands: `TMPDIR=/private/tmp .systems/scripts/validate-workflow --profile full --explain` exited 0 with completion marker; the earlier default-TMPDIR attempt exited 128 inside a Git smoke fixture and is not counted as successful evidence.
- Manual-checks: all 10 candidate case outputs, mandatory skill and safety routes, prompt hashes, candidate SHA stability, no autoload truncation warning, and complete tracked diff reviewed. Command-level telemetry cannot prove all OS file opens or statistical token savings.
- Artifacts-reviewed: scoped Distillation State record exists now, but was not present at the first write; this is a disclosed process finding for Phase 5.
- Changed files: tracked `AGENTS.md` only; ignored project evidence and PE-002 decision record are workspace-local.
- Skipped checks: no product build is applicable to this policy-router-only change; production or target-repo behavior was not exercised. Full-current-state phase-5 review remains required.
- Residual risk: synthetic cases do not cover every natural-language paraphrase; one mixed Web3/UI case made two additional irrelevant explicit reads. The first full smoke failure may recur with default TMPDIR and should be tracked separately if it does.

## Gate Decision

- Result: ready-for-quality.
- Can-proceed: true, only to `phase-5-quality` review; no formal quality verdict or downstream distillation/checkpoint is authorized by Phase 4 alone.

## Plan Quality Contract

- Plan classification: implementation-capable, high risk.
- Testable DoD: accepted CORE specification, including direct read-efficiency, autoload safety and no mandatory-gate regression.
- Artifact QA route: existing `phase-3-spec-qa` for CORE-001; current Plan QA after PE-003.
- Implementation quality route: formal `phase-5-quality` after an evidence-backed phase-4 result.
- Required verification: frozen paired synthetic cases, observed JSONL reads, project-doc loaded-prefix audit, negative-space policy/skill grading, changed-files review and applicable validators after semantic QA.
- Quality-ready criteria: no unresolved P0/P1/material P2, no unapproved write, all promotion evidence complete; full validator is supporting evidence for high-impact final confidence.
- Owner opt-out: none for QA. No deadline/timebox by explicit owner decision.
- Blocking route: stop and escalate if exact scope or direct measurement fails.

## Owner Decision Checkpoint

- Interaction mode: queued during active autopilot.
- Decision state: clear for starting CORE-S1; stop/queue if a new material decision appears.
- Material decisions: PE-002 and PE-003 resolved; no new decision yet.
- Questions asked: none during run.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: none now.
- Decision artifacts: `decisions/pe-002-agents-only-candidate.md`, `decisions/pe-003-skill-sequencing.md`.
- Next route: CORE-S1.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: the paired routing experiment produced a reusable project-local evaluation method; formal distillation remains downstream of quality approval.
- Owner decision required: no.
- Owner decision: not-requested.
- Privacy/scope check: pass; synthetic fixtures only.
- Suggested entry title: Conditional instruction routing evaluation.
- Suggested entry summary: Paired synthetic traces can reveal excess contract reads and autoload truncation while preserving policy boundaries; retain the command-level telemetry caveat.
