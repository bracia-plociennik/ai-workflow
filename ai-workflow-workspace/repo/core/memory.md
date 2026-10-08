# Repo Memory Router

## Purpose

`ai-workflow-workspace/repo/core/memory.md` is the router and index for target-repository memory.

Detailed repo-local entries live in `ai-workflow-workspace/repo/memory/`.

Use this router only for date, topic, type, status, and route to the detailed memory entry. Do not store long memory content in this file.

It is not a source of truth. Repository state, `AGENTS.md`, approved artifacts, `ai-workflow-workspace/repo/core/status.md`, and project artifacts remain authoritative.

## Memory Index

| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| 2026-10-04 | Parallel protocol boundaries | repo-constraint | active | ai-workflow-workspace/repo/memory/2026-10-04-parallel-protocol-boundaries.md |
| 2026-10-04 | Capture parity and QA commit binding | command-note | active | ai-workflow-workspace/repo/memory/2026-10-04-capture-parity-phase-commits.md |
| 2026-10-04 | Parallel compatibility inspection | command-note | active | ai-workflow-workspace/repo/memory/2026-10-04-parallel-compatibility-inspection.md |
| 2026-10-01 | Runtime integrity commands | command-note | active | `ai-workflow-workspace/repo/memory/2026-10-01-runtime-integrity-commands.md` |
| 2026-10-01 | Lean validation integration | testing-note | active | `ai-workflow-workspace/repo/memory/2026-10-01-lean-validation-integration.md` |
| 2026-09-30 | Lean validation verdict, timing and scope | testing-note | active | `ai-workflow-workspace/repo/memory/2026-09-30-lean-validation-verdict-timing-scope.md` |
| 2026-06-10 | Main-only local workspace cleanup | repo-constraint | active | `ai-workflow-workspace/repo/memory/2026-06-10-main-only-local-workspace-cleanup.md` |
| 2026-06-11 | Prompt composition release 0.8.8 | repo-fact | active | `ai-workflow-workspace/repo/memory/2026-06-11-prompt-composition-release-0-8-8.md` |
| 2026-06-15 | AI Workflow development baseline after skill context intake | repo-fact | active | `ai-workflow-workspace/repo/memory/2026-06-15-ai-workflow-development-baseline.md` |
| 2026-06-23 | Intent compliance quality checks | repo-fact | active | `ai-workflow-workspace/repo/memory/2026-06-23-intent-compliance-quality-checks.md` |

Populate this index only through checkpoint/final-check updates after the workflow has produced evidence-backed repo-level knowledge.

Universal workflow/process lessons belong in `ai-workflow-workspace/external-memory/memory/` and are indexed by `ai-workflow-workspace/external-memory/external-memory.md`.
Template maintenance memory belongs in `.systems/ai/memory/` and is indexed by `.systems/ai/core/memory.md`.

## Rules

- Keep this file short. It is an index, not the memory body.
- Store detailed repo-local facts in `ai-workflow-workspace/repo/memory/`.
- Do not store secrets, credentials, private client data, or production-only operational details here.
- Do not treat this file as a substitute for reading the repository.
- Do not copy project-specific memory from another repository into this file.
- Use project-local memory in `ai-workflow-workspace/projects/<project>/memory/` for active project knowledge before syncing stable findings here.
