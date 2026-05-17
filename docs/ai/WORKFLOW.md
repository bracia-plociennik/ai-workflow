# WORKFLOW.md

## Purpose

This is the main operational workflow guide for daily work in the repository.
It routes each phase to the exact phase artifact under `docs/ai/workflow/`, so agents do not need to inspect one long workflow file.

Use this order of authority for process rules:

1. `AGENTS.md` as the repository execution contract.
2. This `WORKFLOW.md` as the main workflow guide and phase router.
3. `docs/ai/workflow/<phase>.md` as the detailed source for the current phase.
4. `docs/ai/workflow/00_overview.md` for global workflow scope, status contract, autopilot, and canonical sequence.

If this guide is insufficient, open the linked phase file. If process documents conflict, stop and follow the most specific applicable phase artifact under `docs/ai/workflow/` together with `AGENTS.md`.

## Status Files

- Repo-local status: [`docs/ai/STATUS.md`](STATUS.md).
- Project-local status, when used: `docs/projects/<project>/STATUS.md`.
- Do not recreate the old workflow-status filename.

For workflow-governed work, update the relevant `STATUS.md` whenever a phase starts, ends, fails, passes, becomes blocked, or changes the next required phase.

## Artifact Paths

Project artifacts live under `docs/projects/<what_we_doing>/...`.

`<what_we_doing>` and `<project>` are equivalent placeholders for the active project workspace directory.

Generic project layout:

- project overview: `docs/projects/<project>/README.md`
- project intake: `docs/projects/<project>/intake/`
- project architecture: `docs/projects/<project>/architecture/`
- project planning: `docs/projects/<project>/planning/`
- task specifications: `docs/projects/<project>/specs/`
- project quality evidence: `docs/projects/<project>/quality/`
- project decisions: `docs/projects/<project>/decisions/`
- project escalations: `docs/projects/<project>/escalations/`
- project distillations: `docs/projects/<project>/distillations/`
- project checkpoints: `docs/projects/<project>/checkpoints/`
- project autopilot runtime: `docs/projects/<project>/autopilot/`
- project status: `docs/projects/<project>/STATUS.md`

The included `docs/projects/EXAMPLE/` directory demonstrates the structure. It is not active project state.

## When Full Workflow Is Mandatory

Full workflow is mandatory for tasks derived from an active project plan under `docs/projects/<what_we_doing>/...` while that plan still has open in-scope work or has not passed `8. FINAL CHECK`.

Full workflow is optional for side tasks after a project plan is closed, unless the user explicitly asks for workflow mode or correctness requires a formal gate.

Even outside full workflow, repository-first execution, stop conditions, and evidence-based quality still apply.

## Canonical Phase Order

| Phase | Detailed Rules |
| --- | --- |
| `0. REPO INTAKE / INITIAL AUDIT` | [`docs/ai/workflow/0_repo_intake_initial_audit.md`](workflow/0_repo_intake_initial_audit.md) |
| `1. FAZA ARCHITEKTURY` | [`docs/ai/workflow/1_architecture.md`](workflow/1_architecture.md) |
| `1.5. ARCHITECTURE QA` | [`docs/ai/workflow/1_5_architecture_qa.md`](workflow/1_5_architecture_qa.md) |
| `1.7. ARCHITECTURE FIX LOOP` | [`docs/ai/workflow/1_7_architecture_fix_loop.md`](workflow/1_7_architecture_fix_loop.md) |
| `2. FAZA PLANU PROJEKTU` | [`docs/ai/workflow/2_project_plan.md`](workflow/2_project_plan.md) |
| `2.5. PLAN QA` | [`docs/ai/workflow/2_5_plan_qa.md`](workflow/2_5_plan_qa.md) |
| `2.6. PLAN FIX LOOP` | [`docs/ai/workflow/2_6_plan_fix_loop.md`](workflow/2_6_plan_fix_loop.md) |
| `2.7. TASK PACKAGING` | [`docs/ai/workflow/2_7_task_packaging.md`](workflow/2_7_task_packaging.md) |
| `2.9. PACKAGING QA` | [`docs/ai/workflow/2_9_packaging_qa.md`](workflow/2_9_packaging_qa.md) |
| `2.9.1. PACKAGE FIX LOOP` | [`docs/ai/workflow/2_9_1_package_fix_loop.md`](workflow/2_9_1_package_fix_loop.md) |
| `3. FAZA SPECYFIKACJI` | [`docs/ai/workflow/3_specification.md`](workflow/3_specification.md) |
| `3.5. SPEC QA` | [`docs/ai/workflow/3_5_spec_qa.md`](workflow/3_5_spec_qa.md) |
| `3.7. SPEC FIX LOOP` | [`docs/ai/workflow/3_7_spec_fix_loop.md`](workflow/3_7_spec_fix_loop.md) |
| `4. FAZA IMPLEMENTACJI` | [`docs/ai/workflow/4_implementation.md`](workflow/4_implementation.md) |
| `5. FAZA JAKOŚCI` | [`docs/ai/workflow/5_quality.md`](workflow/5_quality.md) |
| `5.5. FIX LOOP` | [`docs/ai/workflow/5_5_fix_loop.md`](workflow/5_5_fix_loop.md) |
| `6. FAZA DESTYLACJI` | [`docs/ai/workflow/6_distillation.md`](workflow/6_distillation.md) |
| `7. CHECKPOINT PROJEKTU` | [`docs/ai/workflow/7_checkpoint.md`](workflow/7_checkpoint.md) |
| `8. FINAL CHECK` | [`docs/ai/workflow/8_final_check.md`](workflow/8_final_check.md) |

## Transition Rules

- Do not continue past an unsatisfied gate.
- `PASS` moves only to the next valid phase.
- `FAIL` routes to the matching fix loop and then back to the same QA gate.
- Do not mark `PASS` without explicit evidence.
- Do not guess across unresolved blocking decisions.
- For `2.7. TASK PACKAGING`, skip `2.9. PACKAGING QA` only when no packages were created.
- For `3. FAZA SPECYFIKACJI`, use `/plan` as the implementation plan source and persist it according to [`3_specification.md`](workflow/3_specification.md).
- Do not recommend `8. FINAL CHECK` until all in-scope tasks are completed or explicitly deferred.

## Command Aliases

Natural-language workflow commands map to these phase files:

| User Intent | Phase File |
| --- | --- |
| `repo intake`, `initial audit`, `faza audytu` | [`0_repo_intake_initial_audit.md`](workflow/0_repo_intake_initial_audit.md) |
| `architektura`, `faza architektury` | [`1_architecture.md`](workflow/1_architecture.md) |
| `qa architektury`, `sprawdz architekture` | [`1_5_architecture_qa.md`](workflow/1_5_architecture_qa.md) |
| `fix loop architektury` | [`1_7_architecture_fix_loop.md`](workflow/1_7_architecture_fix_loop.md) |
| `plan projektu` | [`2_project_plan.md`](workflow/2_project_plan.md) |
| `plan qa`, `qa planu` | [`2_5_plan_qa.md`](workflow/2_5_plan_qa.md) |
| `plan fix loop` | [`2_6_plan_fix_loop.md`](workflow/2_6_plan_fix_loop.md) |
| `task packaging`, `packaging` | [`2_7_task_packaging.md`](workflow/2_7_task_packaging.md) |
| `packaging qa` | [`2_9_packaging_qa.md`](workflow/2_9_packaging_qa.md) |
| `package fix loop` | [`2_9_1_package_fix_loop.md`](workflow/2_9_1_package_fix_loop.md) |
| `specyfikacja`, `faza specyfikacji` | [`3_specification.md`](workflow/3_specification.md) |
| `spec qa`, `qa specyfikacji` | [`3_5_spec_qa.md`](workflow/3_5_spec_qa.md) |
| `spec fix loop` | [`3_7_spec_fix_loop.md`](workflow/3_7_spec_fix_loop.md) |
| `implementacja`, `implement now`, `implement plan` | [`4_implementation.md`](workflow/4_implementation.md) |
| `faza jakosci`, `quality check` | [`5_quality.md`](workflow/5_quality.md) |
| `fix loop`, `fix loop po jakosci` | [`5_5_fix_loop.md`](workflow/5_5_fix_loop.md) |
| `destylacja` | [`6_distillation.md`](workflow/6_distillation.md) |
| `checkpoint` | [`7_checkpoint.md`](workflow/7_checkpoint.md) |
| `final check` | [`8_final_check.md`](workflow/8_final_check.md) |
