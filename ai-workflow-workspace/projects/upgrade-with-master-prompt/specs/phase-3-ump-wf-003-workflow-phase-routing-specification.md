# Phase 3 Specification: UMP-WF-003-workflow-phase-routing

## Task

| Field | Value |
| --- | --- |
| Task ID | `UMP-WF-003-workflow-phase-routing` |
| Title | Integrate workflow phase routing |
| Risk | `high` |
| Status | `conditional` |

## Goal

Integrate prompt composition and phase-role guidance into AI Workflow routing without changing authority order, stop conditions, autopilot ranges, status fields, or lock-file policy.

## Scope

- Add references from execution routers to the prompt composition contract.
- Explain when agents read project-local prompting artifacts.
- Define workflow-phase role use as advisory framing for phase quality.
- Keep phase files as the source of pass criteria, fail criteria, evidence, writes, and stops.
- Keep skills as supporting guidance only.
- Preserve parallel-work v1 status-only coordination.

## Out Of Scope

- Adding new workflow phases.
- Adding lock files or scheduler fields.
- Changing autopilot ranges.
- Implementing validators.
- Creating project-local generated artifacts.

## Dependencies

- Blocking: `UMP-CORE-001-prompt-composition-contract`.
- Blocking: `UMP-TPL-002-role-variable-templates`.
- Blocking: owner approval before implementation.

## Implementation Steps

1. Confirm core contract and templates exist.
2. Update `AGENTS.md` read order or routing language only as required by the approved implementation scope.
3. Update core workflow or command routing references so prompt composition questions route to the new contract.
4. Add guidance that project-local prompting artifacts are read after canonical policy and current phase files.
5. Add phase-role language that sharpens review stance without changing pass criteria.
6. Check that parallel work policy still has no lock files or new status fields.
7. Run validators and targeted searches for authority-order conflicts.

## Edge Cases

| Case | Handling |
| --- | --- |
| Prompt artifact says a phase can be skipped | handled: phase files and workflow router win. |
| Generated role conflicts with a skill | handled: source-of-truth order and stricter safety rule decide. |
| Owner asks to use role profile as approval | handled: role profile cannot grant approval. |
| Parallel thread reads stale role variables | handled: project status and accepted artifacts decide current state. |
| Routing reference creates recursive read order | handled: prompt composition docs are supporting guidance, not a new root contract. |

## Potential Errors

- Routing text places prompt composition above existing core policy.
- Phase-role text weakens QA criteria.
- Command routing implies prompt composition can start implementation.
- Parallel-work contract is accidentally expanded with lock-file behavior.

## Tests

| Test | Method | Pass Condition |
| --- | --- | --- |
| Workflow validation | `.systems/scripts/validate-workflow` | Command exits successfully. |
| Required artifacts | `.systems/scripts/check-required-artifacts` after required list updates | Command exits successfully. |
| Status consistency | `.systems/scripts/check-status-consistency` | Command exits successfully. |
| Authority search | targeted `rg` search | No routing text elevates prompt artifacts over policy. |
| Diff check | `git diff --check` | Command exits successfully. |

## User Decisions

Required before implementation:

- Recommendation: route prompt composition through `AGENTS.md`, workflow router, and command routing in a minimal way. Impact: makes the feature discoverable without changing gates.
- Alternative: keep routing only in the new core contract for the first implementation. Impact: smaller change, but weaker discoverability.

## Assumptions

- Minimal routing is preferred over broad edits across every phase file.
- Phase-specific role examples can be referenced without changing phase gate text.

## Uncertainties

Blocking uncertainties: none.

Non-blocking uncertainties:

- Exact router files can be finalized during implementation if the authority order remains intact.

## Implementation Gate

All planning conditions are satisfied.

Implementation may start only after:

- `UMP-CORE-001` and `UMP-TPL-002` are implemented;
- Spec QA PASS;
- owner approval for high-risk implementation.

Can proceed to implementation after owner approval and dependency completion: yes.

## Evidence

- artifacts-reviewed: architecture, project plan, Plan QA, task index, core contract spec, template spec, workflow router, command routing, and parallel work policy.
- manual-checks: routing task does not require new status fields, new lock files, or phase range changes.

