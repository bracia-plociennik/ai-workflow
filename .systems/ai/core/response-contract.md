# response-contract.md

## Purpose

This file defines the required user-facing response shape for Codex when working inside a repository governed by AI Workflow.

The response contract is communication policy. It does not create a new workflow phase and it never replaces phase gates, evidence, status, approval, or Definition of Done.

## When It Applies

Every substantive response to the user must end with a `Co dalej?` footer.

Substantive responses include:

- completed phase summaries;
- completed implementation or documentation work;
- QA, audit, validation, review, and blocker reports;
- guide, recovery, resume, decision review, change request, rollback, side-task, micro-task, micro-project, and autopilot responses;
- clarification responses when the user command is too short or ambiguous to execute safely.

Do not append the footer inside strict machine-readable output such as JSON-only, patch-only, or exact-template output requested by the user. In that case, include the footer in the nearest surrounding normal human-facing response.

## Required Footer

Use this exact section shape:

````text
Co dalej?

Rekomendacja:
<one concrete next step>.
Wpływ: <what this unlocks, protects, or makes clearer>.
Napisz:
```
<copy-paste prompt for the recommended path>
```

Alternatywa:
<one safe alternative next step>.
Wpływ: <tradeoff and when this path is useful>.
Napisz:
```
<copy-paste prompt for the alternative path>
```
````

Do not provide a long option menu. Include `Inny pomysł:` only when the user explicitly asks for extra ideas or when the current interaction is brainstorming.

## Recommendation Sources

Choose the recommendation from the highest applicable source:

1. The user's explicit intent, when it is safe and does not bypass gates.
2. The current phase file's `Next allowed phases`.
3. `workspace/repo/core/status.md`, active project `status.md`, `tasks.md`, current plan, spec, quality evidence, decisions, checkpoint, or autopilot run state.
4. Stop conditions from `AGENTS.md`, `.systems/ai/core/operating-model.md`, risk, permissions, commands, Definition of Done, and prompt-injection policy.
5. `.systems/ai/core/guide.md`, `.systems/ai/core/change-requests.md`, and `.systems/ai/core/command-routing.md` for lost-user, short-command, recovery, owner change request, rollback, side-task, micro-task, micro-project, and autopilot routing.
6. Fresh install defaults: if repo runtime is missing or stale, recommend repo intake; if repo intake is complete but no project workspace exists, recommend project workspace creation.

If these sources conflict, recommend recovery or reconciliation instead of guessing.

## Alternative Selection

The alternative must be:

- safe under the same gates and policy;
- meaningfully different from the recommendation;
- useful for a real user tradeoff, such as slower but safer review, narrower read-only audit, manual execution instead of autopilot, dry-run before mutation, or promotion from micro-task to full workflow.

The alternative must not suggest skipping tests, evidence, QA, approval, Definition of Done, stop conditions, final owner approval, or risk policy.

Both `Napisz:` prompts must be directly usable by the user. If a prompt depends on a missing project, task, phase, or owner decision, make that missing value explicit instead of guessing.

## Common Cases

### Completed Phase

Recommendation should be the next allowed phase when gates are satisfied. Alternative should usually be a manual review, QA rerun, checkpoint, or read-only drift check.

### Blocked Phase

Recommendation should resolve the highest-impact blocker. Alternative should be a narrower read-only status or evidence audit.

### Implementation Complete

Recommendation should run or finish quality verification, distillation, checkpoint, or the next task depending on status. Alternative should be owner review or a narrower validation pass.

### QA FAIL

Recommendation should route to the matching fix loop. Alternative should be an owner review of the failure if the fix requires a scope or risk decision.

### Guide Mode

Guide mode remains a specialized orientation response. It must still include current status, sources checked, blockers, one recommendation with impact, one alternative with impact, and copy-paste prompts for both paths. The `Co dalej?` footer can serve as the recommendation and alternative section.

### Short Or Ambiguous Command

If the user's command can be safely resolved from status and artifacts, route it to the safest matching phase. If not, ask for the missing decision. Recommendation should state the preferred interpretation and impact; alternative should state the other plausible interpretation and impact.

### Micro-task Or Micro-project

Recommendation can close the micro artifact with evidence or perform the next low-risk step. Alternative should promote the work to the full workflow when scope, risk, or verification is uncertain.

### Autopilot

Recommendation can start or continue supervised autopilot only when gates allow it. Alternative should be manual execution or dry-run/status review. High-risk and critical-risk work must route to approval or human-led execution.

## Quality Bar

The footer is invalid when:

- it lists many options instead of one recommendation and one alternative;
- the recommendation ignores a blocker;
- the alternative is just a weaker version of the same step;
- either option would bypass gates, evidence, approval, risk policy, or final owner approval;
- either `Napisz:` block is missing, vague, or not actionable;
- impact is vague, for example `better workflow` without saying what becomes safer, clearer, faster, or unblocked.
