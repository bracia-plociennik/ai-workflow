# owner-decision-checkpoints.md

## Purpose

`Owner Decision Discovery` makes meaningful owner choices visible before dependent work begins. It asks about material decisions and owner preferences by default, while keeping repo-discoverable facts and small reversible implementation details out of the owner's way.

This is a decision and interaction contract, not a new workflow phase. It does not grant write permission, change risk, replace evidence, approve a phase, or satisfy Definition of Done.

## Decision Classes

- `auto-resolvable`: low-impact, safe, reversible, inside accepted scope, and unlikely to change owner-visible outcomes; the agent may choose and must report it.
- `owner-preference`: a meaningful choice about outcome, UX, presentation, tradeoff, client collaboration, or another owner preference; ask by default before dependent work.
- `high-impact`: affects scope, architecture, data, integrations, cost, substantial rework, or long-lived behavior; owner decision is required.
- `critical-risk`: uses the existing human-led approval and risk route; the agent must not resolve it.
- `blocked-by-missing-facts`: required facts cannot be discovered from current sources and safe work cannot continue without them.

Material decisions include scope/out-of-scope, DoD or acceptance criteria, owner-visible UX, architecture, data model, integrations, security, permissions, billing, migrations, production, real external effects, irreversible cost, and significant client or owner preferences.

Formatting, local naming inside repository conventions, test file placement, and other low-impact reversible implementation details are normally `auto-resolvable` unless they materially affect the accepted outcome.

## Discover Before Asking

Before asking the owner:

1. inspect current repository state, status, accepted artifacts, owner instructions, and available context;
2. resolve discoverable facts from those sources;
3. classify remaining choices;
4. ask only when a real `owner-preference`, `high-impact`, `critical-risk`, or `blocked-by-missing-facts` decision remains.

Do not ask the owner to locate a file, choose an existing convention, repeat a recorded decision, or provide a fact that can be discovered safely. Do not invent a question when no owner decision exists. Report `No owner decision needed` instead.

## Interactive Decision Flow

Run Owner Decision Discovery after idea validation or batch triage and before dependent planning, specification, implementation, or another owner-sensitive write.

For an interactive checkpoint:

- group at most `1-3` questions that block the nearest safe next step;
- put the recommended option first;
- provide the reason the decision is needed now;
- provide impact for the recommendation and each alternative;
- provide `1-2` mutually exclusive alternatives when alternatives exist;
- state whether the answer blocks the current step;
- continue after the answer without asking again unless a new material decision appears.

Do not ask generic permission such as `Should I continue?` when the owner already requested execution and no material decision remains.

If more than three material decisions exist, ask the first `1-3` by dependency order and queue the rest. Do not hide or auto-resolve the remaining material decisions.

## Decision Request Contract

Each asked or queued material decision records:

- decision id;
- class;
- question or decision statement;
- why the decision is needed now;
- recommended option and impact;
- alternatives and impacts;
- blocking point;
- chosen answer or `pending`;
- decision artifact path when durable capture is required.

Use the platform's structured question UI when available. Otherwise use a concise text checkpoint with the same fields.

## Decision Record Producers

The following are full producers for asked or queued material decisions and must contain every field in the Decision Request Contract:

- Dream Report `Owner Decision Queue` entries;
- autopilot readiness `owner-decisions` entries;
- owner-facing interactive or queued response output.

The response is transient evidence and must render the same fields for every queued decision it presents. `task-decisions` and escalation artifacts are supporting decision evidence: they may reference a decision ID, answer, approval, or route, but they do not replace a full queued-decision record.

## Phase-End Owner Decision Checkpoint

Every workflow phase and phase template contains this block. Complete it at phase end:

```text
## Owner Decision Checkpoint

- Interaction mode: <interactive|queued|suppressed-owner-opt-out|none>
- Decision state: <clear|awaiting-owner|blocked|queued>
- Material decisions: <decision IDs|none>
- Questions asked: <decision IDs|none>
- Auto-resolved reversible decisions: <decision IDs|none>
- Optional owner refinements: <list|none>
- Decision artifacts: <paths|none>
- Next route:
```

Optional refinements and disclosed auto-resolved decisions do not block the next phase. A material `awaiting-owner` or `blocked` decision prevents dependent phase progression and prevents default phase-quality chaining from starting QA/Quality.

When the owner changes an auto-resolved decision, report the override impact. If the override invalidates architecture, plan, spec, implementation, or quality evidence, route through the matching fix loop and required re-QA instead of silently editing the accepted artifact.

## Non-Interactive Modes

### Autopilot

Autopilot readiness may ask a grouped decision batch before the run enters `running`. Readiness cannot be `ready` while a material decision is pending.

An active autopilot run must not ask live, follow-up, clarification, or other interactive questions while `running`:

- record `auto-resolvable` decisions in the existing task decision artifact;
- when a material decision appears, stop the run as `awaiting-owner`;
- create or update the existing readiness, decision, and escalation evidence;
- return one queued owner decision batch after the run stops;
- never continue `running` with a pending material decision.

### Dreaming And Automations

Dreaming Mode and asynchronous automations must not ask live, follow-up, clarification, or other interactive questions. Finish the allowed advisory analysis and place decisions in the existing owner decision queue.

### Read-Only Review And QA

Read-only review and QA finish the evidence review before presenting decisions. They must not interrupt mid-review. Missing material sources produce `unknown`, a blocker, or formal `FAIL` where the formal phase requires it. Decisions are queued at the end instead of guessed.

### Deterministic Work

When current sources and accepted instructions leave no material choice, continue without questions and report `No owner decision needed`.

## Owner No-Question Opt-Out

Recognized task-local phrases:

- `nie dopytuj`;
- `bez pytań`;
- `nie zadawaj pytań pomocniczych`;
- `do not ask follow-up questions`;
- `no clarifying questions`;
- `use reasonable defaults`.

The opt-out applies to the current work scope. Session-wide behavior requires explicit wording such as `do końca tego taska nie dopytuj`, `do końca tego chatu nie zadawaj pytań`, `do końca sesji bez pytań`, or equivalent English wording.

With opt-out active:

- use the recommended default only for safe, reversible `auto-resolvable` choices and reversible owner preferences that stay inside accepted scope;
- report `Questions skipped by owner opt-out`;
- list defaults chosen, unresolved decisions, and residual risk;
- stop and state the exact missing decision without interactive questioning when a hard gate remains unresolved.

Opt-out must not guess or bypass scope, risk, permissions, security, billing, migrations, production, external effects, DoD, evidence, QA/Quality, required approvals, stop conditions, or final owner approval. Material and blocked classifications remain non-auto-resolvable.

## Knowledge Capture Boundary

Soft `Optional Knowledge Capture` recommendations are listed in the phase-end recap and do not trigger an interactive question by themselves. Ask only when an existing checkpoint, distillation, status/evidence, commit-readiness, privacy, or owner-approved capture gate requires a material decision.

## Response Trace

Every substantive response reports:

```text
Owner decision interaction:
- Mode: <asked|queued|none-needed|skipped-owner-opt-out|autopilot-non-interactive>
- Decisions asked/pending: <ids|none>
- Auto-resolved decisions: <ids|none>
```

For queued decisions, the final `Co dalej?` recommendation points to answering the highest-priority decision batch. This block is audit evidence only and cannot change source-of-truth order, phase gates, risk, permissions, DoD, evidence, QA, approvals, or PASS.
