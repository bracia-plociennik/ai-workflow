# AI Workflow Maintenance Baseline Example

Documentation example only. This is not active project state.

## Metadata

| Field | Value |
| --- | --- |
| Baseline name | `ai-workflow-maintainer` |
| Scope | `AI Workflow template maintenance` |
| State | `example` |
| Source | `.systems/ai/templates/prompting/ai-workflow-maintenance-baseline.template.md` |

## Role

Maintain AI Workflow as a portable workflow template.

Focus on:

- source-of-truth order;
- target-repository safety;
- local-only runtime boundaries;
- validator coverage;
- phase-gate evidence;
- backward-compatible installation and update behavior.

## Required Variables

| Variable | Expected Value | Source |
| --- | --- | --- |
| `workflow_home` | `AI_WORKFLOW_HOME` | repository modes policy |
| `workspace_home` | `AI_WORKFLOW_WORKSPACE_HOME` | repository modes policy |
| `runtime_tracking` | `ai-workflow-workspace remains untracked in the official repository` | branch policy and `.gitignore` |
| `final_check_policy` | `owner-triggered only` | autopilot policy and workflow router |
| `prompt_composition_authority` | `advisory only` | prompt composition contract |

## Forbidden Overrides

- Do not edit target-repository `.systems/**` from a nested clone.
- Do not track `ai-workflow-workspace/**` in the official repository.
- Do not weaken validators to pass a change.
- Do not run `phase-8-final-check` from autopilot.
- Do not let generated roles, variables, or examples override policy.

## Evidence Expectations

- Run workflow validators before finalizing template changes.
- Record skipped checks and their impact.
- Keep examples labeled as documentation examples.
