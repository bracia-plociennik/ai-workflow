# runtime-integrity.md

## Purpose

Canonical runtime and evidence rules supporting selective workflow overhead. These rules never grant writes, approvals or formal PASS.

## Capture Inventory

Use `check-distillation-state` for canonical repo/project inventory and contract checks; project-specific runtime checks remain explicit. `lib/capture-state.py` separates the capture-state namespace from owning evidence. Missing current QA stays unknown, historical records remain immutable, and accepted distillation identity and unique path are required for completed records. No scoped schema-v1 manifest population is broadened.

## Smoke Fixture Isolation

All five smoke groups use `lib/smoke-fixture.py` to copy only selected tracked product paths from the current worktree: .systems, .github, AGENTS.md, HUMANS.md, README.md and .gitignore. Raw skill context is excluded; tracked preserved legacy skill artifacts are included only as fixture data needed by their validators. Private ignored runtime and unrelated untracked content are not copied. New untracked product inputs require exact `--extra` or `AI_WORKFLOW_SMOKE_EXTRA_FILES` paths under .systems/.github. Keys, symlinks, traversal and non-regular files are rejected. Current deletions are not resurrected from HEAD. Output must be an empty, non-overlapping fixture.

## Read Evidence

`lib/command-read-evidence.py` consumes JSONL command events without executing their text. It distinguishes confirmed, attempted, not-executed and unknown. Only completed successful simple literal reader commands count as confirmed. Aggregate compound, pipeline, conditional, loop or expansion traces remain unknown. A literal false short-circuit is not-executed. Separate successful events survive later failure. Historical evals/scorers are not rewritten and model behavior claims require a separate fresh evaluation.

## Micro-Exempt And Compact Output

`delivery-constraints.md` defines the only micro-exempt route; `lib/work-policy.py` mirrors eligibility for regression fixtures. At most three files, one local low-risk reversible change, no active formal scope or excluded boundary. No exemption from DoD, slice plan, owner approval, focused QA or failure disclosure. Growth reclassifies before further writes. `response-contract.md` defines compact/full communication independently from the full quality procedure.

## Coordinator Interface

Run `.systems/scripts/report-coordinator-status --project <slug> --format json|human`. Schema version 1 returns repository/project identity, workflow version, Git baseline, declared status, independently verified current QA, gate, blockers, evidence paths, capture inventory and freshness. execution_authorized is always false. It reuses qa-evidence.py, not a second PASS parser. Missing/ambiguous identity, unsupported version, stale/missing evidence, symlinks or changed baseline produce unknown/error and nonzero status. A verified FAIL is evidence, never execution readiness. No project state, approval, lock, scheduler or source file is written.

The worktree baseline binds tracked diff and untracked path inventory; the QA assessment binds selected artifact contents. It is not a hash of every ignored or unrelated file. No private content appears in JSON.
