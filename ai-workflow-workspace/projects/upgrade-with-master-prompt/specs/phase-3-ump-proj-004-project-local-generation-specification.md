# Phase 3 Specification: UMP-PROJ-004-project-local-generation

## Task

| Field | Value |
| --- | --- |
| Task ID | `UMP-PROJ-004-project-local-generation` |
| Title | Define project-local generation lifecycle |
| Risk | `high` |
| Status | `conditional` |

## Goal

Define how project-local role and variable artifacts are generated, stored, refreshed, and used as supporting context.

## Scope

- Define project-local prompting namespace under each project workspace.
- Define generation inputs from accepted context, phase, task type, role, audience, output needs, owner decisions, assumptions, and sources.
- Define when the agent asks, when it may infer, and how assumptions are recorded.
- Define refresh triggers after context, architecture, plan, spec, status, or owner decisions change.
- Define conflict handling with status, task index, plan, specs, memory, and skills.
- Define how generated artifacts are used without becoming policy.

## Out Of Scope

- Generating artifacts for all existing projects.
- Adding scheduler state or active-thread registry.
- Storing project-specific generated artifacts under `.systems/**`.
- Modifying memory policy.

## Dependencies

- Blocking: `UMP-CORE-001-prompt-composition-contract`.
- Blocking: `UMP-TPL-002-role-variable-templates`.
- Informational: `UMP-WF-003-workflow-phase-routing`.
- Blocking: owner approval before implementation.

## Implementation Steps

1. Confirm core contract and templates exist.
2. Add lifecycle guidance in the selected system-owned doc or template surface.
3. Define the project-local prompting namespace and routers.
4. Define variable generation rules: required variables, inference rules, ask conditions, assumption recording, and source labels.
5. Define role generation rules for workflow-phase and project-domain roles.
6. Define refresh triggers and stale artifact handling.
7. Define conflict resolution when generated artifacts disagree with status, specs, memory, skills, or owner instructions.
8. Run validators and targeted searches.

## Edge Cases

| Case | Handling |
| --- | --- |
| Project context changes after role pack generation | handled: refresh required before relying on stale role or variables. |
| Variable is useful but low confidence | handled: record assumption and ask if it affects implementation correctness. |
| Generated role conflicts with task spec | handled: task spec wins for task scope; role is refreshed or ignored. |
| Project has no prompting artifacts | handled: workflow proceeds without them. |
| Two threads try to update the same project prompting artifact | handled: parallel work stop condition applies. |

## Potential Errors

- Lifecycle creates a hidden scheduler or lock system.
- Project-local artifacts are written into system docs.
- Variables are inferred without source labels.
- Refresh rules are too vague to prevent stale context.

## Tests

| Test | Method | Pass Condition |
| --- | --- | --- |
| Workflow validation | `.systems/scripts/validate-workflow` | Command exits successfully. |
| Naming | `.systems/scripts/check-naming` | New template filenames and examples pass policy. |
| Status consistency | `.systems/scripts/check-status-consistency` | Command exits successfully. |
| Workspace tracking | `git ls-files ai-workflow-workspace` | No workspace files are tracked. |
| Ignore check | `git check-ignore -v ai-workflow-workspace/projects/upgrade-with-master-prompt/status.md` | Workspace remains ignored. |

## User Decisions

Required before implementation:

- Recommendation: define lifecycle and namespace now, but do not generate artifacts for every project automatically. Impact: safe foundation with limited migration risk.
- Alternative: defer project-local lifecycle until after core/templates/routing ship. Impact: smaller first implementation but leaves generation behavior underspecified.

## Assumptions

- Project-local generated artifacts belong under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/`.
- Generation should be explicit and refreshable, not implicit hidden context.

## Uncertainties

Blocking uncertainties: none.

Non-blocking uncertainties:

- Exact project-local subdirectory names can be finalized during implementation if routing and validators agree.

## Implementation Gate

All planning conditions are satisfied.

Implementation may start only after:

- core contract and templates are implemented;
- Spec QA PASS;
- owner approval for high-risk implementation.

Can proceed to implementation after owner approval and dependency completion: yes.

## Evidence

- artifacts-reviewed: architecture, project plan, Plan QA, task index, core contract spec, template spec, routing spec, project context, and parallel work policy.
- manual-checks: lifecycle task does not require system docs to store project-specific generated artifacts.

