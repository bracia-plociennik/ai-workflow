# Human Docs

This directory contains human-facing documentation only.

Use it for artifacts intended for the owner or operators, such as summaries, approved decisions, runbooks, audits, and approvals.

The main human operating guide for the workflow/docs/autopilot system is the root [`HUMANS.md`](../../HUMANS.md). That file explains how a person should work with Codex, workflow phases, docs, gates, autopilot, recovery, and git policy.

AI execution artifacts, project plans, task specs, QA evidence, autopilot state, and distillations belong in `docs/projects/<project>/`.

## Global vs Project-Local Human Docs

- Global human instructions live in root `HUMANS.md`.
- Reusable human-facing examples live in `docs/human/EXAMPLE/`.
- Project-specific human artifacts live in `docs/human/<project>/`.
- AI/project runtime artifacts live in `docs/projects/<project>/`, not in `docs/human/`.

## Example Workspace

- `docs/human/EXAMPLE/` demonstrates every supported human-facing artifact type.
