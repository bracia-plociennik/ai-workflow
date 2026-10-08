# Eval 004 Remediation Candidate: Behavioral Result

## Fixture And Method

- Frozen baseline fixture: `/private/tmp/ai-workflow-skill-discovery-20260928` (not modified).
- Candidate copy: `/private/tmp/ai-workflow-skill-discovery-20260928-candidate`; only `AGENTS.md` and `operating-model.md` replaced with current router text.
- Model: GPT-6 Sol High, read-only, no client data. Same four case prompts as Eval 004; one completed final-source run per case.
- First local generic attempt (`101`) failed before model execution because sandbox denied Codex's state DB; excluded. Earlier candidate runs `generic-review/102`, `name-collision-review/101`, `catalog-only/101` preceded the final delimiter clarification and are not closure evidence.

## Tool-Open Evidence

| Case | Final run | Skill read | Skill selected | Task result |
| --- | --- | --- | --- | --- |
| `generic-review` | `candidate-runs/generic-review/103/` | `awk` stops at second `---`; no body | none | Found integer-division defect |
| `name-collision-review` | `candidate-runs/name-collision-review/102/` | `awk` stops at second `---`; no body | none | Product filename did not trigger skill |
| `catalog-only` | `candidate-runs/catalog-only/102/` | `awk` stops at second `---`; no body | none | Did not open product source |
| `direct-skill-review` | `candidate-runs/direct-skill-review/101/` | frontmatter, then full `cat SKILL.md` and relevant resources | skill-creator | Completed read-only skill review |

All four final runs exited 0 with `fixture_unchanged: true` and the same candidate fixture digest `7d2be10d...`. The source-open classifications above come from `trace.jsonl` command executions, not the agent's self-report. Baseline Eval 004 had 3/3 full irrelevant skill-body reads and a correct positive control; this candidate has 0/3 full/partial body reads in those negatives while retaining the positive activation.

## Findings And Limits

- No observed false activation or missed positive activation in the four cases.
- A prior candidate catalog run used `sed -n '1,35p'`, spilling into the body despite calling it frontmatter. The final router explicitly requires stopping at the closing delimiter; final catalog trace uses `awk` accordingly.
- Single runs per prompt are directional evidence, not statistical reliability or a token/time saving claim. The model still opened lengthy core contracts in some cases; reducing those reads is separate from this Eval 004 finding.
- The candidate fixture is synthetic. No tracked source, workspace status or client content was exposed to the model; only the copied fixture was available through the eval prompt.
