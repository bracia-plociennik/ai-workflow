# Phase 3 Specification: UMP-TPL-002-role-variable-templates

## Task

| Field | Value |
| --- | --- |
| Task ID | `UMP-TPL-002-role-variable-templates` |
| Title | Add role and variable templates |
| Risk | `high` |
| Status | `conditional` |

## Goal

Add reusable system templates for role profiles, variable packs, prompt modules, workflow-phase roles, project-domain roles, and the AI Workflow maintenance baseline.

## Scope

- Add a dedicated prompting template namespace.
- Add a role profile template with purpose, scope, authority limits, forbidden overrides, expected evidence, and source requirements.
- Add a variable pack template with required variables, inference rules, assumptions, source labels, refresh triggers, and owner decisions.
- Add a prompt module template with inputs, outputs, allowed influence, and constraints.
- Add a workflow-phase role template.
- Add an AI Workflow maintenance baseline template or example.

## Out Of Scope

- Concrete project-local role generation.
- Validator implementation.
- Broad routing updates.
- Copying old prompt text verbatim.

## Dependencies

- Blocking: `UMP-CORE-001-prompt-composition-contract`.
- Blocking: owner approval before implementation.

## Implementation Steps

1. Confirm the core prompt composition contract exists.
2. Create the selected prompting template directory.
3. Add role profile template with explicit authority limits and evidence expectations.
4. Add variable pack template with required variables and assumption recording.
5. Add prompt module template with source labels and forbidden override language.
6. Add workflow-phase role template that keeps phase files authoritative.
7. Add AI Workflow maintenance baseline template or example.
8. Link templates only as far as this task requires; broader routing remains in `UMP-WF-003`.
9. Run workflow validators and targeted safety searches.

## Edge Cases

| Case | Handling |
| --- | --- |
| Role profile says to ignore phase gate | handled: template forbids override of phase gates. |
| Variable value is inferred from weak context | handled: template records assumption and source confidence. |
| Project-domain role conflicts with workflow-phase role | handled: phase role and phase file govern the current phase. |
| Maintenance baseline becomes a hidden global persona | handled: baseline stays subordinate to policy and is explicit. |
| Template includes ChatGPT-specific settings | handled: exclude or label as human/platform-specific guidance. |

## Potential Errors

- Templates contain vague persona claims instead of executable boundaries.
- Templates omit source labels or assumption records.
- Templates duplicate policy instead of referencing authority limits.
- AI Workflow maintenance baseline reads as a permission grant.

## Tests

| Test | Method | Pass Condition |
| --- | --- | --- |
| Workflow validation | `.systems/scripts/validate-workflow` | Command exits successfully. |
| Naming | `.systems/scripts/check-naming` | New template filenames pass policy. |
| Required artifacts | validator checks after `UMP-VAL-005` | Required template files are covered. |
| Safety search | targeted `rg` search | No template grants authority over workflow policy. |
| Diff check | `git diff --check` | Command exits successfully. |

## User Decisions

Required before implementation:

- Recommendation: implement templates after the core contract. Impact: gives later routing and project-local lifecycle concrete artifacts to reference.
- Alternative: defer templates and implement only the core contract first. Impact: lowers immediate change size but delays useful role/variable generation.

## Assumptions

- A dedicated prompting template namespace is acceptable.
- Templates should be small, composable, and explicit rather than monolithic.

## Uncertainties

Blocking uncertainties: none.

Non-blocking uncertainties:

- Exact filenames can be finalized in implementation while preserving the required template set.

## Implementation Gate

All planning conditions are satisfied.

Implementation may start only after:

- `UMP-CORE-001` is implemented;
- Spec QA PASS;
- owner approval for high-risk implementation.

Can proceed to implementation after owner approval and dependency completion: yes.

## Evidence

- artifacts-reviewed: architecture, project plan, Plan QA, task index, and `UMP-CORE-001` spec.
- manual-checks: template task has a clear dependency on the core contract and does not require later task outputs.

