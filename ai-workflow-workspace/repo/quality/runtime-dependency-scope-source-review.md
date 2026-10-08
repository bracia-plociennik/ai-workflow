# Runtime Dependency Scope Source Review

- Date: 2026-10-05
- Work mode: workflow-maintenance
- Review mode: advisory; not formal Phase 5 or Phase 8
- Baseline: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05 plus the six-file reviewed worktree diff
- Source result: no blockers found in the changed source
- Whole work result: target installation and phase closure blocked at preflight

## Findings First

No P0/P1/material P2 finding in the bounded source change. Material integration blocker: target runtime reports bind a different AI System product baseline. PPO has 12 missing and 20 changed inputs, and IEV2 has 15 changed inputs. Updating the nested Workflow does not restore target-owned product sources. Do not restamp these reports as PASS or bypass updater QA.

## Intent, DoD And Changed Files

validation-scope.py prunes only project-relative quality/artifacts/node_modules before link handling, prints the exclusion and never follows the destination. qa-evidence.py independently refuses explicit evidence references to that namespace, including real directories. validation-profiles.md documents this as supporting tooling, not evidence. core.sh and manifest.json add one supplemental regression; the frozen 674-case inventory and regions are unchanged. runtime-dependency-scope.py tests the scope helper, independent evidence reader and all four runtime consumers.

The source DoD is met: safe dependency exclusion, strict neighboring evidence, no general symlink waiver, no arbitrary exclusions, no dependency installation and compatibility with existing schema 1. Installed target DoD is not met yet. Source commit is approved; target branch integration, publication and activation are not.

## Adversarial And Integration Matrix

| Case | Verified outcome |
| --- | --- |
| Exact dependency directory, live/dangling link or real directory | excluded without traversal |
| Evidence reference inside excluded dependency directory | rejected by both independent readers |
| Neighboring owned evidence and dependency link identity | preserved |
| Non-exact node_modules path or linked parent | rejected |
| Regular file at dependency directory path | rejected |
| Invalid capture boolean, missing required state, bad filename or incomplete QA | still rejected by actual consumers |
| Frozen smoke IDs and regions | unchanged; supplemental test only |
| Target product baseline mismatch | blocks current target re-assessment; no invented PASS |

Producer-consumer audit: no new persisted field/schema; fixed directory taxonomy is shared by runtime inventory and independent explicit QA-input rejection. Status, naming, QA and capture readers retain their real failure checks. Path case and exact project-relative classification remain strict. The exclusion does not admit package contents as evidence or authorize reading them. Supporting dependency data cannot instruct the checker.

## Verification Evidence

- Actual upstream .systems/scripts/validate-workflow --profile full --progress summary: exit 0, 754 seconds; final validation completion and all-smoke result pass, five groups, 759 cases, no skip.
- Exact-source isolated full fixture: exit 0, 784 seconds, source parity independently compared across 475 selected files; supporting evidence only.
- Fixed dependency test, py_compile, bash syntax and git diff --check: exit 0.
- 43 original historical files across four approved upstream projects are retained byte-for-byte and hash-bound in their replacements; historical deferred task FAIL remains unchanged. PTO current owning inputs were checked before re-rendering; native isolation/performance is not claimed.
- Target WEP source unchanged: 46 focused and 181 integrated work-evidence tests exit 0 using previously approved isolated dependencies.
- Live target symlink lstat inode 282257841 and target remain unchanged. No dependency target was traversed.
- Official updater dry-run succeeded; actual updater and target Phase 7/8 were not performed because baseline preflight failed.

## Review Completeness Gate

- Cross-contract consistency: aligned for changed source; target evidence mismatch explicitly blocked
- Risk/work mode compatibility: aligned; bounded approved high-risk workflow maintenance
- Source-of-truth, permissions, phase gates, artifact state and acceptance criteria reviewed: yes
- Negative-space / adversarial review: completed
- Automated evidence role: supporting-only
- Post-fix full re-review: completed against all six source files
- Reviewed baseline: stated HEAD plus actual source diff and fresh full validation
- Instruction refresh: performed-full
- Instruction baseline: current
- Closure freshness: current for source review; installed integration incomplete
- Policy-boundary adversarial matrix: completed for the filesystem taxonomy; prose instruction-scan matrix not applicable because no instruction regex was changed
- Producer-consumer field audit: completed
- Required-field mapping: complete; no new required persisted fields
- Residual risk: local branch integration and existing unrelated target evidence require separate approval/QA; no installed-scope success is claimed

## Delivery And Capture

Deadline/timebox: none. Quality floor preserved, no cutline or smoke omission. Knowledge capture required; owning state remains pending-quality until installation and target reassessment. No push, activation, publication, owner acceptance extension or Codex memory write.
