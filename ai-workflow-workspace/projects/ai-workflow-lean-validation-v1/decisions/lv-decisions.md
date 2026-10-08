# Project Decisions

## LV-DEC-001 Delivery Constraint - Resolved

- Class: owner-preference.
- Statement: deadline/timebox for this project.
- Owner answer: "Bez deadline'u i timeboxu dla ai-workflow-lean-validation-v1. Wznow planning-range LV001-LV006."
- Source: current explicit owner message, 2026-09-29.
- Impact: no calendar cap; no reduction in safety, QA or coverage. This is not inherited from the previous project.
- Status: approved.

## Planning Authority

The two explicit range requests authorize ignored architecture/plan/specs and their formal artifact QA. They do not authorize tracked changes, model execution, benchmarks, Git changes or formal implementation quality approval.
Architecture design elaborates accepted Plan V2; implementation-stage interface changes require spec refresh and QA.

## Later Decisions (Not Planning Blockers)

| ID | Class | Decision | Why / blocking point | Recommendation and impact | Alternative and impact | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| LV-DEC-002 | high-impact | Implementation range, exact write set and branch/base | Before source writes | Separate new branch from reviewed baseline; isolates the closed project | Owner-selected reconciled base; needs fresh intake/spec checks | pending |
| LV-DEC-003 | high-impact | Model/method/configuration and synthetic eval execution | Before LV005 baseline/model run | Approved isolated synthetic baseline/candidate; no repository/customer payload | Defer LV005; no behavioral improvement or whole-program completion claim | pending |
| LV-DEC-004 | owner-preference | Shared impact for AI System | Before commit/cross-system handoff | yes; one privacy-safe conceptual handoff | no with reason; upstream-only result | pending |

Durable decision path for each row: decisions/lv-decisions.md. No current source write permission is inferred from recommendations.

## Implementation Readiness Audit: 2026-09-29

- Run: autopilot-002; readiness-result awaiting-owner, state awaiting-owner.
- LV-DEC-002: pending high-risk source approval and branch/base reconciliation. Current HEAD f362ce3 and cached origin/main 1b45483 diverge at e8b99e8; remote freshness has not been checked. Recommend a new lean-validation branch in this checkout from f362ce3, followed by non-destructive main reconciliation and affected Spec QA refresh before source writes.
- LV-DEC-003: pending synthetic-only model eval decision for LV005. A full uninterrupted LV001-LV006 range cannot be ready while this choice is pending; a narrower approved LV001-LV004 range is an alternative.
- LV-DEC-004: pending yes/no shared impact for AI System. It is due before commit or handoff, not before implementation-range readiness.
- Reviewable options and impacts: autopilot/runs/autopilot-002/decision-brief.md. No answer or approval was inferred from this readiness request.

## Implementation Owner Decisions: 2026-09-29

- Source: explicit owner message: "Zgadzam się na high risk implementacje. Wybierz odpowiedni branch. Zgoda na izolowany syntetyczny eval. Uwzględnij Handoff do ai system. Wystartuj implementatjon-range."
- LV-DEC-002: approved for high-risk LV001-LV006 implementation in a separate branch chosen by the agent. Selected `codex/ai-workflow-lean-validation-v1` from reviewed `f362ce3`, with non-destructive merge of fetched canonical `origin/main` (`1b45483`) before source implementation. Approval does not authorize force push, reset or Phase 8.
- LV-DEC-003: approved for isolated synthetic-only LV005 eval. Use identical baseline/candidate configuration and no repository or client payload. The exact model execution mechanism, availability and frozen fixture still require a pre-eval safety check.
- LV-DEC-004: yes; prepare one privacy-safe conceptual External Memory handoff to AI System after accepted quality evidence. No write to AI System itself is authorized.
- State: owner decisions resolved. Pre-write branch reconciliation, source/Spec QA refresh, safe environment and readiness gates still apply.

## LV-DEC-005 High-Risk Phase 5 Gate: 2026-09-29

- Class: high-impact.
- Source: owner message, "Zatwierdzam high-risk Phase 5 dla LV001. Wykonaj formalny gate i przy PASS zatrzymaj sie, bez commita."
- Decision: formal Phase 5 review for LV001 approved; stop immediately after a supported PASS.
- Boundary: no Phase 6/7, LV002, commit or push is authorized by this decision.
- Status: applied; quality/phase-5-lv-core-001-verdict-integrity-quality.md records the formal result.

## LV-DEC-006 LV002 Quality, Fix And Capture: 2026-09-30

- Class: high-impact.
- Source: owner approved high-risk Phase 5 for LV002, Phase 6 and a local commit at PASS, then readiness LV003. After the timing-boundary P2 was reported, the owner explicitly said "Zatwierdzam fix-loop".
- Decision: minimal in-scope fix loop, fresh formal Quality verdict, then Phase 6 and local commit only if PASS; prepare LV003 readiness afterwards.
- Boundary: no push, Phase 8 or final closure. Fix remains within the accepted eight-file LV002 ceiling.
- Status: applied; corrected formal Quality PASS, accepted Phase 6 and local commit 0070814 completed. LV003 refreshed Spec QA/readiness completed; stopped before LV003 implementation, with no push.

## LV-DEC-007 LV003 High-Risk Quality And Current Prerequisite Assessment - Pending

- Class: high-impact.
- Source: current owner resumed implementation-range from LV003; this is source implementation authority under LV-DEC-002, not a new formal high-risk Phase 5 approval.
- Statement: approve formal Phase 5 for LV003 with genuine current spec/LV001/LV002 regression assessments after expected source changes.
- Why needed now: source implementation and isolated full verification completed, but three bound prior QA inputs are stale in the actual runtime.
- Recommendation and impact: approve the quality route; preserve old runs and frozen LV002 baselines, append fresh evidence only after complete semantic regression review, then run actual project validation.
- Alternative and impact: read-only adversarial current-diff review first; no formal result or range advancement.
- Blocking point: before formal quality verdict, Phase 6/7, LV004 or commit.
- Owner answer: pending.
- Decision artifact: decisions/lv-decisions.md; detailed queue in escalations/lv003-quality-approval-and-freshness.md.
- Status: awaiting-owner. No Phase 5 PASS/FAIL, commit or push authorized by this pending decision.

## LV-DEC-008 Remaining Range And Explicit Final Check - Approved

- Class: high-impact.
- Source: owner message on 2026-09-30 approving high-risk LV003 Phase 5 with genuine Spec QA/LV001/LV002 regression, then Phase 6/local commit, checkpoint/local commit and sequential LV004-LV006, ending at Phase 8 without final-owner-yes.
- LV-DEC-007 owner answer: approved by this new decision; the earlier pending record is historical, not current authority.
- Approved scope: existing accepted task ceilings, current dependency/spec/readiness refreshes, formal high-risk QA, in-scope evidence-backed fix loops, Phase 6/7 and local source commits at supported PASS. No deadline/timebox remains LV-DEC-001.
- Phase 8: explicitly owner-triggered after the implementation-range final checkpoint; not added to automatic autopilot range.
- Boundaries: no push, destructive Git, network/customer disclosure, new source scope or final-owner-yes. An ignored-only checkpoint/capture creates no empty Git commit.
- LV004 fallback and LV005 promotion gates remain active; uncertain equivalence or behavior requires a recorded scope decision, not invented completion.
- Shared impact: yes, existing single AI System handoff; no counterpart edits.
- Status: approved; applied incrementally only after actual phase evidence.
