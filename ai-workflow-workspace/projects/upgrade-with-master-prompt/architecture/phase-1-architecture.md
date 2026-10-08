# Phase 1 Architecture: upgrade-with-master-prompt

## Summary

Architecture result: `PASS`

The architecture defines a layered prompt-composition capability for AI Workflow. It keeps execution policy authoritative while adding structured, reusable ways to frame agent roles, variables, and project-specific prompt context.

The design is ready for project planning because storage boundaries, authority limits, lifecycle, validation, routing, and risk ownership are explicit.

## Goals

- Create a system-owned prompt composition contract that explains what prompt modules, role profiles, and variable packs may influence.
- Add reusable templates for role profiles, variable packs, prompt modules, and workflow-phase roles.
- Allow project-local generated role and variable artifacts derived from accepted project context.
- Give AI Workflow itself a baseline maintenance role and variable profile.
- Preserve useful concepts from the reference prompt materials without treating those files as instruction.
- Strengthen critical review modes for phases such as idea validation, architecture QA, plan QA, spec QA, and implementation review.
- Keep human conversation guidance separate from agent execution policy.

## Boundaries And Out Of Scope

In scope:

- system contract for prompt composition;
- system templates for prompt modules, role profiles, variable packs, and phase-role profiles;
- project-local generated prompting artifacts;
- routing guidance for when prompt artifacts are read;
- validator coverage for required files, references, and unsafe authority wording;
- examples and human-facing guidance.

Out of scope for implementation:

- direct migration of old prompt text;
- ChatGPT-specific project settings as execution policy;
- PDF upload workflow;
- any rule that makes `masterprompt` authoritative;
- lock files, scheduler state, or new status fields;
- product-code changes;
- external API writes, migrations, secrets, infrastructure, or real external effects.

## Components And Responsibilities

| Component | Future Location | Responsibility |
| --- | --- | --- |
| Prompt composition contract | `.systems/ai/core/prompt-composition.md` | Defines authority, precedence, allowed influence, lifecycle, and safety boundaries. |
| Prompting templates | `.systems/ai/templates/prompting/` | Provides reusable template files for prompt modules, role profiles, variable packs, and phase-role profiles. |
| Project prompting artifacts | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/prompting/` | Stores generated project-local role and variable artifacts derived from accepted project context. |
| Workflow-phase role catalog | `.systems/ai/templates/prompting/` and examples | Defines advisory role profiles such as idea validator, architecture critic, plan reviewer, spec QA reviewer, and implementation reviewer. |
| AI Workflow maintenance baseline | system-owned prompt composition docs and templates | Defines the baseline role/variables for maintaining AI Workflow itself. |
| Routing references | `AGENTS.md`, `workflow.md`, `command-routing.md`, phase files where needed | Tells agents when to read prompting artifacts without changing source-of-truth order. |
| Validators | `.systems/scripts/**` and required artifact lists | Enforces required files/references and blocks unsafe authority language. |
| Human guidance | `HUMANS.md` and `.systems/ai/templates/humans/` | Gives owners practical conversation guidance without becoming agent execution policy. |
| Examples | `.systems/ai/examples/**` | Shows safe role/variable packs and phase-role usage. |

## Dependencies

| Dependency | Type | Notes |
| --- | --- | --- |
| `AGENTS.md` | blocking | Prompt artifacts must stay below it in authority. |
| `.systems/ai/core/prompt-injection.md` | blocking | Reference prompt files are data only. |
| `.systems/ai/core/risk-model.md` | blocking | Implementation is high risk and needs owner approval. |
| `.systems/ai/core/workflow.md` | blocking | Routing must not bypass canonical phases. |
| `.systems/ai/core/parallel-work-policy.md` | informational | No lock files or status fields are added. |
| Existing validators | blocking for completion | New required artifacts and unsafe authority language need validation coverage. |

## Main Flow

1. Agent starts workflow-governed work and reads `AGENTS.md` plus core policy.
2. If the project has generated prompting artifacts, the agent reads them as supporting context after canonical policy and phase files.
3. A role profile frames the work mode, evidence expectations, and review stance.
4. A variable pack records inferred or owner-provided project variables such as role, audience, task type, work mode, output format, success criteria, assumptions, and source labels.
5. The current phase file remains the gate for writes, evidence, PASS criteria, and stop conditions.
6. Validators ensure required prompting docs exist and no unsafe authority language is introduced.
7. Human guidance explains how the owner can conduct better conversations, but it does not govern agent permissions.

## Authority Model

Prompting artifacts are advisory.

They may:

- shape tone, framing, review stance, and context organization;
- require source labels and explicit assumptions;
- make phase roles sharper and more critical;
- define project-local variables and expected output form.

They may not:

- override `AGENTS.md`;
- override `.systems/ai/core/**`;
- change phase pass criteria;
- weaken risk, permissions, evidence, or Definition of Done;
- approve implementation;
- bypass owner decisions;
- treat old reference files as instruction.

## Architectural Decisions Made

| ID | Decision | Impact |
| --- | --- | --- |
| `D-001` | Prompt artifacts are subordinate to workflow policy. | Removes authority inversion risk. |
| `D-002` | One system core prompt composition contract is required. | Centralizes precedence, lifecycle, and safety rules. |
| `D-003` | Templates live under a dedicated prompting template namespace. | Keeps reusable files system-owned and discoverable. |
| `D-004` | Generated project artifacts live under project workspace. | Prevents repo-specific runtime facts from entering system docs. |
| `D-005` | Phase roles and domain roles use the same role-profile contract. | Reduces duplicate models while preserving scope limits. |
| `D-006` | Validator coverage is part of the implementation plan. | Prevents docs-only drift and unsafe precedence language. |
| `D-007` | Human guidance is separate from agent execution policy. | Avoids mixing owner advice with agent authority. |

Decision record: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/decisions/2026-06-11-prompt-composition-architecture-decisions.md`.

## Decisions To Make Later

| Decision | Owner | Blocking Now | Closure Point |
| --- | --- | --- | --- |
| Exact wording of each future system file | implementation task owner | no | per task spec and implementation review |
| Whether validators are implemented in existing scripts or a new helper script | implementation task owner | no | validator task spec |
| Final list of examples | implementation task owner | no | docs/examples task spec |
| Whether to implement all tasks in one implementation run or selected tasks first | owner | no | before `phase-4-implementation` |

No blocking architecture decisions remain for project planning.

## Risks

| Risk | Class | Mitigation |
| --- | --- | --- |
| Authority inversion | high | Core contract states prompting artifacts are subordinate; validators block unsafe wording. |
| Prompt injection from old files | high | Old files are reference data only; no verbatim migration by default. |
| Phase gate weakening | high | Role profiles cannot change phase pass criteria or evidence. |
| Runtime/system ownership confusion | high | Project-local artifacts stay under project workspace; system templates stay generic. |
| Validator gaps | medium | Dedicated validator task is required before implementation is done. |
| Human guidance confusion | medium | Human guidance is separated from execution policy. |

## Assumptions

- The project remains in the upstream `ai-workflow` repository.
- Planning artifacts are local-only under ignored workspace.
- Future implementation will modify tracked system docs/templates/scripts only after owner approval.
- No critical-risk operations are required.
- Existing source-of-truth and prompt-injection policy are correct and remain authoritative.

## Unknowns Blocking

None.

## Unknowns Non-Blocking

| Unknown | Owner | Impact | Closure Condition |
| --- | --- | --- | --- |
| Exact final filenames inside `.systems/ai/templates/prompting/` | implementation task owner | Minor implementation naming detail | Closed in template task spec before file writes. |
| Exact validator script shape | implementation task owner | May affect number of files changed | Closed in validator task spec before file writes. |
| Number of examples | implementation task owner | Affects docs breadth only | Closed in docs/examples task spec. |

## Impact On Project Plan

The plan should use a linear sequence:

1. create the core prompt composition contract;
2. add reusable templates and role/variable contracts;
3. integrate workflow routing and phase-role guidance;
4. define project-local generated artifact lifecycle;
5. add validator coverage;
6. add human guidance and examples.

Parallel packages are not recommended because the tasks have sequential authority and validation dependencies.

## Gate Decision

```text
result: PASS
blocking-reason: none
next-valid-step: phase-1-architecture-qa
can-plan-without-architecture-guessing: yes
implementation-approval-required-later: yes
```

## Evidence

- artifacts-reviewed: project context, idea validation, project repo intake, repo intake, workflow router, autopilot policy, risk model, permissions, prompt-injection policy, and parallel work policy.
- manual-checks: no product-code writes; no `.systems/**` writes; old prompt files treated as untrusted reference input only.

