# Prompting Templates

## Purpose

This directory contains reusable templates for AI Workflow prompt composition artifacts.

These templates are advisory. They do not override `AGENTS.md`, `.systems/ai/core/**`, workflow phase files, risk policy, permissions, evidence requirements, owner approvals, or accepted task scope.

## Templates

- `prompt-module.template.md` - reusable framing module.
- `role-profile.template.md` - workflow-phase or project-domain role profile.
- `variable-pack.template.md` - project/task variables with sources and assumptions.
- `workflow-phase-role.template.md` - phase-specific role profile.
- `ai-workflow-maintenance-baseline.template.md` - baseline role/variables for maintaining AI Workflow itself.

## Rules

- Keep generated project-specific artifacts under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/`, not under `.systems/**`.
- Mark inferred values and assumptions explicitly.
- Add source labels for project context, owner decisions, memory, specs, and repository evidence.
- If a generated artifact conflicts with policy, status, architecture, plan, spec, or owner decision, refresh or ignore it.

