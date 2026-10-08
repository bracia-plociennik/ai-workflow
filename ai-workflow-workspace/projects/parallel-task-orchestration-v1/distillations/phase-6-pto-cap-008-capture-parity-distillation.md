# PTO-008 Distillation

## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-CAP-008-capture-parity
- Date: 2026-10-04
- Workflow phase: phase-6-distillation
- Quality artifact: quality/phase-5-pto-cap-008-capture-parity-quality.md
- Result: completed
- memory-in-repo-memory: true

## What Was Done
Capture inventory, scoped/runtime validation and orchestration parent gates now
share capture-record.py. Existing population boundaries remain unchanged.
Schema1 historical records retain structural/advisory meaning; schema2 current
completion requires current owning implementation QA and accepted distillation.

## Problems And Reusable Decisions
Two independent readers had different historical/current acceptance rules.
Use a common record and collection assessment, not consumer-specific exceptions.
All records, including invalid claims, participate in duplicate detection.
A source artifact must be an exact owning input of the qualifying QA. A gate
must be unique and locally affirmative; unrelated affirmative text cannot rescue
an explicit refusal. Nested Git evidence is outside the selected owner's scope.
Sanitized smoke copies need a narrowly authenticated temporary-child path;
ordinary repository fixtures retain Git-selected inputs and local exclusions.

## Evidence
Formal Phase5 pto-008-formal-quality-001 independently verified require-pass:
15 inputs, all six AC, current HEAD 8a0eeef, current source hashes.
Runtime54 and orchestration89 tests passed. Full source run003 passed all five
smoke groups and 43 checks, exit0,683seconds; authenticated receipt
/tmp/pto-008-full-source-003.json. Current post-fix independent review found no
remaining material findings. Earlier failed/interrupted runs are not evidence.

## Capture And Remaining Boundaries
Project memory receives concise reusable facts; checkpoint will aggregate the
accepted distillation. No client data or target installation is modified.
Cross-system impact for added scope remains pending before commit/handoff.
PTO009 must re-assess affected evidence after its source changes. Native support
remains unverified and ordinary serial execution remains the fallback.

## Distillation Gate
- Captures reusable knowledge: yes
- Avoids local noise: yes
- Ready for checkpoint processing: yes

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D08; PTO-D09
- Questions asked: none
- Auto-resolved reversible decisions: concise capture summary
- Optional owner refinements: none
- Decision artifacts: decisions/pto-008-009-implementation-approval.md; decisions/pto-capability-scope-extension.md
- Next route: fresh PTO009 Spec QA and readiness, then implementation

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: preserve canonical capture acceptance and fixture privacy lessons
- Owner decision required: no
- Owner decision: capture-now
- Privacy/scope check: pass
- Suggested entry title: Canonical historical and current capture semantics
- Suggested entry summary: Structure and current quality are independent classifications.
