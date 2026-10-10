# full-qa-verification.md

## Purpose

`Full QA Verification` defines the minimum meaning of QA across formal artifact QA phases, formal implementation quality, and advisory global review.

QA is a findings-first verification of the relevant artifact or implementation against the owner instruction, governing artifacts, Definition of Done (DoD), scope, acceptance criteria, repository evidence, and applicable risks. Passing tests or a completed checklist alone are supporting evidence, not a quality verdict.

## Artifact-Appropriate Scope

Delegated implementation also reviews accepted unit provenance and the actual
integrated destination under `.systems/ai/core/parallel-task-orchestration.md`.
The adaptive matrix covers copied dependency drift, integration conflicts/partial
effects, stale review, integrated consumer failures and checkpoint cadence. Local
unit checks and verified integration metadata cannot supply the parent task PASS.

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

The overall QA result comes from an explicit result field in artifact metadata or the final gate decision, not from a passing row, command result, or prose elsewhere. Conflicting overall result fields are invalid. A negative final-check artifact may report successful component checks without becoming positive QA evidence.

Existing V1 QA artifacts declare `QA verification contract: full-qa-verification-v1`; `check-qa-evidence` continues enforcing their V1 runtime fields. New formal QA templates use V2 below. Older closed evidence is admitted only through the ignored workspace registry `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy-qa-evidence-v1.md`, which records its exact relative path and SHA-256 fingerprint. Registry classification or other descriptive columns do not change the identity pair. A formal QA `PASS` without a supported marker or registered legacy fingerprint fails.

## Versioned Current QA Assessment

New V2 reports declare `QA verification contract: full-qa-verification-v2` and exactly one top-level `## Current QA Run`. Its required fields are `Run ID`, `Artifact kind`, `Project/task identity`, `Assessed source HEAD`, `Assessed worktree digest`, `Input artifacts: see table`, `Verdict`, and `Gate Decision`. Required current subsections are `### Input Artifacts`, `### Findings`, `### Evidence`, and `### Review Completeness Gate`; old runs may appear only under `## Historical Runs` and cannot supply missing current fields. Run IDs must be unique across current and historical runs in the report. Fenced Markdown headings are not run selectors. Duplicate current sections, keys, input rows, invalid enums, mismatched report filename/kind/identity, and conflicting verdict/gate values fail closed. Report-level `Result`, `Validation Execution Record` final verdict, gate subsection and next-phase routing must agree with the current verdict; a current `PASS` cannot contain a failed check or edge-case row.

For a V2 `PASS`, the current `Findings` section records `Blockers: none|resolved` and `Unresolved findings: none`. Its `Review Completeness Gate` records a complete status, reviewed baseline, current closure, post-fix full re-review, policy-boundary matrix, producer-consumer audit and field mapping. Architecture, plan, packaging and spec QA also keep `QA Verification Scope` and the complete artifact QA gate inside the current run. Phase 5 keeps current-run DoD validation, aligned intent/plan/spec evidence, adaptive data/integration matrix and a satisfied Quality Gate. Phase 8 keeps a technical completion review and explicit owner approval state; a technical `PASS` never supplies `final-owner-yes`. Skipped packaging has no QA run or V2 marker and cannot claim a QA `PASS`.

The input table has `Root kind | Relative path | SHA-256` columns. Allowed root kinds are `workflow-source`, `approved-target-source` only when its root is explicitly supplied, and `owning-project-evidence`. Paths must be relative, unique, inside their approved root, nonsymlinked, readable, nonsecret and not the assessment itself. Hash only explicitly approved nonsecret inputs. The assessed worktree digest is SHA-256 of the sorted UTF-8 lines `<root-kind>:<relative-path>=<input-sha256>\n`; it binds staged, unstaged and untracked in-scope file contents without self-hashing the report. An input change makes current eligibility stale even if unrelated repository commits occurred. The source HEAD is provenance, not a substitute for the input digest.

`check-qa-evidence` and any status consumer must call the same V2 reader `.systems/scripts/lib/qa-evidence.py`. A status `PASS` requires a matching current V2 verdict of `PASS`; it cannot select a historical run, borrow another task's input, or choose the last of multiple current V2 assessments. A V2 marker always takes precedence over legacy fingerprint admission; existing single-run V1 and exact registered pre-V1 evidence keep their existing rules. Bundled EXAMPLE reports receive schema-only validation and label their illustrative hashes; they are never runtime evidence. Ambiguous older reports require recovery, never automatic conversion or a broadened legacy allowlist.

Legacy fingerprint admission is terminal for the exact registered file: once an unmarked pre-V1 artifact has an exact workspace-relative path and current SHA-256 match, later V1 structural and semantic checks are not applied to that file. The admission preserves immutable historical evidence; it does not upgrade the artifact, extend its original scope, authorize a new phase or external effect, or prove that the historical review met current V1 completeness standards. Any byte change invalidates the fingerprint. A V1 marker takes precedence over pre-V1 admission. A historical incomplete artifact may instead be classified `superseded-invalid-v1` only with a same-project recovery QA artifact that itself satisfies the full current V1 contract and whose path and SHA-256 also match. Historical registry entries use this classification even when the original lacks a literal V1 marker. The original remains immutable and cannot serve as PASS evidence on its own.

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


## Intent brief boundary

Use intent-to-execution-brief.md: original owner intent and accepted decisions remain independent verification inputs; an inferred brief or style profile cannot supply permission, scope or final acceptance. Style-profile.md permits only explicitly scoped, provenance-bearing private advisory feedback. Consumer handoff preserves original scope/DoD/exclusions, mode/source, supplied limits, actual action ceiling, corrections and sanitized optional style projection; consumer verifies local gates itself.
