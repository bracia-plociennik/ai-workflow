# Micro-Project: ai-workflow-system-health-v1

## Summary

Workflow-maintenance program implementing four independently reviewable system
health ranges: workspace freshness/topology, Dream Report integrity/lifecycle,
validation observability/smoke partition, and optional skill behavioral evals.

## Metadata

| Field | Value |
| --- | --- |
| Risk | `high` |
| Timebox | `3 business days from implementation start` |
| Timezone | `Europe/Warsaw` |
| Work mode | `workflow-maintenance` |
| Source reports | `2026-07-15-ai-workflow-system-validation`, `2026-08-08-ai-workflow-full-system-validation` |
| Cross-system impact | `yes; one privacy-safe External Memory handoff after final QA` |
| Commit/push | `not authorized by this implementation request` |

## Definition Of Done

- Current ignored repo status/intake facts match `main`, HEAD, origin, path, and observed date.
- Freshness and topology reports are useful and advisory-only.
- Dream schema v2 rejects unresolved placeholders, blank required recommendation fields, duplicate IDs, invalid lifecycle values, and resolved lifecycle states without decision evidence; historical v1 reports remain immutable and valid.
- Timing output records validator and smoke-group metadata; three full baseline runs precede any default smoke-suite split.
- Smoke `--group all` preserves the existing complete coverage and equivalence fallback.
- Optional skill behavioral evals use a shared contract; absent evals remain valid and runtime output stays outside active skill directories.
- Semantic findings-first review precedes scripts; scripts remain supporting-only.
- No unresolved P0/P1/material P2 findings after full current-diff review.
- Full validation passes and `git ls-files ai-workflow-workspace` remains empty.

## Implementation Slice Plan

| slice id | goal | expected files/areas | acceptance check | evidence required | status |
| --- | --- | --- | --- | --- | --- |
| SYSHEALTH-001 | Freshness and topology reporting | core contracts, report scripts, advisory validators, repo runtime | current/stale/unknown and linked/partial/orphaned outputs are report-only | script help, generated reports, targeted validators | completed |
| SYSHEALTH-002 | Dream Report v2 lifecycle/content integrity | Dreaming contract, template, checker | v1 legacy reports pass; v2 placeholders/blank/duplicate/invalid lifecycle cases fail | targeted Dream validator and synthetic fixtures | completed |
| SYSHEALTH-003 | Validation observability and smoke groups | validate-workflow, smoke runner, observability contract | timing output works; `--group all` remains complete; no coverage reduction | three successful baseline runs; equivalence fallback retained | completed |
| SYSHEALTH-004 | Optional skill behavioral evaluation contract | skill contract, validator, skill inventory | valid optional eval passes; malformed/unsafe eval fails; absent eval passes | validator and frontend eval evidence | completed |

Stop rule: stop and route to owner decision if scope creep, missing decision,
dependency conflict, unsafe action, incomplete smoke equivalence, or source
conflict is discovered. Do not weaken existing gates to fit the timebox.

## Slice Execution Evidence

- SYSHEALTH-001: completed; advisory reports generated and dirty-state behavior verified.
- SYSHEALTH-002: completed; legacy v1 reports remained unchanged and v2 synthetic valid/invalid cases passed.
- SYSHEALTH-003: completed; three baseline runs passed, timing was recorded, and no unsafely audited split was shipped.
- SYSHEALTH-004: completed; optional eval contract and inventory added; existing frontend eval passed; no mandatory backfill.

## Quality Closure

- Artifact QA route: `global-quality-review-stance` (advisory)
- Implementation quality route: `phase-5-quality` contract applied as the review lens; this repo-level implementation reports advisory closure until a formal phase artifact is authorized.
- Findings-first review: `completed; no unresolved P0/P1/material P2 identified in current implementation review`
- Review Completeness Gate: `completed; producer-consumer and policy-boundary checks reviewed`
- Producer-consumer audit: `required for Dream v2 and timing output`
- Policy-boundary adversarial matrix: `required for validators`
- Closure freshness: `fresh after final validator and smoke edits; full current-diff review completed`
- Residual risk: smoke-suite group equivalence is not yet proven and may require retaining the monolith.

## Cross-System Handoff

- Owner decision: `yes`
- Counterpart: `ai-system`
- Handoff artifact: `ai-workflow-workspace/external-memory/memory/2026-08-10-ai-workflow-system-health-ai-system-handoff.md`

## Knowledge Capture Decision

- Target: `external-memory`
- Decision: `defer-to-checkpoint`
- Reason: this scope contains reusable AI Workflow improvements for later parity work in ai-system; one privacy-safe handoff is required after final QA.
- Privacy/scope check: `pass`

## Execution Trace

- Sources used: both Dream Reports, current AGENTS/core contracts, validators, templates, CI workflow, active skills, and ignored repo runtime.
- Evidence reviewed: clean `main` at `18b0fb2`, synchronized `origin/main`, empty tracked workspace, stale status/intake before refresh, existing frontend eval flow, and monolithic smoke runner.
- Workflow procedures used: instruction refresh, batch triage, Task Idea Validation, Owner Decision Discovery, Implementation Slice Plan, Plan Quality Contract.
- Skills/roles used: `skill-creator` supporting guidance for optional behavioral eval design.
- Commands/checks run: `git status`, `git log`, `git rev-parse`, `git remote`, `rg`, `sed`, `find`, targeted validators, three smoke baselines, and `.systems/scripts/validate-workflow --profile full --explain`.
- Skipped/unreadable sources: no relevant source skipped; no product repository in scope.
- Instruction refresh: `performed-full`; baseline `main/18b0fb2`, current worktree changes are the accepted implementation scope.
- Model recommendation: `GPT-5.6 Sol High`; high-impact validator/CI/cross-contract work; blocking: `no`.
