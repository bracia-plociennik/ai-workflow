# 000. IDEA VALIDATION - Codex

## Purpose

This phase turns a raw owner brain dump into a validated project idea before `0_context.md` exists.

Use it when the owner has an idea, feature direction, product change, or vague initiative and wants Codex to challenge, clarify, and stabilize it before the formal workflow starts.

## Inputs

- owner brain dump, notes, voice transcript, rough prompt, or imported idea document;
- optional repo-wide context from `docs/repo/CONTEXT.md`;
- optional existing project or human-facing notes.

## Output

Write the accepted validation artifact to:

```text
docs/projects/<project>/intake/000_idea_validation.md
```

This phase does not replace `0_context.md`. It produces the material from which `0_context.md` can be created after the owner accepts the validated idea.

## Required Analysis

Codex must classify the idea into:

- what is strong and should definitely stay;
- what is weak and should be improved or removed;
- what is missing and should be added before project context is created;
- unresolved decisions, classified as `auto-resolvable`, `high-impact`, `critical-risk`, or `blocked-by-missing-facts`;
- known constraints from repo context;
- recommended next shape of the idea.

## Gate Rule

`0_context.md` may be created only after this phase has one of these results:

- `accepted`: owner accepts the validated idea;
- `accepted_with_changes`: owner accepts the idea after documented changes;
- `blocked`: missing owner decisions or facts prevent context creation.

Do not create architecture, project plan, task specs, or implementation work from an unvalidated brain dump.

## Out Of Scope

This phase does not:

- create product architecture;
- create project task plans;
- implement code;
- approve critical-risk decisions;
- perform external side effects.

## Output Checklist

- idea summary is concise and concrete;
- strong parts are listed;
- weak parts are listed with recommendation;
- missing parts are listed with owner/action requirement;
- decisions are classified;
- blockers are explicit;
- next valid step is `create 0_context.md`, `revise idea`, or `owner decision`.

## Prompt Base

```text
Run 000. IDEA VALIDATION.

Use the owner's brain dump as input. Check it against docs/repo/CONTEXT.md if available.

Return:
- what is good and should stay;
- what is weak and should be improved or removed;
- what is missing and should be added;
- decisions required, with classes;
- blocking unknowns;
- recommended next version of the idea;
- gate result: accepted, accepted_with_changes, or blocked.

Do not create 0_context.md until the validated idea is accepted.
```
