# Phase 6 Distillation: UMP-DOCS-006-human-guidance-examples

## Co Zostalo Zrobione

- Added owner-facing prompt composition guidance to `HUMANS.md`.
- Added documentation-only examples for workflow-phase roles, project-domain roles, variable packs, and AI Workflow maintenance baseline.
- Updated version to `0.8.8` and added a changelog entry.
- Required the examples through `check-required-artifacts`.
- Extended `check-prompt-composition` to scan prompting examples.

## Problemy

- The examples are intentionally small and do not form a full role catalog.
- Final consistency still needs phase 7 checkpoint before phase 8.

## Decyzje

- Human guidance stays practical and short instead of duplicating `AGENTS.md`.
- Examples are documentation-only and do not create active project state.
- Prompt examples are included in deterministic validator scope.

## Zasady Na Przyszlosc

- Keep examples labeled as examples.
- Add new example files to required artifacts when they become part of the contract.
- Avoid platform-specific settings as system policy unless a future architecture explicitly maps them.

## Status Repo Memory

memory-in-repo-memory: true

## Evidence

- Quality artifact: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-docs-006-human-guidance-examples-quality.md`.
- Implementation result: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-4-ump-docs-006-human-guidance-examples-implementation-result.md`.
