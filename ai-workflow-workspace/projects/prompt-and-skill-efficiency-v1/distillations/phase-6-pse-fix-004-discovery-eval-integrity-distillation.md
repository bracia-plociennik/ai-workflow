# Phase 6 Distillation: PSE-FIX-004 Discovery And Eval Integrity

## Metadata

- Project: `prompt-and-skill-efficiency-v1`.
- Task/package ID: `PSE-FIX-004-discovery-eval-integrity`.
- Date: 2026-09-29.
- Workflow phase: `phase-6-distillation`.
- Quality artifact: `quality/phase-5-pse-fix-004-discovery-eval-integrity-quality.md`; formal high-risk PASS approved in PE-013.
- Source scope: six approved tracked paths and synthetic Eval 004 evidence only.
- memory-in-repo-memory: true

## What Was Done

- Phase Skill Discovery now selects candidates from active `SKILL.md` frontmatter `name` and `description` through the closing `---`; it opens full bodies only for plausible matches. Three synthetic non-trigger traces avoided the irrelevant body, while a direct skill-review control loaded the relevant skill.
- `run_eval.py` now fingerprints the full eval plan and checks existing graded manifests, eval metadata and grade paths before scaffold writes. Changed graded plans and legacy/missing producer evidence fail closed; compatible graded reruns and changed ungraded scaffolds remain usable.
- Focused regression, smoke mutations, full-current-diff review and full validation support the bounded result. One model run per case does not establish statistical reliability or measured token/time savings.

## Problems And Conversion

| Problem | Conversion | When To Apply |
| --- | --- | --- |
| Routine discovery loaded an irrelevant full skill body; an early fixed-line metadata read still crossed the frontmatter boundary. | Stop candidate reads at the closing delimiter, then open a full contract only for a plausible task match. Test the actual tool-open trace, not the agent's self-report. | Skill selection and other metadata-first routing. |
| A changed eval plan could reuse stale `grading.json` and produce a misleading benchmark. | Bind grades to a canonical full-plan fingerprint and producer metadata; reject incompatible or orphan grades before any output write. | Eval scaffolds and other persisted evidence pipelines. |
| The separate capture-state record was absent although Phase 4 and Phase 5 described the state. | Reconcile the record transparently before Phase 6; keep file-level state and phase evidence synchronized in later work. | Pre-quality and pre-commit artifact completeness reviews. |

## Decisions

| Decision | Reason | Future Use / Boundary |
| --- | --- | --- |
| Keep `skill-creator` unchanged and correct the discovery consumer. | Eval 004 showed the routine overread in router behavior, not a distinct active-skill-body defect. | Do not reopen SKILL-002's historical no-change closeout through this task. |
| Fail closed for graded runs lacking a matching fingerprint or metadata. | Existing grades cannot be proved fresh after a changed plan or legacy manifest. | Use a fresh output directory; do not silently reset or delete grades. |
| Keep standalone aggregation outside the six-path remediation. | PE-012 approved the `run_eval.py`/`run_loop.py` producer path, not a universal aggregator redesign. | Disclose that manually invoking `aggregate_benchmark.py` on arbitrary stale grades remains possible. |

## Rules For Future Tasks

- Select skills from bounded metadata first; a product filename containing `skill` does not itself trigger skill-artifact guidance.
- For stored eval grades, validate source plan identity and all graded producer fields before writing new scaffold metadata or aggregating through the standard loop.
- Test both compatible reruns and changed-plan rejection, including before/after hashes of persisted evidence.
- Report synthetic one-run behavior as observed case coverage, not general model reliability or performance savings.

## Memory And Scope Decision

- Project memory candidate: yes; synchronized at Phase 7 to `memory/2026-09-29-skill-discovery-and-eval-freshness.md`.
- Repo memory candidate: no separate repo-wide fact; tracked contracts and script are canonical, and this project memory should not duplicate them.
- External Memory candidate: owner approved shared impact in PE-014; one privacy-safe AI System handoff was recorded before commit.
- System Insight Candidate: no; these are AI Workflow mechanism lessons, not an anonymized product/client-domain insight.
- Privacy/scope check: pass; only system contracts and synthetic fixtures were reviewed, with no client data or secrets.
- Plan sync: the older `planning/phase-2-project-plan.md` lacks the exact `## **Lista kolejności wykonywania**` section. No completion checkbox was invented; `tasks.md` and project status carry the result, and Phase 7 must classify the historical-plan drift.

## Distillation Gate

- Reusable decisions recorded: yes.
- Material problems converted to operational rules: yes.
- Transient diary or duplicate quality matrix added: no.
- Ready for checkpoint processing: yes, with historical-plan and shared-impact decisions explicitly surfaced.

## Distillation State

- Work ID: `PSE-FIX-004-discovery-eval-integrity`.
- Previous state: `ready` in the reconciled capture-state file.
- State after accepted distillation: `completed`.
- Distillation artifact: this file.
- `is_distilled` derived value: `true`.
- Privacy/scope check: `pass`.
- Residual risk: standalone aggregation bypasses the standard guarded producer path; one final-source model run per case.

## Owner Decision Checkpoint

- Interaction mode: interactive for shared impact before commit.
- Decision state: clear for Phase 6 and shared impact.
- Material decisions: PE-012, PE-013 and PE-014.
- Questions asked: whether AI System needs a conceptual handoff.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: none required for this distillation.
- Decision artifacts: PE-012, PE-013 and PE-014.
- Next route: Phase 7 checkpoint, then commit readiness; shared impact is resolved.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: these decisions affect future evaluation and final verification in this project.
- Owner decision required: no for the project-memory sync through Phase 7.
- Owner decision: defer-to-checkpoint.
- Privacy/scope check: pass.
- Suggested entry title: Metadata-first discovery and graded eval freshness.
- Suggested entry summary: Route by bounded skill metadata and bind persisted grades to a current eval plan before writes.
