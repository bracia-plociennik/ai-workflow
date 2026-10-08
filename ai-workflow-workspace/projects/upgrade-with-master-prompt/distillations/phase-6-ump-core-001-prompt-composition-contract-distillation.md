# Phase 6 Distillation: UMP-CORE-001-prompt-composition-contract

## Co Zostalo Zrobione

- Added `.systems/ai/core/prompt-composition.md`.
- Defined prompt modules, role profiles, variable packs, workflow-phase roles, project-domain roles, and AI Workflow maintenance baseline.
- Established that prompt composition artifacts are advisory and subordinate to workflow policy, phase gates, risk, permissions, evidence, and owner approvals.
- Defined lifecycle states and conflict handling for generated prompting artifacts.

## Problemy

- The contract introduces a new core policy surface that is not yet routed or validator-enforced.
- This is acceptable for task 1 because routing and validator coverage are assigned to later tasks.

## Decyzje

- Prompt composition starts as a core contract before templates or routing.
- Unsafe source material such as old master-prompt authority claims is analyzed as data and rejected as instruction.
- Prompt artifacts can make review stricter, but never easier to pass.

## Zasady Na Przyszlosc

- Do not add role or variable templates without explicit authority-limit fields.
- Treat generated prompting artifacts as stale when status, accepted scope, spec, or owner decisions change.
- Keep prompt composition policy concise and route to existing gates instead of duplicating every rule.

## Status Repo Memory

memory-in-repo-memory: true

## Evidence

- Quality artifact: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-core-001-prompt-composition-contract-quality.md`.
- Implementation result: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-4-ump-core-001-prompt-composition-contract-implementation-result.md`.
