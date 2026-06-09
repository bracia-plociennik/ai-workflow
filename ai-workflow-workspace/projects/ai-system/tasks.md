# AI System Tasks Router

## Purpose

`tasks.md` is the canonical task index and router for this project.

## Task ID Format

`<PROJECT>-<AREA>-<NNN>-<slug>`

## Tasks

Task index state: `phase-2-project-plan-pass`

| Task ID | Title | Risk | Status | Task Card | Spec | Quality | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ASYS-CORE-001-local-ai-system-mode` | Local AI system mode | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Defines isolated root `ai-system/`, workspace, branch policy, and mode docs |
| `ASYS-WORKSPACE-002-workspace-layout-templates` | Workspace layout templates | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Creates template structure under staged `ai-system/` |
| `ASYS-DUMP-003-dump-triage-owner-approval` | Dump triage and owner approval | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Defines classification before file movement |
| `ASYS-MEMORY-004-memory-lifecycle` | Memory lifecycle | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Defines raw memory, distillation, checkpoints, and reminders |
| `ASYS-INSIGHTS-005-system-insights-anonymization` | System insights and anonymization | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Separates system insights from external memory |
| `ASYS-CLIENT-006-client-project-workspaces` | Client and project workspaces | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Adds client and project directory contracts |
| `ASYS-LINKS-007-soft-integrations` | Soft integrations | Low | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Adds link-based context for Mail, Notion, Drive, Notes |
| `ASYS-GUIDE-008-guide-command-routing` | Guide and command routing | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Adds commands for dump, distillation, clients, and projects |
| `ASYS-VALIDATION-009-validators-quality` | Validators and quality | Medium | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Adds checks for privacy boundaries and required README files |
| `ASYS-DOCS-010-human-runbook-examples` | Human runbook and examples | Low | done | none | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/specs/phase-3-ai-system-implementation-package-specification.md` | `AI_WORKFLOW_WORKSPACE_HOME/projects/ai-system/quality/phase-5-ai-system-implementation-package-quality.md` | Documents usage examples |

## Post-final Release Work

- `ASYS-RELEASE-POST-branch-ai-system`: canceled in this repository.
- The temporary `ai-system` branch was removed locally and remotely.
- Future release/setup work belongs in a separate `ai-system` repository.
