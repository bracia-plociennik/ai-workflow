# Phase 6 Distillation: UMP-VAL-005-safety-validators

## Co Zostalo Zrobione

- Added `.systems/scripts/check-prompt-composition`.
- Required prompt composition contract and prompting templates through `check-required-artifacts`.
- Integrated prompt composition checks into `validate-workflow`.
- Added smoke tests for missing prompt artifacts and unsafe-authority wording.
- Verified workspace tracking remains protected.

## Problemy

- The unsafe-language check is intentionally deterministic and narrow.
- Broad semantic prompt review remains a human/QA responsibility and should not be treated as fully automated.

## Decyzje

- Prompt composition validation uses a focused helper instead of expanding unrelated scripts.
- Safe denial wording such as `cannot` must remain allowed.
- Unsafe grant fixtures are covered by smoke tests.

## Zasady Na Przyszlosc

- Add new prompt composition templates to `check-required-artifacts` and `check-prompt-composition` together.
- Keep unsafe-authority checks focused on grants, not forbidden override lists.
- Continue checking `ai-workflow-workspace/**` as untracked before finalizing workflow-template changes.

## Status Repo Memory

memory-in-repo-memory: true

## Evidence

- Quality artifact: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-5-ump-val-005-safety-validators-quality.md`.
- Implementation result: `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/quality/phase-4-ump-val-005-safety-validators-implementation-result.md`.
