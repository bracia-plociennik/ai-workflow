# Phase 3 Specification: UMP-DOCS-006-human-guidance-examples

## Task

| Field | Value |
| --- | --- |
| Task ID | `UMP-DOCS-006-human-guidance-examples` |
| Title | Add human guidance and examples |
| Risk | `medium` |
| Status | `conditional` |

## Goal

Add concise owner-facing guidance and safe examples for prompt composition, role profiles, variable packs, phase roles, and AI Workflow maintenance baseline.

## Scope

- Add or update human guidance so owners know how to use roles and variables safely.
- Add examples for workflow-phase roles.
- Add examples for project-domain roles.
- Add examples for variable packs and source labels.
- Add or link an AI Workflow maintenance baseline example.
- Label examples as examples and not active project state.

## Out Of Scope

- Changing agent execution authority.
- Adding ChatGPT-specific settings as system policy.
- Adding claims based on percentage improvements.
- Creating active runtime artifacts for real projects.
- Skipping validators.

## Dependencies

- Blocking: `UMP-CORE-001-prompt-composition-contract`.
- Blocking: `UMP-TPL-002-role-variable-templates`.
- Informational: `UMP-PROJ-004-project-local-generation`.
- Informational: `UMP-VAL-005-safety-validators`.
- Blocking: owner approval before implementation because this task ships with the high-risk workflow change set.

## Implementation Steps

1. Confirm core contract and templates exist.
2. Update `HUMANS.md` with concise practical guidance if in scope.
3. Add human template or runbook pointers only if they improve owner usage without duplicating policy.
4. Add examples under the approved examples namespace.
5. Mark examples clearly as documentation examples.
6. Avoid motivational percentage claims and platform-specific policy wording.
7. Run validators and targeted searches.

## Edge Cases

| Case | Handling |
| --- | --- |
| Human guidance reads like agent policy | handled: label as owner guidance and link to execution contract for agent policy. |
| Example includes unsafe authority wording | handled: remove or mark as rejected example if validator design allows that. |
| Example looks like active project status | handled: store under examples namespace and label documentation-only. |
| ChatGPT-specific settings are useful | handled: translate to general guidance or leave out. |
| Docs drift from templates | handled: examples reference current templates and validators run. |

## Potential Errors

- Human guidance duplicates `AGENTS.md`.
- Examples are too broad and imply global permission changes.
- Old prompt claims are copied into docs.
- Examples are not connected to templates.

## Tests

| Test | Method | Pass Condition |
| --- | --- | --- |
| Workflow validation | `.systems/scripts/validate-workflow` | Command exits successfully. |
| Naming | `.systems/scripts/check-naming` | Command exits successfully. |
| Required artifacts | `.systems/scripts/check-required-artifacts` | Command exits successfully. |
| QA evidence | `.systems/scripts/check-qa-evidence` | Command exits successfully. |
| Unsafe wording search | targeted `rg` search | No new example or human doc makes prompt artifacts authoritative. |
| Diff check | `git diff --check` | Command exits successfully. |

## User Decisions

Required before implementation:

- Recommendation: add concise human guidance and a small example set after validators are in place. Impact: improves usability while keeping enforcement active.
- Alternative: ship system docs/templates first and defer examples. Impact: lowers documentation scope but makes adoption harder.

## Assumptions

- Human-facing guidance should remain short and practical.
- Examples should demonstrate safe boundaries rather than reproduce old prompt text.

## Uncertainties

Blocking uncertainties: none.

Non-blocking uncertainties:

- Final number of examples can be adjusted during implementation as long as phase-role, domain-role, variable-pack, and maintenance-baseline examples remain covered.

## Implementation Gate

All planning conditions are satisfied.

Implementation may start only after:

- core contract and templates are implemented;
- Spec QA PASS;
- owner approval for the high-risk workflow change set.

Can proceed to implementation after owner approval and dependency completion: yes.

## Evidence

- artifacts-reviewed: architecture, project plan, Plan QA, task index, core contract spec, template spec, lifecycle spec, validator spec, and human runbook context.
- manual-checks: docs task is intentionally last and does not alter execution authority.

