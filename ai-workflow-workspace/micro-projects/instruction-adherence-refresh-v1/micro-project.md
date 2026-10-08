# instruction-adherence-refresh-v1

## Summary

- Date: `2026-07-09`
- Scope: `Add source-of-truth refresh and drift-warning behavior so long Codex sessions keep following AI Workflow contracts rather than relying on chat memory.`
- Risk: `medium`
- Work mode: `workflow-maintenance`
- Artifact role: `supporting plan/evidence record; not repo-level-micro-project execution authority`
- Result: `implemented-awaiting-owner-commit-decision`

## Source Idea

After many chat iterations, Codex can drift toward chat context instead of current AI Workflow instructions. If the agent wants to change its way of working, that should happen only through owner-approved workflow changes. Default behavior should re-anchor on AI Workflow instructions.

## Batch Triage

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| instruction adherence refresh | instruction-adherence | source-of-truth refresh | medium | workflow-maintenance | `AI_WORKFLOW_HOME` | AGENTS, command routing, response contract, prompt-injection | approved implementation | Strengthens official workflow contracts and reduces long-session drift. |

## Task Idea Validation

### Co zostaje

- Strong safety improvement for long-running Codex work.
- Aligns with existing source-of-truth order, prompt-injection policy, and Execution Trace.
- Can be implemented through procedural re-read gates rather than trying to control model internals.

### Co jest słabe / do poprawy lub usunięcia

- Avoid vague rules about "how Codex thinks".
- Avoid requiring full re-read of all docs before every message.
- Do not let chat memory override repository state or current contracts.

### Czego brakuje

- Re-read triggers, e.g. before writes, before commit, after long context, after resume, after source-of-truth conflict.
- Drift warning output format.
- Rule for owner-approved behavior changes.
- Validator/smoke tests for missing refresh references.

### Blokery / decyzje

- Resolved: use boundary-based refresh, not refresh before every message or edit.
- Resolved: targeted refresh runs before the first implementation write for a scope, before commit/handoff/quality closure, and after scope or instruction changes.
- Resolved: full refresh runs after resume, context compaction, working-directory change, long interruption, or source conflict.
- Resolved: every substantive `Execution Trace` reports instruction refresh status, trigger, contracts, baseline, and drift/conflict.
- Resolved: task-local behavior changes use only existing contracted opt-outs; a new default requires owner-approved tracked workflow-maintenance.

## Recommended Routing

- `workflow-maintenance`
- Keep this ignored artifact only as supporting plan/evidence for the owner-approved tracked contract change.

## Acceptance Criteria For Future Plan

- Defines source-of-truth refresh triggers for long sessions, resume, pre-write, pre-commit, and conflict cases.
- Adds a drift warning when chat context conflicts with AI Workflow contracts.
- Requires owner-approved workflow changes before changing default behavior.
- Keeps refresh lightweight enough for normal work.
- Adds validator/smoke tests for routing and response trace references.

## Knowledge Capture

- Knowledge capture: `required`
- Capture target: `micro-project-artifact`
- Reason: `This artifact records the accepted behavior decisions, implementation slices, evidence, and quality closure.`

## Implementation Slice Plan

- Source: accepted owner plan for `instruction-adherence-refresh-v1`.
- Implementation scope: core refresh contract, command/workflow routing, Execution Trace, quality/compliance integration, validator, smoke tests, docs, changelog, and this ignored artifact.
- DoD source: accepted plan and the Definition of Done below.
- Stop rule: stop before commit if refresh weakens source-of-truth, risk, permissions, DoD, QA, approvals, or PASS Integrity; if required trace fields are ambiguous; if full validation fails; or if post-fix full-current-diff review is incomplete.

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| IAR-01 | Define refresh profiles, triggers, authority, and drift routing | core contract, operating/workflow/command routing, AGENTS/HUMANS/README | targeted/full behavior and owner boundary are explicit | contract and cross-reference review | completed |
| IAR-02 | Add trace and quality integration | response contract, implementation slicing, quality review, phase-5/template, contract compliance | every substantive trace reports refresh; stale baseline blocks quality-ready verdict | template/contract validation | completed |
| IAR-03 | Enforce the contract | new validator, required artifacts, validation runner, smoke suite, commands/changelog | required fields/triggers exist; unsafe shortcuts fail; valid light flow passes | targeted validator and smoke mutations | completed |
| IAR-04 | Revalidate and close | complete tracked/untracked worktree and this artifact | full validation succeeds; Review Completeness Gate has no unresolved material findings | full profile, syntax checks, ignored workspace checks | completed |

## Definition Of Done

- Targeted and full refresh have unambiguous triggers and source sets.
- Normal continuation without a new trigger can report `not-needed`; refresh is not required before every message or edit.
- Every substantive response includes instruction refresh evidence in `Execution Trace`.
- Drift warning resolves non-blocking conflict through higher authority and blocks writes when scope, risk, permissions, phase, DoD, approvals, or evidence remain unclear.
- Chat memory and agent adaptation cannot change default behavior; only existing contracted opt-outs apply immediately.
- A new default requires owner-approved tracked workflow-maintenance and validation.
- Refresh grants no write permission and cannot change scope, risk, gates, DoD, QA, approvals, evidence, or PASS.
- Validator and smoke tests cover required triggers, fields, authority boundaries, performance boundary, stale baseline, and positive flows.
- Full validation and fresh full-current-diff advisory review complete with no unresolved material findings.
- Workspace remains ignored/untracked; no commit or push occurs.

## Instruction Refresh Baseline

- Status: `performed-full`
- Trigger: `context compaction/resume and pre-quality-closure refresh`
- Contracts refreshed: `AGENTS.md, operating-model.md, command-routing.md, response-contract.md, risk-model.md, permissions.md, definition-of-done.md, implementation-slicing.md, quality-review.md, contract-compliance.md, workflow.md, prompt-injection.md, validation-profiles.md`
- Reviewed baseline: `HEAD 5b6999d; main ahead 3; complete current tracked diff; two new intended tracked files; ignored workspace artifact`
- Drift/conflict: `none`

## Slice Execution Evidence

| Slice ID | Status | Files/Areas Changed | Checks Run Or Skipped | Acceptance Result | Residual Risk | Next Slice Or Stop Reason |
| --- | --- | --- | --- | --- | --- | --- |
| IAR-01 | completed | core refresh contract, routing, AGENTS/HUMANS/README | contract review, reference search | aligned | none material | IAR-02 |
| IAR-02 | completed | response, slicing, quality, compliance, phase files/templates | targeted cross-contract validators | aligned | none material | IAR-03 |
| IAR-03 | completed | new validator, existing validators, smoke suite, validation integration | shell syntax, negative/positive smoke mutations | aligned | regex coverage remains heuristic | IAR-04 |
| IAR-04 | completed | complete current worktree and ignored evidence | full validation, workspace tracking checks, full-current-diff review | aligned | procedural adherence cannot be mathematically guaranteed | owner commit decision |

## Validation Evidence

- `git diff --check`: completed successfully after the final tracked fix.
- Shell syntax for modified validators and validation runner: completed successfully.
- Targeted validators: instruction adherence refresh, response evidence trace, implementation slicing, global quality review, intent/plan/spec compliance, contract compliance, and required artifacts completed successfully.
- `.systems/scripts/check-validator-smoke-tests`: completed successfully after the final validator fix.
- `.systems/scripts/validate-workflow --profile full --explain`: completed successfully on the final tracked baseline; full chain and embedded smoke suite ran.
- `git ls-files ai-workflow-workspace`: empty.
- `git check-ignore -v ai-workflow-workspace/micro-projects/instruction-adherence-refresh-v1/micro-project.md`: ignored by root `.gitignore`.

## Quality Closure

- Closure type: `advisory`
- Findings/blockers: `none unresolved`; review found and fixed literal-field regex false negatives, declarative unsafe-wording false negatives, and over-broad per-edit refresh cadence.
- DoD fit: `aligned`
- Intent/plan/spec/prompt compliance: `aligned`
- Cross-contract consistency: `aligned`
- Risk/work mode compatibility: `aligned`
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: `yes`
- Negative-space / adversarial review: `completed`
- Automated evidence role: `supporting-only`
- Post-fix full re-review: `completed`
- Reviewed baseline: `HEAD 5b6999d plus complete current tracked worktree diff and intended new files`
- Instruction refresh: `performed-full`
- Instruction baseline: `current`
- Closure freshness: `current`
- Result wording: `No blockers found; No findings found; Ready for owner review`
- Residual risk: `The contract and validators make drift auditable and block known unsafe wording, but agent adherence remains a procedural control rather than an absolute runtime guarantee.`

## Contract Compliance

- Work mode compliance: `pass`
- Work mode: `workflow-maintenance`
- Risk/work mode compatible: `yes`
- Scope/acceptance clear: `yes`
- Required artifacts current: `yes`
- Write-set conflicts: `none`
- Evidence available: `yes`
- Quality closure: `advisory`
- Review completeness gate: `complete`
- Instruction baseline current: `yes`
- Closure freshness: `current`
- Commit: `not performed; owner decision required`
- Push: `not performed; owner decision required`
