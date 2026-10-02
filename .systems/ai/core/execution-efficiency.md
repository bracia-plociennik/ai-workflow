# Execution Efficiency

## Purpose

Reduce repeated execution and formatting rework while preserving semantic QA,
DoD, approvals, privacy, failure-path review and evidence integrity.
Seven explicit capabilities live in .systems/ai/capabilities/execution-efficiency-v1.json.
Missing capability means the existing installed route.

## One Check Plan

Classify checks as product, runtime-artifact, integration or environment.
Record changed producers, known consumers, coverage and each invocation reason.
Use existing validation-checks.json and validation-scope.py for dependency and
owned-runtime coverage. Unknown applicability requires fresh broader checks.
Semantic review precedes scripts and remains current.

```sh
.systems/scripts/validate-workflow --profile scoped \
  --execution-plan /tmp/check-plan.json --evidence-output /tmp/run.json \
  --receipt-key-file /tmp/private-key
```

Iteration plans have schema 1, purpose iteration, workflow_root,
scope_manifest null and checks with id, category, inputs, arguments (empty
in v1) and coverage. Fixed registered validators and declared dependencies only;
no arbitrary command. This route reports coverage unverified and
final_evidence_eligible false. Existing scoped manifests retain coverage authority.

## Source-Bound Check Reuse

Add --reuse-record /tmp/previous-run.json only for iteration. Supply an existing
owner-only key of at least 32 bytes outside published evidence; no implicit key.
HMAC-authenticated receipts bind complete successful planned-check inventory,
full source/dependency inventory, inputs, arguments, coverage, tool binaries,
versions and environment hashes. No environment values enter the receipt.
Changed bindings execute fresh; tampered, failed, timeout, interruption and
incomplete records reject. HEAD alone is provenance, not an input change.
V1 reuses only check-required-artifacts and check-full-qa-verification, whose
inputs are the entire workflow source tree. Other checks execute fresh.
Each check discloses executed/reused/invalidated and its source run.
Not-applicable is separately justified, never executed evidence.
Full, CI and updater always execute fresh. Local authentication assumes key
integrity; a process already possessing the key can create authenticated data.
Reuse never replaces semantic QA, product verification, DoD, approval or PASS.

## Source Verification And Artifact Closure

```sh
.systems/scripts/validate-workflow --profile full --project project-slug \
  --source-receipt /tmp/full-source.json --receipt-key-file /tmp/private-key
python3 .systems/scripts/lib/execution-efficiency.py artifact-closure \
  --workspace /absolute/ai-workflow-workspace --project project-slug \
  --receipt /tmp/full-source.json --key-file /tmp/private-key \
  --output /tmp/artifact-closure.json
```

One fresh full gate after the last source change can produce a source receipt.
Subsequent artifact-only Phase 6/7/8 updates run fresh owned naming, QA, status
and distillation consumers; unchanged source-based contract/privacy rules are
backed by that authenticated full receipt. All current registered checks,
including smoke, source inventory and tools/environment must match.
Runtime is inventoried before/after execution. Source or environment change
invalidates this route. Unknown namespaces/wider capture require their checks.
CI, updater, release verification and explicit full remain fresh independent gates.
The source receipt is supporting evidence; artifact closure grants no formal
PASS, writes or owner approval. Fresh semantic/privacy review remains necessary.

## Historical QA Lifecycle

Current QA compares inputs to live files. Historical/superseded assessment bytes
remain immutable. An explicit project quality-assessments.json registry binds
path, sha256, state, assessed_head, decision and decision_sha256. Admission is
only historical/superseded and only in the owning quality root. Report and
decision hashes must match. The decision states History decision approved,
Approved report, Approved state and Source. No automatic admission, relocation or migration.
Historical integrity validation checks the original schema/input digest without
requiring historical source hashes to match live files. Direct current/status
PASS consumers reject registered history.

## Schema-Driven Quality Producer

prepare-quality-record renders supplied reviewer sections and input references
through qa-evidence.py before atomic no-clobber publication. Safe names,
metadata and input fingerprints are mechanical. Findings, DoD, verdict,
completeness and approvals must be supplied evidence, never invented.
Missing/contradictory evidence blocks publication. Technical Phase 8 remains
awaiting owner. A separate owner-approval record requires a checksum-bound
owning decision: Owner decision final-owner-yes, Approved scope, Source,
and a current passing final check. Technical PASS alone is insufficient.

## Bounded Defect

Low/medium reversible defects may use one compact work record under existing
full-project or workflow-maintenance mode when not already bound to formal
phase gates. This is not a micro-task/micro-project risk exemption.
Require approved scope, testable DoD, known consumers, regression evidence,
semantic review and capture disposition. It replaces duplicate paperwork only.
Security, permissions, credentials, billing, migration, production,
irreversibility, architecture changes and unknown impact exclude eligibility.
Scope growth reroutes. Medium risk still requires accepted plan and QA.
Existing formal gates remain authoritative; eligibility grants no writes.

## Selective Refresh And Preflight

Snapshot schema, scope, stage, approval_reference, repository identity,
baseline HEAD, authority_inputs and actual opened contract paths/hashes.
After resume/compaction perform full refresh: verify repo/status,
accepted scope and relevant authority fingerprints; reread changed sources
and any source needed for the current stage or conflict. Unchanged opened
content can be verified by fingerprint instead of copied into context again.
Missing/conflicting scope stops writes. Do not repeat resolved questions
without new material evidence. Snapshots remain private supporting evidence.
Preflight checks cwd/root, tools, process metadata, output containment and
writable destinations before expensive work. Failure reports the missing
capability early; it cannot grant permission or disable cleanup.

## Whole-Process Timing

Schema 1 process records use clock monotonic, intervals and unknown phases.
Each interval has phase, start, end, measurement observed/estimate, reason
and input_fingerprint. Phases: discovery-refresh, implementation, review,
product-tests, artifact-work, artifact-rework, owner-waiting, publication.
Union observed overlapping intervals; keep child time separate. Estimates
and unmeasured phases are not observed wall time. Reading/model latency
without telemetry is unknown. No raw prompts, secrets or client data.
Collect three samples per variant for bounded multi-consumer defect,
runtime-only closure and shared-contract change with equivalent assertions.
Synthetic script savings do not prove whole-agent/production speedup.
Record no-improvement and inconclusive results.
