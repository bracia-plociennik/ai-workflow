# EX-CR-001-pre-final-copy-correction

## Metadata

| Field | Value |
| --- | --- |
| Change request ID | `EX-CR-001-pre-final-copy-correction` |
| Project | `EXAMPLE` |
| Date | `2026-05-21` |
| Requested by | `example-owner` |
| Timing | `pre-final-approval` |
| Type | `acceptance-gap` |
| Risk | `low` |
| Status | `done` |
| Routing | `phase-fix-loop` |
| Blocks final-owner-yes | `yes` |

## Owner Request

The owner does not give `final-owner-yes` yet and asks to correct example copy before closing the scope.

## Context Checked

- Project status: `docs/projects/EXAMPLE/status.md`
- Final check: `docs/projects/EXAMPLE/quality/phase-8-final-check.md`
- Task index: `docs/projects/EXAMPLE/tasks.md`
- Quality evidence: `docs/projects/EXAMPLE/quality/`
- Decisions: `docs/projects/EXAMPLE/decisions/`
- Checkpoint: `docs/projects/EXAMPLE/checkpoints/`
- Related specs/plans: `docs/projects/EXAMPLE/specs/`, `docs/projects/EXAMPLE/planning/`

## Triage

- Affected scope: existing example task output.
- Affected artifacts: example docs and quality evidence.
- Acceptance impact: final closure cannot proceed until the owner comment is resolved.
- Risk rationale: documentation-only example correction.
- Required owner decisions: none after request acceptance.
- First valid route: `phase-fix-loop`.

## Routing Decision

- Selected route: `phase-fix-loop`.
- Why this route: the project was already at final approval, so the correction must route back through the narrowest valid fix path and then rerun quality/checkpoint/final check.
- Why simpler route is not allowed: direct final approval would ignore an open owner comment.
- Next phase or artifact: appropriate fix loop, quality rerun, checkpoint, final check.

## Evidence Required

- Required checks: relevant workflow validators or documented not-applicable reason.
- Required artifacts: updated evidence showing the owner comment was resolved.
- Required approvals: final owner approval after rerun.
- Required reruns: quality, checkpoint when needed, final check.

## Closure Criteria

- [x] Routed work is complete.
- [x] Required evidence exists.
- [x] Status/task/decision artifacts are updated when required.
- [x] Pre-final requests reran required quality/checkpoint/final-check path.
- [x] Post-final requests preserve historical final approval evidence.

## Result

- Final status: `done`
- Completed at: `2026-05-21`
- Links to resulting artifacts: `docs/projects/EXAMPLE/quality/phase-8-final-check.md`
