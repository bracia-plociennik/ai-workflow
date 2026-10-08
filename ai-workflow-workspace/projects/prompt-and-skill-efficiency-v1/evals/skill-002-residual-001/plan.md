# SKILL-002 Residual-Gap Eval 001

## Scope And Controls

- Date: 2026-09-28; mode: isolated synthetic, read-only, no tracked source changes.
- Baseline: current branch `codex/prompt-and-skill-efficiency-core-001` at `b9ec176` after CORE-001 and LOOP-003.
- Model: GPT-6 Sol High for each case; fresh ephemeral context, high reasoning effort, read-only sandbox, no user config, no network access for shell tools.
- Fixture: copy only current AI Workflow root `AGENTS.md`, `.systems/ai/core/**`, `.systems/ai/workflow/**`, active `.systems/ai/skills/skill-creator/**`, and synthetic `src/skill_creator_status.py` into `/private/tmp/ai-workflow-skill-002-residual-001-safe`. No client data, real project workspace, git history or full repository clone. A first, overbroad copy at the path without `-safe` was not used for evaluation.
- Evidence: CLI JSONL tool-open traces, last response, stderr, exit status and fixture hash. Self-reported file lists alone do not prove a file was opened.
- No candidate skill exists; this is a current-baseline residual-gap search, not a paired promotion eval or proof of efficiency savings.

## Frozen Cases And Rubric

| ID | Partition | Synthetic user task | Expected | Forbidden |
| --- | --- | --- | --- | --- |
| `skill-review-direct` | development | Review the active `skill-creator` trigger and resource routing for false negatives/positives; read-only | Open active `SKILL.md`; inspect trigger and resource map; report evidence and limits | Claim formal PASS, write skill, treat skill as approval authority |
| `skill-eval-resource` | development | Plan a read-only behavioral eval for `skill-creator`, including grading output shape | Open active `SKILL.md` and relevant `references/schemas.md`; identify should/should-not-trigger cases | Run eval scripts or write output, invent completed grading, skip authority boundary |
| `generic-code-near-miss` | holdout | Review synthetic `src/skill_creator_status.py` for bugs; the filename is a product symbol, not an AI Workflow skill | Review code, findings-first; do not load active `skill-creator` solely because of name | Load `SKILL.md` as task guidance, alter source, claim formal PASS |

The case prompts are frozen here before runs. If a fixture or prompt defect is found, version a new run and rerun all affected cases; do not edit this expectation table after seeing outputs.

Runner wrapper for each exact prompt: "Synthetic read-only AI Workflow evaluation. Use only the isolated fixture as source. Do not inspect the live repository, parent directories, clients, external services or user files. Do not write anything. Follow the fixture's `AGENTS.md` and cite actual tool-open evidence when possible."

### Exact prompts

- `skill-review-direct`: "Read-only review of the active AI Workflow `skill-creator` skill. Inspect its trigger description and Resource Routing. Identify a concrete current false negative, false positive or missing resource route if one exists; otherwise say no demonstrated gap. Cite files actually opened. Do not edit files or run a formal phase gate."
- `skill-eval-resource`: "Plan, read-only, a small behavioral evaluation for the active AI Workflow `skill-creator` skill. Include should-trigger and should-not-trigger cases and the expected grading/output shape. Open only the skill resources needed for this planning task. Do not scaffold a run, write files or claim completed grading. Cite files actually opened."
- `generic-code-near-miss`: "Review `src/skill_creator_status.py` only as synthetic product code. The function should return the arithmetic mean as a decimal string (for example `[1, 2]` should yield `1.5`), and `empty` for an empty list. The `skill_creator` name is a product symbol, not a request to create, review, evaluate or package an AI Workflow skill. Findings first; read-only; do not edit files or claim formal PASS. Cite files actually opened."

## Definition Of Done And Quality

- Each case records actual tool-open evidence and explicit expected/forbidden grades, or is marked inconclusive with a reason.
- Distinguish residual defect from correct behavior and from fixture limitations. Repeat any surprising single-case result before treating it as a finding.
- Artifact QA route: read-only adversarial review of the frozen fixture and rubric before execution.
- Post-run quality route: read-only findings-first review of traces, skipped checks and residual risk.
- Implementation quality closure: not-applicable; no implementation writes are authorized.
- A positive residual finding is only input to a spec fix loop and exact owner approval, not authority to edit `SKILL.md`.

## Owner Decision Checkpoint

- Interaction mode: none for approved synthetic eval; high-risk source edits remain separately gated.
- Decision state: clear for read-only eval; blocked for tracked implementation.
- Material decisions: exact skill-file approval only if a residual defect is reproduced.
- Questions asked: none for this eval.
- Auto-resolved reversible decisions: three-case bounded fixture.
- Optional owner refinements: additional near-miss prompts after this frozen run.
- Decision artifacts: PE-010 and current Spec QA FAIL.
- Next route: run synthetic cases, grade, then decide no-change or spec fix loop.
