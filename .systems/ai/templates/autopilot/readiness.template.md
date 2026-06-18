# readiness.md

Purpose: pre-start and pre-resume readiness audit for one autopilot run.

Autopilot must not enter `running` until `readiness-result` is `ready`.

```yaml
readiness:
  run-id: <autopilot-001>
  project: <project>
  requested-mode: <supervised|semi-autonomous|autonomous-execution>
  requested-range: <planning-range|implementation-range>
  start-phase: <phase-1-architecture|phase-4-implementation|current-stable-phase>
  stop-phase: <phase-3-spec-qa|phase-7-checkpoint>
  stop-condition: <all-planned-specs-pass|final-checkpoint-complete|owner-stop|blocked>
  requested-scope: <task|task-range|package|remaining-ready-tasks>
  requested-by: <owner|operator|agent>
  created-at: null
  updated-at: null
  readiness-result: draft # draft | blocked | awaiting-owner | ready | superseded
  superseded-by: null

scanned-sources:
  repo:
    - AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md
    - AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md
    - AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md
    - AI_WORKFLOW_WORKSPACE_HOME/repo/context/
  project:
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/status.md
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/tasks.md
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/plans.md
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/planning/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/specs/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/decisions/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/change-requests.md
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/change-requests/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/escalations/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/checkpoints/
    - AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/
  policy:
    - AGENTS.md
    - .systems/ai/core/autopilot.md
    - .systems/ai/core/workflow.md
    - .systems/ai/core/risk-model.md
    - .systems/ai/core/permissions.md
    - .systems/ai/core/definition-of-done.md
    - .systems/ai/core/commands.md
    - .systems/ai/core/rollback.md
    - .systems/ai/core/dependencies.md
    - .systems/ai/core/prompt-injection.md
    - .systems/ai/core/task-intake.md
  skills:
    - AI_WORKFLOW_WORKSPACE_HOME/skills/
    - .systems/ai/skills/

gate-matrix:
  project-context: <present|missing|stale|not-applicable>
  project-context-intake: <pass|fail|missing|not-applicable>
  architecture-qa: <pass|fail|missing|not-applicable>
  project-plan-qa: <pass|fail|missing|not-applicable>
  task-packaging: <complete|skipped-with-reason|missing|not-applicable>
  spec-qa: <pass|fail|missing|not-applicable>
  implementation-write-scope: <clear|blocked|not-applicable>
  checkpoint-cadence: <clear|required|blocked|not-applicable>
  final-check-owner-only: <confirmed|blocked>
  command-map: <known|missing|unsafe>
  safe-environment: <known|missing|unsafe>
  git-branch-policy: <clear|blocked|not-applicable>
  dirty-state-policy: <clear|blocked|not-applicable>
  evidence-expectations: <clear|missing|blocked>

range-readiness:
  planning-range:
    accepted-project-context: <present|missing|not-applicable>
    missing-architecture-plan-packaging-specs-are-expected-outputs: <yes|no|not-applicable>
    product-code-writes: forbidden
    stop-before-implementation: <confirmed|blocked|not-applicable>
  implementation-range:
    architecture-qa-pass: <yes|no|not-applicable>
    plan-qa-pass: <yes|no|not-applicable>
    first-spec-qa-pass: <yes|no|not-applicable>
    spec-refresh-before-each-next-task: <confirmed|blocked|not-applicable>
    hard-checkpoint-after-every-3-tasks: <confirmed|blocked|not-applicable>
    final-checkpoint-after-last-task: <confirmed|blocked|not-applicable>
    stop-before-phase-8: <confirmed|blocked|not-applicable>

blockers:
  - id: <blocker-id>
    source: <artifact-or-policy>
    severity: <blocking|warning|critical>
    affected-task: <task-id-or-scope>
    required-owner-action: <decision-or-approval>
    status: <open|resolved|approved|not-applicable>

owner-decisions:
  - id: <decision-id>
    decision: <decision-needed>
    options:
      - option: <recommended-option>
        impact: <impact>
      - option: <alternative-option>
        impact: <impact>
    recommendation: <recommended-option>
    chosen-answer: null
    approval-evidence: null
    status: <pending|approved|rejected|not-applicable>

external-effects:
  email: <none|test-adapter|real-write|unknown>
  payments: <none|sandbox|real-write|unknown>
  crm-api-writes: <none|test-adapter|real-write|unknown>
  migrations: <none|safe-test|production-risk|unknown>
  production-data: <none|read-only|write-risk|unknown>
  secrets: <none|required|unknown>
  destructive-operations: <none|possible|unknown>
  infrastructure: <none|local-only|production-risk|unknown>

owner-prompt:
  recommended-next-prompt: |
    <exact prompt the owner should answer before autopilot starts>
  alternative-next-prompt: |
    <safe alternative prompt>
```

## Readiness Decision

`ready` is allowed only when every blocking item is `resolved`, `approved`, or `not-applicable`, all high-risk approvals are recorded, no critical-risk task is routed to autopilot, command/safe-env/evidence gates are clear, and the selected range gates are satisfied.

For `planning-range`, missing architecture, plan, optional owner-requested packaging, and specs are not blockers when they are explicit outputs of the run. Product-code writes are always forbidden.

For `implementation-range`, missing Architecture QA PASS, Plan QA PASS, packaging decision or solo-by-default/not-requested packaging decision, first Spec QA PASS, safe implementation write scope, or checkpoint policy is blocking.

Autopilot must not run `phase-8-final-check`; owner-only final check must be confirmed before readiness can be `ready`.
