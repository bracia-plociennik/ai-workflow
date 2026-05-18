# AUTOPILOT.md

## Purpose

This file is the repo-level launch checklist for Codex Autopilot.
It does not replace `AGENTS.md`, `docs/ai/WORKFLOW.md`, `docs/ai/workflow/`, `docs/repo/STATUS.md`, or project-local `STATUS.md`.

Use it to verify that the AI docs and active project workspace are ready before starting supervised, semi-autonomous, or autonomous execution.

## Owner-Approved Default Contract

When the owner approves autopilot without a narrower mode, the default mode is `autonomous_execution`.

Default autopilot rules:

- execute tasks sequentially unless Task Packaging explicitly approves a package or parallel execution;
- continue only after evidence-backed `PASS`;
- STOP on critical-risk, retry limit, blocking drift, or missing required test/QA evidence;
- auto-resolvable decisions may be chosen automatically after recording the recommendation and chosen option;
- high-impact and critical-risk decisions require the owner protocol;
- retry budget is 2 spec/quality fix loops per task or phase and 32 total retries per autopilot run;
- checkpoint cadence is after every 3 completed tasks and after the final task;
- final check ends in `AWAITING_OWNER_FINAL_YES` until the owner explicitly approves closure;
- real emails, alerts, tickets, external API writes, production cron, production credentials, and paid-vendor live calls are disabled by default;
- use fake/log/array/test adapters unless a later owner decision explicitly enables real side effects.

Git policy for autopilot:

- use an isolated autopilot branch, for example `codex/<project>-autopilot`;
- commit only after `QUALITY PASS` for the completed task;
- push and PR only under later explicit approval or policy.

## Required Global Inputs

Autopilot can run only when these repo-level inputs exist:

| Required Input | Path | Status Check |
| --- | --- | --- |
| Execution contract | `AGENTS.md` | Must define workflow gates, stop conditions, quality rules, and artifact locations. |
| Main workflow guide | `docs/ai/WORKFLOW.md` | Must route every phase to a detailed phase file. |
| Detailed workflow rules | `docs/ai/workflow/` | Must contain phase files for 000, 0, 1, 1.5, 1.7, 2, 2.5, 2.6, 2.7, 2.9, 2.9.1, 3, 3.5, 3.7, 4, 5, 5.5, 6, 7, 8. |
| Repo context | `docs/repo/CONTEXT.md` | Must describe the target repository globally before project work starts. |
| Repo intake | `docs/repo/REPO-INTAKE.md` | Must exist as the repo-level workflow/bootstrap readiness artifact. |
| Repo status | `docs/repo/STATUS.md` | Must identify current repo-level workflow state. |
| External memory | `docs/ai/EXTERNAL-MEMORY.md` | Must exist as universal workflow/process memory, not repo-specific source of truth. |
| Repo memory | `docs/repo/MEMORY.md` | Must exist as aggregate memory, not source of truth. |
| Templates | `docs/ai/templates/` | Must include AI runtime, workflow, autopilot, project, and human templates. |

## Required Active Project Inputs

Before autopilot starts for `docs/projects/<project>/`, the project workspace must have:

| Required Input | Typical Path |
| --- | --- |
| Project README | `docs/projects/<project>/README.md` |
| Project status | `docs/projects/<project>/STATUS.md` |
| Project memory | `docs/projects/<project>/PROJECT-MEMORY.md` |
| Intake artifacts | `docs/projects/<project>/intake/` |
| Idea validation when needed | `docs/projects/<project>/intake/000_idea_validation.md` |
| Architecture artifact and QA PASS evidence | `docs/projects/<project>/architecture/`, `docs/projects/<project>/quality/` |
| Project plan and Plan QA PASS evidence | `docs/projects/<project>/planning/`, `docs/projects/<project>/quality/` |
| Task packaging result or explicit no-package decision | `docs/projects/<project>/planning/` or `docs/projects/<project>/quality/` |
| Ready task/package specification | `docs/projects/<project>/specs/` |
| Decisions directory | `docs/projects/<project>/decisions/` |
| Escalations directory | `docs/projects/<project>/escalations/` |
| Distillations directory | `docs/projects/<project>/distillations/` |
| Checkpoints directory | `docs/projects/<project>/checkpoints/` |
| Autopilot runtime directory | `docs/projects/<project>/autopilot/` |

## Runtime Files

Create these when autopilot is active or when an owner-approved autopilot preflight is preparing a ready-to-start run, using `docs/ai/templates/autopilot/`:

- `docs/projects/<project>/autopilot/AUTOPILOT_STATE.md`
- `docs/projects/<project>/autopilot/AUTOPILOT_LEDGER.md`
- `docs/projects/<project>/autopilot/AUTOPILOT_EVENTS.md`

Do not create fake runtime files for inactive or speculative autopilot runs.

## Autopilot Start Checklist

1. Read `AGENTS.md`.
2. Read `docs/ai/WORKFLOW.md`.
3. Read the detailed phase file for the intended start phase under `docs/ai/workflow/`.
4. Read `docs/repo/REPO-INTAKE.md`.
5. Read `docs/repo/STATUS.md`.
6. Read `docs/repo/CONTEXT.md`.
7. Read `docs/ai/EXTERNAL-MEMORY.md` only for universal workflow guidance; do not let it override active repo/project contracts.
8. Read `docs/projects/<project>/STATUS.md`.
9. Confirm the project plan has required predecessor gates satisfied.
10. Confirm the next task/package has a ready specification or a documented dependency gate.
11. Confirm no unresolved high-impact or critical-risk owner decision blocks execution.
12. Check `git status` and identify overlapping write-set risks.
13. If autopilot starts, create or refresh runtime files under `docs/projects/<project>/autopilot/` from templates.
14. Append the first ledger entry before entering the first execution phase.

## Stop Conditions

Autopilot must stop and write an escalation artifact under `docs/projects/<project>/escalations/` when any of these occurs:

- required gate is unsatisfied;
- dependency or readiness state is inconsistent;
- repo state, plan, spec, status, ledger, or autopilot state conflict;
- critical-risk action would be required;
- retry limit is reached;
- budget is exceeded;
- owner decision is required and not auto-resolvable;
- quality evidence cannot support PASS.

## Current Global Readiness

As of this template setup, `docs/ai` contains the required global materials for running autopilot. Actual readiness still depends on `docs/repo/`, the active project workspace, and current `STATUS.md` values.
