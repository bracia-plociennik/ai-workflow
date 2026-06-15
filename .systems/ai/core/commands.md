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
```

`check-knowledge-capture-gate` validates the phase-level `Optional Knowledge Capture` blocks and keeps them advisory rather than mandatory durable memory writes.

Before creating a commit, also apply `.systems/ai/core/contract-compliance.md` and report the advisory work mode compliance plus knowledge capture decision. If capture is required, run the appropriate phase/artifact path before committing.

## Skipped Checks

Skipped checks must include:

- command name;
- reason skipped;
- whether the skip affects `PASS`;
- fallback evidence, if any.
