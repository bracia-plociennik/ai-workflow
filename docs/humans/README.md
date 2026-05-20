# Human Docs

This directory contains human-facing documentation only.

Use it for artifacts intended for the owner or operators, such as summaries, approved decisions, runbooks, audits, approvals, and human-readable plans.

The main human operating guide for the workflow/docs/autopilot system is the root [`HUMANS.md`](../../HUMANS.md). That file explains how a person should work with Codex, workflow phases, docs, gates, autopilot, recovery, and git policy.

AI execution artifacts, authoritative project plans, task specs, QA evidence, autopilot state, and distillations belong in `docs/projects/<project>/`.

Human-facing plans in `docs/humans/<project>/plans/` are tracking and coordination artifacts for people. They do not replace workflow plans under `docs/projects/<project>/planning/`.

## Global vs Project-Local Human Docs

- Global human instructions live in root `HUMANS.md`.
- Reusable human-facing examples live in `docs/humans/EXAMPLE/`.
- Project-specific human artifacts live in `docs/humans/<project>/`.
- AI/project runtime artifacts live in `docs/projects/<project>/`, not in `docs/humans/`.

## Example Workspace

- `docs/humans/EXAMPLE/` demonstrates every supported human-facing artifact type.
