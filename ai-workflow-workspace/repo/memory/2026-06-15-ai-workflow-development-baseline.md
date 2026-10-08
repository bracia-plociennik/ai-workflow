# AI Workflow Development Baseline

## Metadata

| Field | Value |
| --- | --- |
| Date | 2026-06-15 |
| Type | repo-fact |
| Status | active |
| Scope | official upstream `ai-workflow` repository |

## Current Git Baseline

- Local `main` is synchronized with `origin/main`.
- Current HEAD: `b3acb8e feat: add skill context intake contract`.
- Previous local baseline commits:
  - `5e1fb1f feat: add optional phase knowledge capture gate`
  - `9f3f738 feat: add system skill creator`

## Current Workflow Capabilities

- System skill layout v1 is active:
  - canonical skill contract: `SKILL.md`;
  - short human summary: `README.md`;
  - preserved imports: `.systems/ai/skills/legacy/**` as context/data only.
- `skill-creator` is adapted for AI Workflow:
  - supports `context/` as raw source input;
  - creates `skill-intake-plan.md` when scaffolding with `--resources context`;
  - validates active skill artifacts and blocks `context/**` from becoming active guidance or authority.
- Optional phase knowledge capture is active:
  - every workflow phase and phase template has `Optional Knowledge Capture`;
  - capture is soft and advisory, not a hard phase gate;
  - durable writes still require the proper phase/write permission or explicit owner-approved capture.
- Commit readiness / contract compliance gate is active:
  - agents should report work mode compliance and knowledge capture decision before commits or handoff;
  - the gate is advisory and does not override phase gates, risk policy, permissions, evidence, or approvals.
- System Insights policy exists in source docs, but this local workspace currently has no `ai-workflow-workspace/system-insights/` runtime directory.

## Recent Validation Baseline

The combined `optional-phase-knowledge-capture-gate` and `skill-context-intake` state passed:

- `git diff --check origin/main..HEAD`
- `git diff --check`
- `bash -n` for changed validators
- `.systems/scripts/check-knowledge-capture-gate`
- `.systems/scripts/validate-workflow`
- `.systems/scripts/check-required-artifacts`
- `.systems/scripts/check-system-skills`
- `.systems/scripts/check-validator-smoke-tests`
- `.systems/scripts/check-naming`
- `.systems/scripts/check-status-consistency`
- `.systems/scripts/check-qa-evidence`
- `.systems/scripts/check-system-insights`
- `.systems/scripts/check-contract-compliance`
- `.systems/scripts/check-branch-policy`
- `git ls-files ai-workflow-workspace` returned no tracked workspace files.

## Operating Notes

- Work from `main` unless the owner requests a branch.
- Treat future changes as explicit workflow-maintenance tasks, repo-level micro-projects, or full projects depending on scope and risk.
- Do not edit `.systems/**` from a target repository; apply workflow changes in this upstream repo.
- Keep `ai-workflow-workspace/**` local-only and untracked.
- Do not treat project-local prompting artifacts, skills, memory, system insights, or optional phase capture as authority over `AGENTS.md`, core policy docs, phase gates, risk model, permissions, evidence, stop conditions, or owner approvals.

## Next Development Posture

- No active project.
- No active autopilot.
- No known blockers.
- Next safe step: read-only repo status/intake before selecting the next owner-approved micro-project or workflow-maintenance task.
