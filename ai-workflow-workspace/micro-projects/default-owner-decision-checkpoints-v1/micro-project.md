# default-owner-decision-checkpoints-v1

## Summary

- Date: `2026-07-10`
- Scope: `Add default owner decision discovery, phase-end decision checkpoints, safe question opt-out, and non-interactive decision queues.`
- Risk: `medium`
- Work mode: `workflow-maintenance`
- Artifact role: `supporting plan/evidence record; not repo-level-micro-project execution authority`
- Result: `implemented-awaiting-owner-commit-decision`

## Accepted Decisions

- Ask by default about material choices and meaningful owner preferences.
- Group 1-3 questions upfront; ask later only for newly discovered material blockers.
- At phase end, report optional refinements and reversible auto-resolved decisions.
- Active autopilot, Dreaming/automations, and read-only review do not stop for mid-run questions; they queue decisions.
- Explicit no-question wording applies to the current work scope unless the owner explicitly makes it session-wide.

## Definition Of Done

- DoD source: `accepted owner plan for default-owner-decision-checkpoints-v1`
- Done when:
  - a canonical decision checkpoint contract and `owner-preference` class exist;
  - task intake, routing, workflow, autopilot, review, implementation, response, and human guidance use the contract;
  - all 22 phase files and 22 phase templates contain the canonical checkpoint block;
  - active autopilot, async modes, and read-only review use queued decisions rather than mid-run questions;
  - owner opt-out cannot bypass risk, permissions, DoD, QA, approvals, or stop conditions;
  - validator, smoke suite, and explicit full validation pass;
  - a fresh full-current-diff advisory review has no unresolved material findings;
  - workspace remains ignored and no commit or push occurs.

## Implementation Slice Plan

- Source: `accepted owner plan and current AI Workflow contracts`
- Implementation scope: `tracked workflow contracts, phase files/templates, decision/autopilot templates, validators, smoke tests, docs, changelog, and this ignored evidence artifact`
- DoD source: `Definition Of Done above`
- Instruction refresh: `performed-targeted`
- Refresh trigger: `first implementation-class write for a new accepted scope`
- Contracts refreshed: `AGENTS.md, operating-model.md, task-intake.md, command-routing.md, workflow.md, autopilot.md, dreaming-mode.md, quality-review.md, implementation-slicing.md, response-contract.md, risk-model.md, permissions.md`
- Reviewed baseline: `clean main at cc88a5b; origin/main matches; 22 phase files and 22 phase templates`
- Drift/conflict: `none`

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| ODC-01 | Define decision taxonomy, interactive flow, opt-out, and exception routing | core contract, routing, intake, workflow, autopilot, review, response, AGENTS/HUMANS/README | boundaries and precedence are explicit | contract review and targeted searches | completed |
| ODC-02 | Add phase-end checkpoints and decision schema | all phase files/templates, decision/autopilot templates | all 44 artifacts contain the canonical block and existing phase semantics remain intact | structural validator | completed |
| ODC-03 | Enforce positive and adversarial behavior | new validator, required artifacts, validation runner, smoke suite, commands/changelog | required behavior passes and unsafe variants fail | targeted validator and smoke mutations | completed |
| ODC-04 | Revalidate and close | complete current worktree and ignored evidence | full profile succeeds and Review Completeness Gate is current | full validation and full-current-diff review | completed |

## Stop Rule

Stop before commit if the change causes question fatigue, asks for repo-discoverable facts, lets no-question opt-out bypass hard gates, allows active autopilot to continue with a pending material decision, interrupts async/read-only work mid-run, weakens phase quality chaining, or leaves validator coverage incomplete.

## Knowledge Capture

- Knowledge capture: `required`
- Capture target: `micro-project-artifact`
- Reason: `Record accepted interaction decisions, slice evidence, validation, and advisory quality closure in ignored workspace.`

## Slice Execution Evidence

| Slice ID | Status | Files/Areas Changed | Checks Run Or Skipped | Acceptance Result | Residual Risk | Next Slice Or Stop Reason |
| --- | --- | --- | --- | --- | --- | --- |
| ODC-01 | completed | core contract, intake/routing/workflow, autopilot, quality, response, docs | contract review and targeted validators | aligned | none material | ODC-02 |
| ODC-02 | completed | 22 phase files, 22 phase templates, human/autopilot/Dreaming decision schemas | exact-one checkpoint audit and taxonomy search | aligned | none material | ODC-03 |
| ODC-03 | completed | validator, required artifacts, validation runner, response and quality-chain validators, smoke suite | positive and adversarial mutations | aligned | text validators remain heuristic | ODC-04 |
| ODC-04 | completed | complete tracked worktree and ignored evidence | explicit full profile and full-current-diff review | aligned | platform-level instructions remain higher authority than repo contracts | owner commit decision |

## Validation Evidence

- `git diff --check`: completed successfully on final tracked baseline.
- Shell syntax for modified/new validators and smoke suite: completed successfully.
- Targeted validators: owner decision checkpoints, default idea validation opt-out, default quality phase chaining, response evidence trace, required artifacts, contract compliance, implementation slicing, and global quality review completed successfully.
- `.systems/scripts/check-validator-smoke-tests`: completed successfully after final adversarial fixes.
- `.systems/scripts/validate-workflow --profile full --explain`: completed successfully after final tracked fixes.
- Structural audit: exactly 22 phase files and 22 phase templates contain exactly one `Owner Decision Checkpoint`.
- `git ls-files ai-workflow-workspace`: empty.
- Workspace artifact remains ignored by root `.gitignore`.

## Quality Closure

- Closure type: `advisory`
- Findings/blockers: `none unresolved`; review found and fixed phase taxonomy omissions, combined opt-out precedence conflict, and narrow autopilot/async question regexes.
- DoD fit: `aligned`
- Intent/plan/spec/prompt compliance: `aligned`
- Cross-contract consistency: `aligned`
- Risk/work mode compatibility: `aligned`
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: `yes`
- Negative-space / adversarial review: `completed`
- Automated evidence role: `supporting-only`
- Post-fix full re-review: `completed`
- Reviewed baseline: `HEAD cc88a5b plus complete current tracked worktree and two intended new tracked files`
- Instruction refresh: `performed-targeted`
- Instruction baseline: `current`
- Closure freshness: `current`
- Result wording: `No blockers found; No findings found; Ready for owner review`
- Residual risk: `Repository contracts and validators cannot override higher-priority platform instructions; behavioral adherence remains a procedural control, and text-regex coverage cannot prove every future paraphrase.`

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
- Owner decision state: `clear`
- Instruction baseline current: `yes`
- Closure freshness: `current`
- Commit: `not performed; owner decision required`
- Push: `not performed; owner decision required`
