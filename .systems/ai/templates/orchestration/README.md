# Orchestration Templates

Canonical contract: `../../core/parallel-task-orchestration.md`.

- `run.template.json`: one coordinator-owned protocol manifest, existing task/slice units, capacity/resources/checkpoint slots and optional lifecycle.
- `unit.template.json`: existing parent task subset with testable DoD and exact scopes; optional execution contract required at dispatch.
- `result.template.json`: private scoped submitted result, not accepted output or formal task PASS. Durable ledger admits only sanitized referenced records.
- `worker-prompt.template.md`: minimum frozen context and stop rules; prompts are not write enforcement.
- `integration-review.template.md`: actual destination/provenance/diff/DoD/findings evidence for serial integration; flags do not replace review.

Templates are incomplete examples, not executable inputs or approvals. Replace
all example identities/digests/paths using current owning evidence. The helper
does not initialize workers, create/clean worktrees, transport, copy, merge or
provide a sandbox. Validate actual approved manifest before any transition.
Source schemas are version1. Coordinator schema1 remains default; explicit
schema2 installed capability is separate from native support and owner permission.
Native verification is deferred/unverified; missing isolation/capacity means
ordinary serial fallback, no unverified native dispatch. A genuine future backend
requires its own approved isolation/capacity preflight and integrated task QA.
