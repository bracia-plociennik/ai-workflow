# Phase 3 Specification: UMP-CORE-001-prompt-composition-contract

## Task

| Field | Value |
| --- | --- |
| Task ID | `UMP-CORE-001-prompt-composition-contract` |
| Title | Define prompt composition core contract |
| Risk | `high` |
| Status | `conditional` |

## Goal

Create a system-owned core contract for prompt composition that defines authority, allowed influence, lifecycle, conflict handling, and safety boundaries for prompt modules, role profiles, and variable packs.

## Scope

- Add a core policy document for prompt composition.
- Define artifact types: prompt module, role profile, variable pack, workflow-phase role, project-domain role, and AI Workflow maintenance baseline.
- Define source-of-truth order and explicit subordination to `AGENTS.md`, core policy, phase gates, permissions, risk model, owner approvals, and evidence.
- Define source-use rules for old prompt files and project context.
- Define conflict handling when prompt artifacts disagree with status, memory, skills, phase files, or owner instructions.
- Define lifecycle states for generated prompting artifacts.

## Out Of Scope

- Creating templates.
- Creating project-local generated artifacts.
- Updating validators.
- Adding examples.
- Changing phase pass criteria.
- Changing autopilot ranges.

## Dependencies

- Architecture QA PASS.
- Owner approval before implementation.

No future task output is required to implement this task.

## Implementation Steps

1. Confirm tracked working tree state and preserve unrelated files.
2. Add `.systems/ai/core/prompt-composition.md`.
3. Include sections for purpose, authority, artifact types, allowed influence, forbidden overrides, lifecycle, source use, conflict handling, memory/status interaction, and implementation approval.
4. State that old prompt files and generated artifacts are supporting data unless promoted through approved workflow docs.
5. State that no prompt artifact may weaken gates, evidence, permissions, risk policy, owner approvals, or Definition of Done.
6. Add minimal cross-reference notes only where needed by this task; leave broader routing to `UMP-WF-003-workflow-phase-routing`.
7. Run workflow validators and targeted searches listed in the test plan.

## Edge Cases

| Case | Handling |
| --- | --- |
| Old source file claims it is authoritative | handled: classify as reference data and reject authority inversion. |
| Project role asks to skip evidence | handled: core contract forbids weakening evidence gates. |
| Generated variables conflict with project status | handled: status wins; generated variables must be refreshed or ignored. |
| Skill guidance conflicts with prompt module | handled: source-of-truth order decides; stricter safety rule wins. |
| Owner asks to bypass gates through a prompt profile | handled: stop under existing workflow policy. |

## Potential Errors

- Wording implies prompt artifacts can override phase files.
- Contract duplicates too much existing policy instead of routing to it.
- Contract omits lifecycle and conflict handling.
- Contract fails to distinguish human guidance from agent execution policy.

## Tests

| Test | Method | Pass Condition |
| --- | --- | --- |
| Workflow validation | `.systems/scripts/validate-workflow` | Command exits successfully. |
| Naming | `.systems/scripts/check-naming` | Command exits successfully. |
| Required artifacts | `.systems/scripts/check-required-artifacts` after validator task updates | Command exits successfully. |
| Unsafe authority wording search | targeted `rg` search | No new tracked text makes prompt artifacts authoritative over workflow policy. |
| Diff check | `git diff --check` | Command exits successfully. |

## User Decisions

Required before implementation:

- Recommendation: approve implementation of the core prompt composition contract first. Impact: creates the safety foundation for every later task.
- Alternative: stop after planning and request another architecture review. Impact: delays implementation but adds another safety pass.

## Assumptions

- Candidate path `.systems/ai/core/prompt-composition.md` is acceptable unless implementation review finds a stronger local convention.
- The contract should be concise and reference existing policy instead of duplicating it.

## Uncertainties

Blocking uncertainties: none.

Non-blocking uncertainties:

- Exact section titles can be adjusted during implementation if the same contract content remains present.

## Implementation Gate

All planning conditions are satisfied.

Implementation may start only after:

- Spec QA PASS;
- owner approval for high-risk implementation;
- clean or understood working tree for intended tracked write set.

Can proceed to implementation after owner approval: yes.

## Evidence

- artifacts-reviewed: architecture, Architecture QA, project plan, Plan QA, task index, decision record, risk model, permissions, prompt-injection policy.
- manual-checks: task has no dependency on later tasks and can be implemented first.

