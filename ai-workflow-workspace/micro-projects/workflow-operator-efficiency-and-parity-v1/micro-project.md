# Workflow Operator Efficiency And Parity V1

## Metadata

- Work mode: `workflow-maintenance`
- Risk: `high`
- Status: `ready-for-owner-review`
- Owner-approved scope: `yes`
- Cross-system impact: `yes`
- Counterpart: `ai-system`

## Cross-system Impact

- Owner decision: `yes`
- Counterpart: `ai-system`
- Handoff artifact: `ai-workflow-workspace/external-memory/memory/2026-07-24-workflow-operator-efficiency-ai-system-handoff.md`

## Summary

Improve operator ergonomics and cross-system parity without changing the workspace layout:

- exact `Koniec pracy` and `Koniec zadania` capture-now routing;
- safe target-worktree bootstrap;
- semantic QA before applicable workflow scripts;
- advisory Luna/Sol model recommendation;
- mandatory owner decision and External Memory handoff for shared-impact upgrades.

## Definition Of Done

- Exact terminal phrases cannot end as acknowledge-only responses.
- Bootstrap requires a strong marker, explicit approval, correct origin, clean clone, and collision-free root shim creation.
- Product implementation QA starts with semantic and product evidence; workflow scripts are supporting-only and run only when applicable.
- Model guidance is advisory and cannot change workflow authority.
- Shared-impact `yes` has one privacy-safe handoff artifact.
- Targeted validators, smoke tests, explicit full validation, and a fresh full-current-diff advisory review complete without unresolved `P0`, `P1`, or material `P2`.
- No workspace layout changes, commit, or push occur before owner approval.

## Implementation Slice Plan

| Slice | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| `S1` | Cross-system handoff | core contract, template, validator, External Memory | pending blocks handoff; yes requires artifact | targeted validator and handoff review | `completed` |
| `S2` | Reliable terminal capture | end-task contract, routing, validator | exact triggers route to capture-now | trigger and precedence smoke tests | `completed` |
| `S3` | Worktree bootstrap | bootstrap contract, portable script/shim, validator | marker, origin, approval, collision, self-clone checks | local bare-remote and linked-worktree smoke tests | `completed` |
| `S4` | Semantic QA routing | validation routing, phases, templates, validator | semantic QA first; scripts supporting-only | producer-consumer audit and smoke tests | `completed` |
| `S5` | Model guidance | model contract, response/routing docs, validator | Luna/Sol recommendation is explicit and non-blocking | classification smoke tests | `completed` |
| `S6` | Integration and quality | docs, required artifacts, validation suite | no unresolved material findings | full validation and current-diff review | `completed` |

## Stop Rules

- Stop on ambiguous target repository marker, existing root `AGENTS.md`, wrong clone origin, dirty clone, missing platform approval, or official-repo self-clone.
- Stop before commit/handoff when cross-system impact is `pending` or `yes` lacks the required handoff artifact.
- Stop quality closure when owner intent, DoD, findings-first review, or required product evidence is incomplete.
- Do not use model selection, deadline pressure, or green workflow scripts to bypass any gate.

## Owner Decisions

- Exact terminal phrases: `capture-now`.
- Bootstrap: exact clone after platform approval.
- Workspace layout: unchanged.
- QA scripts: applicable supporting evidence only, after semantic QA.
- Cross-system impact for this scope: `yes`.
- Model recommendation: advisory-only.

## Knowledge Capture Decision

- External Memory: `required`
- Target: `ai-workflow-workspace/external-memory/memory/2026-07-24-workflow-operator-efficiency-ai-system-handoff.md`
- System Insights: `not-required`
- Commit needed for workspace evidence: `no, workspace ignored`
- Push allowed: `no`

## Quality Closure

- Current baseline: `HEAD e554c09 + full current tracked diff`
- Semantic review: `completed`
- Findings/blockers: `none unresolved`
- Producer-consumer audit: `completed for capture, bootstrap/init, QA templates, model output, cross-system handoff`
- Adversarial matrix: `completed`
- Full validation: `.systems/scripts/validate-workflow --profile full --explain` passed
- Smoke suite: `passed`, including local bare remote and linked Git worktree
- Result wording: `Ready for owner review`
- Residual risk: `ai-system enforcement starts only after later adaptation`
