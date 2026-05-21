# EXAMPLE Change Requests Router

## Purpose

`change-requests.md` is the canonical router/index for owner change requests before or after `final-owner-yes`.

Detailed change request entries live in `.systems/ai/examples/projects/EXAMPLE/change-requests/`.

This EXAMPLE content is illustrative only. It is not an active project state.

## Status Summary

| Field | Value |
| --- | --- |
| Open blocking requests | `0` |
| Pre-final requests open | `0` |
| Post-final requests open | `0` |
| Last updated | `2026-05-21` |

## Change Requests

| ID | Timing | Type | Risk | Status | Routing | Entry | Blocks final-owner-yes? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `EX-CR-001-pre-final-copy-correction` | `pre-final-approval` | `acceptance-gap` | `low` | `done` | `phase-fix-loop` | `.systems/ai/examples/projects/EXAMPLE/change-requests/2026-05-21-example-cr-001-pre-final-copy-correction.md` | `yes` |
| `EX-CR-002-post-final-docs-note` | `post-final-approval` | `docs-only` | `low` | `done` | `micro-task` | `.systems/ai/examples/projects/EXAMPLE/change-requests/2026-05-21-example-cr-002-post-final-docs-note.md` | `not-applicable` |

## Rules

- Pre-final blocking change requests prevent `final-owner-yes`.
- Post-final requests do not rewrite historical final approval.
- Store each request in `change-requests/`.
- Product-code writes happen only after the request is routed to an allowed phase, fix loop, micro-task, iteration, decision rollback, or new project.
