# Phase 6 Distillation: UMP-PROJ-004-project-local-generation

## Co Zostalo Zrobione

- Defined the project-local prompting namespace under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/prompting/`.
- Added lifecycle rules for generating, refreshing, using, ignoring, superseding, or rejecting project-local prompt artifacts.
- Defined ask/infer rules for variable packs and required source/confidence/assumption metadata.
- Added a project prompting router template for `prompting/README.md`.

## Problemy

- Lifecycle remains policy/docs only until validator coverage is added.
- Concrete examples are still needed so owners can see safe role and variable usage.

## Decyzje

- Project-local prompting artifacts live in the project workspace and never under `.systems/**`.
- Owner input is required when variables affect scope, risk, acceptance criteria, permissions, external effects, high-risk decisions, or final acceptance.
- Hidden prompt context is not valid workflow evidence; material use must list artifact paths.

## Zasady Na Przyszlosc

- Treat stale project-local prompting artifacts as unusable until refreshed.
- Serialize writes to a project prompting router just like status and memory routers.
- Validator coverage should require the project prompting router template and check core/router references.

## Status Repo Memory

memory-in-repo-memory: true

## Evidence

- Quality artifact: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-proj-004-project-local-generation-quality.md`.
- Implementation result: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-4-ump-proj-004-project-local-generation-implementation-result.md`.
