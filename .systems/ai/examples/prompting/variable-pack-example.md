# Variable Pack Example

Documentation example only. This is not active project state.

## Metadata

| Field | Value |
| --- | --- |
| Pack name | `web-app-planning-variables` |
| Scope | `project planning` |
| State | `example` |
| Source | `.systems/ai/templates/prompting/variable-pack.template.md` |

## Variables

| Variable | Value | Source | Confidence | Requires Owner Confirmation |
| --- | --- | --- | --- | --- |
| `project_type` | `web application` | accepted project context | high | no |
| `primary_role` | `web-application-specialist` | owner request and project context | medium | no |
| `review_stance` | `critical-but-gate-bound` | prompt composition contract | high | no |
| `implementation_permission` | `requires active phase and owner-approved gate` | `AGENTS.md` and current phase file | high | yes |
| `external_effects_allowed` | `false until explicitly approved` | permissions policy and repo intake | high | yes |

## Assumptions

| Assumption | Source | Impact | Requires Owner Confirmation |
| --- | --- | --- | --- |
| The first implementation target is documentation and workflow behavior, not product code. | accepted project plan | medium | no |
| Real deployment, migrations, billing, or secrets are outside scope. | permissions policy | high | yes before any exception |

## Refresh Conditions

- Project context changes.
- Architecture, plan, spec, or status changes.
- Owner changes scope or approval.
- Risk classification changes.
- New source evidence conflicts with any value.

## Usage Evidence

When used for a real project, list the project-local variable pack path in the relevant phase artifact evidence.
