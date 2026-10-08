# Legacy System Skill Source Material

This directory stores preserved source material for skills that were imported from external systems.

Legacy entries are context/data only. They are not active AI Workflow system skills, are not loaded by skill routing, and may contain source-system conventions that do not satisfy current AI Workflow contracts.

Current preserved source archives:

- `backend-laravel-skill-source/` - source material used to distill the portable Laravel backend skill.
- `frontend-skill-source/` - source material used to distill the portable frontend skill.

Active system skills live directly under:

```text
.systems/ai/skills/<skill-name>/
```

Each active system skill must define `SKILL.md` as the canonical agent contract and `README.md` as a short human-facing summary.
