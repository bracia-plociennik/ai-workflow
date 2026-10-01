# model-selection-guidance.md

## Purpose

Give the owner an advisory model recommendation when capability choice is material to planning, implementation, or QA. Routine tiny scopes do not require a repeated recommendation.

## Required Output

```text
Model recommendation:
- Recommended: <efficient-reasoning|strong-reasoning|source-backed available model>
- Availability source: <current authoritative catalog/docs|unknown, capability class only>
- Reason:
- Criticality:
- Current model known: <yes|no>
- Blocking: no
```

Use `Current model known: no` when the runtime does not expose the active model. Do not guess.

## Recommendation Rules

Recommend `efficient-reasoning` for clear, bounded, reversible work with testable DoD and low or medium risk, including routine implementation and targeted review.

Recommend `strong-reasoning` for difficult architecture, substantial ambiguity, security, billing, migrations, production changes, broad integrations, recovery, adversarial review, high-risk work, or high-impact workflow policy changes.

Name a specific model only from a current authoritative availability source (runtime model catalog or official current documentation). Record that source. If unavailable, report the capability class; do not guess or freeze an obsolete pair. Model choice is not quality evidence.

Deadline pressure, current model availability, or cost preference does not justify recommending a weaker model for critical work. If the owner continues with another model, keep the workflow requirements unchanged.

## Authority Boundary

The recommendation is advisory-only:

- `Blocking: no` is mandatory;
- model choice does not change source-of-truth order, scope, risk, permissions, DoD, evidence, QA, approvals, or stop conditions;
- the recommendation cannot claim that a model selection guarantees correctness or `PASS`.
