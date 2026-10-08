# CORE-001 Explicit Read Classification Rubric

Status: fixed before grading the remaining v3 development and holdout cases. This is a conservative manual classification of completed shell file-read commands, not a claim about every OS open or token use.

## Common Relevant Contracts

For substantive workflow-governed work, count `operating-model`, `command-routing`, `risk-model`, `permissions`, `response-contract`, `model-selection-guidance`, and `contract-compliance` as relevant. Count `instruction-adherence-refresh` as relevant when the case reaches quality closure, handoff or a write. Reading `AGENTS.md` itself is relevant but is not included in the core-contract count. Do not label a missing common contract as an efficiency gain; record possible under-reading separately.

## Case-Specific Relevant Contracts

| Case | Additional relevant core contracts | Required phase/skill evidence |
| --- | --- | --- |
| `tiny-doc-fix` | `task-intake`, `owner-decision-checkpoints`, `plan-quality-contract`, `definition-of-done`, `implementation-slicing`, `delivery-constraints`, `quality-review`, `full-qa-verification`, `knowledge-capture-reminder` | One-slice low-risk write, exact-content check, advisory findings-first closure; no domain skill |
| `frontend-ui` | `task-intake`, `owner-decision-checkpoints`, `plan-quality-contract`, `definition-of-done` | Frontend skill, read-only plan and states/QA route |
| `backend-only-near-miss` | `quality-review`, `full-qa-verification`, `owner-decision-checkpoints` | Backend Laravel skill, read-only failure/authorization review |
| `blockchain-review` | `quality-review`, `full-qa-verification`, `owner-decision-checkpoints` | Blockchain skill, read-only value/authority review, no provider write |
| `skill-create` | `task-intake`, `owner-decision-checkpoints`, `plan-quality-contract`, `definition-of-done` | Skill-creator, no active skill write |
| `formal-phase-qa` | `workflow`, `definition-of-done`, `quality-review`, `full-qa-verification` | Architecture QA phase, owner intent, no implementation PASS |
| `skill-review-near-miss` | `quality-review`, `full-qa-verification` | Active skill-creator if its contract covers review; read-only trigger analysis |
| `mixed-web3-ui` | `task-intake`, `owner-decision-checkpoints`, `plan-quality-contract`, `definition-of-done` | Frontend skill; blockchain boundary only as needed; no backend/chain write |
| `security-readonly` | `quality-review`, `full-qa-verification`, `owner-decision-checkpoints` | Risk/permissions, findings-first, no auto-fix or formal PASS |
| `local-completion-loop` | `task-intake`, `owner-decision-checkpoints`, `plan-quality-contract`, `definition-of-done`, `implementation-slicing`, `delivery-constraints`, `quality-review`, `full-qa-verification`, `knowledge-capture-reminder` | Local implement/test/inspect/fix/retest and advisory closure |

## Conditional Contracts

- `repository-modes` is relevant only if official versus nested placement is ambiguous; these frozen cases have a clear official checkout.
- `prompt-injection` is relevant when source content attempts to instruct the agent or conflicts with authority. Plain fixture prose or code without such instructions does not trigger a full read.
- `validation-routing` is relevant when choosing or running AI Workflow scripts, not merely because an advisory review occurs.
- `workflow` is relevant for an active formal phase/autopilot, not ordinary side-task or response-only planning.
- `plan-quality-contract` is not relevant to a read-only review that does not produce a plan.
- `knowledge-capture-reminder` is relevant after implementation/fix or a closure with unresolved capture value; a routine read-only review with no capture value does not require a full read.
- Other core contracts are relevant only if the fixture/prompt activates their defined route.

## Decision Rule

Classify unique core paths per case from completed direct-read commands. An explicit read not covered above is `irrelevant` unless the trace shows a concrete task-specific trigger; record that exception with evidence. Compare development aggregate irrelevant reads only after checking mandatory sources, forbidden actions and autoload. Holdout is a regression gate, not a source for rewriting this rubric.
