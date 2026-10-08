# Phase 6 Distillation: UMP-TPL-002-role-variable-templates

## Co Zostalo Zrobione

- Added `.systems/ai/templates/prompting/` as the reusable template namespace.
- Added templates for prompt modules, role profiles, variable packs, workflow-phase roles, and AI Workflow maintenance baseline.
- Required every template to carry scope, source labels, evidence expectations, refresh conditions, and authority limits.
- Kept templates advisory and subordinate to the prompt composition contract and workflow policy.

## Problemy

- Templates are useful only after router references and project-local lifecycle rules are added.
- Validator enforcement still has to require the new template namespace and block unsafe authority language.

## Decyzje

- Templates define structure and safety boundaries, not permission.
- Variable packs must distinguish required variables, inferred variables, assumptions, and conditions that require asking the owner.
- Role profiles may make review stricter but cannot make workflow gates easier to pass.

## Zasady Na Przyszlosc

- New role or variable templates need explicit forbidden override sections.
- Generated variables should record their source, confidence, assumption policy, and refresh triggers.
- Keep ChatGPT-specific personalization separate from AI Workflow execution policy unless a future task explicitly maps it.

## Status Repo Memory

memory-in-repo-memory: true

## Evidence

- Quality artifact: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-tpl-002-role-variable-templates-quality.md`.
- Implementation result: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-4-ump-tpl-002-role-variable-templates-implementation-result.md`.
