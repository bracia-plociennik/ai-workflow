# Direct Read-Evidence Feasibility Probe

## Scope

- Date: 2026-09-25.
- Goal: determine whether controlled GPT-6 Sol High evals can produce directly observed command/file-read and token evidence instead of relying on agent self-report.
- Environment: isolated `/private/tmp/ai-workflow-pse-controlled-baseline` clone; read-only CLI invocation; no tracked source edit.

## Probe

- Command: `codex exec --ephemeral --ignore-user-config --json -m gpt-6-sol -c 'model_reasoning_effort="high"' -s read-only -C /private/tmp/ai-workflow-pse-controlled-baseline 'Read the first five lines of AGENTS.md. Do not modify files. Report which file you read.'`
- Sandbox-only attempt could not initialize the CLI state database under the normal Codex home. A single escalated read-only probe was approved by the platform reviewer.
- JSONL emitted a completed `command_execution` for `/bin/zsh -lc 'head -n 5 AGENTS.md'` with exit code 0 and the expected five lines.
- `turn.completed` exposed `input_tokens: 50257`, `cached_input_tokens: 36608`, `output_tokens: 259`, and `reasoning_output_tokens: 134` for this probe. These are not baseline/candidate savings.
- CLI stderr warned that project `AGENTS.md` exceeded its remaining autoload budget and was truncated at 32768 bytes. This is a separate safety/coverage concern and is not counted as an explicit tool read.

## Measurement Protocol For Later Phase 4/5

1. Rerun both baseline and candidate with the same CLI version, GPT-6 Sol High, reasoning effort, flags, prompt wrapper, runtime snapshot, permissions and synthetic fixtures. Earlier subagent results remain behavioral discovery, not a metric baseline for this CLI method.
2. Capture JSONL for every case. Count explicit contract reads from completed `command_execution` commands, resolve command paths against the fixed checkout, and classify each read using the case's required-source rubric. Record ambiguous commands as `unknown`, not as measured absence.
3. Report automatic `AGENTS.md` project-doc loading separately from explicit tool reads. The warning shows an autoload truncation boundary; record baseline truncation and verify the candidate keeps mandatory always-on instructions within the actual loaded portion. Do not infer this from tool-read commands.
4. Compare per-case and aggregate irrelevant explicit contract reads. Report token usage separately with cache context; do not treat total input tokens as a pure document-cost metric.
5. If JSONL is incomplete, commands cannot be classified, autoload coverage is unsafe, or the paired runs differ materially, mark efficiency `unknown` and block promotion rather than using self-reported source lists.

## Result And Limits

- Feasible: direct observation of explicit file-read commands and turn token totals in CLI JSONL.
- Not yet established: full per-case collection, reliable classification of commands that read multiple files, automatic project-doc bytes actually consumed, or paired baseline/candidate improvement.
- No candidate was prepared or promoted. No claim of efficiency gain follows from this probe.
