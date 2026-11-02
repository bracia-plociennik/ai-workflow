> Compatible new implementation tasks use `default-sprint.md` V2: bounded targeted QA after acceptance and incremental phases5–7; explicit full verification/Phase8 remains separate. This scoped rule takes precedence over ordinary implementation/checkpoint chaining below. V1 and unsupported tasks retain installed rules. `Phase X` / `-all` follows `phase-x-maintenance.md`; manual only, never autopilot/Dreaming.

# Task Resource Cleanup V1

## One lifecycle and durable evidence
Only new explicitly registered task resources participate. Actual scoped owner approval and installed Workflow gates remain independently required; metadata, --approved, a push and a done label are not permission or QA. Extend the existing owning work record; no second task tracker, approval store, background executor or cron. Ownership pointers/locks in Git administrative metadata contain routing and exclusivity only, no duplicate lifecycle state. Unknown owners or unsupported counterpart versions retain resources.

QA, Capture, checkpoints and their required durable evidence must be written from the beginning into the owning persistent Workflow runtime outside .worktrees/, .tmp/ and OS temporary storage. System project-state contains coordination pointers only. Never create a second technical QA copy. A local Git-administrative binding points at the existing work record and persists across fresh sessions; conflicting environment/source/common identity rejects. Temporary execution without binding is inspect-only. Do not write to inherited tracked workspace snapshots. Historical reports remain byte-preserved, with separate current assessments when needed.

## Task hooks
Before a new task, resolve persistent runtime and inspect resources of the selected owning work record. Before creating a new environment, verify the existing coordinator's scope and resources; register its exact auxiliary environment immediately, before any worker dispatch. Before reusing a registered environment claim/resume it under the common resource lock, then start writers. Keep one executor per resource; cooperating allocation/release/apply share the same canonical-Git lock. Never infer termination from stale heartbeat, accepted output, timeout or a done message.

At task end, finish actual Quality and required distillation/checkpoint, preserve code under a durable canonical Git ref and confirm required publication, stop/confirm all owned workers and release claims, save immutable reviewed closure evidence, then release exact registered resources. Run plan followed by scoped apply for eligible resources. A closure receipt is not semantic QA: run existing installed current QA/Capture consumers before release and again after relevant source/evidence changes. The complete current dependency closure and report hashes remain binding. A current proof referencing/needing the execution environment pins it; do not rewrite that report to permit deletion.

At the next task/session for the same repo, inspect the known owning records and run the same eligible sweep. No unrelated workspace scan/adoption. Cache/scratch can be removed immediately after safe release; whole worktrees wait exactly seven days from safe release, then the first eligible agent run. A resume clears eligibility; repeated release never extends the old timestamp. There is no guarantee a cleanup runs while no agent is working.

## Interface
Workflow .systems/scripts/manage-task-resources takes an existing JSON --record in its durable runtime. init explicitly attaches task_resource_cleanup to that record using --canonical, --workspace, --collection. bind-runtime --target associates the source worktree with it. register --id --kind cache|scratch|worktree --path declares exact resources. claim/resume, release --closure, keep, enable/disable and apply --id require --approved after the caller checks actual scope. inspect and plan are read-only and never create a lock, file or timestamp. System invokes the installed compatible Workflow interface; it does not duplicate deletion code.

The versioned reviewed-task-closure-v1 evidence names owning work, current reports/dependencies with hashes, complete live source roots, confirmed terminated workers/released claims, canonical commit/ref and actual push requirement/remote ref. Keep required QA/Capture outside temporary source roots; final current QA assesses the integrated canonical result. Legacy records without task_resource_cleanup stay inspect-only. Missing evidence, unknown fields/version, stale source/proof or incomplete observation means retained, never a fabricated success.

## Read-only physical storage audit

`audit-storage --path DIR --priority-filesystem /` reports metadata for explicitly
named candidates, including legacy directories. Repeat `--path` as needed.
Parent/child paths and physical aliases are not added twice; inode overlap with
an excluded candidate also excludes an alias estimate. Incomplete inventories are excluded from
aggregate estimates. It never follows symlinks or nested mounts or reads candidate
file contents. Optional paired `--canonical REPO --workspace DURABLE_RUNTIME`
reads registered ownership pointers and reports overlapping keep/active/disabled
state. This is not a complete dependency, activity or task assessment. No
registration or cleanup occurs.

`--exclude-month YYYY-MM --timezone ZONE` excludes a candidate estimate when any
observed path name or mtime matches. Repeat `--exclude-path DIR` for owner
exclusions; overlapping candidates are excluded too. Missing visibility and the
per-candidate `--max-entries` bound or fixed 128-directory depth bound produce an incomplete report. Allocated blocks
are classification potential, not guaranteed freed space. Every report retains
authority none, execution_authorized false and safe_reclaimable_bytes zero.
Existing review, plan, release and apply gates remain independently binding.

Source validation may encounter a local native `AGENTS.override.md` entrypoint.
The naming check accepts only an ignored, untracked root copy; tracked, nested
or nonignored copies remain invalid. This naming rule grants no execution
authority or adapter approval; exact source/entrypoint review remains separate.

## Removal boundaries
Only registered .next/cache, exact generated scratch manifests under collection .tmp/<work-id>/, and auxiliary linked worktrees under collection .worktrees/ are eligible. Canonical repos are never disposable. Cache profile excludes tracked source and rejects evidence/secrets/special/linked/hardlinked content. Git-clean alone is insufficient: ignored/untracked/modified files, nested repositories, submodules, mounts, identity changes or unique data retain a whole environment. Never silently adopt old directories or globally ignore .next as QA input. Establish generated-input classification before new QA; unknown existing inputs keep current strict rules.

Use a complete read-only Linux process/open-FD/mapping/mount/container observation before release and immediately before removal. Missing visibility, sudo, Docker inventory or platform support retains the resource. Only the small read-only observer may use sudo -n; the deletion engine runs unprivileged. No service stop, Docker prune, volume deletion or broad npm/OS cleanup. Resource locking coordinates cooperating callers, not malicious processes sharing the Unix account.

Whole worktrees use ordinary git worktree remove, without --force or branch deletion. Code/ref and required push preservation are independently checked; a push is not a deletion trigger by itself. Generated scratch changes invalidate its registered manifest. Atomic records include a pre-delete intent. After interruption, inspect actual files/Git and keep uncertain state; never replay automatically. Short receipts (resource, result, bytes, skip reason) live in the same work record. Ordinary safe skips stay quiet unless asked, accumulated under an actually activated maintenance policy or blocking the current goal. No per-cache Capture/new phase/owner question.

## Activation and rollback
Publish/test the compatible Workflow consumer before System producer. Officially update only owner-selected installations; no migrations, old environment adoption or installation enrollment. New scopes use the capability after actual compatibility checks. Disable policy to stop further apply; keep records, code refs and evidence. Historical QA/Capture are immutable. Explicit final-owner-yes remains separate from publication authority.

Disable also writes one repo-wide Git-administrative stop marker, checked by every owning record in that repository. Enable removes only that marker under the common lock; explicit per-record disabled/kept states still retain their resources. No lifecycle state is duplicated in that marker.

Closure dependencies may explicitly use role=archive for immutable historical reports/test-run data retained in durable runtime. Their hashes stay required, but a recorded old execution location does not imply a live-source dependency. Current reports cannot use that role; complete independently reviewed source_roots still pin every required live source. A role label never supplies current QA, consent or permission to drop a real dependency. Unknown roles/fields reject.

At the next task use `manage-task-resources list --canonical <verified-repo> --workspace <selected-durable-runtime>` to discover only already registered record pointers in that Git repository. It is read-only, creates nothing and excludes foreign runtime pointers before reading their target. Review actual current owner scope/revocation for each record, then plan and apply only eligible authorized resources; read-only work never applies. No filesystem-wide scan or legacy adoption. System infers the installed executor from the explicit canonical target for list/init as well as existing records.

Task-local Sprint under sprint-iteration.md pins release/apply while iterating, paused, verifying or stale. The executor checks the actual owning record under the shared lock; no state label/owner appearance acceptance can replace current implementation Quality.

## Opt-in reviewed webpack cache profile

Capability: `next-webpack-cache-v1`. Explicit `init --schema 2` creates a new policy;
the existing closed schema1 is never converted. Schema2 retains the same policy
fields. Old consumers reject schema2, including its runtime binding. Update the
compatible Workflow consumer first and review the System counterpart before any
installation; this source capability does not advertise installed/native support.

Only `register --kind cache --profile next-webpack-cache-v1 --cache-review FILE`
selects this profile. The exact target is `<auxiliary-source>/.next/cache/webpack`,
inside the approved `.worktrees` collection with the canonical common Git identity.
It cannot qualify an ancestor, canonical repository, scratch cache or lookalike.
Registration requires actual exact owner scope, `--approved`, a current reviewed
snapshot and activity observation of the whole source environment. Existing data
is explicitly enrolled as existing data; no automatic discovery/adoption. The
resource starts active. Registration is neither release nor apply.

Schema2 profiled resources have exactly the existing fields `id`, `kind`, `path`,
`state`, `keep`, `released_at`, `closure`, `identity`, `manifest`, plus `profile`,
`enrollment_review` (durable path/SHA reference), and `review_revision` (32 lowercase
hex characters). Claim/resume clears closure and enrollment review and replaces
the revision, invalidating old proofs even if bytes did not change. Explicit
`release --closure NEW --cache-review NEW` may renew a review for an active cache;
the proof must use the current inspect revision and current cache/source snapshot.
Without renewal the release proof must match the enrollment review exactly.

The separate closed proof has `schema: 1`, `kind: reviewed-cache-eviction-v1`,
`work_id`, nonempty `reviewed_by`, `state: complete`, `profile`, exact `path`,
`identity` (device/inode), `manifest`, `source`, `source_manifest`, `index_sha256`,
`reports`, `dependencies`, `task_records`, `workers`, `claims`, `reconstruction`,
`dependency_review` and `review_revision`. No unknown fields are accepted. `source`
contains exact `root`, `git_common`, `head`, and root filesystem `identity`.
`dependency_review` has exactly `complete: true`, `cache_required: false`, and a
nonempty `evidence` rationale. `reconstruction` describes reviewed generation from
retained inputs; no command from proof data is executed. These are substantive
review attestations, not application Quality PASS or proof from a filename.
Workers/claims are lists of exact `{state, evidence}` objects, terminated/released
respectively with nonempty evidence; actual termination remains a caller duty.

Reports, dependencies and task_records are unique exact durable owning-runtime
`{path, sha256}` references; reports/tasks are nonempty. No archive escape. Required
reports/dependencies mentioning the target or `.next/cache/webpack` retain it.
Task records cover the one owning task, every record in canonical Git ownership
pointers, and all additional relevant tasks found by actual semantic review.
Unknown or unreviewed relevant tasks retain the cache. Their hash binds the full
parsed JSON, except the owning task's current cache resource and cleanup receipts
(to avoid proof cycles). Other resources/holds, scope and Sprint remain bound.
Malformed, missing, conflicting/foreign pointers and overlapping foreign owners
retain. Explicit active/kept same-record overlaps also retain. Labels and empty
claims never establish factual completeness by themselves.

`source_manifest` exhaustively inventories the current worktree, excluding only
root Git administrative `.git` and this exact webpack subtree. Ignored/untracked
inputs and image/SWC/build siblings remain bound. This deliberately conservative
profile rejects environments containing links, mounts, hardlinks, nested Git or
special files. Known secret-bearing paths are rejected before hashing. There is
no automatic node_modules/.env exemption; unsupported environments are retained.
Entries are `[dir, mode, device, inode]` or
`[file, mode, logical_bytes, sha256, device, inode, allocated_bytes]`.
The cache manifest uses the same format. Its only allowed directories are
`(client|server|edge-server)-(production|development)`; regular filenames directly
inside are `(index|decimal).pack`, optionally `.gz`/`.br` then `.old`. No source,
evidence, secrets, tracked inputs or unknown contents are eligible. Exact HEAD,
index bytes, source/cache/root identities, manifests and evidence must still match.

This proof separates required parent source from reviewed generated cache only
for this profile. It never supplies whole-worktree closure or weakens V1
source_roots pinning/retention. Unknown reconstructibility/dependency resolution
retains. No historical QA is migrated or edited to obtain eligibility.

`review-cache --record RECORD --path EXACT --profile next-webpack-cache-v1`
performs read-only legacy qualification. It returns exact path/profile, identity,
logical/allocated bytes and a SHA-256 of canonical JSON inventory, eligibility and
reasons. An unregistered candidate remains retained even when geometrically valid.
It may inspect geometry for proposed schema2 while clearly preserving the actual
schema1 policy. It creates no lock, policy, enrollment, timestamp or proof; an
optional supplied proof cannot authorize an unregistered candidate. `inspect` and
`plan` stay read-only. Apply always needs separate actual exact scope and approval.

Apply reuses the common Git lock/journal, observes the whole environment and then
revalidates all current evidence/inputs. Descriptor-relative removal checks root
identity and the full approved manifest again before the first unlink, then
deletes only approved entries through checked directory descriptors. New/changed
data, symlinks, races, interruption and partial removal retain recovery state;
there is no recursive deletion of unknown files or automatic replay. Cooperating
exclusive control is required: the Unix account is not isolated from malicious
or noncooperating writers. Disable/keep and pending Sprint retain their precedence.
Never test this feature by evicting a real candidate; acceptance uses disposable
synthetic fixtures, preservation checks and real read-only dry-run only.
