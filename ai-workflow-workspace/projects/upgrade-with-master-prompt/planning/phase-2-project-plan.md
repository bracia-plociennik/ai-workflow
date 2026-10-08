# Phase 2 Project Plan: upgrade-with-master-prompt

## Summary

Plan result: `PASS`

This plan converts the accepted architecture into six implementation-ready task contracts. All tasks are marked `conditional` because implementation changes workflow-system behavior and requires owner approval before `phase-4-implementation`.

The plan intentionally uses linear sequencing. No packages are created because the tasks have real authority, template, routing, lifecycle, validation, and documentation dependencies.

## Inputs

- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/context.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/intake/phase-0-idea-validation.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/intake/phase-0-repo-intake.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/architecture/phase-1-architecture.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/decisions/2026-06-11-prompt-composition-architecture-decisions.md`

## Planning Strategy

- Build authority and safety first.
- Add templates after the core contract exists.
- Route workflow usage after template and role concepts are defined.
- Add project-local generation lifecycle after routing boundaries are clear.
- Add validators after required artifacts and references are known.
- Add human guidance and examples last, so they reflect the final safe contract.

## Task Sequence

| Order | Task ID | Title | Risk | Readiness | User Decision Before Implementation |
| --- | --- | --- | --- | --- | --- |
| 1 | `UMP-CORE-001-prompt-composition-contract` | Define prompt composition core contract | high | conditional | yes |
| 2 | `UMP-TPL-002-role-variable-templates` | Add role and variable templates | high | conditional | yes |
| 3 | `UMP-WF-003-workflow-phase-routing` | Integrate workflow phase routing | high | conditional | yes |
| 4 | `UMP-PROJ-004-project-local-generation` | Define project-local generation lifecycle | high | conditional | yes |
| 5 | `UMP-VAL-005-safety-validators` | Add safety validator coverage | high | conditional | yes |
| 6 | `UMP-DOCS-006-human-guidance-examples` | Add human guidance and examples | medium | conditional | yes |

## Task Contracts

### UMP-CORE-001-prompt-composition-contract

Goal: create the future core policy contract for prompt composition.

Scope:

- define authority and source-of-truth boundaries;
- define allowed and forbidden influence for prompt modules, role profiles, and variable packs;
- define lifecycle states for generated prompting artifacts;
- define conflict handling with phase files, skills, memory, status, and owner instructions;
- define safety boundaries for old reference prompt material.

Out of scope:

- creating templates;
- updating validators;
- adding project-local generated artifacts;
- changing phase behavior beyond documented routing.

Definition of Done:

- core contract exists in the selected system-owned path;
- contract states prompting artifacts are advisory and subordinate;
- contract forbids bypassing gates, permissions, evidence, risk policy, and owner approvals;
- contract includes source-use and prompt-injection boundaries;
- references are added only where the implementation spec permits.

Dependencies:

- blocking: architecture QA PASS;
- blocking: owner approval before implementation.

Risk: high.

Main risk: unsafe authority wording could weaken AI Workflow gates.

Start condition: planning-range Spec QA PASS and owner approval for implementation.

End condition: core contract is implemented, linked, and validated without tracked workspace files.

Readiness status: conditional.

User decision: required before implementation.

### UMP-TPL-002-role-variable-templates

Goal: add reusable system templates for roles, variables, and prompt modules.

Scope:

- add a dedicated prompting template namespace;
- add role profile template with scope, authority limits, evidence expectations, and forbidden overrides;
- add variable pack template with required variables, inference rules, assumptions, and source labels;
- add prompt module template with purpose, scope, inputs, outputs, and constraints;
- add an AI Workflow maintenance baseline template or example as specified.

Out of scope:

- generating concrete project role packs;
- adding validators;
- changing command routing.

Definition of Done:

- templates are generic and system-owned;
- templates do not include unsafe authority language;
- templates include explicit authority limits and source labels;
- templates can support both workflow-phase and project-domain roles.

Dependencies:

- blocking: `UMP-CORE-001-prompt-composition-contract`;
- blocking: owner approval before implementation.

Risk: high.

Main risk: templates could encode broad persona behavior without policy limits.

Start condition: core prompt composition contract is implemented and validated.

End condition: templates exist, are linked by required docs, and pass naming/required-artifact checks.

Readiness status: conditional.

User decision: required before implementation.

### UMP-WF-003-workflow-phase-routing

Goal: integrate prompt composition and phase-role guidance into workflow routers.

Scope:

- add routing references where agents discover prompt composition guidance;
- define when workflow-phase roles are read;
- make phase roles advisory and gate-subordinate;
- preserve `AGENTS.md`, workflow phase files, task intake, guide, command routing, and response contract authority;
- avoid adding new status fields or lock files.

Out of scope:

- implementing generated project artifacts;
- adding new workflow phases;
- changing autopilot ranges;
- weakening stop conditions.

Definition of Done:

- core routers reference the prompt composition contract;
- routing order is explicit and does not conflict with source-of-truth order;
- phase roles cannot override current phase files;
- parallel work policy remains unchanged in shape.

Dependencies:

- blocking: `UMP-CORE-001-prompt-composition-contract`;
- blocking: `UMP-TPL-002-role-variable-templates`;
- blocking: owner approval before implementation.

Risk: high.

Main risk: routing references could make advisory prompt artifacts look mandatory or higher priority than policy.

Start condition: core contract and templates exist.

End condition: routing docs are updated and validators confirm required references.

Readiness status: conditional.

User decision: required before implementation.

### UMP-PROJ-004-project-local-generation

Goal: define lifecycle and storage for project-local generated role and variable artifacts.

Scope:

- define project-local prompting artifact namespace;
- define generation inputs from accepted context, phase, task type, owner decisions, and assumptions;
- define when to ask, when to infer, and how assumptions are recorded;
- define refresh rules when project context, architecture, plan, or spec changes;
- define how generated artifacts are used as supporting context only.

Out of scope:

- generating artifacts for all existing projects;
- adding a scheduler or active-thread registry;
- storing repo-specific generated artifacts under `.systems/**`.

Definition of Done:

- lifecycle is documented;
- generation inputs and assumptions are explicit;
- project-local storage is separated from system docs;
- refresh and conflict handling are defined;
- examples or templates point to the lifecycle.

Dependencies:

- blocking: `UMP-CORE-001-prompt-composition-contract`;
- blocking: `UMP-TPL-002-role-variable-templates`;
- informational: `UMP-WF-003-workflow-phase-routing`;
- blocking: owner approval before implementation.

Risk: high.

Main risk: project-local artifacts could be mistaken for policy or become stale.

Start condition: core contract and templates exist.

End condition: project-local lifecycle is documented and cross-referenced.

Readiness status: conditional.

User decision: required before implementation.

### UMP-VAL-005-safety-validators

Goal: add validator coverage for prompt composition artifacts and unsafe authority wording.

Scope:

- require the core prompt composition contract;
- require expected template namespace files;
- require key router references;
- block tracked workspace prompting artifacts;
- detect unsafe authority language patterns such as old masterprompt precedence;
- keep validator smoke tests passing.

Out of scope:

- semantic review of every role sentence;
- network or external lint tooling;
- weakening existing validators.

Definition of Done:

- validation command catches missing required prompt-composition artifacts;
- unsafe authority language is covered by a deterministic check;
- `validate-workflow` and focused validators pass;
- no existing branch/workspace protection is weakened.

Dependencies:

- blocking: `UMP-CORE-001-prompt-composition-contract`;
- blocking: `UMP-TPL-002-role-variable-templates`;
- blocking: `UMP-WF-003-workflow-phase-routing`;
- blocking: `UMP-PROJ-004-project-local-generation`;
- blocking: owner approval before implementation.

Risk: high.

Main risk: validator gaps could allow unsafe prompt precedence into tracked workflow docs.

Start condition: docs/templates and references exist in implementation branch.

End condition: validators fail on unsafe or missing artifacts and pass on the intended implementation.

Readiness status: conditional.

User decision: required before implementation.

### UMP-DOCS-006-human-guidance-examples

Goal: add owner-facing guidance and safe examples.

Scope:

- add concise `HUMANS.md` guidance for using roles and variables safely;
- add human templates or runbook pointers if needed;
- add examples for workflow-phase roles, project-domain roles, variable packs, and AI Workflow maintenance baseline;
- ensure examples are clearly marked as examples, not active project state.

Out of scope:

- changing execution authority;
- adding ChatGPT-specific settings as system policy;
- adding claims such as percentage improvements.

Definition of Done:

- human guidance is practical and separate from agent execution policy;
- examples show authority limits and source labels;
- docs link to the core contract and templates;
- examples do not create active project runtime state.

Dependencies:

- blocking: `UMP-CORE-001-prompt-composition-contract`;
- blocking: `UMP-TPL-002-role-variable-templates`;
- informational: `UMP-PROJ-004-project-local-generation`;
- informational: `UMP-VAL-005-safety-validators`;
- blocking: owner approval before implementation.

Risk: medium.

Main risk: human guidance could be read as agent policy if not labeled clearly.

Start condition: core contract and templates exist.

End condition: docs/examples are linked, labeled, and validated.

Readiness status: conditional.

User decision: required before implementation.

## Dependency Map

```text
UMP-CORE-001
-> UMP-TPL-002
-> UMP-WF-003
-> UMP-PROJ-004
-> UMP-VAL-005
-> UMP-DOCS-006
```

`UMP-PROJ-004` can use `UMP-WF-003` as informational input, but it still depends on the core contract and templates. `UMP-DOCS-006` depends on the final safety shape and should stay last.

## Tasks package

Packages created: none.

Reason:

- all planned tasks have sequential authority, template, routing, lifecycle, validation, or documentation dependencies;
- packaging would hide dependency order and increase review risk;
- no two tasks have independent write sets sufficient for a safe shared spec.

Solo execution blocks:

- `UMP-CORE-001-prompt-composition-contract`
- `UMP-TPL-002-role-variable-templates`
- `UMP-WF-003-workflow-phase-routing`
- `UMP-PROJ-004-project-local-generation`
- `UMP-VAL-005-safety-validators`
- `UMP-DOCS-006-human-guidance-examples`

Detected conflicts: none.

Next specification target: `UMP-CORE-001-prompt-composition-contract`.

Packaging QA is omitted because no package exists.

## Risk Summary

Highest-risk tasks:

- `UMP-CORE-001-prompt-composition-contract`
- `UMP-WF-003-workflow-phase-routing`
- `UMP-VAL-005-safety-validators`

All high-risk tasks require owner approval before implementation.

## Blocked And Conditional Tasks

Blocked tasks: none.

Conditional tasks:

- all planned tasks are conditional because implementation approval is required after planning-range stops.

No task has an unresolved planning blocker.

## Gate Decision

```text
result: PASS
blocking-reason: none
next-valid-step: phase-2-plan-qa
can-create-specs-after-plan-qa: yes
implementation-approval-required-later: yes
```

## Evidence

- artifacts-reviewed: architecture, Architecture QA, project context, project repo intake, idea validation, and architecture decision record.
- manual-checks: every task has ID, goal, scope, out-of-scope, Definition of Done, dependencies, risk, main risk, start condition, end condition, readiness status, and user-decision flag.
- manual-checks: task sequence exposes authority and validator risks before docs/examples.
- manual-checks: packaging was evaluated and omitted because no safe packages exist.

