# phase-5-ex-01-quality.md - EXAMPLE

## Metadata

- Project: EXAMPLE
- Date: 2026-05-16
- Artifact under review: `.systems/ai/examples/projects/EXAMPLE/quality/phase-4-ex-01-implementation-result.md`
- Workflow phase: `phase-5-quality`
- Result: `PASS`
- QA verification contract: `full-qa-verification-v1`

## Definition Of Done Validation

| DoD Item | Result | Evidence |
| --- | --- | --- |
| Example artifact flow is linked and internally consistent | PASS | Manual artifact review and linked task/spec evidence |

## Intent / Plan / Spec Compliance

- Result: `PASS`
- Owner instruction reviewed: `yes`
- Accepted plan reviewed: `yes`
- Accepted spec reviewed: `yes`
- Scope/out-of-scope reviewed: `yes`
- Acceptance criteria reviewed: `yes`
- Compliance status: `aligned`
- Wrong problem solved: `no`
- Owner instruction mismatch: `no`
- Accepted plan mismatch: `no`
- Accepted spec mismatch: `no`
- Acceptance criteria gap: `no`
- Scope creep: `no`
- Underbuild: `no`
- Overbuild: `no`
- Evidence: Example task, specification, implementation result, and quality artifact were compared.

## Review Completeness Gate

- Cross-contract consistency: `aligned`
- Risk/work mode compatibility: `aligned`
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: `yes`
- Negative-space / adversarial review: `completed`
- Automated evidence role: `supporting-only`
- Post-fix full re-review: `not-required`
- Reviewed baseline: `EXAMPLE quality artifact baseline`
- Instruction refresh: `not-needed`
- Instruction baseline: `current`
- Closure freshness: `current`
- Policy-boundary adversarial matrix: `not-applicable`
- Producer-consumer field audit: `not-applicable`
- Producers/consumers reviewed: `not-applicable`
- Required-field mapping: `not-applicable`
- Evidence: Manual example artifact review and linked artifact comparison.

## Adaptive Data / Integration Verification Matrix

- Applicability: `not-applicable`
- Not-applicable reason: `Example implementation creates no data, integration, parser, state-flow, or executable entrypoint.`

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Evidence

```yaml
commands:
  - command: "manual example artifact review"
    result: "PASS"
    notes: "Example files exist and are internally linked."
manual-checks:
  - check: "example DoD satisfied"
    result: "PASS"
    notes: "The example demonstrates artifact flow only."
  - check: "no product code impact"
    result: "PASS"
    notes: "Implementation result states that no product code changed."
artifacts-reviewed:
  - ".systems/ai/examples/projects/EXAMPLE/quality/phase-4-ex-01-implementation-result.md"
  - ".systems/ai/examples/projects/EXAMPLE/specs/phase-3-ex-01-example-task-specification.md"
  - ".systems/ai/examples/projects/EXAMPLE/tasks.md"
skipped-checks: []
```

## Findings

- Critical errors: none.
- Warnings: none.
- Residual risk: example-only artifact.

## Quality Gate

- Intent / Plan / Spec Compliance PASS: `yes`
- Review Completeness Gate PASS: `yes`
- Cross-contract consistency aligned: `yes`
- Risk/work mode compatibility aligned: `yes`
- Negative-space / adversarial review complete or not applicable: `yes`
- Automated evidence treated as supporting-only: `yes`
- Post-fix full re-review complete or not required: `yes`
- Instruction baseline current: `yes`
- Closure freshness current: `yes`
- Policy-boundary adversarial matrix complete or not applicable: `yes`
- Producer-consumer field audit complete or not applicable: `yes`
- Required-field mapping complete or not applicable: `yes`
- 100% DoD satisfied: `yes`
- No known bug in scope: `yes`
- No regression in changed/direct paths: `yes`
- Edge cases covered or explicitly rejected: `yes`
- Explicit evidence attached: `yes`
- Quality result: `PASS`

## Gate Decision

```yaml
result: PASS
can-proceed: true
required-next-phase: "phase-6-distillation"
```
