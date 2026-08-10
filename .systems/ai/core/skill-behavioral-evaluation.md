# Optional Skill Behavioral Evaluation Contract

## Purpose

Active skills share a layout contract, but behavioral evaluation is optional in
v1. A skill without an evaluation plan remains valid and usable.

When an evaluation exists, it must record:

- skill;
- trigger scenarios and non-trigger scenarios;
- baseline configuration and with-skill configuration;
- expected behavior and forbidden behavior;
- evidence, result, and residual risk.

The preferred machine-readable shape is `evals/evals.json`, compatible with the
skill-creator evaluation flow. Evaluation modes must be safe and deterministic;
runtime reports belong in workspace or temporary output, outside active skill
directories and never inside `.systems/ai/skills/**`.

Evaluation is supporting evidence only. It cannot approve implementation, skip
workflow gates, change risk or permissions, or require a mandatory backfill for
existing skills. Coverage inventory and candidate evals are allowed without
executing them.
