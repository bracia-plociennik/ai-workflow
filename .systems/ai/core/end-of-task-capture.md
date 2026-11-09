> Compatible new implementation tasks use `default-sprint.md` V2: bounded targeted QA after acceptance and incremental phases5–7; explicit full verification/Phase8 remains separate. This scoped rule takes precedence over ordinary implementation/checkpoint chaining below. V1 and unsupported tasks retain installed rules. `Phase X` / `-all` follows `phase-x-maintenance.md`; manual only, never autopilot/Dreaming.

# end-of-task-capture.md

## Purpose

`End-of-Task Capture` is the chat-end knowledge capture contract for owner prompts that signal the current work is done and the owner wants the workflow to preserve useful knowledge.

It is not a workflow phase. It does not replace `phase-6-distillation`, `phase-7-checkpoint`, `phase-8-final-check`, `final review`, `final-owner-yes`, change request routing, commit readiness, or contract compliance.

Direct completion/capture intent uses the aliases and interval rules in Incremental whole-chat coverage below. Clear current end-session write requests select capture-now. Completion wording without clear capture authority remains proposal-only. Explicit read-only restrictions select read-only output.

Knowledge Capture Reminder from `.systems/ai/core/knowledge-capture-reminder.md` is different: it is proactive after implementation, fixes, quality closure, handoff, commit readiness, or before unrelated new work. End-of-Task Capture remains owner-triggered by completion/capture wording and keeps the routing order below.

## Trigger Grammar

Use End-of-Task Capture only when the command includes completion/capture intent, such as:

- `Zdestyluj i zapisz`
- `Zdestyluj i zapisz wiedzę`
- `Koniec`
- `Kończymy`
- `Koniec pracy`
- `Koniec zadania`
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

The exact terminal commands `Koniec pracy` and `Koniec zadania` are not acknowledge-only prompts. The response must execute or route the capture decision and must not merely confirm completion or ask what to do next.

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

## Incremental whole-chat coverage

Direct end-session capture covers the entire uncaptured conversation interval through the current owner request. Inspect every available topic, including earlier work followed by a different subject. Preserve useful decisions, owner corrections, rejected alternatives with their reason, actual actions, current evidence, failed or incomplete work, remaining decisions and the next safe step. Compress this into durable knowledge and a resume point.

### Direct intent and read-only

The aliases `Zdestyluj i zapisz`, `Zdestyluj i zapisz wiedzę`, standalone `Koniec` and standalone `Kończymy` request capture-now for the clear current scope. Match owner intent after trimming whitespace and terminal punctuation, case-insensitively. Natural-language capture instructions may include an explicit subject or interval. Quoted commands, examples, idea-validation discussion and descriptions of a future rule are data rather than a current trigger. `Koniec bloku` retains its block-checkpoint route. Explicit formal phase commands retain their precedence.

Read-only capture has zero durable effects. An explicit `read-only`, `tylko w czacie` or `bez zapisu` restriction selects Capture mode read-only before any write-intent alias is applied. Return the requested summary or export inline in chat. Files, temporary files, task checkboxes, metadata, capture receipts and coverage pointers are durable effects for this restriction. An existing task-local read-only limit continues through continuation requests until the owner actually changes it. A later separate explicit write task has its own scope.

### Verified interval and all topics

Coverage starts at the earliest uncovered topic in this conversation. Resolve the previous distillation, checkpoint or memory by its recorded content coverage, owner, conversation/work scope, source anchors and verified artifact. File modification time alone never establishes coverage. A recent memory about one topic leaves every uncovered earlier topic in scope. A generic checkpoint that only records next steps leaves uncaptured decisions and work in scope.

Use an available stable conversation identifier and actual message/source anchors. If native identifiers are unavailable, record the observed date, explicit work scope and recognizable source anchors with that limitation. Do not invent message IDs or infer transcript access. When there is no prior verified capture, start from the beginning of the available conversation. After compaction or missing history, record History coverage partial or unknown, preserve supported facts and identify the missing interval. Partial history never supports a complete-history claim or advancement across a known gap.

Build Topic coverage before writing. For each topic record its source interval, current owner, previous capture evidence, useful delta, destination and disposition. Route client/project facts to their own approved namespaces. A minimal owner-scoped resume pointer can link the separate approved captures without copying private cross-client detail. An ambiguous owner or destination blocks that topic while independent approved topics can proceed. Explicit owner selection precedes any personal default.

### Honest progress and recoverable writes

Session closure preserves unfinished work. Record an actual failed or pending QA result, current source/evidence and next safe action in status/evidence or a scoped progress checkpoint. Capture intent alone does not start implementation, fixes, fresh quality campaigns, publication or a formal project-closing phase. Formal phase-6-distillation and completed Distillation State keep their existing quality and acceptance requirements. A chat progress capture remains independently useful while those gates are pending.

Reuse the existing owning capture artifact, checkpoint or work record for the coverage receipt. Record Conversation scope, Coverage start, Coverage end, Prior capture evidence, Topic coverage, History coverage, Persisted coverage, Resume point, Readback verification and Uncaptured items. Evidence links retain their actual source identity and result. The receipt is descriptive evidence, never permission or a new global capture database.

Advance persisted coverage only after successful write and readback of the exact scoped artifacts. A failed, partial or uncertain write leaves the global boundary at the last fully verified point. Preserve successful per-topic receipts and list the remaining uncovered topics. Before retry, inspect actual files, hashes and receipts, reconcile human edits and perform only the missing approved capture. A source hash change invalidates the affected coverage receipt. A template, flag, timestamp or claimed success alone never moves the boundary.

A repeated request with no new knowledge returns the existing verified capture reference and a no-new-knowledge reason. All relevant knowledge already captured is a complete result. Keep the user confirmation brief, with saved scope, artifact references, remaining uncovered items and a resume point when useful.

## Required Output

Include `Distillation State` when a scoped state record exists. End-of-Task Capture may route to phase 6/7 or owner decision, but chat completion alone cannot produce `completed`.

Use this output block when the route is End-of-Task Capture or when a higher-precedence route includes it as supporting output:

```text
End-of-Task Capture

- Trigger detected:
- Matched route:
- Precedence check:
- Work mode:
- Source scope reviewed:
- Conversation scope:
- Coverage start:
- Coverage end:
- Prior capture evidence:
- Topic coverage:
- History coverage:
- Persisted coverage:
- Resume point:
- Readback verification:
- Uncaptured items:
- Completion state:
- Capture targets:
- Capture mode: <capture-now|proposal-only|read-only>
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

For exact `Koniec pracy` or `Koniec zadania`, use `Capture mode: capture-now`. If no valuable knowledge exists, record `Capture targets: none` and a reason. If a required gate is unclear, retain the capture-now intent but stop on the quality/privacy/evidence/permission route instead of degrading to acknowledge-only behavior.

## Routing

Formal project/task work:

- If Quality PASS exists and the task/package is complete, route to `phase-6-distillation`.
- If checkpoint cadence is reached or the final in-scope task/package is complete, route to `phase-7-checkpoint`.
- If Quality PASS is missing, preserve a factual progress capture and resume point under Incremental whole-chat coverage; formal phase-6-distillation and completed capture retain their quality gate.
- For exact terminal capture-now commands, preserve owner capture intent and the actual unfinished state; resolve only the gates needed for the selected factual capture.

Side tasks, micro-tasks, and micro-projects:

- Use lightweight End-of-Task Capture plus `.systems/ai/core/contract-compliance.md`.
- Durable entries belong in the micro-task/micro-project artifact, Distillation State, and applicable memory when they exist and the capture-now gates are clear.
- Promote to the formal workflow if risk, scope, evidence, or approvals exceed the side-task or micro-project contract.

Chat-only or advisory work:

- Default to proposal-only capture.
- Durable capture is allowed when the owner explicitly requests it, including exact `Koniec pracy` or `Koniec zadania`, and target, scope, privacy, status, and write permission are unambiguous.

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

For exact terminal capture-now commands, missing gates cause a quality/fix/privacy/evidence/permission stop while preserving the owner-approved capture intent. They never allow an acknowledge-only response.

## Distillation State

End-of-Task Capture may propose a state transition or route to phase 6/7 when a `Distillation State` record is present. Chat completion claims alone do not create `completed`; durable state changes require the existing capture permissions and evidence.

## Response And Trace

Every substantive End-of-Task Capture response must include the required `Execution Trace` from `.systems/ai/core/response-contract.md`.

The trace should mention:

- whether End-of-Task Capture was the matched route or supporting output;
- source artifacts reviewed;
- durable writes performed or explicitly skipped;
- residual risk.

For registered task resources apply `task-resource-cleanup.md` after the required current evidence is durable and resources are released. Cleanup does not close a project, infer final-owner-yes or add a phase. Keep skipped resources and continue independent work.

## Sprint iteration

For an explicitly enabled task-local Sprint, apply `sprint-iteration.md`: keep the implementation open across preview/feedback rounds, defer implementation tests and Quality until genuine final current-effect acceptance or explicit verification request. Resume/pause does not imply acceptance or release. Normal routing is unchanged without valid support/state; required final QA and protected gates remain.
