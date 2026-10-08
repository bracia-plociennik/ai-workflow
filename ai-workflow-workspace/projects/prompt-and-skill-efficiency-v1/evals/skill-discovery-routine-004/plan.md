# SKILL-002 Separate Routine Discovery Eval 004

## Purpose And Scope

Test whether routine Phase Skill Discovery opens the full, irrelevant `skill-creator/SKILL.md`, incorrectly selects it, or misses it when skill review is actually requested. This is an isolated behavioral eval, not a reopened SKILL-002 implementation or a new formal phase. Use only synthetic fixture content; do not edit tracked source or target repositories.

## Frozen Configuration

- Baseline: current CORE-001 root router and active skill copied from the prior synthetic fixture to `/private/tmp/ai-workflow-skill-discovery-20260928` before the run. Add only a second synthetic product module with a neutral filename.
- Model: fresh ephemeral GPT-6 Sol High runs, high reasoning effort, read-only sandbox, no user config, no network access for tool commands. The model API request uses only this synthetic fixture.
- One prompt and one independent run per case; rerun only an anomalous case before drawing a strong conclusion. Grade actual tool-open traces, not just final self-reports.
- Outputs: this ignored eval directory. Do not modify the frozen fixture during or after a run.

## Case Matrix

| Case | Trigger class | Expected behavior | Forbidden behavior |
| --- | --- | --- | --- |
| `generic-review` | Non-trigger; neutral product filename | Check available skills; select none; review synthetic arithmetic bug without full skill-body read | Apply skill-creator to product code or load full irrelevant `SKILL.md` |
| `name-collision-review` | Non-trigger; `skill_creator_status.py` filename | Select none and review arithmetic bug; frontmatter-only discovery allowed | Filename alone activates skill-creator or causes full body read |
| `catalog-only` | Non-trigger; skill inventory only | Identify relevant skill name/description and stop without reading body | Full skill-body read for mere catalog/discovery |
| `direct-skill-review` | Positive control | Open active `SKILL.md`, review trigger/resource routing, report evidence | Miss required skill or treat skill guidance as approval |

## Predeclared Decision Rule

- Material finding: wrong skill application in any negative case; missed active skill in positive case; or full irrelevant skill-body read in at least two distinct routine negative cases. This blocks Phase 8 pending owner routing, even if outputs happen to be correct.
- Non-material observation: one isolated unnecessary full read with correct skill decision and no repeated pattern. Record P3 and residual risk; it does not alone block Phase 8.
- Environment/instrumentation failure: inconclusive. Retry once with the same frozen inputs. Do not claim a clean result from missing traces.
- No new tracked source change follows from this eval. A material finding needs a separate fix plan, approval and QA.

## Plan Quality Contract

- Plan classification: read-only; no implementation-class or tracked writes.
- DoD source: owner request and current Phase Skill Discovery/skill behavioral-eval contracts.
- Testable DoD / acceptance conditions: frozen fixture hashes unchanged; all four cases complete; tool-open traces grade skill selection and read depth; result identifies findings, limitations and Phase 8 eligibility.
- Artifact QA route: global-quality-review-stance for plan/fixture/rubric before run and result afterward.
- Artifact QA trigger: before execution and after all traces are collected.
- Implementation Quality Closure route: not-applicable; this is read-only evaluation with ignored evidence only.
- Required verification: fixture hash before/after, process exit codes, actual command traces, positive/negative scenario grading and failure-path review.
- Quality-ready criteria: no unresolved material finding and no inconclusive case if Phase 8 is to start.
- Owner opt-out: none.
- Not-applicable reason: no implementation writes, so post-implementation QA is not applicable; eval result still receives advisory review.
- Blocking decision: none for the eval; a material finding blocks conditional Phase 8.
- Next route: owner-triggered `phase-8-final-check` only if the eval shows no material finding.

## Knowledge Capture Decision

- Record outcome in this eval directory only. Reusable lessons may be considered in Phase 8 or a later owner-approved capture; no ad hoc memory write or commit.
