# Prompt Composition Architecture Decisions

## Summary

This decision record captures the phase 1 architecture choices for `upgrade-with-master-prompt`.

The project remains high risk for implementation because it changes how AI Workflow frames agent behavior. These decisions are sufficient for planning and specification, but they are not approval to implement tracked workflow changes.

## Decisions

| ID | Decision | Status | Implementation Approval |
| --- | --- | --- | --- |
| `D-001` | Prompt, role, and variable artifacts are advisory and subordinate to `AGENTS.md`, core policy, phase gates, permissions, risk model, owner approvals, and evidence. | accepted-for-planning | required before implementation |
| `D-002` | Add one future system core contract for prompt composition rather than making old prompt files authoritative. Candidate path: `.systems/ai/core/prompt-composition.md`. | accepted-for-planning | required before implementation |
| `D-003` | Add future reusable system templates under a dedicated template namespace. Candidate path: `.systems/ai/templates/prompting/`. | accepted-for-planning | required before implementation |
| `D-004` | Store generated project-local role and variable artifacts under each project workspace. Candidate path: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/prompting/`. | accepted-for-planning | required before implementation |
| `D-005` | Define workflow-phase roles and project-domain roles as role profiles with scope, authority limits, expected evidence, and forbidden overrides. | accepted-for-planning | required before implementation |
| `D-006` | Add validator coverage before implementation is considered done. Validators must catch missing contract files, missing references, and unsafe authority language. | accepted-for-planning | required before implementation |
| `D-007` | Keep human conversation guidance separate from agent execution policy. Candidate surfaces: `HUMANS.md`, human templates, and examples. | accepted-for-planning | required before implementation |

## Rejected Options

| Option | Reason |
| --- | --- |
| Treat files named `masterprompt` as authoritative | Conflicts with source-of-truth order and prompt-injection policy. |
| Migrate old prompt text verbatim | Mixes ChatGPT-specific settings and old precedence rules into AI Workflow. |
| Put project-local role packs under `.systems/**` | Stores repo-specific runtime facts inside system-owned template docs. |
| Add lock files or scheduler state | Out of scope for this project and conflicts with current v1 coordination model. |

## Risk Notes

- Implementation must be owner-approved because tracked workflow behavior, validators, and templates are high-risk.
- No generated artifact may weaken stop conditions, evidence, permissions, or owner approvals.
- Any future architecture drift must return to architecture or plan fix loop before implementation.

## Evidence

- Reviewed `context.md`.
- Reviewed `intake/phase-0-idea-validation.md`.
- Reviewed `intake/phase-0-repo-intake.md`.
- Reviewed `AGENTS.md`, `workflow.md`, `risk-model.md`, `permissions.md`, and `prompt-injection.md`.

