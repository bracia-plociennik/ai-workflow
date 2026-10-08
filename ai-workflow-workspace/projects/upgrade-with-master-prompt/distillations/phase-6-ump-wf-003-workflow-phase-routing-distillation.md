# Phase 6 Distillation: UMP-WF-003-workflow-phase-routing

## Co Zostalo Zrobione

- Added prompt composition references to `AGENTS.md`, `.systems/ai/core/workflow.md`, and `.systems/ai/core/command-routing.md`.
- Added command routing for master prompts, prompt modules, role profiles, generated variables, workflow-phase roles, and project-domain roles.
- Clarified that project-local prompting artifacts are read only after canonical policy and phase files.
- Preserved phase-file authority over pass criteria, fail criteria, evidence, writes allowed, and stop conditions.

## Problemy

- Routing is visible now, but project-local lifecycle and validator enforcement still depend on later tasks.
- Examples and human runbook guidance are still needed to make the model usable by operators.

## Decyzje

- Prompt composition routing belongs in the existing command router and workflow router, not in new phases.
- Workflow-phase roles are review stance, not gate logic.
- Project-domain roles cannot approve implementation or expand accepted scope.

## Zasady Na Przyszlosc

- Add discoverability through existing routers before introducing new workflow surfaces.
- Any role or variable route must explicitly preserve source-of-truth order and phase gates.
- Do not add lock files or status fields for prompting behavior without a separate approved architecture change.

## Status Repo Memory

memory-in-repo-memory: true

## Evidence

- Quality artifact: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-wf-003-workflow-phase-routing-quality.md`.
- Implementation result: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-4-ump-wf-003-workflow-phase-routing-implementation-result.md`.
