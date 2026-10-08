# Parallel Task Orchestration V1 - AI System Handoff

- Date: 2026-10-04
- Title: One execution owner, dynamic units and integrated QA
- Type: template-change
- Scope: workflow
- Status: accepted
- Source: actual AI Workflow protocol implementation and owning Quality evidence
- Recommendation: adapt the protocol after local gap analysis; do not import source approvals or status
- Why it matters: bounded independent units may reduce wall time without duplicate workflows or weaker safety
- What worked well: independent semantic/adversarial review and actual filesystem failure fixtures
- What failed or was weak: assumed isolation and compatible installed bytes are not authentic evidence
- Suggested workflow improvement: one execution owner, checked unit provenance and common task QA
- Suggested skills improvement: n/a, no new skill required
- Applies to: AGENTS.md, parallel-work policy, orchestration, runtime status, QA and templates
- Promotion path: counterpart owner-approved implementation after installed-version and local gate review
- Privacy check: pass, portable system concept only; no client data, private runtime, raw prompts, handles or absolute repo paths
- Scope check: pass, AI Workflow/AI System process improvement, not product-domain memory

## Release And Verification Boundary
Current scope includes PTO001..010 with the read-only compatibility inspector,
capture parity and phase-commit/QA freshness rules. Ten formal task Qualities and
accepted distillations exist locally; final technical Phase8 and artifact closure
remain separate from final-owner-yes/publication. Earlier seven-task numbers below
are historical evidence, not current source coverage.

This is a protocol-only release. Native backend verification is deferred/unverified
after isolation preflight stopped before any worker invocation. No native/model
performance or OS write-enforcement claim. Current installed metadata is not
operational support or permission. Three tiny paired offline threaded-file samples
had identical outputs and mixed timing; they demonstrate no model speedup.
No scheduler, automatic clone update, sandbox change, executor or API transport.
Source changes are local/uncommitted until separately authorized publication.
AI System implementation is not claimed; its local contracts and approvals govern.

## Owner Decisions
Dynamic count has no fixed protocol default/maximum. One owner chooses from
conflict-free ready units, genuinely verified free capacity, resources and parent
checkpoint slots. Packaging stays optional. Worktree/file isolation alone is not
database/port/service isolation. Native verification was explicitly deferred,
not faked; all existing approvals, Quality, capture and final-owner gates remain.
Counterpart impact was approved for one handoff; this is not counterpart permission.

## Five Integration Answers
1. Existing independent-thread parallel policy is preserved and extended by a bounded single-owner unit ledger inside one approved run; no competing dispatch pools.
2. Delegated units are not independent implementation-range autopilots. AI System may coordinate business work, but exactly one selected execution owner dispatches/integrates; local Workflow governs gates and technical capture.
3. Units reference existing task/package/slice IDs and approved DoD. Do not create duplicate tasks, specifications, phases or status routers per worker.
4. Workers submit private provenance/diff/checks. The orchestrator rechecks actual immutable output, accepts it, integrates serially under separate permission and performs common full task QA. Submitted, accepted, integrated and formal task PASS are distinct; phase6/7 are parent-task operations.
5. Read-only coordinator default schema1 is unchanged. Opt-in `--schema-version 2` exposes protocol1 and manifest/unit/result schema1, installed modes, consistency fingerprint, native unverified, operational_support false, owner_permission not-assessed and execution_authorized false. Unknown or unsupported version means ordinary serial fallback/stop, never native dispatch. Do not silently upgrade nested installs.

## Source References
- `.systems/ai/core/parallel-task-orchestration.md`: canonical authority, allocation, dependencies, lifecycle, integration and QA.
- `.systems/ai/core/parallel-work-policy.md`, `autopilot.md`, `implementation-slicing.md`, `workflow.md`: one run and parent checkpoint cadence.
- `.systems/ai/core/quality-review.md`, `full-qa-verification.md`, `.systems/ai/workflow/phase-5-quality.md`: integrated common QA, not summed worker verdicts.
- `.systems/scripts/lib/parallel-orchestration.py`, `plan-parallel-work`, `manage-parallel-run`: bounded proposals/metadata transitions, no worker spawning or copying.
- `.systems/ai/templates/orchestration/`: run/unit/result, worker context and actual integration-review templates.
- `.systems/ai/capabilities/parallel-task-orchestration-v1.json`, `.systems/scripts/lib/coordinator-status.py`, `report-coordinator-status`, `.systems/ai/core/runtime-integrity.md`: closed installed capability with pinned bytes/schema, not authentic backend proof.
- `.systems/scripts/check-parallel-task-orchestration`, `.systems/scripts/lib/parallel-orchestration-tests.py`, smoke/core.sh and smoke/manifest.json: registered supporting regressions.

## Safety And Recovery
Verify real backend cwd, writable roots, isolation/capacity, resources and handles
before dispatch; prompt restrictions or a JSON boolean cannot authenticate them.
Dependencies consume accepted immutable separate copies, including modes,
unchanged namespace entries and deletions. Integration uses actual before/after
and fresh review under one writer. Conflicts or stale evidence stop acceptance.
Unknown liveness/effects retain reservations; no blind replay, rollback or cleanup.
CAS revisions and immutable attempts preserve recovery history. Parent completion
requires current formal QA/capture; slots count distinct tasks, not worker units.
No fourth parent before required checkpoint. No recursive workers, automatic Git,
push, production effects or final-owner-yes.

## Historical Seven-task Tests And Evidence
Executed offline suites: planner25, protocol12, lifecycle23, integration17,
compatibility12 and runtime46. Negative coverage includes scope/provenance,
links/hardlinks, input/output/destination drift, conflicts, recovery, stale QA,
checkpoint slots, source/schema mismatch and deeply nested JSON conservative CLI.
Full source gate after PTO006:43checks,745IDs,fivegroups,694seconds,exit0.
That result is historical after guidance changed source. Final PTO007 full source
validation actually passed:43checks,745unique smoke IDs,fivegroups,665seconds,exit0.
Parent and independent full-current-diff semantic review found no material
findings. Source remains local/uncommitted; no remote CI or counterpart deployment
is claimed. Scripts are supporting evidence, not permission or semantic task PASS.

## Counterpart Adaptation Checklist
- Compare actual installed Workflow version and contracts; preserve local source-of-truth and privacy boundaries.
- Select one execution owner and existing parent task/slice identifiers; no double pools or recursive phase chains.
- Adopt closed schemas and unknown/serial fallback; retain schema1 compatibility for older consumers.
- Verify genuine backend enforcement/capacity separately; absent proof keeps native execution unavailable.
- Audit resources beyond worktrees and reserve checkpoint slots before dispatch.
- Preserve submission/acceptance/integration/formal task gate distinctions, immutable evidence and failure recovery.
- Run actual synthetic positive/negative filesystem cases and current integrated QA; do not infer speed from agent count or test timings.
- Require counterpart approvals for its own writes/update; this handoff conveys none.

## Implemented Compatibility Adaptation PTO010
- Contract: `.systems/ai/core/parallel-compatibility.md`.
- Sidecar: `.systems/ai/templates/orchestration/compatibility.template.json`, schema1.
- Inspector: `.systems/scripts/inspect-parallel-compatibility`; read-only CLI with explicit Workflow root, target Git root, peer run and mapping paths.
- Consumer: `.systems/scripts/lib/parallel-compatibility.py`.
- Regressions: `.systems/scripts/tests/parallel-compatibility.py`,22 offline tests.

Supported input is an explicit closed subset of AI System contract1, not all
future extensions. Exact run/coordinator/unit/attempt mappings are required.
Every local task/slice label remains supporting metadata, not proof of approval
or existence. Peer source digest is SHA256 of sorted path=sha256 newline rows.
Actual target HEAD and declared source/result bytes/modes are rechecked; unknown
versions, missing sources, aliases, unsafe/key paths and stale results reject.
One complete caller-supplied pool includes both systems' workers and reviewers.
Matching observed termination is required to release occupancy; this is not
authenticated native telemetry. Peer acceptance requires local review/receipt.
Inspection success returns execution_authorized:false and operational_support:false.
No imported PASS, state writes, agent launch, automatic worktree executor, logical
rebase or nested update exists. Native isolation and installed interoperability
remain unverified. AI System must independently review its adapter and installed
local capability; this handoff does not resolve its pending-counterpart gate.

## Capture Parity And Phase Commit Additions
`.systems/scripts/lib/capture-record.py` is the shared semantic consumer for
canonical/scoped/runtime and parent completion checks. Schema1 historical integrity
is not current QA; schema2/3 require current qualified inputs and owning accepted
distillation. Do not downgrade records or broaden historical selectors.
`.systems/ai/core/phase-commit-policy.md` defines future approved planning/capture
commit boundaries. Explicit no-commit wins; ignored-only/no-op has no commit;
Phase8 publication requires real final-owner-yes and push is never inferred.
Opt-in QA binding cannot replace fresh owned artifact closure or approvals.

## Current Supporting Evidence And Adaptation Limits
Actual fresh full003 passed:44registered checks,758unique smoke IDs,fivegroups,
705seconds,exit0. Existing89 orchestration,54 runtime and26 binding regressions,
plus22 adapter tests passed. Parent and independent adversarial/source reviews
corrected privacy, source/receipt closing drift and producer-consumer differences.
Failed earlier runs are not passing evidence. No remote CI, counterpart rollout,
native calls or performance improvement is claimed. Semantic QA remains primary.
Newly created product source needs the existing explicit smoke fixture extras
before commit; fixture selection must not copy arbitrary private/ignored runtime.
Cross-system impact for the full scope is yes; one handoff only, without imported
source approvals, client data, credentials or private project runtime.

## Residual Risk
Cooperative local controls are not distributed locks or a malicious-host sandbox.
Offline tests are finite; native backend/performance verification remains separate.
Current helper intentionally rejects Git-bearing/unsafe transport trees instead
of inventing an adapter. Source is not yet published; no AI System install tested.
