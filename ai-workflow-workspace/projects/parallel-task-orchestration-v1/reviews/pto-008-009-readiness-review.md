# PTO-008/009 Readiness And Freshness Review

## Findings First
- P2 blocker: both accepted write sets omit `.systems/ai/capabilities/parallel-task-orchestration-v1.json`, although both change its pinned `.systems/scripts/lib/parallel-orchestration.py`. coordinator-status.py compares exact source SHA-256 and returns unknown on mismatch. Updating the pin needs an explicit scope extension and fresh Spec QA; native verification must remain unverified.
- No other material prior-spec mismatch found by independent bounded review. All36 original AC remain coherent; this is advisory, not formal PASS.

## Earlier QA Freshness Disposition
| Evidence | Current disposition | Required action |
| --- | --- | --- |
| Original seven Spec QA | stale against revised canonical plan | fresh substantive regression Spec QA, preserve prior runs |
| Original implementation Quality | reassess affected bound inputs, not blanket downgrade | source consumer changes currently stale002/003/004/005; fresh regression review after final source edit |
| Original Phase8 | superseded seven-task assessment | retain immutable history; cannot qualify nine-task closure |
| CR Architecture QA and Spec008 | current at008 entry; source-bound inputs changed during partial implementation | do not reuse at final gate; fresh assessment after final edits |
| PTO009 readiness | conditional, not started | accepted008 Quality/Phase6, scope correction and fresh Spec QA |

This distinguishes a valid prior assessment from current eligibility. No stored
hash or verdict was silently rebound. No historical source report was rewritten.
decisions/phase-8-pre-cr-history.md records disposition intent; registry binding
has not yet been published, so project-wide QA still correctly rejects stale
canonical evidence.

## Implementation State
PTO008 began after its then-current Spec QA and PTO-D08. Partial first/second
slices introduced capture-record.py, shared capture-state/scoped semantics and
collection-first parent lookup. Existing source changes were preserved. No
consumer capability file was edited without approval. Source remains unfinished;
new conformance regressions, source docs and final QA are not complete.

## Evidence Reviewed
Accepted008/009 specifications, expanded plan and architecture, installed
capability source pins, coordinator-status.py, capture/scoped/parent consumers;
independent Lagrange prior-task assessment and actual current artifact checks.

## Checks And Limits
- python3 -B .systems/scripts/tests/runtime-integrity.py:46 existing tests passed in5.807seconds; supporting baseline regression only, not complete008 DoD.
- git diff --check: clean
- git diff --cached --stat: empty index
- git ls-files ai-workflow-workspace: empty
- check-qa-evidence --project parallel-task-orchestration-v1: exit1, correctly rejecting stale plan/source/final inputs listed above
- Full validation: not run for incomplete source work with a material readiness blocker
- Native/model evals, commits, push, final-owner-yes: not performed

## Quality Closure
- Findings/blockers: capability scope omission unresolved
- Intent/plan/spec/DoD compliance: partial implementation, not done
- Adversarial focus: metadata cannot falsely advertise a source version; historical evidence cannot supply a current gate
- Producer-consumer audit: installed source pin -> coordinator capability discovery exposes the omitted consumer dependency
- Residual risk: partial source refactor is not release-ready; collection regressions and old-current QA reassessment remain outstanding
- Next route: owner scope extension -> Spec Fix Loop/Spec QA -> resume008, then009 and fresh full-current-diff Quality
- Formal PASS: not issued
