# code-review.md

## Purpose

Review checklist for larger changes, standard-tasks, and work in high-risk areas.

Use this file to validate:

- correctness against task DoD
- regression risk in changed and directly dependent paths
- architecture and workflow compliance
- test evidence quality
- documentation and operational impact

## Review Checklist

- Scope matches the approved task or task package.
- No unresolved blocking decisions were silently implemented.
- Behavior matches repo state, architecture, and plan.
- Edge cases are covered or explicitly rejected with justification.
- Changed paths and direct dependencies were reviewed for regressions.
- Validation evidence is explicit, reproducible, and tied to the change.
- PASS is claimed only when all DoD conditions are met.
- Security, data, infrastructure, or contract risks are called out when relevant.
- Required docs and operational artifacts are updated when the change affects them.

## Output Format

Each review should end with:

- `PASS` or `FAIL`
- explicit findings or `No findings`
- verification evidence
- residual risks or testing gaps
