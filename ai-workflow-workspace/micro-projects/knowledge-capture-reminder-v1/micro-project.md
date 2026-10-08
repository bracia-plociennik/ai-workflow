# knowledge-capture-reminder-v1

## Summary

- Date: `2026-07-09`
- Scope: `Add reminders after implementation/fixes to consider distillation, checkpoint, memory, or knowledge capture, and define commit boundaries for capture.`
- Risk: `medium`
- Work mode: `workflow-maintenance`
- Artifact role: `supporting plan/evidence record; not repo-level-micro-project execution authority`
- Result: `implemented-awaiting-owner-commit-decision`

## Source Idea

After implementation and/or fixes, AI Workflow should remind the owner about distillation or knowledge capture. If the owner moves to a new unrelated task, the workflow should still prompt for capture unless the owner explicitly insists on skipping it. Capture/distillation should include commit readiness; auto-push stays disabled unless the owner asks.

## Batch Triage

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capture reminder | knowledge-lifecycle | post-implementation capture reminder | medium | workflow-maintenance | `AI_WORKFLOW_HOME` | end-of-task capture, contract compliance, phase 6/7 | approved implementation | Reminder behavior extends official workflow contracts and validators. |
| capture commit policy | knowledge-lifecycle | capture commit boundary | medium | workflow-maintenance | `AI_WORKFLOW_HOME` + target repos | commit readiness, ignored workspace policy, target repo mode | resolved in contract | Tracked capture uses commit readiness; ignored workspace capture is not committed. |

## Task Idea Validation

### Co zostaje

- Strongly supports the goal of not losing useful decisions and lessons.
- Builds on existing End-of-Task Capture, Optional Knowledge Capture, and contract-compliance gates.
- Auto-push disabled by default is safe.

### Co jest słabe / do poprawy lub usunięcia

- Do not make every implementation automatically write memory.
- Do not force commits for ignored/local-only workspace artifacts.
- Avoid interrupting urgent owner-directed task switches with hard blockers unless capture is actually required by gates.

### Czego brakuje

- Reminder trigger grammar.
- Rules for when reminder is soft vs required.
- Commit boundary for capture artifacts in official repo mode and target repo mode.
- Clear statement that push is owner-requested only.

### Blokery / decyzje

- Resolved: tracked durable capture goes through commit readiness before any local commit; ignored/local-only workspace capture reports `Commit needed: no, workspace ignored`.
- Resolved: explicit skip grammar is accepted for optional capture, but the response must report residual risk and the skip cannot bypass existing hard gates.
- Resolved: push remains disabled unless the owner explicitly requests it.

## Recommended Routing

- `workflow-maintenance`
- Keep this ignored artifact only as supporting plan/evidence for the owner-approved workflow-maintenance scope.
- Keep commit policy inside the tracked contract; it is not an automatic commit or push grant.

## Acceptance Criteria For Future Plan

- Workflow reminds about capture after implementation/fix/handoff when capture may be valuable.
- Reminder does not bypass owner intent, phase gates, Quality PASS, or memory scope boundaries.
- Owner can explicitly skip capture, with residual risk recorded.
- Capture commit policy states: commit only tracked artifacts by default; ignored workspace capture is not committed unless repository mode makes it tracked and approved.
- Push remains disabled unless the owner explicitly requests push.

## Knowledge Capture

- Knowledge capture: `completed-as-local-evidence`
- Capture target: `micro-project-artifact`
- Reason: `This file preserves implementation evidence and review closure; canonical behavior is stored in tracked workflow contracts.`

## Implementation Slice Plan

| slice | goal | expected files/areas | acceptance check | evidence required | status |
| --- | --- | --- | --- | --- | --- |
| KC-01 | Define reminder behavior and output | core contract and capture template | advisory routing, trigger grammar, output fields, memory boundaries | contract and template review | completed |
| KC-02 | Route the reminder through workflow guidance | AGENTS, HUMANS, README, routing, memory, DoD, response and compliance docs | reminder does not replace existing gates or End-of-Task Capture | cross-reference review | completed |
| KC-03 | Enforce the contract | validator, required-artifact list, validation runner | validator detects missing artifacts and unsafe authority wording | targeted validator run | completed |
| KC-04 | Prove regressions and close quality | smoke tests and full workflow validation | all smoke mutations fail as intended; full profile exits successfully | command evidence and findings-first review | completed |

## Definition Of Done

- Reminder triggers cover implementation, fixes, quality closure, handoff, commit readiness, and unrelated new work with unresolved capture value.
- Optional capture remains advisory; existing phase, status, evidence, privacy, and commit gates remain authoritative.
- Explicit owner skip reports residual risk and cannot bypass hard gates.
- Tracked and ignored capture artifacts have distinct commit behavior; auto-push is disabled.
- Validator, smoke tests, required-artifact integration, and full validation succeed.
- `ai-workflow-workspace/**` remains ignored and untracked.

## Slice Execution Evidence

- `git diff --check`: exit `0`.
- `.systems/scripts/check-knowledge-capture-reminder`: exit `0`.
- `.systems/scripts/check-required-artifacts`: exit `0`.
- `.systems/scripts/validate-workflow --profile scoped --checks check-knowledge-capture-reminder --explain`: exit `0`.
- `.systems/scripts/check-validator-smoke-tests`: `Validator smoke tests passed.`
- `.systems/scripts/validate-workflow --profile full --explain`: all validators completed; embedded smoke tests passed; exit `0`.
- `git ls-files ai-workflow-workspace`: empty output.
- `git check-ignore -v ai-workflow-workspace/micro-projects/knowledge-capture-reminder-v1/micro-project.md`: ignored by `/ai-workflow-workspace/`.

## Advisory Quality Closure

- Intent / plan compliance: `aligned`.
- Cross-contract consistency: `aligned`.
- Risk/work mode compatibility: `aligned`; medium-risk official workflow changes use `workflow-maintenance`, while this ignored file is supporting evidence only.
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: `yes`.
- Negative-space / adversarial review: `completed`; reviewed full product-domain taxonomy, inverse wording, safe negation, owner-skip bypass targets, template field masking, green-check verdicts, and closure self-invalidation.
- Automated evidence role: `supporting-only`.
- Post-fix full re-review: `completed` against the full current tracked/untracked worktree after the last substantive fix.
- Reviewed baseline: `HEAD 597a193 plus the complete unstaged/untracked worktree reported by git status and git diff`.
- Closure freshness: `current`.
- Findings history: initial two material P2 findings and one P3 evidence finding were fixed; post-fix review also found and fixed safe-negation, closure-recording-loop, and owner-skip bypass coverage gaps.
- Blockers: `none found`.
- Unresolved findings: `none found`.
- DoD fit: `aligned`.
- Skipped checks: `none required by the accepted plan`.
- Residual risk: text validators cannot enumerate every future natural-language paraphrase; cross-contract and negative-space review remain required supporting controls.
- Formal gate eligibility: `not-applicable`; this is advisory workflow-maintenance closure, not formal `phase-5-quality`.
- Result wording: `Ready for owner review`.

## Fix Loop Slice Plan

- Source: accepted owner plan for three findings plus four quality-review process errors.
- Implementation scope: current reminder validator/artifact plus global and formal quality-closure contracts, templates, validators, smoke tests, and human routing guidance.
- DoD source: accepted plan and the acceptance criteria below.
- Stop rule: stop before commit if risk/work-mode compatibility remains unresolved, any material finding remains, full validation fails, or the post-fix full-current-diff review is incomplete.

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| KCR-F1 | Resolve the three current findings | reminder artifact, validator, smoke tests | workflow-maintenance routing; full product-domain coverage; stale closure removed | targeted validator and mutation evidence | completed |
| KCR-F2 | Encode the four review-completeness safeguards | quality contracts, phase-5, templates, routing | cross-contract, negative-space, supporting-evidence, post-fix full re-review, freshness fields | validator references and template review | completed |
| KCR-F3 | Enforce safeguards | quality/compliance/slicing validators and smoke tests | unsafe shortcuts fail; valid advisory/formal routes pass | smoke suite | completed |
| KCR-F4 | Revalidate and close | full current diff and workspace evidence | full validation succeeds; independent review has no unresolved material findings | full profile, findings-first review, ignored workspace checks | completed |

## Fix Loop Definition Of Done

- Work mode is `workflow-maintenance` and remains compatible with `medium` risk.
- External Memory unsafe-authority checks cover all System Insights product-domain categories without false positives for valid targets.
- Global review and formal phase-5 both require Review Completeness Gate evidence.
- Automated checks are explicitly supporting evidence, not a standalone verdict.
- Any post-review fix invalidates the previous closure and requires a full-current-diff re-review.
- Final closure is written only after the last fix, targeted tests, full validation, and independent findings-first review.
- Workspace remains ignored/untracked; no commit or push occurs.

## Fix Loop Execution Evidence

- `git diff --check`: exit `0` after the final substantive fix.
- `bash -n` for modified validators, smoke runner, and validation runner: exit `0`.
- Targeted reminder, global-quality, contract-compliance, implementation-slicing, intent/spec, required-artifact, status, and QA-evidence checks: exit `0`.
- `.systems/scripts/check-validator-smoke-tests`: `Validator smoke tests passed.` after full taxonomy, safe-negation, owner-skip bypass, Review Completeness Gate, and stale-closure mutations.
- `.systems/scripts/validate-workflow --profile full --explain`: all core validators and embedded smoke tests completed with exit `0`.
- `git ls-files ai-workflow-workspace`: empty output.
- `git check-ignore -v ai-workflow-workspace/micro-projects/knowledge-capture-reminder-v1/micro-project.md`: ignored by `/ai-workflow-workspace/`.
- `git diff --cached --stat`: empty output; no files staged.
