# Phase Commit Policy

## Authority And Boundaries
This installed policy applies to future owner-approved implementation scopes.
It is not retroactive: explicit no-commit always wins. Risk, privacy, semantic
QA, DoD, staging scope, owner approvals and counterpart impact remain required.
The coordinator is the single index/commit owner; worker submission grants none.
No automatic push, PR, merge, force-add, reset, stash, history rewrite or empty
commit. Ignored-only/no-op capture reports commit not-required. A pending
cross-system impact blocks commit/handoff, never resolved by no-question opt-out.

| Boundary | Required evidence | Local commit behavior |
| --- | --- | --- |
| planning-range end | current artifact QA and publishable approved tracked changes | scoped commit, stop for implementation readiness |
| phase-6-distillation | actual task Quality, accepted distillation, coherent approved tracked scope | implementation/capture commit unless explicitly forbidden |
| phase-7-checkpoint | current atomic checkpoint and new tracked synchronization | scoped commit; no changes means not-required |
| phase-8-final-check | current technical gate AND actual scoped final-owner-yes | final closure commit; awaiting owner means none |

Select a dedicated branch before substantive high-risk/shared-contract or
multi-task implementation. Reuse the correct owned branch. Detached HEAD,
unknown ownership, unrelated staging or collisions stop; never auto-stash/reset.
Commit only the reviewed exact staging scope. Failed commit/hook mutation means
re-read, fix and fresh applicable QA, not a fabricated publication success.

## Immutable Freshness Protocol
Capability phase-commit-policy-v1 opts into full-qa-verification-v3 with
bound:implementation-quality and Capture schema3. V1 bound eligibility covers
implementation quality; other QA kinds retain strict installed behavior and need
fresh assessment if their baselines change. V2/schema1/schema2 remain unchanged.
Frozen old readers reject V3/schema3 as current evidence. No V2 marker or old V2
historical run is embedded in V3. Unknown versions fail closed.

Before reviewer QA, produce source snapshot schema1 with project/task identity,
actual typed repository/common-directory identities and baseline HEAD/tree,
independently selected complete source populations, modes, hashes and deletion
tombstones. Fixed workflow roots are .systems, .github, AGENTS.md, HUMANS.md,
README.md and .gitignore. Baseline/tree/index/untracked union detects new inputs;
tracked paths remain in scope regardless of ignore changes. Unknown ignored
production input, unsafe path, symlink, gitlink or nested repository rejects.
Only generated __pycache__ bytecode is excluded. Legacy/context skill imports are
typed data, never active dependency guidance. Explicit dependencies must be
existing active sources. Inventory membership is not a submitted ignore list.

Required stable evidence roles are spec-dod, owner-approval, implementation and
review under the exact owning project. Snapshot never hashes the QA output or
future result commit. QA binds that immutable snapshot and stable evidence;
read-time binding recomputes equivalence and hashes the unchanged QA. The graph
is snapshot -> reviewed QA -> computed result, not a self-referential receipt.

The verifier checks the live complete population and, after a commit, the actual
committed tree AND index. Expected first source-only commit extends the exact
baseline. V1 does not authenticate tracked runtime commit chains: any runtime
path or later nonempty commit rejects reuse and requires fresh QA. Ignored
artifact-only closure instead runs fresh owned checks without a Git commit.
No workspace prefix or ancestry alone grants equivalence. Merge/rebase,
unrelated staged content, partial staging, hook changes, extra paths, mode/delete
or dependency drift, missing evidence, FAIL/history/wrong identity reject.
Saved eligible JSON is supporting-only and never loaded as authority.

Existing HMAC full-source receipts authenticate only workflow bytes, registered
checks and tools/environment. An explicit owner-only key must already exist;
AI_WORKFLOW_QA_BINDING_KEY_FILE declares it for consumers. The key content is
never emitted. No implicit key or changed receipt is admitted. Modes and paths
are independently compared. Target roots can be inventoried only with explicit
typed workspace/install exclusions; existing receipts do not attest target
product checks, so target equivalence remains ineligible and requires fresh QA.

Changes to DoD, approvals, semantic scope, review or source require re-QA. Mutable
status/capture/QA outputs are separate typed closure inputs, not snapshot ignores;
run fresh owned artifact checks after each runtime closure. Full-required CI,
updater and source verification remain fresh. Green scripts never equal PASS.

## Read-only Interfaces
verify-qa-commit-binding snapshot writes only a new ignored/temporary evidence
file; verify performs no Git mutation or network. Missing proof exits nonzero.
Consumer-computed source_equivalence_verified is not accepted from stored input.
Opt-in migration is explicit; never downgrade schema3 or restamp old report hashes.
