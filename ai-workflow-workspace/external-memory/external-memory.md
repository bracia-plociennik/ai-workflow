# External Memory Router

## Purpose

`ai-workflow-workspace/external-memory/external-memory.md` is the router and index for portable External Memory.

Detailed entries live in `ai-workflow-workspace/external-memory/memory/`.

Use this router only for date, topic, type, status, and route to the detailed memory entry. Do not store long memory content in this file.

External Memory is advisory. It does not override `AGENTS.md`, workflow docs, phase gates, risk model, permissions, Definition of Done, required evidence, or final owner approval.

In target repositories, this is the place to record proposed AI Workflow improvements. Do not edit `.systems/**` directly from target work.

## Memory Index

| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| 2026-10-08 | Execution modes for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-10-08-execution-modes-ai-system-handoff.md` |
| 2026-10-05 | Fixed runtime dependency scope for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-10-05-runtime-dependency-scope-ai-system-handoff.md` |
| 2026-10-04 | Parallel task orchestration protocol for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-10-04-parallel-task-orchestration-ai-system-handoff.md` |
| 2026-05-17 | Repo-level intake before project workspace | rule | implemented | `ai-workflow-workspace/external-memory/memory/2026-05-17-repo-level-intake-before-project-workspace.md` |
| 2026-05-17 | Universal workflow memory separate from repo memory | rule | implemented | `ai-workflow-workspace/external-memory/memory/2026-05-17-universal-workflow-memory-separate-from-repo-memory.md` |
| 2026-06-10 | Separate repo state from stale context | recommendation | proposed | `ai-workflow-workspace/external-memory/memory/2026-06-10-separate-repo-state-from-stale-context.md` |
| 2026-07-24 | Workflow operator efficiency and AI System parity | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-07-24-workflow-operator-efficiency-ai-system-handoff.md` |
| 2026-09-25 | Conditional instruction router for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-09-25-conditional-instruction-router-ai-system-handoff.md` |
| 2026-09-28 | Bounded local recovery for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-09-28-bounded-local-recovery-ai-system-handoff.md` |
| 2026-09-29 | Skill discovery and eval freshness for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-09-29-skill-discovery-eval-freshness-ai-system-handoff.md` |
| 2026-09-29 | Lean validation verdict integrity and source-bound timing for AI System | handoff | accepted-for-handoff | `ai-workflow-workspace/external-memory/memory/2026-09-29-lean-validation-ai-system-handoff.md` |

## Rules

- Keep this file short. It is an index, not the memory body.
- Store detailed external memory entries in `ai-workflow-workspace/external-memory/memory/`.
- Do not store repo-specific facts, project-specific facts, secrets, client data, or product-domain details here.
- Promote accepted entries into `AGENTS.md`, `HUMANS.md`, workflow docs, templates, or skills before treating them as enforceable rules.
- Before sharing entries externally, run a privacy check.
