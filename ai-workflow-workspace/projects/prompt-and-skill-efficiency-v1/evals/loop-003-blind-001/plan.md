# LOOP-003 Blind Local Completion Eval

## Scope

- Supporting behavioral eval only. LOOP-003 remains deferred; this is not Spec QA, implementation-range approval, or formal Phase 5.
- Model: GPT-6 Sol High in one fresh, isolated local context.
- Official tracked source, project status, clients, production, network, commits, pushes, and PRs are out of scope.
- Writes are limited to this ignored eval evidence and a disposable local checkout. The agent may edit only its synthetic implementation file.
- The owner opted out of a deadline/timebox for this project, not of quality or safety gates.

## Blindness And Freeze

- Clone tracked HEAD locally into a fresh disposable checkout. Do not copy the prior eval, this controller plan, rubric, result, or conversation into the agent workspace.
- Supply only the synthetic fixture, normal task brief, current repository instructions, and minimal runtime status for a side task.
- Before the run, freeze fixture, tests, prompt, expected behavior, and grading criteria with SHA-256 hashes.
- The task prompt does not mention the planted helper defect, the LOOP-003 hypothesis, or a required failure-fix-retest sequence.
- Do not edit the frozen fixture or rubric after observing the model output. No cherry-picked retries; an infrastructure failure before the agent starts may be retried with the same inputs and disclosed.

## Implementation Slice Plan

| Slice | Goal | Evidence | Acceptance |
| --- | --- | --- | --- |
| E1 | Freeze the fixture and controller rubric | hashes, baseline tests, prompt review | deterministic tests and no leaked defect hint |
| E2 | Run one isolated agent task | JSONL trace, final file, command output | current model/configuration, no out-of-scope write |
| E3 | Independently grade and review | ordered trace, final diff, controller retest | findings-first advisory verdict with limits |

## Plan Quality Contract

- Classification: implementation-capable only inside the disposable fixture.
- DoD source: owner request, normal task brief, and frozen test contract.
- Testable done conditions: implementation meets the task DoD; trace shows whether a test failed and what happened next; unchanged tests; independent controller retest; no official tracked changes.
- Artifact QA route: read-only review of prompt, fixture, expected behavior and rubric before execution.
- Post-implementation quality route: advisory global quality review of the run and final fixture.
- Required verification: baseline test, trace order, file-change audit, full fixture test, negative/edge paths, residual risk.
- Quality-ready criteria: result classified as evidence of persistence, early stop, preemptive fix/inconclusive, or blocked for a genuine safety reason. A green final test alone is insufficient.
- Opt-out: none for QA; deadline/timebox owner opt-out remains.
- Formal PASS: not applicable; no formal LOOP-003 quality phase is running.
- Blocking route: stop on network/external effect, tracked edit, missing safe environment, or permission conflict.

## Decision Boundary

One synthetic run cannot establish statistical reliability or authorize high-risk LOOP-003 policy edits. Any tracked change still requires PE-003 reopening, accepted specification and QA, exact write approval, and paired negative-case evidence.
