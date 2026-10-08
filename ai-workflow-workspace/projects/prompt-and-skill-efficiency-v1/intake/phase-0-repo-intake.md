# Phase 0 Project Repo Intake: Prompt And Skill Efficiency V1

## Repository Identity

- Mode: official upstream AI Workflow repository, not a target nested clone.
- Repository path: `/Users/jakubplociennik/ai-system/onlinen-workspace/projects/ai-workflow`.
- Branch and HEAD observed: `main`, `7a904f736eaf029bea750c3a735cd53fa61ef4c0`.
- Upstream tracking: `origin/main` at the same commit; tracked worktree clean at intake.
- Runtime project: `ai-workflow-workspace/projects/prompt-and-skill-efficiency-v1/`, ignored and untracked.

## Sources And Scope

- Repo-level intake and status, owner priority matrix, accepted project context, `AGENTS.md`, skill contracts, validation profiles, risk model, permissions, and autopilot contract.
- Existing `context/` source materials: none. No unreadable project sources.
- Tracked source areas expected later: `AGENTS.md`, relevant `.systems/ai/core/`, active skills, validators, templates, and human guidance only when justified by baseline.
- AI System repository, target repositories, personal Codex configuration, and actual client projects are out of scope.

## Command Map And Safe Environment

| Purpose | Command or mode | Status |
| --- | --- | --- |
| Read-only facts | `git status --short --branch`, `git rev-parse`, `rg`, `sed`, `wc` | usable |
| Skill layout | `.systems/scripts/check-system-skills` | usable, supporting evidence |
| Fast workflow checks | `.systems/scripts/validate-workflow --profile scoped --checks <explicit-check>` | usable during iteration |
| Final workflow checks | `.systems/scripts/validate-workflow --profile full --explain` | required after semantic QA for high-impact contract changes |
| Eval scaffold | `skill-creator/scripts/run_eval.py` | local scaffold only; does not execute model runs |
| Controlled model runs | isolated GPT-6 Sol High subagents on disposable, anonymized fixtures | pending explicit authorization |

No application build, database, migration, production test, or external API call is required. Behavioral eval fixtures must be disposable, local-only, and contain no real client facts or secrets. A static document audit is not behavioral evidence.

## Restricted Zones And Stop Conditions

- No tracked source writes before a completed and reviewed behavioral baseline.
- No external model CLI, subagent, browser, network, production, secrets, or destructive operations without the applicable approval.
- No silent weakening of source-of-truth order, permissions, DoD, QA, privacy, approvals, or phase gates.
- Formal autopilot must have a run-scoped readiness artifact and only one declared range per run; planning-range stops before implementation-range.
- Any material model/settings drift invalidates the paired comparison until rerun.
- Owner opt-out of deadline and timebox applies only to this scope and does not waive quality or approval gates.

## Readiness Result

Project/context intake: completed for planning and static baseline design. Controlled behavioral baseline: awaiting-owner decision on eval execution method. Autopilot: not ready and not running. Next route: prepare the stage 0 eval specification and queue the decision; do not alter tracked contracts.

## Owner Decision Checkpoint

- Interaction mode: queued
- Decision state: awaiting-owner
- Material decisions: PE-001 controlled behavioral eval method
- Questions asked: PE-001
- Auto-resolved reversible decisions: none
- Optional owner refinements: none
- Decision artifacts: `intake/phase-0-idea-validation.md`
- Next route: static eval design; model runs after PE-001.

## Optional Knowledge Capture

- Capture recommended: no
- Target: none
- Reason: no validated reusable lesson yet.
- Owner decision required: no
- Owner decision: not-requested
- Privacy/scope check: pass
- Suggested entry title: none
- Suggested entry summary: none
