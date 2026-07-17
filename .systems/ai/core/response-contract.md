# response-contract.md

## Purpose

This file defines the required user-facing response shape for Codex when working inside a repository governed by AI Workflow.

The response contract is communication policy. It does not create a new workflow phase and it never replaces phase gates, evidence, status, approval, or Definition of Done.

## When It Applies

Every substantive response to the user must end with a `Co dalej?` footer.

Substantive responses include:

- completed phase summaries;
- completed implementation or documentation work;
- QA, audit, validation, review, and blocker reports;
- guide, recovery, resume, decision review, change request, rollback, side-task, micro-task, micro-project, and autopilot responses;
- clarification responses when the user command is too short or ambiguous to execute safely.

Do not append the footer inside strict machine-readable output such as JSON-only, patch-only, or exact-template output requested by the user. In that case, include the footer in the nearest surrounding normal human-facing response.

## Execution Trace

Every substantive response must include an `Execution Trace` block immediately before the final `Co dalej?` footer.

The block is an audit summary for the owner. It does not create a new gate and does not replace phase evidence, quality artifacts, status, approvals, or Definition of Done.

Use this exact field set:

```text
Execution Trace

Sources used:
- <files/artifacts/chats/tools used as source>

Evidence reviewed:
- <repo state, diffs, phase artifacts, logs, screenshots, command output, or n/a>

Workflow procedures used:
- <task-intake|request-batch-triage|phase file|global-quality-review-stance|contract-compliance|none>

Skills/roles used:
- <skill name and source path, role/lens, or none>

Commands/checks run:
- <command: result, or not-run with reason>

Skipped/unreadable sources:
- <source and reason, or none>

Limits/residual uncertainty:
- <remaining uncertainty or none>

Instruction refresh:
- Status: <performed-targeted|performed-full|not-needed|blocked>
- Trigger: <trigger|none>
- Contracts refreshed: <paths|not-needed>
- Reviewed baseline: <HEAD/worktree/status/artifacts|not-needed>
- Drift/conflict: <none|warning|blocked>

Owner decision interaction:
- Mode: <asked|queued|none-needed|skipped-owner-opt-out|autopilot-non-interactive>
- Decisions asked/pending: <ids|none>
- Auto-resolved decisions: <ids|none>
```

Keep the trace concise. For very small substantive answers, each field may be a single line. For strict JSON-only, patch-only, or exact-template output, include the trace in the nearest surrounding human-facing response instead of inside the constrained payload.

Instruction refresh fields are always present in substantive responses. Use `.systems/ai/core/instruction-adherence-refresh.md` to decide whether the status is `performed-targeted`, `performed-full`, `not-needed`, or `blocked`. A performed refresh must list the contracts and reviewed baseline. `not-needed` is allowed only when no new refresh trigger occurred.

When refresh detects drift or source conflict, include the required `Drift Warning` block before `Co dalej?`. A blocked conflict stops implementation-class writes and must be reflected under limits/residual uncertainty.

Owner decision interaction fields are always present in substantive responses. Use `.systems/ai/core/owner-decision-checkpoints.md`. For queued decisions, the `Co dalej?` recommendation must point to the highest-priority decision batch. If no material choice exists, report `Mode: none-needed` and `No owner decision needed` rather than inventing a question.

Do not say `no sources needed` for a substantive response. If no files, tools, or artifacts were needed, write `Sources used: owner prompt only` and explain the limit under `Limits/residual uncertainty`.

If the owner explicitly opts out of Default Idea Validation with `bez idea validation`, `bez walidacji pomysłu`, `without idea validation`, `skip idea validation`, or `fast path no idea validation`, the trace must include `Idea validation skipped by owner opt-out` and residual risk. This reports only the skipped idea/task validation lens; it does not waive source-of-truth order, risk model, permissions, safe environment checks, required evidence, QA/Quality, owner approvals, phase gates, change-request routing, or final owner approval.

If End-of-Task Capture is used, the trace must state whether it was the matched route or supporting output, which sources were reviewed, whether durable writes were performed or skipped, and residual risk. Use `.systems/ai/core/end-of-task-capture.md` for the required `End-of-Task Capture` block.

If Knowledge Capture Reminder is used, the trace must state the trigger, previous work scope, capture state, recommended target, whether capture is required or optional, whether writes are allowed, whether commit or push is allowed, owner skip state, and residual risk. Use `.systems/ai/core/knowledge-capture-reminder.md` for the required block.

## Delivery And Distillation Trace

When deadline-aware delivery applies, the substantive response should report the agreed deadline/timebox, delivered and deferred scope, overrun status, and quality-floor impact. When capture state applies, it should report the `Distillation State`, derived `is_distilled` value, source/quality evidence, owner disposition, and next consumer. These fields are evidence only and do not grant writes or change gates.

## Required Footer

Use this exact section shape:

````text
Co dalej?

Rekomendacja:
<one concrete next step>.
Wpływ: <what this unlocks, protects, or makes clearer>.
Napisz:
```
<copy-paste prompt for the recommended path>
```

Alternatywa:
<one safe alternative next step>.
Wpływ: <tradeoff and when this path is useful>.
Napisz:
```
<copy-paste prompt for the alternative path>
```
````

Do not provide a long option menu. Include `Inny pomysł:` only when the user explicitly asks for extra ideas or when the current interaction is brainstorming.

`Co dalej?` must remain the final human-facing section of every substantive response. `Execution Trace` must appear before it, not after it.

## Recommendation Sources

Choose the recommendation from the highest applicable source:

1. The user's explicit intent, when it is safe and does not bypass gates.
2. Task intake result from `.systems/ai/core/task-intake.md` when the response handles a new task, planning request, approach request, side-task/micro-task, change request, or autopilot request.
3. The current phase file's `Next allowed phases`.
4. `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md`, active project `status.md`, `tasks.md`, current plan, spec, quality evidence, decisions, checkpoint, or autopilot run state.
5. Stop conditions from `AGENTS.md`, `.systems/ai/core/operating-model.md`, risk, permissions, commands, Definition of Done, and prompt-injection policy.
6. `.systems/ai/core/guide.md`, `.systems/ai/core/change-requests.md`, and `.systems/ai/core/command-routing.md` for lost-user, short-command, recovery, owner change request, rollback, side-task, micro-task, micro-project, and autopilot routing.
7. Fresh install defaults: if `AI_WORKFLOW_WORKSPACE_HOME` is missing or init status is unknown, recommend `phase-0-init`; if init is ready but repo runtime is missing or stale, recommend repo intake; if repo intake is complete but no project workspace exists, recommend project workspace creation.

If these sources conflict, recommend recovery or reconciliation instead of guessing.

## Alternative Selection

The alternative must be:

- safe under the same gates and policy;
- meaningfully different from the recommendation;
- useful for a real user tradeoff, such as slower but safer review, narrower read-only audit, manual execution instead of autopilot, dry-run before mutation, or promotion from micro-task to full workflow.

The alternative must not suggest skipping tests, evidence, QA, approval, Definition of Done, stop conditions, final owner approval, or risk policy.

Both `Napisz:` prompts must be directly usable by the user. If a prompt depends on a missing project, task, phase, or owner decision, make that missing value explicit instead of guessing.

## Common Cases

### New Task, Plan, Or Approach Request

Start with the Task Idea Validation summary from `.systems/ai/core/task-intake.md`: `Co zostaje`, `Co jest słabe / do poprawy lub usunięcia`, `Czego brakuje`, `Blokery / decyzje`, and `Rekomendowany routing`. Only then provide the plan, clarification, or implementation route.

Every substantive plan, including `/plan`, must render the `Plan Quality Contract` from `.systems/ai/core/plan-quality-contract.md` before describing implementation readiness. For read-only planning, state the justified `not-applicable` routes instead of implying implementation quality closure.

If a blocker exists, the recommendation must resolve the most important blocker. If the task is a new project idea, recommend formal `phase-0-idea-validation`. If the task is small and low-risk, the alternative may be normal workflow instead of side-task/micro-task.

### Completed Phase

Recommendation should be the next allowed phase when gates are satisfied. Alternative should usually be a manual review, QA rerun, checkpoint, or read-only drift check.

### Blocked Phase

Recommendation should resolve the highest-impact blocker. Alternative should be a narrower read-only status or evidence audit.

### Implementation Complete

Recommendation should run or finish quality verification, distillation, checkpoint, or the next task depending on status. Alternative should be owner review or a narrower validation pass.

### QA FAIL

Recommendation should route to the matching fix loop. Alternative should be an owner review of the failure if the fix requires a scope or risk decision.

### Guide Mode

Guide mode remains a specialized orientation response. It must still include current status, sources checked, blockers, one recommendation with impact, one alternative with impact, and copy-paste prompts for both paths. The `Co dalej?` footer can serve as the recommendation and alternative section.

### Short Or Ambiguous Command

If the user's command can be safely resolved from status and artifacts, route it to the safest matching phase. If not, ask for the missing decision. Recommendation should state the preferred interpretation and impact; alternative should state the other plausible interpretation and impact.

### Micro-task Or Micro-project

Recommendation can close the micro artifact with evidence or perform the next low-risk step. Alternative should promote the work to the full workflow when scope, risk, or verification is uncertain.

### Autopilot

Recommendation can start or continue supervised autopilot only when gates allow it, the requested range is clear, and run-scoped readiness is `ready`. If readiness is missing, blocked, or awaiting owner decisions, recommendation must create/update `readiness.md` or resolve the top blocker before the requested range. Alternative should be manual execution or dry-run/status review. High-risk and critical-risk work must route to approval or human-led execution.

For autopilot, the footer must distinguish:

- `planning-range`: phase 1 architecture through phase 3 Spec QA, then stop before implementation;
- `implementation-range`: phase 4 implementation through required phase 7 checkpoint, then stop before phase 8;
- owner-triggered `phase-8-final-check`, which must not be recommended as an automatic autopilot step.

## Quality Bar

The footer is invalid when:

- it lists many options instead of one recommendation and one alternative;
- the recommendation ignores a blocker;
- the alternative is just a weaker version of the same step;
- either option would bypass gates, evidence, approval, risk policy, or final owner approval;
- either `Napisz:` block is missing, vague, or not actionable;
- impact is vague, for example `better workflow` without saying what becomes safer, clearer, faster, or unblocked.
