# PTO-006 Distillation

## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-COMPAT-006-capability-evaluation
- Date: 2026-10-04
- Workflow phase: phase-6-distillation
- Quality artifact: quality/phase-5-pto-compat-006-capability-evaluation-quality.md
- Result: completed
- memory-in-repo-memory: true

## What Was Done
Optional coordinator schema2 reports installed protocol consistency separately
from native operational support and owner permission. Legacy schema1 stays default.
Local six-source hashes and template versions must match. Native support is
unverified under approved protocol-only PTO-D06; zero native calls were made.

## Problems And Reusable Lessons
Initial discovery merely hashed arbitrary installed bytes and failed to catch
deep JSON recursion. Post-fix checks reject incompatible bytes/schema and return
generic unknown/serial for parser exhaustion, without executing candidate code.
Real CLI negatives matter alongside parser unit tests. Hashes prove consistency,
not trusted provenance, platform isolation, capacity or authorization.
Runtime evidence must also be canonical: truthful Phase4 transition, fresh
Architecture/Plan/Spec assessments, derived false for pending capture and no
pointer to a nonexistent Quality report. Failed full runs remain history.

## Decisions And Future Use
Installed metadata, authenticated backend observations, owner permission and
task QA are separate. Native testing remains a separately approved follow-up,
not completed by offline simulation. Three paired threaded file samples have
same outputs but mixed tiny timings; they do not demonstrate model/native speed.

## Evidence
Current formal Phase5 and reviews/pto-006-quality-review.md. Compatibility12,
predecessor77 and runtime46 passed. Full004:694seconds,43checks,fivegroups,745IDs,
exit0; /tmp/pto-006-full-source-004.json. Both material P2 fixed and independently
re-reviewed. Finite synthetic coverage and unavailable native isolation remain.

## Capture
Project memory records these boundaries. Repo synchronization is due now3/3.
System Insight candidate: none. One final AI System handoff belongs to PTO007;
it must explicitly disclose native verification as deferred, not done.

## Distillation Gate
- Captures reusable knowledge: yes
- Avoids local noise: yes
- Ready for checkpoint processing: yes

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D06 and prior conditional high-risk gates approved
- Questions asked: none
- Auto-resolved reversible decisions: concise memory summary
- Optional owner refinements: future isolated backend verification
- Decision artifacts: decisions/pto-006-007-protocol-only-scope.md; decisions/pto-quality-range-approval.md
- Next route: phase-7-checkpoint PTO004..006

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: preserve conservative discovery and honest verification limits
- Owner decision required: no
- Owner decision: defer-to-checkpoint
- Privacy/scope check: pass
- Suggested entry title: Installed does not mean operational
- Suggested entry summary: Pinned protocol consistency and backend authority remain distinct.
