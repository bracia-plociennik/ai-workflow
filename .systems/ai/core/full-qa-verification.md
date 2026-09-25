# full-qa-verification.md

## Purpose

`Full QA Verification` defines the minimum meaning of QA across formal artifact QA phases, formal implementation quality, and advisory global review.

QA is a findings-first verification of the relevant artifact or implementation against the owner instruction, governing artifacts, Definition of Done (DoD), scope, acceptance criteria, repository evidence, and applicable risks. Passing tests or a completed checklist alone are supporting evidence, not a quality verdict.

## Artifact-Appropriate Scope

Every QA run must review the following where applicable:

- owner instruction and intended outcome;
- governing artifact and its input artifacts;
- DoD or phase acceptance criteria;
- scope and out-of-scope boundaries;
- changed artifact, implementation diff, or delivered output;
- findings by severity and blockers;
- failure, rework, edge, regression, dependency, and compatibility risks;
- evidence reviewed, skipped/unreadable checks, and residual risk.

Formal architecture, plan, packaging, and specification QA evaluate the quality and readiness of their own artifacts. Their `PASS` does not claim that product implementation is complete or correct. `phase-5-quality` alone can issue the formal implementation `PASS` or `FAIL`. Global review remains advisory and must not issue a formal result.

## Artifact QA Completeness Gate

Before a formal artifact QA phase declares `PASS`, record:

- Owner intent and governing sources reviewed: `<paths|missing>`.
- DoD / phase acceptance criteria reviewed: `<yes|no>`.
- Scope and out-of-scope consistency: `<aligned|partial|mismatch|unknown>`.
- Artifact / relevant diff review: `<completed|incomplete>`.
- Findings-first review: `<completed|incomplete>`.
- Failure / rework / dependency scenarios: `<completed|not-applicable|incomplete>`.
- Repository and source compatibility: `<aligned|partial|mismatch|unknown>`.
- Post-fix full artifact re-review: `<completed|not-required|incomplete>`.
- Evidence reviewed: `<paths|commands|manual checks>`.
- Skipped or unreadable sources: `<none|list>`.
- Residual risk: `<none|list>`.
- Closure freshness: `<current|stale>`.

Missing governing sources, an incomplete required review, a material mismatch, unresolved blocker, stale closure, or incomplete post-fix re-review means `FAIL` or a stop condition. A formal artifact QA result is valid only for that artifact and its next gate.

New QA artifacts created from V1 templates declare `QA verification contract: full-qa-verification-v1`; `check-qa-evidence` enforces the V1 runtime fields when that marker is present. Older closed evidence is admitted only through the ignored workspace registry `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy-qa-evidence-v1.md`, which records its exact relative path and SHA-256 fingerprint. Registry classification or other descriptive columns do not change the identity pair. A formal QA `PASS` without a V1 marker or registered legacy fingerprint fails.

Legacy fingerprint admission is terminal for the exact registered file: once an unmarked pre-V1 artifact has an exact workspace-relative path and current SHA-256 match, later V1 structural and semantic checks are not applied to that file. The admission preserves immutable historical evidence; it does not upgrade the artifact, extend its original scope, authorize a new phase or external effect, or prove that the historical review met current V1 completeness standards. Any byte change invalidates the fingerprint. A V1 marker takes precedence over pre-V1 admission. An incomplete V1 artifact may instead be classified `superseded-invalid-v1` only with a same-project recovery QA artifact that itself satisfies the full current V1 contract and whose path and SHA-256 also match. The original remains immutable and cannot serve as PASS evidence on its own.

The registry accepts the historical three-column path/SHA/classification layout and the five-column classification/path/original-SHA/replacement-path/replacement-SHA layout. For `pre-v1` the replacement fields are `none`; for `superseded-invalid-v1` both fingerprints and the replacement are mandatory. Registry admission does not bypass privacy or secret checks. `check-qa-evidence --project <slug>` limits runtime QA evidence to that project while product examples remain global; the default still checks every project. Project-scoped `validate-workflow` also scopes runtime status and naming, not global product checks.

## Formal Phase 5 PASS Evidence

A V1 `phase-5-quality` artifact may declare `PASS` only when it records a completed DoD validation, `aligned` Intent / Plan / Spec Compliance, a complete and current Review Completeness Gate, explicit findings status, the applicable adaptive matrix, evidence, and a satisfied Quality Gate. A missing section, an incomplete review, a stale baseline, an unresolved `P0`, `P1`, or material `P2`, or any unsatisfied Quality Gate condition blocks `PASS`.

## Adaptive Data / Integration Verification Matrix

The matrix is required for `phase-5-quality` and global review when the changed scope affects a data model, parser, transformation, integration, state transition, executable entrypoint, derived output, or persisted error state. It is not required for unrelated changes only when recorded as `not-applicable` with a reason.

For each relevant flow, report:

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |

Every material row needs an automated check or explicit safe limitation, plus one representative end-to-end manual trace and one relevant failure-path trace. A `PASS` is blocked when a required matrix is missing, a forbidden state is unexamined, or failure behavior is unknown.

## Authority Boundary

Full QA Verification does not grant write permission, change risk, expand scope, replace phase gates, weaken approvals, or turn advisory review into formal `PASS` or `FAIL`.
