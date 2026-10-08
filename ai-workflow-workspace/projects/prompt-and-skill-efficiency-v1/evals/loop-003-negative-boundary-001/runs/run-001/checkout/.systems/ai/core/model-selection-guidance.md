# model-selection-guidance.md

## Purpose

Give the owner an advisory model recommendation for each new planning, implementation, and QA scope.

## Required Output

```text
Model recommendation:
- Recommended: <GPT-5.6 Luna High|GPT-5.6 Sol High>
- Reason:
- Criticality:
- Current model known: <yes|no>
- Blocking: no
```

Use `Current model known: no` when the runtime does not expose the active model. Do not guess.

## Recommendation Rules

Recommend `GPT-5.6 Luna High` for clear, bounded, reversible work with testable DoD and low or medium risk, including routine implementation and targeted review.

Recommend `GPT-5.6 Sol High` for difficult architecture, substantial ambiguity, security, billing, migrations, production changes, broad integrations, recovery, adversarial review, high-risk work, or high-impact workflow policy changes.

Deadline pressure, current model availability, or cost preference does not justify recommending a weaker model for critical work. If the owner continues with another model, keep the workflow requirements unchanged.

## Authority Boundary

The recommendation is advisory-only:

- `Blocking: no` is mandatory;
- model choice does not change source-of-truth order, scope, risk, permissions, DoD, evidence, QA, approvals, or stop conditions;
- the recommendation cannot claim that a model selection guarantees correctness or `PASS`.
