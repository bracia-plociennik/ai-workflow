# Existing Status History Selector Limitation

- Observed: 2026-10-04 during final-owner publication artifact checks
- Source: .systems/scripts/check-status-consistency, validate_v2_current_status
- Scope: pre-existing source, not part of approved PTO001..010 write sets
- Follow-up: separate workflow-maintenance candidate; no source fix approved here

When a router declares phase-8-final-check plus PASS, the selector counts both
the canonical current report and a checksum-registered superseded recovery report
as current candidates. qa-evidence.py correctly rejects that historical report
as current PASS; the selector nevertheless emits duplicate/current errors.
Failed closure002 is retained as evidence, not claimed as successful.

The project has actually moved beyond technical Phase8 to explicitly completed
owner-final-approval. Its closed status must represent that real route. This is
not an exception to QA: the canonical current technical report and checksum-bound
owner-approval record remain independently assessed; qa-evidence and all capture
consumers still run in final artifact closure. No report is deleted, downgraded,
renamed, admitted as current or removed from validation. Future projects staying
on active Phase8 plus PASS with registered recovery history may encounter this
false-positive; a separately approved fix should select current/nonhistorical
assessments consistently and retain duplicate-current rejection.
