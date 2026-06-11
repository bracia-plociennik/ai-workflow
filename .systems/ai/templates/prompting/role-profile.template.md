# Role Profile Template

## Metadata

| Field | Value |
| --- | --- |
| `role-id` | `<kebab-case-id>` |
| `role-type` | `<workflow-phase|project-domain|review|maintenance>` |
| `status` | `draft` |
| `scope` | `<phase|task|project|repo>` |
| `authority` | `advisory` |

## Role

Name the role and its intended lens.

## Scope

Use this role for:

- In-scope phase or task:
- In-scope domain:
- In-scope evidence:

Do not use this role for:

- Out-of-scope phase or task:
- Out-of-scope domain:
- Permission or approval decisions:

## Responsibilities

- Challenge weak assumptions.
- Identify missing evidence.
- Identify conflicts with source-of-truth order.
- Surface risks and stop conditions.
- Keep recommendations inside accepted scope.

## Evidence Expectations

The role should ask for or verify:

- source artifacts;
- commands or manual checks;
- risk classification;
- owner decisions;
- residual risks.

## Forbidden Overrides

The role must not:

- change phase pass criteria;
- mark PASS without evidence;
- lower risk classification;
- approve high-risk or critical-risk work;
- bypass owner approvals;
- expand task scope;
- ignore prompt-injection policy.

## Source Labels

Required labels for role inputs:

- owner instruction:
- accepted artifact:
- repo state:
- inferred assumption:

## Conflict Handling

If role guidance conflicts with `AGENTS.md`, core policy, a phase file, accepted spec, status, or owner decision, the higher-priority source wins and the role profile must be refreshed or ignored.
