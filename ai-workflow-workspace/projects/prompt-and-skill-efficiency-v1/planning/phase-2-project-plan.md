# Phase 2 Project Plan: Prompt And Skill Efficiency V1

## Metadata And Sources

- Project: `prompt-and-skill-efficiency-v1`; date: 2026-09-24; amended 2026-09-25 under PE-003, 2026-09-28 under PE-005/PE-010, and 2026-09-29 for PE-012/FIX-004 plan reconciliation; workflow phase: `phase-2-project-plan`.
- Architecture: `architecture/phase-1-architecture.md`; Architecture QA: `quality/phase-1-architecture-qa.md` with artifact-level PASS.
- Intake/context: `intake/phase-0-repo-intake.md`, `intake/phase-0-idea-validation.md`, `context.md`.
- Routers: `plans.md`, `tasks.md`; rules: `.systems/ai/workflow/phase-2-project-plan.md` and `.systems/ai/core/autopilot.md`.
- Historical baseline: tracked `main` at `7a904f736eaf029bea750c3a735cd53fa61ef4c0` when the original baseline started. PE-010 planning baseline: clean `codex/prompt-and-skill-efficiency-core-001` at `b9ec1769e80fe537cbed0f3d35c06e4bcc5b724f`, one local commit ahead of origin. Reconciliation baseline: clean local `f362ce3`, two commits ahead of origin; no push is claimed.

## Planning Constraints

- Owner opted out of deadline and timebox. No invented cutoff may dilute DoD or QA.
- Formal planning-range stops after every planned Spec QA. A separate implementation-range readiness and high-risk tracked-write approval are required before phase-4.
- Complete and review the synthetic same-model behavioral baseline before any tracked instruction or skill edit.
- Historical PE-010 SKILL-002 tranche excluded target repository, client data, external API, production effect, commit, push, and Phase 8. Later owner-approved tranches have separate evidence; this historical constraint does not erase their completed commits or final check.
- Optional Task Packaging is not requested. One task receives one spec and later one formal phase-5 quality artifact.
- Candidate work is evidence-gated: a task may be deferred if baseline or paired comparison does not justify its risk.
- Historically, PE-003 deferred SKILL-002 and LOOP-003 until CORE-001 had controlled paired candidate evidence. CORE-001 subsequently completed its CORE-only tranche; PE-005 changes only LOOP-003 planning status, not the historical CORE write set.
- The original planning-range `all-planned-specs-pass` condition was not met for the three-task set. That run was superseded, not retroactively completed. The later CORE-only implementation-range obtained separate readiness and a start request.
- Baseline-002 is pre-implementation evaluation evidence authorized separately by PE-001, not a retroactive phase-4 task. Its report belongs under `evals/`; the task index contains the four formal task dispositions, not preparatory evals.
- PE-005 historically lifted PE-003 deferral for LOOP-003; LOOP-003 is now completed through Phase 7 and committed as `b9ec176`. PE-010 reopens SKILL-002 planning and artifact QA. The CORE-001 candidate already loaded `skill-creator` in the observed skill-review near-miss, so this task needs independent evidence of a remaining trigger or resource-routing gap before any tracked edit.

## Decisions Closed During Planning

| Decision | Chosen option | Reason | Impact |
| --- | --- | --- | --- |
| Eval model | GPT-6 Sol High | Explicit owner decision | Same model/effort for all paired cases |
| Delivery limit | No deadline and no timebox | Explicit owner opt-out | Retry and stop safety remain |
| Eval execution | Isolated local subagents, synthetic fixtures | Explicit owner approval | No real data/network |
| Task packaging | Not requested | Owner-only optional route | Solo task/spec planning |
| Optional refinements | Defer model and response verbosity edits | Insufficient behavioral evidence now | No speculative scope growth |
| PE-002 first tracked candidate | `AGENTS.md` only | Explicit owner approval | No authority to edit other tracked files |
| PE-003 task sequencing | Defer SKILL-002 and LOOP-003 until CORE-001 paired evidence | Explicit owner instruction on 2026-09-25 | Historical CORE-only tranche; later work needs plan amendment and QA |
| PE-005 LOOP-003 planning re-entry | Reopen LOOP-003 planning, Plan QA, specification and Spec QA; no tracked source changes | Explicit owner instruction on 2026-09-28 | Separate conditional planning tranche; exact high-risk write approval remains pending; SKILL-002 remains deferred |
| PE-009 LOOP-003 closeout | One privacy-safe AI System handoff and local commit `b9ec176`; SKILL-002 remains unfinished | Explicit owner instruction | LOOP-003 is no longer a pending implementation dependency |
| PE-010 SKILL-002 planning re-entry | Reopen planning, Plan QA and Spec QA; implement only after positive QA and a demonstrated independent gap | Historical owner instruction | No speculative skill edit; exact high-risk write boundary remained applicable |
| PE-011 SKILL-002 closeout | Close no-change after residual-gap eval; preserve Spec QA FAIL and make no tracked skill edit | Explicit owner instruction on 2026-09-28 | Execution task list complete; Phase 8 remains owner-triggered |

## Tasks

### PSE-CORE-001-conditional-instruction-router

- Goal: preserve a compact always-on authority/safety core while making detailed contract reads task-conditional.
- Scope: first tracked candidate changes root `AGENTS.md` only; relevant core command/refresh dependencies, validators and smoke tests are read-only verification inputs. If their source must change, stop for a new exact-file decision and spec/plan refresh.
- Out of scope: weakening source-of-truth, risk, privacy, permissions, approvals, phase gates, response evidence, or QA; arbitrary deletion of core policy docs.
- Definition of Done: simple cases avoid unrelated detail; formal phase/security/completion cases still load required policy; negative-space smoke and paired holdout show no mandatory-gate regression; full-current-diff review finds no material P2+.
- Dependencies: blocking for implementation: reviewed controlled baseline, accepted Spec QA, exact high-risk owner write approval; informational: skill task; optional: actual file-open telemetry if available.
- Risk type: high; main risk: a conditional route silently omits a safety-critical rule.
- Start condition: baseline reviewed, spec accepted, high-risk approval recorded.
- End condition: semantic QA and formal phase-5 quality with paired candidate evidence; no promotion on unobserved read savings alone.
- Readiness status: completed through owner-approved Phase 5, Phase 6, Phase 7 and commit `6e483fd`; paired evidence and mandatory-policy safety were reviewed. This approval is historical and CORE-only.
- Requires user decision before implementation: satisfied historically for `AGENTS.md` only by PE-002 and later range approvals; not transferable to LOOP-003 or SKILL-002.

### PSE-SKILL-002-trigger-and-resource-routing

- Goal: establish whether active `skill-creator` still has a trigger or resource-routing defect after CORE-001, then correct only a demonstrated defect while preserving required guidance.
- Scope: evidence-supported trigger/reference routing in `.systems/ai/skills/skill-creator/SKILL.md` only, if justified and approved; should-trigger/non-trigger cases and focused validation. Other active skills are out of this tranche.
- Out of scope: deleting legacy assets, converting skill evals into hard gates, rewriting all domain skills without evidence, or using skills as approval authority.
- Definition of Done: an independently demonstrated residual gap is improved versus the current CORE-001 baseline; paired cases show no missed mandatory skill; adjacent near-misses do not load an irrelevant skill; useful scripts/resources remain; `quick_validate.py` and relevant system-skill checks pass after semantic review. If no residual gap exists, document no-change rather than claim implementation success.
- Dependencies: CORE-001 paired result is available and fixed the observed review miss; PE-010 reopens planning. A separate residual-gap audit, accepted Spec QA and exact high-risk owner approval remain required before a source edit. If no material gap remains, close the candidate without editing the skill.
- Risk type: high; main risk: trigger narrowing causes false negatives.
- Start condition: baseline reviewed, spec accepted, approval recorded.
- End condition: formal phase-5 quality and paired candidate/holdout evidence; defer edits that cannot be justified.
- Readiness status: `done` as no-change under PE-011. The earlier conditional implementation candidate is closed, not approved or implemented.
- Requires user decision before implementation: not applicable to the closed candidate; a future new skill edit would require a new decision and QA route.

### PSE-LOOP-003-local-completion-persistence

- Goal: remove the pre-quality local-failure routing ambiguity documented in `planning/loop-003-contract-gap-audit.md`, without claiming an observed early-stop defect or extending permissions.
- Scope: completed five-file contract, Phase 4, validator and smoke change under PE-006/PE-007; see task spec and Phase 5 evidence for exact paths.
- Out of scope: automatic external effects, unapproved writes, forced full workflow scripts for product changes, or claiming formal PASS from a green test.
- Definition of Done: the contract unambiguously routes a failed local check before first quality closure to in-scope diagnosis, permitted correction and retest, or a genuine stop; repeated attempts require new evidence and progress. Synthetic positive and negative cases preserve no unauthorized test/state edits, no new write authority, no false PASS, and unchanged formal Phase 5/fix-loop semantics. Any behavioral improvement claim requires comparable direct evidence; current evals show safe behavior, not a defect.
- Dependencies: completed through Spec QA, implementation, Phase 5, Phase 6, Phase 7 and local commit `b9ec176`; no remaining implementation dependency on SKILL-002.
- Risk type: high if core execution rules change; main risk: persistence wording bypasses a stop condition.
- Start condition: the documented contract ambiguity provides a defensible specification need; exact policy write-set approval is still required before implementation.
- End condition: formal phase-5 quality and paired candidate evidence; reject or defer source promotion if no material clarity gain or a safety regression is found.
- Readiness status: `done` through local Phase 7. This historical approval does not transfer to SKILL-002.
- Requires user decision before implementation: satisfied historically under PE-006/PE-007.

### PSE-FIX-004-discovery-eval-integrity

- Goal: correct the two confirmed Eval 004 findings: irrelevant full skill-body reads during routine discovery and stale graded evidence reuse after an eval-plan change.
- Scope: the exact six tracked paths in `planning/phase-2-eval-004-remediation.md`; metadata-first active-skill selection and graded-run compatibility checks, with focused tests and smoke coverage.
- Out of scope: changing active `skill-creator/SKILL.md`, speculative context routing, standalone aggregator redesign, target/client repositories, CI policy or model defaults.
- Definition of Done: three routine negative synthetic cases avoid irrelevant full skill-body reads; positive skill-review control still loads the relevant body; a changed graded eval plan fails before run mutation; same-plan rerun, ungraded overwrite and orphan-grade failure paths behave as specified. Formal Phase 5 evidence must review the actual traces, hashes, diff and residual limits.
- Dependencies: PE-011 no-change closeout, Eval 004 adversarial findings, PE-012 exact-write approval, plan addendum and its Plan QA, accepted specification and Spec QA, PE-013 Phase 5 approval; these are now recorded as satisfied for the implemented scope.
- Risk type: high; main risks were missing a required skill and accepting stale grades as fresh evidence.
- Start condition: accepted PE-012 addendum and Spec QA plus exact high-risk owner approval.
- End condition: formal Phase 5, Phase 6 distillation, Phase 7 checkpoint and source commit; all are recorded, with bounded residual risks in task quality and checkpoint artifacts.
- Readiness status: `done` through Phase 7 and local commit `f362ce3`; no push or final-owner-yes is implied.
- Requires user decision before implementation: satisfied historically by PE-012; PE-013 approved the formal quality gate and PE-014 approved one AI System handoff.

## Final Execution Order

Current project execution order is below. Exploratory baseline-002/003 remains non-promotional evidence. The CORE-001 paired skill-review result informed SKILL-002's no-change decision; Eval 004 later justified the separate FIX-004 task.

1. Historical completed tranche: `PSE-CORE-001-conditional-instruction-router` through Phase 7; its `AGENTS.md`-only write authority does not transfer.
2. Historical PE-005/PE-009 LOOP-003 tranche: completed through local Phase 7 and commit `b9ec176`; no retroactive expansion of its write authority.
3. Historical PE-010 SKILL-002 tranche: compare CORE-001 candidate with the original false negative, audit for a separate material gap, amend plan/index and run Plan QA; refresh spec and run Spec QA. Only a positive implementation-ready Spec QA and exact high-risk approval could start a one-file implementation. PE-011 followed the no-material-gap route and closed this task without tracked changes.
4. PE-012 Eval 004 remediation tranche: after the SKILL-002 no-change closeout, the adversarial Eval 004 review found two distinct material gaps. PE-012 created PSE-FIX-004 with its own addendum, Plan QA, specification, Spec QA and exact six-path approval. PE-013 approved formal Phase 5; Phase 6/7 and local commit `f362ce3` completed the tranche. The task is `done`; PE-014 records the privacy-safe AI System handoff. Owner-triggered Phase 8 remains separate and never counts as `final-owner-yes`.

Each implemented task has a separate specification, implementation slices, formal Phase 5, Phase 6 and Phase 7. SKILL-002 was closed no-change and has no implementation quality claim. The current task index contains all four dispositions; no unplanned implementation task remains.

## **Lista kolejności wykonywania**

This current-state map is reconciled after the Phase 8 plan-drift finding. Earlier Phase 6 artifacts remain unchanged; a check mark here relies on the task's existing formal Phase 5 quality evidence, not on this plan edit.

1. ✅ `PSE-CORE-001-conditional-instruction-router`: completed after formal Phase 5, distillation and checkpoint.
2. ✅ `PSE-LOOP-003-local-completion-persistence`: completed after formal Phase 5, distillation and checkpoint.
3. `PSE-SKILL-002-trigger-and-resource-routing`: owner-closed no-change under PE-011; its Spec QA FAIL is historical and it has no implementation-quality check mark.
4. ✅ `PSE-FIX-004-discovery-eval-integrity`: separate PE-012 task completed after formal Phase 5, distillation and checkpoint; source committed locally as `f362ce3`.

## Task Index Sync

| Task ID | Present in `tasks.md`? | Risk matches? | Status matches? | Task card needed? | Spec path set? | Quality path set? |
| --- | --- | --- | --- | --- | --- | --- |
| PSE-CORE-001-conditional-instruction-router | yes | yes | yes | no | present, Spec QA PASS | present, Phase 5 PASS and Phase 7 completed |
| PSE-SKILL-002-trigger-and-resource-routing | yes | yes | yes; done no-change under PE-011 | no | refreshed; Spec QA FAIL preserved | Spec QA FAIL artifact present; no implementation QA required for canceled write |
| PSE-LOOP-003-local-completion-persistence | yes | yes | yes | no | present, Spec QA PASS | present, Phase 5 PASS and Phase 7 completed |
| PSE-FIX-004-discovery-eval-integrity | yes | yes | yes; done under PE-012 | no | present, Spec QA PASS | present, Phase 5 PASS and Phase 7 completed |

## Dependency And Architecture Coverage

| Area | Covered by | Gap |
| --- | --- | --- |
| Frozen eval and comparison | Pre-implementation baseline-002 and each candidate task | No; true tool-open telemetry may remain unavailable and must be disclosed |
| Root conditional router | PSE-CORE-001 | No |
| Skill discovery and skill-creator | PSE-CORE-001, PSE-SKILL-002 disposition and PSE-FIX-004 | CORE fixed the observed review miss; SKILL-002 had no independent gap; later Eval 004 showed routine overread and FIX-004 addressed it without changing active skill text |
| Safe local completion loop | PSE-LOOP-003 | Completed and committed locally; no open implementation task |
| Eval freshness and grading integrity | PSE-FIX-004 | Guard applies to `run_eval.py`/`run_loop.py`; standalone direct aggregation remains a documented bounded residual risk, not a claimed guard |
| Safety, authority, validators | Every tracked task and formal QA | No known open implementation gap in the approved scope |

Highest-risk tasks: CORE-001 (missed policy), SKILL-002 (missed skill if edited), LOOP-003 (overbroad persistence) and FIX-004 (required skill omission or stale grades). Implemented tasks had precise specs, owner approvals, adverse-case evidence and formal QA; SKILL-002 was closed without a source edit.

## Plan Quality Contract

- Plan classification: `implementation-capable` for the historical execution tranches; all implemented tasks now have their own completed readiness and quality records. This plan correction grants no new implementation readiness.
- DoD source: accepted owner objective and Architecture QA PASS; each task has a testable DoD above.
- Artifact QA route: `phase-2-plan-qa` after plan/index synchronization.
- Implementation Quality Closure route: `phase-5-quality` for every later formal implementation task.
- Required verification: plan/index sync, dependency review, risk/approval map, negative-space and holdout cases, changed-files review, targeted scripts and explicit full validation after semantic QA when high-impact workflow changes occur.
- Quality-ready criteria: all four task dispositions complete and aligned with plan/router/index, no hidden scope or dependency, SKILL-002 no-change explicitly distinguished from implemented tasks, no invented deadline.
- Owner opt-out: none for QA; deadline/timebox opt-out recorded.
- Not-applicable reason: data/integration matrix is not applicable to this planning artifact; it changes no runtime data flow. Eval producer/consumer evidence and failure paths are covered.
- Blocking decision: PE-010 and PE-011 resolve SKILL-002 as no-change; PE-012/PE-013/PE-014 resolve FIX-004 implementation, formal quality and shared impact. No new implementation approval is inferred from this plan correction.
- Next route: `phase-2-plan-qa`.

## Plan Gate Decision

Historical PE-010 Plan Gate entry below. It does not describe the current four-task execution state; the 2026-09-29 whole-project re-QA in `quality/phase-2-plan-qa.md` governs the corrected plan.

- All tasks have full contract: yes.
- `plans.md` routes to this plan: yes after router sync; PE-010 amendment needs fresh Plan QA evidence.
- `tasks.md` exists and matches the plan: yes after PE-010 index sync; CORE and LOOP artifacts are complete; SKILL-002 spec needs refresh and Spec QA.
- Dependencies are labeled: yes.
- Blocking decisions resolved for current planning tranche: yes; SKILL-002 is `conditional` for specification and QA, with implementation still gated by evidence and exact approval.
- Ready for Plan QA: yes after router sync.
- Blocking reason: none for Plan QA; source implementation remains gated.

## Delivery Constraints

- Mode: `owner-opt-out`; deadline/time budget: none.
- Must-have outcome: project-level evidence-backed behavioral improvement without mandatory safety/QA regression. CORE-001 supplies reviewed paired evidence; LOOP-003 supplies separate contract clarity without a claimed behavior gain; SKILL-002 was closed no-change for lack of an independent gap; FIX-004 addresses the later routine-discovery and graded-eval findings. File-open and token savings remain unknown without telemetry.
- Cutline: optional model-guidance/response-verbosity changes and unproven skill edits remain deferred. Do not cut core safety or QA.
- Quality floor: frozen baseline, paired candidate runs, no missed required policy/skill, formal phase-5 quality.
- Overrun checkpoint: ask owner if evidence is inconclusive or scope expands, not because an invented timer expires.

## Model Recommendation

- Recommended: GPT-6 Sol High, explicitly chosen by owner for paired eval.
- Reason: high-impact policy, skill, and quality-loop work.
- Criticality: high-risk workflow maintenance; advisory only.
- Current model known: eval subagents yes; main agent not inferred.
- Blocking: no.

## Owner Decision Checkpoint

Historical PE-010 checkpoint; PE-011 resolves the conditional SKILL-002 route and PE-012/PE-014 later resolve the separate FIX-004 route.

- Interaction mode: queued for future high-risk implementation approval.
- Decision state: clear for SKILL-002 Plan QA and specification, awaiting owner before any high-risk tracked skill write.
- Material decisions: PE-010 planning re-entry resolved; exact SKILL-002 write-set approval and independent residual-gap evidence before implementation; optional model/verbosity scope deferred.
- Questions asked: PE-001 answered.
- Auto-resolved reversible decisions: no packaging; evidence-gated deferral of optional refinements.
- Optional owner refinements: whether to retain response/model text as-is after results.
- Decision artifacts: `decisions/pe-010-skill-002-planning-reentry.md`, CORE-001 paired quality and the accepted architecture.
- Next route: `phase-2-plan-qa`.

## Optional Knowledge Capture

- Capture recommended: no.
- Target: none.
- Reason: this is a plan; reusable lessons require baseline and implementation evidence.
- Owner decision required: no.
- Owner decision: not-requested.
- Privacy/scope check: pass.
- Suggested entry title: none.
- Suggested entry summary: none.

## PE-011 Execution Closeout Addendum

- Owner decision: `decisions/pe-011-skill-002-no-change-closeout.md` closes SKILL-002 without a tracked skill change, as the conditional no-gap route in this plan allowed.
- Evidence: `evals/skill-002-residual-003/result.md` found no material residual defect and no improvement from the description-only candidate. The refreshed SKILL-002 Spec QA remains `FAIL`; it was not converted to PASS.
- Execution scope: CORE-001 and LOOP-003 are the only implemented tasks, each with its own completed quality, distillation, and checkpoint route. SKILL-002's proposed implementation is explicitly out of scope; there is no open task.
- Historical plan state after PE-011: the original three-task execution set was complete, but the project remained active. This was before Eval 004 created a separate formal task and is not the current four-task closeout verdict.

## Eval 004 Remediation Addendum

The later Eval 004 report introduced two material new findings after PE-011. PE-012 and `PSE-CR-001-eval-004-remediation` added `PSE-FIX-004-discovery-eval-integrity` as a separate formal task. Its exact write set, DoD and QA route remain in `planning/phase-2-eval-004-remediation.md`; the original PE-010 Plan QA and SKILL-002 no-change history are not rewritten. FIX-004 is now completed through Phase 7 and locally committed. The owner-triggered first Phase 8 failed on base-plan drift; the current four-task state above passed fresh whole-project Plan QA and awaits repeat Phase 8.
