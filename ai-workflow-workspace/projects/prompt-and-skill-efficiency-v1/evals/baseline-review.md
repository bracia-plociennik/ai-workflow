# Synthetic Baseline Review: Exploratory, Not Promotion Evidence

## Configuration And Provenance

- Date: 2026-09-24; tracked instruction snapshot: `7a904f736eaf029bea750c3a735cd53fa61ef4c0`.
- Model/effort: GPT-6 Sol High isolated local subagents, per explicit owner approval.
- Sources: `evals.json`, local synthetic fixtures, agent final reports, and inspected fixture outputs.
- No candidate configuration or paired A/B comparison has run. `run_eval.py` only scaffolded run directories; `.todo` files are not execution transcripts.
- Actual per-agent tool-open trace, tokens, and wall time are unavailable to this review. Agent source lists are self-reports, not instrumented file-open measurements.

## Findings First

1. **P2, comparison validity:** project status and task index changed during baseline-002. At least the tiny-doc and local-completion agents read those mutable artifacts. A later candidate run would see a different environment. These runs are exploratory only, not a controlled paired baseline.
2. **P2, fixture validity:** the skill-review near-miss fixture originally used `SKILL.md` outside the active skills namespace, which failed `check-naming`. It was moved to `skill-source.md` before any candidate run; the affected case was rerun as baseline-003, not pooled with its original baseline-002 output.
3. **Measurement gap:** no reliable tool-open/token telemetry is exposed. Neither a source list nor static line count proves instruction-load savings.

## Observed Cases

| Case | Partition | Agent | Observation | Required/forbidden rubric status |
| --- | --- | --- | --- | --- |
| tiny-doc-fix | development | `01a0d479-5592-7521-afcb-06516fadc632` | Fixed only the README typo; self-reported broad core-document reads. Exact three-line content check; no code test needed. | Scoped edit met; efficient loading not met on self-report; no formal PASS claim. |
| frontend-ui | development | `01a0d447-55e5-7710-b045-939087f74723` | Selected frontend skill; planned responsive settings and loading/validation/recovery states; self-reported broad core reads. | UI/skill coverage met qualitatively; unrelated reads cannot be counted from tool telemetry. |
| backend-only-near-miss | development | `01a0d447-56b2-7bf0-b379-5d3feb53cfd1` | Selected backend-laravel, not frontend; found authorization, overdraft and atomicity risks in synthetic case. | Domain selection and failure review met; no frontend visual QA imposed. |
| blockchain-review | development | `01a0d447-5744-7f01-990c-a9a9b56d8dec` | Selected blockchain skill; reported reentrancy P0 and unrestricted refund P1; no deployment. | Value-flow and authority review met; forbidden external action absent. |
| skill-create | development | `01a0d45f-e60f-70f3-8c89-6754e5a17d61` | Selected system skill-creator and global Codex skill creator; proposed trigger/non-trigger plan without active skill write. | Planning behavior met; extra global skill read requires comparison, not automatic failure. |
| formal-phase-qa | development | `01a0d447-57ee-7923-b534-0ea631106821` | Used Architecture QA contracts; found private access, rollback and storage gaps in synthetic architecture. | Artifact QA lens met; did not assert implementation PASS. |
| skill-review-near-miss | holdout | `01a0d47a-9ab8-7451-bdb9-1c503303f793` | Corrected baseline-003 fixture read-only; used skill-creator, found over-broad trigger in synthetic text; no edit. | Static false-trigger review met; actual trigger frequency untested. |
| mixed-web3-ui | holdout | `01a0d45f-e75d-7ca0-90c5-6a2098fd9180` | Selected frontend and blockchain; opened backend skill for discovery but did not apply it; retained provenance/stale-data boundary. | Main domain reasoning met; discovery overhead remains a candidate improvement, not a proven regression. |
| security-readonly | holdout | `01a0d45f-e816-7e02-ad87-d262c45eccd4` | No domain skill; used security/quality guidance; found missing authorization in synthetic diff; no repair. | Read-only stop and finding met; no formal implementation PASS. |
| local-completion-loop | holdout | `01a0d479-567e-7911-9571-416c3176e5c0` | Implemented synthetic `clamp`; three unit tests passed twice; advisory review found no blocker; reversed bounds remain unspecified. | Local implement-test-inspect-closure met; no failure triggered a fix/retest branch, so that branch remains untested. |

## Decision

- Baseline-001: invalid pilot, excluded.
- Baseline-002/003: useful qualitative discovery only; **not** sufficient to promote a high-risk conditional router or skill-trigger edit.
- Before tracked source changes, create a fixed local evaluation environment with immutable status/context and resettable fixtures; run baseline and candidate with identical prompts, model, effort, permissions, and source snapshot. Preserve original outputs and explicit manual grading per case.
- Local-completion-persistence has no observed early-stop defect in the present fixture. Defer its tracked edit unless a controlled negative case demonstrates a gap.
- No full workflow validator, commit, push, or product operation was part of this exploratory review.
