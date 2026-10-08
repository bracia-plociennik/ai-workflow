# Runtime Dependency Scope Handoff

## Metadata
- Date: 2026-10-05
- Source system: ai-workflow
- Counterpart: ai-system
- Status: accepted-for-handoff
- Privacy/scope check: pass
- Raw client data included: no

## Improvement Proposal
Classify the fixed project-relative quality/artifacts/node_modules directory as
supporting tooling, never active evidence. Print the exclusion and prune before
link validation without traversing or changing the target.

## Decisions
The owner requests upstream remediation and official update of the named local
installation, then fresh owned artifact checks and technical final assessment.
Preserve existing links. No publication, activation or final-owner-yes follows.

## Safety Boundaries
Only the fixed dependency directory is excluded. Other runtime links remain
invalid. Both QA and scope evidence readers reject references into the excluded
directory even when it is a real directory. Arbitrary ignores and schema changes
are not introduced. Historical assessments retain original bytes and approvals;
fresh compatibility reviews do not invent a new owner closure.

## Source-System Reference Map
- .systems/scripts/lib/validation-scope.py: inventory classification and evidence containment
- .systems/scripts/lib/qa-evidence.py: independent evidence-reader boundary
- .systems/scripts/tests/runtime-dependency-scope.py: positive and fail-closed regression
- .systems/scripts/smoke/core.sh and manifest.json: supplemental test registration
- .systems/ai/core/validation-profiles.md: fixed classification contract

## Adaptation Checklist
Install only via the official update-from-upstream route. Preview workspace
schema updates separately. Check the actual owned project after installation;
source-only tests cannot replace its runtime checks. Compare link identity and
target text before/after, without reading dependency contents.

## Validation Expectations
Fresh full validation with every smoke group, immutable reference manifest,
direct forbidden evidence references, live/dangling links, real dependency
directory, other-link rejection and invalid capture/status/QA/name regressions.
Then fresh owned naming, status, QA and capture checks followed by Phase7/8.

## Residual Risk
Dependency contents are intentionally outside evidence. Real application use
needs its own tool/dependency validation. This handoff is advisory, not a write,
commit, push or owner-approval grant.

## Current Delivery State
Local source commit a9a5c40 is available on codex/runtime-dependency-scope-fix;
full upstream validation exited 0 with all five smoke groups and 759 cases.
No push. The actual downstream update remains stopped at preflight because
existing target runtime assessments bind a different target-product baseline,
including absent product inputs. Fresh compatible source evidence must be
established before install/final closure; do not restamp missing-source reports,
skip update validation or infer final human approval. A dry-run is not install
evidence. No schema backfill or activation has occurred.
