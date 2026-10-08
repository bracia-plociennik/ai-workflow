# PTO-006 Native Backend Preflight

- Date: 2026-10-04
- Baseline: 8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1 on codex/parallel-task-orchestration-v1; approved PTO-001..005 source union unchanged
- Owner permission: approved bounded plan, maximum two synthetic invocations, isolated fixtures only in /tmp, stop when isolation is not confirmed
- Result: blocked before worker launch; native isolation unverified
- Native worker invocations: 0/2
- Fixture setup, copying, integration or cleanup: not performed
- Source writes: none

## Direct Backend Observations
The available native tool is multi_agent_v1__spawn_agent. Its exposed arguments
are fork_context, items, message, model and reasoning_effort. It has no per-worker
cwd, writable_roots, sandbox/permission profile, isolated environment or verified
capacity parameter. The return identifies agent_id and nickname, not an isolated
filesystem or permissions receipt. Existing messaging/wait/close tools identify
agents but do not establish a worker sandbox or independently prove process cleanup.

The current parent environment permits writes to the AI System tree and other
roots, not just the proposed /tmp fixture. The native interface supplies no
pre-launch observation or enforcement narrowing a new worker to its own root.
Exact backend version, free capacity and inherited model cannot be independently
authenticated through the exposed interface. They remain unknown, not invented.
No worker was spawned to ask it to attest to its own isolation.

## Capability Versus Permission
The owner permission blocker is resolved. The remaining blocker is technical:
native-backend-isolation-unverified. Prompt instructions to write only under /tmp,
fork_context=false, disjoint directory names, worker self-attestation or a clean
post-run diff cannot enforce or authenticate exclusive writable roots.
Do not work around this with another task/thread, shell model runner, API client,
changing global sandbox settings or a simulated native-support claim.

Official background reference:
https://developers.openai.com/api/docs/guides/agents-api/multi-agent
The fetched Agents API documentation says coordinator/subagents share their
environment filesystem and delegation does not create another environment. This
is background only, not proof of this desktop tool implementation or version.
The decisive evidence is the current exposed native tool schema and parent limits.

## Semantic Review And Adversarial Checks
- Approved permission is not backend capability or formal Quality PASS.
- No executable fixture or model dispatch is necessary once preflight fails.
- Two calls is a ceiling, not permission to perform an unisolated first call.
- Earlier PTO-001..005 results remain accepted; PTO-006 AC6 and dependent PTO-007,
  final checkpoint and Phase 8 remain incomplete.
- The request to reach Phase 8 does not waive the explicit stop-on-isolation rule.
- There is no new source diff, no speedup claim, no counterpart write and no
  automatic final-owner-yes, commit or push.

## Supporting Artifact Verification
- Authenticated source reuse and artifact closure: /tmp/pto-006-preflight-artifact-closure-002.json, exit_code 0, coverage complete, source run 8137b58a758c4a87ad48f4e8df9fba81 unchanged.
- Fresh naming, QA evidence, status consistency and distillation-state checks: executed, each exit_code 0. They support the recorded stop, not PTO-006 implementation PASS.
- Initial sandbox-environment receipt reuse was rejected as stale/incomplete; no gate was bypassed. Re-run in the original source-run environment verified the receipt and completed the local checks, without network or workers.
- git diff --check: exit 0; index empty; workspace ignored and untracked.
- Conditional prerequisite artifact assessments refreshed after actual design/readiness comparison, preserving prior reports; no execution readiness or native support inferred.

## Plan Quality Contract
- Plan classification: read-only preflight with approved evidence writes
- DoD source: bounded owner test permission and PTO-006 AC6
- Testable done conditions: inspect actual native interface before dispatch; stop if isolation cannot be confirmed
- Artifact QA route: advisory interface, authority and producer-consumer review
- Implementation QA route: not-applicable; no task implementation or native test executed
- Required verification: native tool schema, current permission boundary, accepted spec and repo baseline
- Quality-ready criteria: honest approval/capability distinction and stopped unsupported dispatch
- Residual risk: no verified native adapter; task completion remains blocked

## Owner Decision Checkpoint
- Interaction mode: none
- Decision state: blocked
- Material decisions: none; bounded test approval is recorded
- Questions asked: none
- Auto-resolved reversible decisions: no worker launch after failed preflight
- Optional owner refinements: a separately approved compatible backend/environment, or explicit plan change
- Decision artifacts: decisions/pto-006-native-backend-authorization.md
- Next route: obtain independently verifiable isolated native backend; otherwise remain stopped

## Contract Compliance
- Work mode: full-project
- Work mode compliance: blocked for dependent implementation, compliant stop for preflight
- Knowledge capture: required
- Capture target: decision and status/evidence; recorded locally, no task distillation
- Privacy/scope check: pass; no fixture/repo/client data sent to workers
- Cross-system impact: yes; final single handoff remains dependent PTO-007 work
- Commit/push/final-owner-yes: not authorized
