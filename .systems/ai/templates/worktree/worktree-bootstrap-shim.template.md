# AI Workflow Worktree Bootstrap Shim

## Shared installation in a registered AI System

A configured shared default uses one policy/tool clone at `${AI_SYSTEM_HOME}/ai-workflow`.
Project repositories keep their own `ai-workflow-workspace/`; no per-project clone is
required. Read `.systems/ai/core/shared-installation.md` before shared init, update
or worktree bootstrap. Resolve the real target from CWD or pass `--target` to init
and the resolver; other shared tools accept `AI_WORKFLOW_TARGET_ROOT`. Preserve
existing custom instructions, artifacts, owner/risk/QA gates and persistent runtime
bindings. The nested-clone instructions below apply to standalone target mode.


For an owner-registered System, resolve its user registration and neutral agent-startup.md from the actual CWD. Read the installed Workflow work-lead.md: System leads covered configurable decisions through one human/System procedure; actual owner reservations, facts/QA, risk/privacy and tool restrictions remain binding. A context/status projection never grants consent. Do not import an ancestor management role into this project. If unbound, standalone human-led Workflow remains unchanged. Unknown bound context permits inspection and blocks affected execution; no implicit installation or enrollment.

Before workflow-governed work:

1. Confirm `ai-workflow-workspace/` or another owner-accepted strong installation marker.
2. Confirm the worktree is not the official AI Workflow repository.
3. Confirm root `AGENTS.md` and nested `ai-workflow/`.
4. If the strong marker exists but `ai-workflow/` is missing, obtain platform approval and run:

```sh
git clone https://github.com/bracia-plociennik/ai-workflow.git ai-workflow
```

5. Verify origin and required clone files, then run:

```sh
ai-workflow/.systems/scripts/init-workspace
```

Stop on missing approval, a weak marker, existing root `AGENTS.md`, wrong origin, dirty clone, ambiguous contents, or official-repo self-clone. Do not overwrite or merge target-owned instructions automatically.
