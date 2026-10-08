# Implementation-range005 Events

## Blocking Drift
- Severity: blocking
- Task: PTO-CAP-008-capture-parity
- Source: reviews/pto-008-009-readiness-review.md
- Owner action: approve adding existing parallel capability JSON to both write sets, followed by Spec Fix Loop and fresh Spec QA
- Recommendation: update exact source pin only; preserve protocol/native-unverified/isolation/permissions boundaries
- Alternative: leave implementation paused; no technical Phase8 or release verdict
- Impact: completing the approved extension avoids coordinator capability becoming unknown after source refactor
