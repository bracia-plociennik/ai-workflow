#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp -d "${TMPDIR:-/tmp}/ai-workflow-validator-smoke.XXXXXX")"
smoke_group="${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}"
progress="summary"
test_timeout_seconds="180"
smoke_started_at=$SECONDS
smoke_completion_emitted=0
smoke_suite_completed=0
smoke_final_status=0

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --group)
      [[ "$#" -ge 2 ]] || { echo "Missing value for --group"; exit 1; }
      smoke_group="$2"
      shift 2
      ;;
    --progress)
      [[ "$#" -ge 2 ]] || { echo "Missing value for --progress"; exit 1; }
      progress="$2"
      shift 2
      ;;
    --test-timeout-seconds)
      [[ "$#" -ge 2 ]] || { echo "Missing value for --test-timeout-seconds"; exit 1; }
      test_timeout_seconds="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: check-validator-smoke-tests [--group all|core|policy|quality|skills|workspace] [--progress quiet|summary|verbose] [--test-timeout-seconds seconds]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

case "$smoke_group" in
  all|core|policy|quality|skills|workspace) ;;
  *) echo "Unknown smoke group: $smoke_group"; exit 1 ;;
esac

case "$progress" in
  quiet|summary|verbose) ;;
  *) echo "Unknown progress mode: $progress"; exit 1 ;;
esac

if ! [[ "$test_timeout_seconds" =~ ^[0-9]+([.][0-9]+)?$ ]] || [[ "$test_timeout_seconds" == "0" || "$test_timeout_seconds" == "0.0" ]]; then
  echo "--test-timeout-seconds must be greater than zero"
  exit 1
fi

# Copied fixtures own their roots. Do not inherit the dispatcher's private runtime
# or forced repository mode; individual tests set their explicit environment.
unset AI_WORKFLOW_MODE AI_WORKFLOW_MODE_RESOLVED AI_WORKFLOW_HOME AI_WORKFLOW_WORKSPACE_HOME TARGET_REPO_ROOT

timeout_runner="$(pwd -P)/.systems/scripts/run-with-timeout"
timing_helper="$(pwd -P)/.systems/scripts/lib/validation-timing.py"
smoke_timing_start=""
smoke_timing_run_id="${AI_WORKFLOW_TIMING_RUN_ID:-$(date -u +%Y%m%dT%H%M%S)-$$}"
if [[ -n "${AI_WORKFLOW_TIMING_OUTPUT:-}" && "${AI_WORKFLOW_SMOKE_CHILD:-0}" != 1 ]]; then
  if [[ ! -e "$AI_WORKFLOW_TIMING_OUTPUT" ]]; then
    python3 "$timing_helper" init "$AI_WORKFLOW_TIMING_OUTPUT"
  fi
  smoke_timing_start="$(python3 "$timing_helper" now)"
fi

finish_smoke() {
  local status="${1:-$?}"
  local result="fail"
  if [[ "$status" -eq 0 ]]; then result="pass"; fi
  if [[ "$status" -eq 124 ]]; then result="timeout"; fi
  if [[ "$status" -eq 130 || "$status" -eq 143 ]]; then result="interrupted"; fi
  if [[ -n "${AI_WORKFLOW_TIMING_OUTPUT:-}" && -n "$smoke_timing_start" ]]; then
    if ! python3 "$timing_helper" record "$AI_WORKFLOW_TIMING_OUTPUT" "$smoke_timing_run_id" smoke-suite-wall smoke "$result" "smoke-$smoke_group" wall validation-wall "$smoke_timing_start"; then
      echo "Smoke timing wall record failed" >&2
      status=1
      result="fail"
    fi
  fi
  smoke_final_status="$status"
  if [[ "$smoke_completion_emitted" -eq 0 ]]; then
    smoke_completion_emitted=1
    printf 'AI_WORKFLOW_SMOKE_GROUP_COMPLETE group=%s result=%s exit_code=%s duration_seconds=%s\n' \
      "$smoke_group" "$result" "$status" "$((SECONDS - smoke_started_at))"
  fi
}

cleanup() {
  rm -rf "$tmp"
}
on_smoke_exit() {
  local status="$1"
  if [[ "$status" -eq 0 && "$smoke_suite_completed" -ne 1 ]]; then
    echo "Smoke suite ended before the final completion point" >&2
    status=1
  fi
  finish_smoke "$status"
  cleanup
  trap - EXIT
  exit "$smoke_final_status"
}
trap 'on_smoke_exit "$?"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

printf 'AI_WORKFLOW_SMOKE_GROUP_START group=%s progress=%s\n' "$smoke_group" "$progress"

tar --exclude='.git' --exclude='ai-workflow-workspace' -cf - . | tar -xf - -C "$tmp"

source "$(pwd -P)/.systems/scripts/smoke/common.sh"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md" "$tmp/example-status.orig"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/tasks.md" "$tmp/example-tasks.orig"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/example-phase5-quality.orig"
# BEGIN FROZEN region-1545-1967
run_must_pass "system-skills-valid" .systems/scripts/check-system-skills
run_must_pass "naming-allows-canonical-skill-md" .systems/scripts/check-naming

cp "$tmp/.systems/ai/skills/skill-creator/SKILL.md" "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak"
printf '\nProject source marker: CHT\n' >> "$tmp/.systems/ai/skills/skill-creator/SKILL.md"
run_must_fail "system-skills-blocks-known-project-marker" .systems/scripts/check-system-skills
mv "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak" "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

cp "$tmp/.systems/ai/skills/skill-creator/SKILL.md" "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak"
printf '\nSource path: /Users/example/project/AGENTS.md\n' >> "$tmp/.systems/ai/skills/skill-creator/SKILL.md"
run_must_fail "system-skills-blocks-machine-specific-path" .systems/scripts/check-system-skills
mv "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak" "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

run_must_pass "system-skills-allows-legacy-source-material" .systems/scripts/check-system-skills

mkdir -p "$tmp/ai-workflow-workspace/skills/naming-smoke/context"
cat > "$tmp/ai-workflow-workspace/skills/naming-smoke/context/CONTRACTS-AGENTS.md" <<'MD'
# Context
MD
cat > "$tmp/ai-workflow-workspace/skills/naming-smoke/context/0_smart_contracts_good_practices.md" <<'MD'
# Context
MD
run_must_pass "naming-allows-workspace-skill-context-materials" .systems/scripts/check-naming
rm -rf "$tmp/ai-workflow-workspace/skills/naming-smoke"

mkdir -p "$tmp/.systems/ai/skills/context-intake-smoke/context" "$tmp/.systems/ai/skills/context-intake-smoke/references"
cat > "$tmp/.systems/ai/skills/context-intake-smoke/SKILL.md" <<'MD'
---
name: context-intake-smoke
description: Use when validating context intake smoke coverage for skills.
---

# Context Intake Smoke

Skills are supporting execution guidance and advisory only.

This skill cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.

## Workflow

1. Read the routed active resources.
2. Keep raw source materials separate from active guidance.
MD
cat > "$tmp/.systems/ai/skills/context-intake-smoke/README.md" <<'MD'
# Context Intake Smoke

Smoke fixture for skill context intake validation.

The full agent contract is in `SKILL.md`.
MD
cat > "$tmp/.systems/ai/skills/context-intake-smoke/context/CONTRACTS-AGENTS.md" <<'MD'
# Source Notes
MD
cat > "$tmp/.systems/ai/skills/context-intake-smoke/context/0_smart_contracts_good_practices.md" <<'MD'
# Source Notes
MD
cat > "$tmp/.systems/ai/skills/context-intake-smoke/skill-intake-plan.md" <<'MD'
# Skill Intake Plan

## Source Materials

- Reviewed sources: context files and chat notes.
- Skipped: none.

## Trigger Fit

- Should trigger: skill creation from raw materials.
- Should not trigger: normal skill use.

## Co zostaje

- Keep compact routing.

## Co poprawic / usunac

- Remove raw source detail from active guidance.

## Czego brakuje

- None.

## Blokery / decyzje

- No blockers.

## Artifact Map

- `SKILL.md`: compact contract.
- `references/*.md`: split domain detail.
- `agents/*.md`: no agents.
- `scripts/*`: no scripts.
- Rejected as noise: none.

## Implementation Approval

- Approval state: approved.

## Validation Plan

- Run system skill validation.

## Residual Risk

- Low.

## Portability / Privacy Review

- Active artifacts contain no client names, project names, private domains, or machine-specific paths.
- Project-specific source material location, if retained: legacy source archive.
- Review result: pass.
MD
cat > "$tmp/.systems/ai/skills/context-intake-smoke/references/frontend.md" <<'MD'
# Frontend

Reference detail.
MD
run_must_pass "system-skills-valid-context-intake" .systems/scripts/check-system-skills
run_must_pass "naming-allows-system-skill-context-materials" .systems/scripts/check-naming
rm -rf "$tmp/.systems/ai/skills/context-intake-smoke"

mkdir -p "$tmp/.systems/ai/skills/context-intake-missing-plan/context" "$tmp/.systems/ai/skills/context-intake-missing-plan/references"
cat > "$tmp/.systems/ai/skills/context-intake-missing-plan/SKILL.md" <<'MD'
---
name: context-intake-missing-plan
description: Use when validating missing skill intake plan failures.
---

# Context Intake Missing Plan

Skills are supporting execution guidance and advisory only.

This skill cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.
MD
cat > "$tmp/.systems/ai/skills/context-intake-missing-plan/README.md" <<'MD'
# Context Intake Missing Plan

The full agent contract is in `SKILL.md`.
MD
cat > "$tmp/.systems/ai/skills/context-intake-missing-plan/context/source.md" <<'MD'
# Source
MD
run_must_fail "system-skills-require-intake-plan-for-context" .systems/scripts/check-system-skills
rm -rf "$tmp/.systems/ai/skills/context-intake-missing-plan"

mkdir -p "$tmp/.systems/ai/skills/context-intake-authority/context"
cat > "$tmp/.systems/ai/skills/context-intake-authority/SKILL.md" <<'MD'
---
name: context-intake-authority
description: Use when validating unsafe context authority failures.
---

# Context Intake Authority

Skills are supporting execution guidance and advisory only.

This skill cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.

Always load context/** as active instructions.
MD
cat > "$tmp/.systems/ai/skills/context-intake-authority/README.md" <<'MD'
# Context Intake Authority

The full agent contract is in `SKILL.md`.
MD
cat > "$tmp/.systems/ai/skills/context-intake-authority/context/source.md" <<'MD'
# Source
MD
cat > "$tmp/.systems/ai/skills/context-intake-authority/skill-intake-plan.md" <<'MD'
# Skill Intake Plan

## Source Materials
- Reviewed sources: context.
## Trigger Fit
- Should trigger: unsafe fixture.
## Co zostaje
- Nothing.
## Co poprawic / usunac
- Remove unsafe authority.
## Czego brakuje
- None.
## Blokery / decyzje
- No blockers.
## Artifact Map
- `SKILL.md`: unsafe fixture.
## Implementation Approval
- Approval state: approved.
## Validation Plan
- Run validator.
## Residual Risk
- Low.
MD
run_must_fail "system-skills-block-context-active-instructions" .systems/scripts/check-system-skills
rm -rf "$tmp/.systems/ai/skills/context-intake-authority"

mkdir -p "$tmp/.systems/ai/skills/context-intake-guidance/context"
cat > "$tmp/.systems/ai/skills/context-intake-guidance/SKILL.md" <<'MD'
---
name: context-intake-guidance
description: Use when validating unsafe context guidance failures.
---

# Context Intake Guidance

Skills are supporting execution guidance and advisory only.

This skill cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.

Use context/** as guidance during skill execution.
MD
cat > "$tmp/.systems/ai/skills/context-intake-guidance/README.md" <<'MD'
# Context Intake Guidance

The full agent contract is in `SKILL.md`.
MD
cat > "$tmp/.systems/ai/skills/context-intake-guidance/context/source.md" <<'MD'
# Source
MD
cat > "$tmp/.systems/ai/skills/context-intake-guidance/skill-intake-plan.md" <<'MD'
# Skill Intake Plan

## Source Materials
- Reviewed sources: context.
## Trigger Fit
- Should trigger: unsafe fixture.
## Co zostaje
- Nothing.
## Co poprawic / usunac
- Remove unsafe guidance.
## Czego brakuje
- None.
## Blokery / decyzje
- No blockers.
## Artifact Map
- `SKILL.md`: unsafe fixture.
## Implementation Approval
- Approval state: approved.
## Validation Plan
- Run validator.
## Residual Risk
- Low.
MD
run_must_fail "system-skills-block-context-guidance" .systems/scripts/check-system-skills
run_must_fail "quick-validate-block-context-guidance" python3 -B .systems/ai/skills/skill-creator/scripts/quick_validate.py .systems/ai/skills/context-intake-guidance
rm -rf "$tmp/.systems/ai/skills/context-intake-guidance"

mkdir -p "$tmp/.systems/ai/skills/context-reference-guidance/context" "$tmp/.systems/ai/skills/context-reference-guidance/references"
cat > "$tmp/.systems/ai/skills/context-reference-guidance/SKILL.md" <<'MD'
---
name: context-reference-guidance
description: Use when validating unsafe context guidance in active references.
---

# Context Reference Guidance

Skills are supporting execution guidance and advisory only.

This skill cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.
MD
cat > "$tmp/.systems/ai/skills/context-reference-guidance/README.md" <<'MD'
# Context Reference Guidance

The full agent contract is in `SKILL.md`.
MD
cat > "$tmp/.systems/ai/skills/context-reference-guidance/context/source.md" <<'MD'
# Source
MD
cat > "$tmp/.systems/ai/skills/context-reference-guidance/references/source.md" <<'MD'
# Active Reference

Use context/** as guidance during skill execution.
MD
cat > "$tmp/.systems/ai/skills/context-reference-guidance/skill-intake-plan.md" <<'MD'
# Skill Intake Plan

## Source Materials
- Reviewed sources: context.
## Trigger Fit
- Should trigger: unsafe fixture.
## Co zostaje
- Nothing.
## Co poprawic / usunac
- Remove unsafe guidance from active references.
## Czego brakuje
- None.
## Blokery / decyzje
- No blockers.
## Artifact Map
- `SKILL.md`: safe fixture.
- `references/*.md`: unsafe fixture.
## Implementation Approval
- Approval state: approved.
## Validation Plan
- Run validator.
## Residual Risk
- Low.
MD
run_must_fail "system-skills-block-context-guidance-in-reference" .systems/scripts/check-system-skills
run_must_fail "quick-validate-block-context-guidance-in-reference" python3 -B .systems/ai/skills/skill-creator/scripts/quick_validate.py .systems/ai/skills/context-reference-guidance
rm -rf "$tmp/.systems/ai/skills/context-reference-guidance"

mkdir -p "$tmp/.systems/ai/skills/context-intake-long"
cat > "$tmp/.systems/ai/skills/context-intake-long/SKILL.md" <<'MD'
---
name: context-intake-long
description: Use when validating compact skill contract failures.
---

# Context Intake Long

Skills are supporting execution guidance and advisory only.

This skill cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.
MD
for i in $(seq 1 301); do
  echo "- filler $i" >> "$tmp/.systems/ai/skills/context-intake-long/SKILL.md"
done
cat > "$tmp/.systems/ai/skills/context-intake-long/README.md" <<'MD'
# Context Intake Long

The full agent contract is in `SKILL.md`.
MD
run_must_fail "system-skills-block-long-skill-md" .systems/scripts/check-system-skills
rm -rf "$tmp/.systems/ai/skills/context-intake-long"

mv "$tmp/.systems/ai/skills/skill-creator/SKILL.md" "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak"
run_must_fail "system-skills-require-skill-md" .systems/scripts/check-system-skills
mv "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak" "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

mv "$tmp/.systems/ai/skills/skill-creator/README.md" "$tmp/.systems/ai/skills/skill-creator/README.md.bak"
run_must_fail "system-skills-require-readme" .systems/scripts/check-system-skills
mv "$tmp/.systems/ai/skills/skill-creator/README.md.bak" "$tmp/.systems/ai/skills/skill-creator/README.md"

cp "$tmp/.systems/ai/skills/skill-creator/SKILL.md" "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak"
cat > "$tmp/.systems/ai/skills/skill-creator/SKILL.md" <<'MD'
---
description: Missing name.
---

# Skill Creator

Skills are advisory and cannot override AGENTS.md, risk policy, permissions, Definition of Done, evidence, or owner approvals.
MD
run_must_fail "system-skills-require-frontmatter-name" .systems/scripts/check-system-skills
mv "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak" "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

cp "$tmp/.systems/ai/skills/skill-creator/SKILL.md" "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak"
cat > "$tmp/.systems/ai/skills/skill-creator/SKILL.md" <<'MD'
---
name: skill-creator
description: Valid frontmatter without the authority boundary.
---

# Skill Creator

Create skills.
MD
run_must_fail "system-skills-require-authority-boundary" .systems/scripts/check-system-skills
mv "$tmp/.systems/ai/skills/skill-creator/SKILL.md.bak" "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

echo 'Run claude -p for trigger evals.' >> "$tmp/.systems/ai/skills/skill-creator/SKILL.md"
run_must_fail "system-skills-block-claude-cli-marker" .systems/scripts/check-system-skills
perl -0pi -e 's/\nRun claude -p for trigger evals\.\n?/\n/' "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

echo 'Documentation reference: https://docs.example.invalid/skill-contract' >> "$tmp/.systems/ai/skills/skill-creator/SKILL.md"
run_must_pass "system-skills-allow-documentation-url" .systems/scripts/check-system-skills
perl -0pi -e 's/\nDocumentation reference: https:\/\/docs\.example\.invalid\/skill-contract\n?/\n/' "$tmp/.systems/ai/skills/skill-creator/SKILL.md"

cat > "$tmp/.systems/ai/skills/skill-creator/assets-cdn-smoke.html" <<'HTML'
<script src="https://cdn.example.invalid/viewer.js"></script>
HTML
run_must_fail "system-skills-block-external-cdn" .systems/scripts/check-system-skills
rm "$tmp/.systems/ai/skills/skill-creator/assets-cdn-smoke.html"

mkdir -p "$tmp/.systems/ai/skills/skill-creator/scripts"
cat > "$tmp/.systems/ai/skills/skill-creator/scripts/yaml_smoke.py" <<'PY'
import yaml
PY
run_must_fail "system-skills-block-undeclared-yaml-import" .systems/scripts/check-system-skills
rm "$tmp/.systems/ai/skills/skill-creator/scripts/yaml_smoke.py"

mkdir -p "$tmp/.systems/ai/skills/skill-creator/scripts/__pycache__"
touch "$tmp/.systems/ai/skills/skill-creator/scripts/__pycache__/cache.pyc"
run_must_fail "system-skills-block-python-cache-artifacts" .systems/scripts/check-system-skills
rm -rf "$tmp/.systems/ai/skills/skill-creator/scripts/__pycache__"

run_must_fail "system-skills-package-blocks-output-inside-skill" python3 .systems/ai/skills/skill-creator/scripts/package_skill.py .systems/ai/skills/skill-creator --output .systems/ai/skills/skill-creator/skill-creator.zip
test ! -e "$tmp/.systems/ai/skills/skill-creator/skill-creator.zip" || { echo "package_skill created archive inside skill directory"; exit 1; }

cat > "$tmp/skill-run-eval-path-traversal.json" <<'JSON'
{
  "skill_name": "skill-creator",
  "target_path": ".systems/ai/skills/skill-creator",
  "mode": "manual-review",
  "configurations": ["with_skill", "../escape"],
  "evals": [
    {
      "id": "../escape",
      "prompt": "Create a skill safely.",
      "expected_behavior": ["Preserves path boundaries"]
    }
  ]
}
JSON
run_must_fail "system-skills-run-eval-blocks-path-traversal" python3 .systems/ai/skills/skill-creator/scripts/run_eval.py "$tmp/skill-run-eval-path-traversal.json" --output-dir "$tmp/run-eval-path-traversal"
test ! -e "$tmp/escape" || { echo "run_eval created path traversal directory"; exit 1; }

cat > "$tmp/skill-run-eval-config-path-traversal.json" <<'JSON'
{
  "skill_name": "skill-creator",
  "target_path": ".systems/ai/skills/skill-creator",
  "mode": "manual-review",
  "configurations": ["with_skill", "../escape"],
  "evals": [
    {
      "id": "safe-eval",
      "prompt": "Create a skill safely.",
      "expected_behavior": ["Preserves path boundaries"]
    }
  ]
}
JSON
run_must_fail "system-skills-run-eval-blocks-config-path-traversal" python3 .systems/ai/skills/skill-creator/scripts/run_eval.py "$tmp/skill-run-eval-config-path-traversal.json" --output-dir "$tmp/run-eval-config-path-traversal"
test ! -e "$tmp/run-eval-config-path-traversal" || { echo "run_eval created output for invalid configuration"; exit 1; }
# END FROZEN region-1545-1967

# BEGIN FROZEN region-4873-4878
run_must_pass "skill-evaluation-validator-valid" .systems/scripts/check-skill-evaluation-contract
cp "$tmp/.systems/ai/core/skill-behavioral-evaluation.md" "$tmp/.systems/ai/core/skill-behavioral-evaluation.md.bak"
printf '\nAll existing skills must have evals.\n' >> "$tmp/.systems/ai/core/skill-behavioral-evaluation.md"
run_must_fail "skill-evaluation-remains-optional" .systems/scripts/check-skill-evaluation-contract
mv "$tmp/.systems/ai/core/skill-behavioral-evaluation.md.bak" "$tmp/.systems/ai/core/skill-behavioral-evaluation.md"

# END FROZEN region-4873-4878


echo "Owned smoke group passed."
smoke_suite_completed=1
