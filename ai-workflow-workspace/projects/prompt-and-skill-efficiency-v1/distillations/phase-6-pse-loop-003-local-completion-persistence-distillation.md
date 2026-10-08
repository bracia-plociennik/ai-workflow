# Phase 6 Distillation: PSE-LOOP-003 Local Completion Persistence

## Metadata

- Project: `prompt-and-skill-efficiency-v1`.
- Task/package ID: `PSE-LOOP-003-local-completion-persistence`.
- Date: 2026-09-28.
- Workflow phase: `phase-6-distillation`.
- Quality artifact: `quality/phase-5-pse-loop-003-local-completion-persistence-quality.md`; formal high-risk quality approved in PE-008.
- Source scope: five approved tracked files and synthetic-only LOOP-003 evaluations.
- memory-in-repo-memory: true

## What Was Done

- Defined a bounded pre-quality route for a failed safe local check: record failure evidence, diagnose, correct only within the accepted slice and authority, rerun the failed and relevant regression checks, or stop at the named gate.
- Preserved the separate formal Phase 5 fix loop and full post-review re-review; passing scripts remain supporting evidence, not a quality verdict.
- Narrowed `check-naming` so raw files in a marker-backed project eval `fixture/**` or `runs/<run>/checkout/**` retain their frozen source filenames while canonical eval and unrelated workspace artifacts remain subject to naming rules.
- Added validator and smoke coverage for missing contracts, direct and compound unsafe wording, inverse retest/diagnosis wording, safe conditional retest, frozen-input allow paths and naming denial paths. The final full workflow validation passed on the five-file diff.
- Compared two paired GPT-6 Sol High synthetic cases. Both baseline and candidate recovered from the permitted runtime fault and stopped at the owner-controlled state; no behavioral improvement or regression was observed in those cases.

## Problems And Conversion

| Problem | Conversion | When To Apply |
| --- | --- | --- |
| Required phrase matching accepted a contradictory `Do not rerun the failed check` sentence. | Test mandatory policy both directly and with an inverse clause in the same active section; reject a contradiction even when positive wording remains elsewhere. | Policy validators and review of natural-language contracts. |
| A first inverse-wording regex rejected a legitimate safety condition about waiting for a safe environment. | Pair every negative adversarial case with a positive conditional-safety case; narrow the match to an unconditional prohibition. | Regex-based safety validators. |
| Broad naming validation treated immutable synthetic source filenames as canonical workspace artifacts. | Exempt only marker-backed frozen input subtrees, then test missing marker and bad canonical/unrelated paths. | Eval fixture scanners and workspace naming rules. |
| Synthetic baseline already behaved safely. | Report contract clarity and bounded coverage, not a model-behavior improvement claim. | Promotion decisions based on controlled evals. |

## Decisions

| Decision | Reason | Future Use / Boundary |
| --- | --- | --- |
| Allow an in-spec correction before the first quality verdict, with diagnosis and retest evidence. | A local failing check is implementation evidence, not automatically a formal Phase 5 fix loop. | Only within the approved write set, risk class, permissions and safe environment; changed authority routes to owner/earlier phase. |
| Keep formal post-quality fixes separate. | A quality verdict cannot be reused after source changes. | Phase 5 failure uses the formal fix loop; any later edit requires full current-state re-review. |
| Use synthetic-only agent eval for this scope. | Owner declined the repository-disclosing full-clone route and approved isolated fixtures. | Preserve its external-validity limit; do not infer a full-repo behavior gain. |
| Keep the naming exception behind a nonempty `freeze.md` and raw-input paths. | Canonical eval records must remain linted. | Do not generalize to all eval folders or entire workspace. |

## Rules For Future Tasks

- A failed safe local check before quality requires command/exit/surface/DoD evidence, diagnosis, and either an authorized same-slice correction with failed-plus-regression retest or an explicit STOP route.
- A further repair attempt needs a new evidence-backed hypothesis and safe progress; green output after an unauthorized change is not acceptance.
- Policy validators need paired negative and positive adversarial cases, including inverse wording and safe conditions, plus a full semantic current-diff review.
- Frozen source inputs can keep original filenames only inside a narrowly marked fixture/archive namespace; canonical reports and other workspace artifacts retain naming validation.
- A controlled eval that ties the baseline supports safety/no-regression only for its tested cases, not a causal improvement claim.

## Memory And Scope Decision

- Project memory candidate: yes; keep the bounded recovery and eval-limit decisions for remaining project work.
- Repo memory candidate: yes at checkpoint only if reduced to a repository-wide validator/fixture rule without task-local detail.
- External Memory candidate: cross-system handoff only if the owner approves shared impact; decision remains pending before commit.
- System Insight Candidate: no; these are AI Workflow contract and validator lessons rather than a reusable product/client-domain insight.
- Privacy/scope check: pass; sources are system contracts and synthetic inputs, with no client data or secrets.
- Plan sync: `planning/phase-2-project-plan.md` lacks the exact `## **Lista kolejności wykonywania**` section required by the older phase-6 synchronization instruction. No task completion marker was invented in that plan; `tasks.md` and project status are updated, and Phase 7 must classify the planning drift.

## Distillation Gate

- Reusable decisions recorded: yes.
- Significant problems have an operational conversion: yes.
- Transient execution diary or duplicated quality matrix: no.
- Ready for checkpoint processing: yes, subject to the separately tracked plan-sync warning and cross-system decision before commit.

## Distillation State

- Work ID: `PSE-LOOP-003-local-completion-persistence`.
- Previous state: `ready`.
- State after accepted distillation: `completed`.
- Distillation artifact: this file.
- `is_distilled` derived value: `true`.
- Privacy/scope check: `pass`.
- Residual risk: no observed behavior improvement in two synthetic pairs; current project plan is historical and lacks the exact task-order section.

## Owner Decision Checkpoint

- Interaction mode: interactive for the cross-system pre-commit decision.
- Decision state: awaiting-owner for shared impact; clear for this owner-triggered Phase 6 content.
- Material decisions: PE-006, PE-007, PE-008; counterpart handoff decision pending.
- Questions asked: shared AI System impact before commit.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: decide whether to pursue the deferred SKILL-002 in a later tranche.
- Decision artifacts: PE-006, PE-007, PE-008 and the recorded owner reply when received.
- Next route: Phase 7 checkpoint, after the Phase 6 state and task index are synchronized.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: bounded failure routing and eval interpretation affect later project tasks.
- Owner decision required: no for project-memory synchronization through Phase 7.
- Owner decision: defer-to-checkpoint.
- Privacy/scope check: pass.
- Suggested entry title: Safe local failure routing and eval boundaries.
- Suggested entry summary: Correct only inside approved scope, retest with evidence, stop at real authority boundaries, and avoid behavior-gain claims from baseline ties.
