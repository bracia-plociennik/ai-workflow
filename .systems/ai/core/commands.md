# commands.md

## Purpose

Codex must know how to verify work. Repository-specific commands live in `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`. This file defines the required command categories and workflow-template checks.

## Required Command Categories

Each target repository should define these in `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`:

- Install
- Development server
- Lint/style
- Typecheck/static analysis
- Unit tests
- Integration tests
- E2E/browser tests
- Build
- Migration/schema check
- Scheduler/cron/queue check

If a command is not configured, write `not configured`. Do not invent commands.

## Before Final Answer

For implementation work, run the relevant configured checks for the changed area.

For workflow-template maintenance, run:

```sh
git diff --check
.systems/scripts/validate-workflow
.systems/scripts/check-naming
.systems/scripts/check-required-artifacts
.systems/scripts/check-status-consistency
.systems/scripts/check-qa-evidence
.systems/scripts/check-system-insights
.systems/scripts/check-system-skills
.systems/scripts/check-contract-compliance
.systems/scripts/check-knowledge-capture-gate
.systems/scripts/check-default-quality-phase-chaining
.systems/scripts/check-dreaming-mode
.systems/scripts/check-global-quality-review-stance
.systems/scripts/check-intent-plan-spec-compliance-review
.systems/scripts/check-implementation-slicing
.systems/scripts/check-request-batch-triage
.systems/scripts/check-response-evidence-trace
.systems/scripts/check-phase-skill-discovery
.systems/scripts/check-default-quality-closure
.systems/scripts/check-default-idea-validation-opt-out
.systems/scripts/check-end-of-task-capture
```

`check-knowledge-capture-gate` validates the phase-level `Optional Knowledge Capture` blocks and keeps them advisory rather than mandatory durable memory writes.

`check-default-quality-phase-chaining` validates default working-phase to QA/Quality chaining, owner opt-out wording, and owner-requested task packaging boundaries.

`check-dreaming-mode` validates the advisory-only Dreaming Mode contract, report templates, workspace bootstrap namespace, privacy boundaries, and the split between `workflow-artifacts-only` and `full-repo` reports.

`check-global-quality-review-stance` validates the read-only/advisory review stance, review/findings/blockers routing, formal `phase-5-quality` separation, and final-review/final-check boundary.

`check-intent-plan-spec-compliance-review` validates the shared review/quality lens that compares implementation against owner instruction, accepted plan, accepted spec, scope, and acceptance criteria, and blocks technical-only PASS/review wording.

`check-implementation-slicing` validates the Implementation Slice Plan contract, DoD source, mandatory quality closure, PASS Integrity Gate, phase-4/template integration, side-task/micro-task/micro-project routing, and the boundary that slicing cannot bypass spec, scope, risk, permissions, approvals, or QA.

`check-request-batch-triage` validates owner request batch triage, triage matrix fields, mixed-list routing, high-risk routing, and the boundary that triage cannot automatically implement, commit, or create workflow artifacts.

`check-response-evidence-trace` validates the required `Execution Trace` for substantive responses and preserves `Co dalej?` as the final footer.

`check-phase-skill-discovery` validates phase/procedure skill discovery, workspace-before-system skill precedence, `Skills used: none` fallback, and skill authority boundaries.

`check-default-quality-closure` validates default quality/review closure for substantive work, owner opt-out grammar, and the rule that opt-out cannot satisfy required QA PASS.

`check-default-idea-validation-opt-out` validates Default Idea Validation for single new work, broad project ideas, and batch validation routes, plus owner opt-out grammar and the boundary that opt-out cannot bypass safety gates.

`check-end-of-task-capture` validates chat-end knowledge capture routing, conflict-free precedence against formal phase/review/final commands, required output fields, and safety boundaries for memory, System Insights, External Memory, status, and final approval.

Before creating a commit, also apply `.systems/ai/core/contract-compliance.md` and report the advisory work mode compliance plus knowledge capture decision. If capture is required, run the appropriate phase/artifact path before committing.

## Skipped Checks

Skipped checks must include:

- command name;
- reason skipped;
- whether the skip affects `PASS`;
- fallback evidence, if any.
