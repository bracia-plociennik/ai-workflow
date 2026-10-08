# PTO-006 Native Backend Decision Queue

- Decision ID: pto-006-native-backend-test-authorization
- Classification: high-impact
- Statement: authorize a bounded native-backend preflight and synthetic smoke test, not a model benchmark or repository dispatch.
- Why needed now: PTO-005 Quality and Phase 6 are complete; PTO-006 readiness and AC6 require separate runtime authorization and observable backend constraints.
- Recommendation and impact: first specify/inspect the available Codex native backend/version/model and observations without launching workers; then permit one synthetic smoke only if cwd, exclusive writable roots, capacity, handles and termination are independently observable. Enables honest PTO-006 evidence; unsupported constraints remain blocked/unverified.
- Alternatives and impacts: explicitly authorize offline-only partial PTO-006 work, retaining native unverified and no task/project completion; or keep PTO-006/007 postponed with source unchanged.
- Blocking point: PTO-006 pre-write readiness, dependent PTO-007 and final project checkpoint/Phase 8.
- Chosen answer: approved bounded plan; maximum two synthetic invocations, exclusively isolated fixtures in /tmp, stop if isolation is not confirmed
- Status: approved
- Approval evidence: owner command on 2026-10-04 approving this exact plan and isolation stop; subsequent request to reach Phase 8 does not waive that stop
- Durable artifact path: decisions/pto-006-native-backend-authorization.md
- Source: accepted PTO-006 spec AC6 and planned-write boundary; decisions/implementation-approval.md; decisions/pto-quality-range-approval.md; reviews/pto-006-prewrite-readiness.md.
- Owner action: none required for this permission; technical preflight blocked on unverified isolation, see reviews/pto-006-native-backend-preflight.md

## Proposed Test Boundary For Owner Review
- Backend: installed Codex native subagent backend; exact version/model and exposed observations must be identified before launch, not guessed.
- Tested mode: only the mode whose actual isolation/capacity is independently verified; no general native implementation support claim.
- Budget: maximum two synthetic units, two concurrent workers, two worker invocations, no retries or model-performance benchmark.
- Fixtures: one newly created disposable /tmp/pto-006-native-XXXXXX root with two isolated synthetic workers and one synthetic destination; preflight records exact resolved paths and rejects collision/links or broader writable roots.
- Evidence: sanitized project reviews/pto-006-native-backend-evidence.md; no raw worker logs, credentials or private source content.
- Allowed actions if approved: bounded setup/copy, worker execution in verified fixture roots, serial synthetic integration and cleanup of only the newly created fixture after termination/effects are known.
- Stop: missing authentic backend observations, unknown capacity/termination, wider write access, shared roots, source drift, unexplained effects, missing evidence, failed DoD or any resource beyond the approved budget.
- Exclusions: whole-repo/client inputs, secrets, real product writes, production, external API effects, counterpart updates, commits, pushes and final-owner-yes.

The boundary below is now owner-approved conditionally on verified isolation.
The explicit approval is permission evidence only. Read-only preflight rejected
the available interface before launch: zero invocations; no native support proof.
