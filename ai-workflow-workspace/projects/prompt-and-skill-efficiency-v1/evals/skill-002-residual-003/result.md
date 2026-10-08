# SKILL-002 Residual-Gap Eval Result

## Verdict

- Current active `skill-creator` has no reproduced false selection or missed required activation in these synthetic cases.
- `P3`, isolated read-efficiency concern: a routine skill-discovery prompt caused the agent to open the entire irrelevant `skill-creator/SKILL.md`, even though it ultimately selected no skill. The one-line description-only candidate produced the same full read and the same correct non-selection. This is not a demonstrated improvement or a basis to promote the candidate.
- The direct-review candidate run suggested adding `scripts/utils.py` to Resource Routing. That is not an accepted finding: `utils.py` is an internal import of `improve_description.py`, not a user-facing entrypoint; no missing helper, failure or wrong resource selection was observed.
- No tracked source change, Spec QA revision, formal quality PASS, commit or push is warranted from this eval. SKILL-002 remains at Spec QA FAIL pending a separate material gap and exact high-risk approval.

## Controls And Evidence

- Fresh ephemeral GPT-6 Sol High, high reasoning effort, CLI read-only sandbox and no user config for each completed case. Fixture contains only AI Workflow contracts, one active system skill and synthetic product code; no full repository clone or client data.
- Baseline fixture hashes stayed constant: `AGENTS.md` `eab833e3...`, `SKILL.md` `645c67b7...`, synthetic source `b835c923...`. Candidate differs only in frontmatter `description`; candidate skill hash `df6c6976...`.
- One first CLI attempt exited 1 before reaching the model because the outer sandbox denied Codex state DB/app-server initialization. It was excluded from behavioral grading. A separately authorized retry ran with CLI state access while the agent remained read-only.
- Prompt hashes match within every baseline/candidate pair: direct review `3fce2047...`, eval resource `595c72ce...`, routine discovery `de8df4e5...`. All six paired runs exited 0. Both routine-discovery metadata files report `fixture_unchanged: true`.

## Findings-First Case Matrix

| Case | Baseline tool-open and behavior | Candidate tool-open and behavior | Grade |
| --- | --- | --- | --- |
| Direct skill review | Opened entire active `SKILL.md`; identified only a wording-based false-positive hypothesis, no observed misroute | Opened entire candidate `SKILL.md`; no trigger misroute, raised an unsupported `utils.py` routing concern | Required activation retained; no proven incremental benefit |
| Skill eval resource | Opened `SKILL.md` and `references/schemas.md`; planned positive/negative cases and grading without writes | Opened `SKILL.md` and `references/schemas.md`; planned cases and grading without writes | Required resource route retained |
| Generic code near-miss | Reviewed synthetic product file, did not open active `SKILL.md`, selected no skill, found arithmetic-mean bug | Not rerun; no candidate-specific signal from the harder discovery case | Baseline negative case passed; candidate unknown |
| Routine discovery near-miss | Opened entire `SKILL.md`, then correctly selected no skill and found arithmetic-mean bug | Opened entire `SKILL.md`, then correctly selected no skill and found arithmetic-mean bug | Same full overread; no false application and no candidate improvement |

Actual opens were graded from `trace.jsonl` command executions, not solely the agents' source lists. The synthetic arithmetic-mean bug is fixture data, not an AI Workflow product finding. The direct-review result's P3 `utils.py` suggestion was checked against the import in `scripts/improve_description.py`; Python resolves that dependency internally when the entrypoint runs.

## Adversarial Review And Limits

- Intent/plan/spec: the eval searched for a post-CORE residual trigger/resource gap without altering tracked source. It did not turn a repaired historical false negative into a new finding.
- Authority: neither configuration wrote files, ran a formal phase gate, claimed formal PASS, or applied skill-creator to product code. The read-only CLI sandbox and post-run hashes support this boundary.
- Producer-consumer: frontmatter is the trigger surface; root skill discovery is the consumer. A full-body read in both variants suggests the consumer's discovery behavior, not this description line alone, controls the observed overread. This is an inference from paired traces, not proven root cause.
- Negative space: only one completed run per case/configuration; no statistical reliability. The candidate was not tested on create, adapt, update, package or legacy skill cases. It therefore cannot be promoted even if a single case had improved.
- Cost: durations were recorded, but one run per case and different model trajectories do not support time/token savings claims.
- Environment: fixture has no `.git` or runtime workspace; agents disclosed those limits. Initial outer-sandbox CLI failure was excluded. The read-only sandbox prevented writes but did not itself provide a filesystem no-read boundary outside the fixture; reviewed command traces showed fixture-relative reads and no observed external source access.
- Freshness: all runs used the same copied CORE-001 router and skill body; no tracked changes occurred during the run.

## Quality Closure

- Findings/blockers: no P0/P1/material P2 in active skill behavior from this eval; one P3 synthetic overread with an ineffective description-only candidate.
- DoD: actual open traces and expected/forbidden grades are recorded; fixture and prompt parity verified. Residual-gap improvement was not demonstrated.
- Skipped checks: no full repository validation, because no tracked source changed; no broader skill regression suite or repeated near-miss run, so promotion remains blocked.
- Residual risk: a different prompt may still reveal a skill-routing defect; the current data supports no change to active `SKILL.md`.
- Recommended route: keep Spec QA FAIL and either close SKILL-002 no-change with owner decision or plan a separate discovery-routing experiment against the root router. Do not edit `SKILL.md` based on this candidate.

## Knowledge Capture Decision

- Recommended: project memory at a later authorized distillation/checkpoint; no ad hoc durable memory write from this eval.
- Lesson candidate: distinguish reading a skill for discovery from applying it; test the routing consumer and candidate separately before changing active trigger wording.
- Privacy check: pass; synthetic fixture and system contracts only.
