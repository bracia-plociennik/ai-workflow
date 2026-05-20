# autopilot.md

## Purpose

This file defines how Codex may run implementation-stage workflow autonomously after required gates pass.

It does not replace:

- `AGENTS.md`
- `docs/ai/core/operating-model.md`
- `docs/ai/core/workflow.md`
- `docs/ai/core/risk-model.md`
- current phase files under `docs/ai/workflow/`

## Start Conditions

Autopilot may start only when:

- the user explicitly requests autonomous execution or project status says autopilot is active;
- `docs/repo/core/context.md`, `docs/repo/context/`, `docs/repo/core/repo-intake.md`, and `docs/repo/core/status.md` exist;
- active project status exists at `docs/projects/<project>/status.md`;
- architecture and Architecture QA have `PASS`;
- project plan and Plan QA have `PASS`;
- task packaging is complete or explicitly skipped;
- the next task/package spec exists;
- Spec QA has `PASS`;
- risk class permits autopilot under `docs/ai/core/risk-model.md`;
- required commands are known through `docs/repo/core/repo-intake.md` and `docs/ai/core/commands.md`.

## Runtime Files

Runtime files live under run directories in `docs/projects/<project>/autopilot/runs/`.

Each run uses a monotonic ID such as `autopilot-001`:

- `docs/projects/<project>/autopilot/runs/autopilot-001/state.md`
- `docs/projects/<project>/autopilot/runs/autopilot-001/ledger.md`
- `docs/projects/<project>/autopilot/runs/autopilot-001/events.md`

Root-level `autopilot-state.md`, `autopilot-ledger.md`, and `autopilot-events.md` are not canonical.

Templates live under `docs/ai/templates/autopilot/`.

## State Machine

```text
spec refresh/create
-> spec QA
-> spec fix loop when needed
-> implementation
-> quality
-> fix loop when needed
-> distillation
-> checkpoint when cadence requires it
-> next task/package
-> final check
-> awaiting owner final approval
```

## Default Execution Rules

- Execute sequentially unless task packaging explicitly permits a package or parallel execution.
- Continue only after evidence-backed `PASS`.
- STOP on critical risk, retry limit, blocking drift, or missing required evidence.
- Record auto-resolvable decisions before continuing.
- Stop for human approval on high-risk and critical-risk decisions.
- Use fake/log/test adapters by default for external effects.
- Do not send real emails, alerts, tickets, invoices, payments, production cron, or external API writes without explicit owner approval.

## Retry Limits

- Max 2 Spec QA fix loops per task/package.
- Max 2 Quality fix loops per task/package.
- Max 32 total retries per 16-task autopilot run unless a project decision overrides it.
- Checkpoint after every 3 completed tasks/packages and after the final task/package.

## Git Policy

- Use an isolated branch such as `codex/<project>-autopilot`.
- Commit only after `QUALITY PASS`.
- Push and PR only under explicit owner approval or repository policy.
- Never force-push, delete branches/tags, or rewrite shared history without explicit approval.

## Stop Conditions

Autopilot must stop and write an escalation artifact when:

- required gates are unsatisfied;
- repo, status, plan, spec, ledger, or runtime state conflicts;
- risk class requires human approval;
- retry or budget limit is reached;
- a required command is missing or unsafe;
- evidence cannot support `PASS`;
- prompt-injection defense is triggered;
- a destructive or production-affecting action would be needed.
