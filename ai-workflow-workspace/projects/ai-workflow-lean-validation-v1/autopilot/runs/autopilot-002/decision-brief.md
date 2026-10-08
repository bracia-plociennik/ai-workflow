# Owner Decision Brief: LV001-LV006

## Current State

The planning-range is complete. Architecture QA, Plan QA and all six Spec QA reports passed as artifact reviews. Implementation has not started. The tracked worktree is clean at f362ce3; cached origin/main is 1b45483 and diverges from this branch. The local workspace remains ignored.

The requested implementation-range would execute six tasks sequentially, use formal Phase 5 after each implementation, distill after each Quality PASS, checkpoint after task 3 and the final task, then stop before Phase 8. The project has an explicit owner-approved no-deadline/no-timebox constraint.

## Three Decisions

| ID | Decide | Recommendation | Impact | Alternative | Impact |
| --- | --- | --- | --- | --- | --- |
| LV-DEC-002 | Approve high-risk source work and branch/base | Use this checkout; create codex/ai-workflow-lean-validation-v1 from f362ce3, reconcile refreshed origin/main without history rewrite, refresh affected Spec QA, then start LV001. | Preserves current reviewed source while incorporating the main QA parser fix. | Branch from refreshed origin/main, selectively reapply necessary local commits and re-review planning baseline. | Cleaner main ancestry if local commits are not all required, more reconciliation. |
| LV-DEC-003 | Approve LV005 behavioral eval or defer it | Synthetic-only paired GPT-6 Sol High eval, same settings and fresh isolated sessions, with method confirmed before run. | Allows evidence-based instruction changes. | Defer LV005 and narrow current execution range; revisit LV006 after owner scope decision. | Avoids model run, but the six-task project remains incomplete. |
| LV-DEC-004 | Does this upgrade affect AI System? | Yes; one privacy-safe External Memory handoff after quality evidence. | Makes adaptation possible without touching AI System now. | No, with reason. | AI Workflow result remains upstream-only. |

LV-DEC-002 blocks any source implementation. LV-DEC-003 blocks LV005 and six-task uninterrupted readiness. LV-DEC-004 blocks a later commit/counterpart handoff, not the start of implementation. Answers will be recorded in decisions/lv-decisions.md. The user has not provided them in this request.

## Scope Offered For Approval

The source ceiling is the combined Proposed Write Set in the six accepted task specifications. LV001 affects the smoke runner, QA/status consumers, the new shared QA reader, the full QA contract, six QA templates, the corresponding six EXAMPLE quality reports and the two governing validators. Later task write sets are conditional on predecessor outputs and must be rechecked before each task.

This brief does not seek approval for force-push, reset, rebase, remote push, PR, Phase 8, production or customer data access. Local commit timing will be decided at the applicable quality and capture gate; no commit is part of this readiness preparation.

## Response Format

The owner can answer the three IDs in one message, for example:

```text
LV-DEC-002: Zatwierdzam implementację LV001-LV006 w tym checkoutcie; utwórz osobny branch z f362ce3, uzgodnij go z aktualnym origin/main bez przepisywania historii i ponów wymagane Spec QA.
LV-DEC-003: Zatwierdzam izolowany eval tylko na syntetycznych fixture'ach z GPT-6 Sol High przy tych samych ustawieniach obu wariantów.
LV-DEC-004: Tak, przygotuj jeden privacy-safe handoff do AI System.
```

Any narrower answer keeps remaining decisions pending at their declared blocking points.
