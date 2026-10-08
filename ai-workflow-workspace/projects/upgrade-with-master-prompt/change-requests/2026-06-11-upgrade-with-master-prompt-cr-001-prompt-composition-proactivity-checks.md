# Change Request: prompt-composition proactivity checks

## Required Fields

| Field | Value |
| --- | --- |
| Change request ID | `UPGRADE-WITH-MASTER-PROMPT-CR-001-prompt-composition-proactivity-checks` |
| Project | `upgrade-with-master-prompt` |
| Timing | `post-final-approval` |
| Type | `defect` |
| Status | `done` |
| Risk | `high` |
| Owner request | Fix PR review P2 in `check-prompt-composition`, add smoke tests for `prompting artifacts` and `prompt modules`, validate, commit, push, and add suggest-only follow-up policy for proactive role/variable suggestions. |
| Affected artifacts and files | `.systems/scripts/check-prompt-composition`; `.systems/scripts/check-validator-smoke-tests`; `.systems/ai/core/prompt-composition.md`; `.systems/ai/core/command-routing.md`; `HUMANS.md` |
| Triage result | Valid post-final defect/follow-up. The prior final scope remains historical; this request does not rewrite final check or owner approval. |
| Routing decision | `phase-fix-loop` |
| Evidence required before done | Requested validator and workflow checks pass; workspace remains untracked/ignored; final diff reviewed; commit and push complete. |
| Final check impact | Does not alter historical phase 8 PASS; records post-final fix on same PR branch. |
| Post-final impact | Narrows validator false negatives and documents suggest-only proactivity boundaries. |

## Owner Approval

Owner approval for high-risk implementation is recorded in chat on 2026-06-11:

```text
Zgoda na zapis: popraw P2 w check-prompt-composition, dodaj smoke tests dla prompting artifacts i prompt modules, uruchom walidację i push na ten sam branch oraz Zaplanuj follow-up policy: kiedy AI Workflow ma proaktywnie proponować role i zmienne, a kiedy czekać na jawne polecenie.
```

## Routing Notes

- Do not track `ai-workflow-workspace/**`.
- Do not touch root untracked `checkpoints/`, `memory.md`, or `status.md`.
- Do not create durable project-local prompting artifacts except this required change-request evidence.
- Keep prompt composition artifacts advisory only.

## Completion Evidence

Commit pushed: `3a18b63` (`fix: tighten prompt composition proactivity checks`) to `origin/codex/upgrade-with-master-prompt-autopilot`.

Commands completed successfully on 2026-06-11:

- `git diff --check main..HEAD`
- `git diff --check`
- `.systems/scripts/check-prompt-composition`
- `.systems/scripts/check-validator-smoke-tests`
- `.systems/scripts/validate-workflow`
- `.systems/scripts/check-naming`
- `.systems/scripts/check-required-artifacts`
- `.systems/scripts/check-status-consistency`
- `.systems/scripts/check-qa-evidence`
- `.systems/scripts/check-branch-policy`
- `git ls-files ai-workflow-workspace`
- `git check-ignore -v ai-workflow-workspace/projects/upgrade-with-master-prompt/status.md`
- `git diff --cached --check`
- `git push origin codex/upgrade-with-master-prompt-autopilot`

Manual checks:

- Final tracked diff was limited to five intended files.
- `ai-workflow-workspace/**` stayed ignored and untracked.
- Root untracked `checkpoints/`, `memory.md`, and `status.md` were not modified.
