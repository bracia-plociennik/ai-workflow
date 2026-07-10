# end-of-task-capture.md

## Purpose

`End-of-Task Capture` is the chat-end knowledge capture contract for owner prompts that signal the current work is done and the owner wants the workflow to preserve useful knowledge.

It is not a workflow phase. It does not replace `phase-6-distillation`, `phase-7-checkpoint`, `phase-8-final-check`, `final review`, `final-owner-yes`, change request routing, commit readiness, or contract compliance.

Default behavior is capture review/proposal. Durable writes are allowed only when the owner explicitly requests capture and target, scope, privacy, status, and write gates are clear.

Knowledge Capture Reminder from `.systems/ai/core/knowledge-capture-reminder.md` is different: it is proactive after implementation, fixes, quality closure, handoff, commit readiness, or before unrelated new work. End-of-Task Capture remains owner-triggered by completion/capture wording and keeps the routing order below.

## Trigger Grammar

Use End-of-Task Capture only when the command includes completion/capture intent, such as:

- `to koniec zadania`
- `koniec taska`
- `kończymy ten task`
- `zamykamy ten task`
- `dziękuję, utrwal wiedzę`
- `utrwal wiedzę z tej rozmowy`
- `zrób końcowe utrwalenie wiedzy`
- `end task and capture knowledge`
- `done, capture learnings`
- `finish this task and preserve learnings`

Do not route generic phase, review, checkpoint, distillation, final approval, or commit-readiness commands here unless they also include completion/capture intent and no higher-precedence route applies.

## Precedence Rules

Apply this order before End-of-Task Capture:

1. `final-owner-yes`, pre-final change requests, and post-final change requests.
2. Explicit formal phase commands: `phase-6-distillation`, `phase-7-checkpoint`, `phase-8-final-check`, and `phase-5-quality`.
3. `final review`, `code review`, `find blockers`, and `find findings` through `.systems/ai/core/quality-review.md`.
4. Commit readiness, contract compliance, and knowledge capture before commit through `.systems/ai/core/contract-compliance.md`.
5. End-of-Task Capture.

Existing commands stay unchanged:

- `Zrób distillation` and `Run phase 6` route to `phase-6-distillation`.
- `Zrób checkpoint` and `Run checkpoint` route to `phase-7-checkpoint`.
- `Zrób final check` routes to `phase-8-final-check`.
- `Zrób final review` routes to `global-quality-review-stance`, not final check.

If a command contains both completion wording and explicit phase wording, route by explicit phase first and include the End-of-Task Capture decision as supporting output only.

## Required Output

Use this output block when the route is End-of-Task Capture or when a higher-precedence route includes it as supporting output:

```text
End-of-Task Capture

- Trigger detected:
- Matched route:
- Precedence check:
- Work mode:
- Source scope reviewed:
- Completion state:
- Capture targets:
- Writes allowed:
- Owner approval:
- Privacy/scope check:
- Distillation needed:
- Checkpoint needed:
- Memory/status updates:
- System Insight candidates:
- External Memory candidates:
- Skipped capture:
- Residual risk:
```

## Capture Targets

Allowed targets are:

- `project-memory`
- `repo-memory`
- `external-memory`
- `system-insights`
- `status/evidence`
- `phase-6-distillation`
- `phase-7-checkpoint`
- `proposal-only`
- `none`

Use `proposal-only` when the owner signaled completion but did not approve durable capture, or when target, scope, privacy, status, source evidence, or write permission is unclear.

## Routing

Formal project/task work:

- If Quality PASS exists and the task/package is complete, route to `phase-6-distillation`.
- If checkpoint cadence is reached or the final in-scope task/package is complete, route to `phase-7-checkpoint`.
- If Quality PASS is missing, do not write final distillation for a completed task/package; route to quality/fix/review or produce proposal-only capture.

Side tasks, micro-tasks, and micro-projects:

- Use lightweight End-of-Task Capture plus `.systems/ai/core/contract-compliance.md`.
- Durable entries belong in the micro-task/micro-project artifact when one exists.
- Promote to the formal workflow if risk, scope, evidence, or approvals exceed the side-task or micro-project contract.

Chat-only or advisory work:

- Default to proposal-only capture.
- Durable capture is allowed only when the owner explicitly requests it, for example `utrwal wiedzę`, and target, scope, privacy, status, and write permission are unambiguous.

Memory routing:

- Use project memory for one-project facts needed by later project work.
- Use repo memory for repo-wide facts, commands, constraints, integrations, risks, or reusable repo rules.
- Use External Memory only for AI Workflow improvement proposals.
- Use System Insights only for anonymized cross-project operating lessons and skill candidates.
- Use status/evidence only for source-backed state synchronization.

## Safety Boundaries

End-of-Task Capture must not:

- mark `PASS` automatically;
- run `phase-8-final-check` automatically;
- close a project without `final-owner-yes`;
- update status from chat-only claims;
- bypass Quality PASS, evidence, risk, permissions, phase gates, stop conditions, or owner approvals;
- write raw client data, client names, secrets, credentials, production identifiers, repo-specific facts, or project-specific details into System Insights;
- write frontend, backend, SEO, ads, smart-contract, product, or client-work lessons into External Memory.

If scope, target, privacy, evidence, safe environment, status, or write permission is unclear, stop with proposal-only capture and ask for the missing decision.

## Response And Trace

Every substantive End-of-Task Capture response must include the required `Execution Trace` from `.systems/ai/core/response-contract.md`.

The trace should mention:

- whether End-of-Task Capture was the matched route or supporting output;
- source artifacts reviewed;
- durable writes performed or explicitly skipped;
- residual risk.
