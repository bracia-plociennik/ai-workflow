# Workflow Templates

Reusable templates for artifacts produced by `docs/ai/workflow/*` phases.

Use these templates as starting points only. The phase rules in `docs/ai/workflow/` remain authoritative.

## Template Map

| Phase | Template | Typical Destination |
| --- | --- | --- |
| 0. Repo Intake / Initial Audit | `0_initial_audit_template.md` | `docs/projects/<project>/intake/0_initial_audit.md` |
| 1. Architecture | `1_architecture_phase_template.md` | `docs/projects/<project>/architecture/1_architecture_phase.md` |
| 1.5 Architecture QA | `1_5_architecture_qa_template.md` | `docs/projects/<project>/quality/1_5_architecture_qa.md` |
| 1.7 Architecture Fix Loop | `1_7_architecture_fix_loop_template.md` | `docs/projects/<project>/quality/1_7_architecture_fix_loop.md` |
| 2. Project Plan | `2_project_plan_template.md` | `docs/projects/<project>/planning/2_project_plan.md` |
| 2.5 Plan QA | `2_5_plan_qa_template.md` | `docs/projects/<project>/quality/2_5_plan_qa.md` |
| 2.6 Plan Fix Loop | `2_6_plan_fix_loop_template.md` | `docs/projects/<project>/quality/2_6_plan_fix_loop.md` |
| 2.7 Task Packaging | `2_7_task_packaging_template.md` | `docs/projects/<project>/planning/2_project_plan.md` section or `quality/2_7_task_packaging.md` |
| 2.9 Packaging QA | `2_9_packaging_qa_template.md` | `docs/projects/<project>/quality/2_9_packaging_qa.md` |
| 2.9.1 Package Fix Loop | `2_9_1_package_fix_loop_template.md` | `docs/projects/<project>/quality/2_9_1_package_fix_loop.md` |
| 3. Specification | `3_task_specification_template.md` | `docs/projects/<project>/specs/3_<task>_specification.md` |
| 3.5 Spec QA | `3_5_spec_qa_template.md` | `docs/projects/<project>/quality/3_5_<task>_spec_qa.md` |
| 3.7 Spec Fix Loop | `3_7_spec_fix_loop_template.md` | `docs/projects/<project>/quality/3_7_<task>_spec_fix_loop.md` |
| 4. Implementation | `4_implementation_result_template.md` | response body or `docs/projects/<project>/quality/4_<task>_implementation_result.md` when persisted |
| 5. Quality | `5_quality_template.md` | `docs/projects/<project>/quality/5_<task>_quality.md` |
| 5.5 Fix Loop | `5_5_fix_loop_template.md` | `docs/projects/<project>/quality/5_5_<task>_fix_loop.md` |
| 6. Distillation | `6_distillation_template.md` | `docs/projects/<project>/distillations/3_<task>_distillation.md` |
| 7. Checkpoint | `7_checkpoint_template.md` | `docs/projects/<project>/checkpoints/7_checkpoint_<date>_<scope>.md` |
| 8. Final Check | `8_final_check_template.md` | `docs/projects/<project>/quality/8_final_check.md` |

Autopilot runtime templates live in `../autopilot/`.
