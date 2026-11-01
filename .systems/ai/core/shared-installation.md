# Shared Workflow Installation

Shared installation contract: shared-installation-v1.

An explicitly owner-enabled registered AI System can provide one `ai-workflow/`
policy/tool clone for project repositories inside its real root. Each project
keeps its own `ai-workflow-workspace/`; existing persistent durable-worktree
bindings retain their canonical workspace. Shared availability is descriptive,
never enrollment, write approval, current QA or final-owner-yes.

The user registration selects the System. Its local configuration
`ai-workflow-workspace/shared-installation.json` has exactly these fields:

```json
{"schema_version": 1, "enabled": true, "workflow_home": "ai-workflow"}
```

No repository-provided marker selects an unrelated System. Invalid/linked inputs,
an unavailable configured installation, outside-System targets and conflicting
durable-runtime overrides block the affected operation. An activated shared
default must not silently fall back to an older project-local clone.

`resolve-workflow-env` uses the common `durable_runtime.py` consumer. It accepts
`--target <exact-git-root>` and `--mode shared` when executed directly. Sourceable
tools accept `AI_WORKFLOW_TARGET_ROOT`; without it shared mode uses the actual
CWD's Git root. It exports the established four path/mode variables as literal
data, without evaluating source content. Run product commands in the target.
Pass the target explicitly when invoking tools from another directory.

The shared installation itself is not a project target. Explicit `official`
mode still tests the Workflow product source. Standalone projects retain
`official` and nested `target` behavior without enabling shared mode.

Shared `init-workspace --target ROOT` needs no nested clone. It creates only
missing neutral runtime, preserves existing project files, and uses the shared
root-shim template only when root AGENTS.md is absent. Existing custom
instructions require a reviewed merge. `--no-root-agents` preserves the root
entrypoint. Backfill accepts the same target and is non-overwriting.

Shared `bootstrap-target-worktree` retains its actual approval, strong-marker,
Git-identity, custom-instruction and durable-runtime gates; it delegates to the
shared initializer instead of cloning. Source libraries and imported data are
not automatically bootstrapped as projects.

Update the one clone with the existing updater's dirty-tree and FF-only guards
and required full source/smoke validation. Project artifacts are not update
inputs to rewrite. Select an owning runtime only when validating that runtime;
source-only validation uses an explicitly separate neutral workspace and does
not certify historical project QA. Required failing installation gates remain
binding; do not repair or relabel old projects automatically.

Retiring old project installations requires exact owner scope and successful
shared discovery for each affected project. Preserve local changes/commits in a
verified private backup and preserve every project artifact workspace, including
any nonstandard workspace nested inside an obsolete clone. No automatic deletion
follows from configuration alone. No remote publication or source-development
permission follows from installing the shared clone.
