# Pre-final Compatibility Architecture Delta

PTO-D10 adds a pure read-only inspector, not a second execution pool.
AI System contract1 is an external envelope, not a Workflow manifest.
An explicit closed mapping binds units to local task/slice/read paths and one
complete run-wide capacity observation, including external workers and reviewers.
Unknown completeness blocks budget qualification. It cannot verify backend
enforcement: operational_support and execution_authorized stay false.

Source verification checks actual target HEAD and each declared stable manifest
file using the peer path=sha256-newline digest algorithm. Record actual modes in a
separate observation fingerprint; this is not a whole-repo lock or output digest.
Workflow capability/inventory/output digests retain their separate populations.
Before/after input reads and target HEAD checks reject mixed snapshots.

Strict bounded parsing rejects duplicate keys/IDs/paths, unsupported versions,
unsafe/private/linked input, non-finite values, missing facts, stale results,
retired identities, incomplete mapping/graph, overlaps and unknown capacity.
No counterpart code or worker commands execute. State mappings are review
dispositions, not imported local acceptance, QA or approvals.

Git-bearing worker trees require a separately verified adapter; never hide .git.
Logical rebase remains unsupported; new baseline needs fresh local run/review.
Cross-task results require owning formal Quality/capture/checkpoint. Existing
reducer/capability pins remain unchanged; native interoperability is not claimed.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: PTO-010 AC1..8 and PTO-D10
- Testable DoD / acceptance conditions: closed mapping, actual baseline/digest checks, all six gap dispositions and authority preservation
- Artifact QA route: phase-1-architecture-qa
- Artifact QA trigger: complete delta before Plan QA and source writes
- Implementation Quality Closure route: phase-5-quality
- Required verification: producer-consumer and adversarial fixtures, semantic review, fresh full source validation
- Quality-ready criteria: no material findings, all AC evidenced and current
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none; native execution explicitly excluded
- Next route: Plan QA then Spec QA

## Owner Decision Checkpoint
- Interaction mode: none
- Decision state: clear
- Material decisions: PTO-D10
- Questions asked: prior scope question resolved
- Auto-resolved reversible decisions: existing branch, serial implementation
- Optional owner refinements: future native adapter, outside this release
- Decision artifacts: decisions/pto-010-compatibility-approval.md
- Next route: artifact QA

## Optional Knowledge Capture
- Capture recommended: yes
- Target: external-memory
- Reason: exact counterpart mappings and limits
- Owner decision required: no, shared impact approved
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Inspection is not native execution
- Suggested entry summary: Compatibility metadata remains supporting-only.
