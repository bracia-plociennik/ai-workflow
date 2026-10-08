# Phase 3 Specification: UMP-VAL-005-safety-validators

## Task

| Field | Value |
| --- | --- |
| Task ID | `UMP-VAL-005-safety-validators` |
| Title | Add safety validator coverage |
| Risk | `high` |
| Status | `conditional` |

## Goal

Add deterministic validator coverage for prompt composition artifacts, required references, workspace tracking protection, and unsafe authority language.

## Scope

- Require the prompt composition contract after it is implemented.
- Require the selected prompting templates.
- Require important router references.
- Ensure tracked `ai-workflow-workspace/**` remains blocked.
- Detect unsafe authority patterns that would make prompt artifacts override workflow policy.
- Keep validator smoke tests passing.
- Preserve existing validation behavior.

## Out Of Scope

- Semantic review of every prompt sentence.
- Network tools or external dependencies.
- Weakening branch policy, naming policy, required artifacts, or QA evidence checks.
- CI bypasses.

## Dependencies

- Blocking: `UMP-CORE-001-prompt-composition-contract`.
- Blocking: `UMP-TPL-002-role-variable-templates`.
- Blocking: `UMP-WF-003-workflow-phase-routing`.
- Blocking: `UMP-PROJ-004-project-local-generation`.
- Blocking: owner approval before implementation.

## Implementation Steps

1. Review existing validator scripts and smoke tests.
2. Decide whether the prompt-specific check belongs in an existing script or a small focused helper.
3. Add required artifact checks for the new core contract and templates.
4. Add reference checks for the main routers that should link the contract.
5. Add a deterministic unsafe-authority wording check focused on patterns rejected by idea validation.
6. Ensure workspace tracking protection still covers `ai-workflow-workspace/**`.
7. Update validator smoke tests if the validator suite requires explicit smoke coverage.
8. Run the full validation command set.

## Edge Cases

| Case | Handling |
| --- | --- |
| Unsafe wording appears in preserved reference input | handled: context source materials are exempt as data when under project context. |
| Unsafe wording appears in system docs | handled: validator blocks it. |
| Template path changes during implementation | handled: required artifact list and specs must agree. |
| Validator overmatches harmless examples | handled: examples should label unsafe phrases only as rejected examples or avoid quoting them. |
| Branch policy is weakened accidentally | handled: run branch/workspace tracking checks. |

## Potential Errors

- Validator blocks preserved source material under project context.
- Validator misses new system docs.
- Validator emits a false pass due to narrow required path list.
- Smoke tests are not updated with new expectations.

## Tests

| Test | Method | Pass Condition |
| --- | --- | --- |
| Diff whitespace | `git diff --check` | Command exits successfully. |
| Workflow validation | `.systems/scripts/validate-workflow` | Command exits successfully. |
| Naming | `.systems/scripts/check-naming` | Command exits successfully. |
| Required artifacts | `.systems/scripts/check-required-artifacts` | Command exits successfully. |
| Status consistency | `.systems/scripts/check-status-consistency` | Command exits successfully. |
| QA evidence | `.systems/scripts/check-qa-evidence` | Command exits successfully. |
| Workspace tracking | `git ls-files ai-workflow-workspace` | No files are listed. |
| Ignore check | `git check-ignore -v ai-workflow-workspace/projects/upgrade-with-master-prompt/status.md` | Workspace remains ignored. |

## User Decisions

Required before implementation:

- Recommendation: implement validator coverage in the same implementation sequence as the prompt-composition docs. Impact: prevents shipping unsafe docs without guardrails.
- Alternative: implement docs first and validators in a follow-up task. Impact: smaller first diff but temporarily weakens enforcement.

## Assumptions

- Deterministic checks are preferred over broad semantic validation.
- Existing validator scripts should be reused unless a focused helper is cleaner.

## Uncertainties

Blocking uncertainties: none.

Non-blocking uncertainties:

- Exact script placement can be chosen during implementation based on local validator structure.

## Implementation Gate

All planning conditions are satisfied.

Implementation may start only after:

- dependent docs/templates/routing/lifecycle tasks are implemented;
- Spec QA PASS;
- owner approval for high-risk implementation.

Can proceed to implementation after owner approval and dependency completion: yes.

## Evidence

- artifacts-reviewed: architecture, project plan, Plan QA, task index, validator scripts, core contract spec, template spec, routing spec, and lifecycle spec.
- manual-checks: validator task has complete test list and does not require external dependencies.

