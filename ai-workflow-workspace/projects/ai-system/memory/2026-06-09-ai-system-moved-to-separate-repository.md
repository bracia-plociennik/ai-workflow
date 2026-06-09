# AI System Moved To Separate Repository

## Date

2026-06-09

## Type

project-status

## Status

active

## Summary

The owner decided that `ai-system` should no longer continue as a branch or active project inside the `ai-workflow` repository.

The temporary `ai-system` branch was removed locally and remotely. Future implementation, governance, and workspace setup for AI System should happen in a separate repository.

## Impact

- `ai-workflow` returns to maintaining the public template and dev workspace.
- `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/` remains historical context only.
- New `ai-system` work should not be routed through this project unless the owner explicitly reopens it in this repository.

## Evidence

- Local branch `ai-system` deleted.
- Remote branch `origin/ai-system` deleted.
- Repository is currently on `dev`.
