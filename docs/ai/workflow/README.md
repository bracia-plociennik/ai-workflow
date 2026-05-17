# docs/ai/workflow

Use:

- [`../../HUMANS.md`](../../HUMANS.md) as the human operating guide.
- [`../WORKFLOW.md`](../WORKFLOW.md) as the main operational guide and phase router.
- The phase file below when a phase requires exact rules, gates, prompts, or edge-case handling.
- [`../STATUS.md`](../STATUS.md) for the repo-local workflow snapshot.
- `docs/projects/<project>/STATUS.md` for project-local workflow status when a project workspace owns one.

## Global Workflow Rules

| Area | File |
| --- | --- |
| Overview, scope, status contract, autopilot, canonical sequence | [`00_overview.md`](00_overview.md) |

## Phase Files

| Phase | File |
| --- | --- |
| `0. REPO INTAKE / INITIAL AUDIT` | [`0_repo_intake_initial_audit.md`](0_repo_intake_initial_audit.md) |
| `1. FAZA ARCHITEKTURY` | [`1_architecture.md`](1_architecture.md) |
| `1.5. ARCHITECTURE QA` | [`1_5_architecture_qa.md`](1_5_architecture_qa.md) |
| `1.7. ARCHITECTURE FIX LOOP` | [`1_7_architecture_fix_loop.md`](1_7_architecture_fix_loop.md) |
| `2. FAZA PLANU PROJEKTU` | [`2_project_plan.md`](2_project_plan.md) |
| `2.5. PLAN QA` | [`2_5_plan_qa.md`](2_5_plan_qa.md) |
| `2.6. PLAN FIX LOOP` | [`2_6_plan_fix_loop.md`](2_6_plan_fix_loop.md) |
| `2.7. TASK PACKAGING` | [`2_7_task_packaging.md`](2_7_task_packaging.md) |
| `2.9. PACKAGING QA` | [`2_9_packaging_qa.md`](2_9_packaging_qa.md) |
| `2.9.1. PACKAGE FIX LOOP` | [`2_9_1_package_fix_loop.md`](2_9_1_package_fix_loop.md) |
| `3. FAZA SPECYFIKACJI` | [`3_specification.md`](3_specification.md) |
| `3.5. SPEC QA` | [`3_5_spec_qa.md`](3_5_spec_qa.md) |
| `3.7. SPEC FIX LOOP` | [`3_7_spec_fix_loop.md`](3_7_spec_fix_loop.md) |
| `4. FAZA IMPLEMENTACJI` | [`4_implementation.md`](4_implementation.md) |
| `5. FAZA JAKOŚCI` | [`5_quality.md`](5_quality.md) |
| `5.5. FIX LOOP` | [`5_5_fix_loop.md`](5_5_fix_loop.md) |
| `6. FAZA DESTYLACJI` | [`6_distillation.md`](6_distillation.md) |
| `7. CHECKPOINT PROJEKTU` | [`7_checkpoint.md`](7_checkpoint.md) |
| `8. FINAL CHECK` | [`8_final_check.md`](8_final_check.md) |

## Maintenance Rule

Do not recreate one long workflow source file. Add or update the smallest relevant phase artifact and keep `../WORKFLOW.md` pointing to it.
