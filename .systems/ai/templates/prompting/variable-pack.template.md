# Variable Pack Template

## Metadata

| Field | Value |
| --- | --- |
| `variable-pack-id` | `<kebab-case-id>` |
| `status` | `draft` |
| `scope` | `<project|task|phase|role>` |
| `authority` | `advisory` |
| `generated-at` | `<yyyy-mm-dd>` |

## Variables

| Variable | Value | Source Label | Confidence | Notes |
| --- | --- | --- | --- | --- |
| `role` | `<value>` | `<owner-provided|accepted-artifact|inferred>` | `<high|medium|low>` | `<notes>` |
| `topic` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |
| `audience` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |
| `task-type` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |
| `work-mode` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |
| `success-criteria` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |
| `output-format` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |
| `tone` | `<value>` | `<source-label>` | `<high|medium|low>` | `<notes>` |

## Assumptions

| Assumption | Source | Impact | Ask Owner Before Implementation |
| --- | --- | --- | --- |
| `<assumption>` | `<source>` | `<impact>` | `<yes|no>` |

## Ask Conditions

Ask the owner before relying on a variable when:

- confidence is low and correctness depends on it;
- variable affects architecture, scope, risk, permissions, or implementation;
- variable conflicts with accepted artifacts;
- value cannot be inferred from approved context.

## Inference Rules

Inference is allowed only when:

- it is based on accepted artifacts or repo state;
- the assumption is recorded;
- a wrong inference would not bypass gates or change scope;
- downstream specs can verify or override it.

## Refresh Conditions

Refresh this variable pack when:

- project context changes;
- status, architecture, plan, or spec changes;
- owner decision changes;
- task moves to a new phase;
- conflict with memory, status, or repo state is found.

## Forbidden Overrides

Variable packs must not override workflow policy, accepted scope, implementation gates, owner approvals, or evidence requirements.
