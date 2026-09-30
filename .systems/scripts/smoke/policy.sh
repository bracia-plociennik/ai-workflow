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
# BEGIN FROZEN region-1512-1544
cp "$tmp/.systems/ai/core/contract-compliance.md" "$tmp/.systems/ai/core/contract-compliance.md.bak"
perl -0pi -e 's/side-task/side_task/g' "$tmp/.systems/ai/core/contract-compliance.md"
run_must_fail "contract-compliance-requires-side-task-mode" .systems/scripts/check-contract-compliance
mv "$tmp/.systems/ai/core/contract-compliance.md.bak" "$tmp/.systems/ai/core/contract-compliance.md"

cp "$tmp/.systems/ai/templates/projects/micro-task.template.md" "$tmp/.systems/ai/templates/projects/micro-task.template.md.bak"
cat > "$tmp/.systems/ai/templates/projects/micro-task.template.md" <<'MD'
# <Micro-task Title>

## Summary

- Date: `<YYYY-MM-DD>`
- Project: `<project>`
- Risk: `low`

## Follow-up / Promote Decision

- Promote to full workflow: `<yes|no>`
- Reason: `<why>`
MD
run_must_fail "contract-compliance-requires-micro-task-knowledge-capture" .systems/scripts/check-contract-compliance
mv "$tmp/.systems/ai/templates/projects/micro-task.template.md.bak" "$tmp/.systems/ai/templates/projects/micro-task.template.md"

cp "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak"
perl -0pi -e 's/Risk: `low`/Risk: `medium`/' "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"
run_must_fail "contract-compliance-blocks-medium-risk-micro-project-template" .systems/scripts/check-contract-compliance
mv "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"

cp "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak"
perl -0pi -e 's/Work mode: `repo-level-micro-project`/Work mode: `workflow-maintenance`/' "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"
run_must_fail "contract-compliance-requires-micro-project-work-mode" .systems/scripts/check-contract-compliance
mv "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"

# END FROZEN region-1512-1544

# BEGIN FROZEN region-1972-2310

cat > "$tmp/.systems/ai/examples/system-insights/bad-missing-privacy.md" <<'MD'
# 2026-06-12 - Bad Missing Privacy

- Date: `2026-06-12`
- Category: `frontend`
- Status: `proposed`
- Source scope: `QA review`
- Skill candidate: `no`
- Suggested skill target: `n/a`

## TEMAT

- `Frontend - quality`

## 0. SYGNAŁY

- Reusable signal.

## 1. CO ZOSTAŁO FAKTYCZNIE ZROBIONE

- Reusable action.

## 2. PROBLEMY (→ KONWERSJA)

| Problem | Przyczyna | Konwersja |
| --- | --- | --- |
| issue | cause | rule |

## 3. WZORCE

- Pattern.

## 4. DECYZJE

| Treść | Wpływ |
| --- | --- |
| Decision | Impact |

## 5. ZASADY NA PRZYSZŁOŚĆ

| Zasada | Kiedy stosować |
| --- | --- |
| Rule | Future work |

## 6. OTWARTE LUKI

- None.

## 7. ODRZUCONE JAKO SZUM

| Pominięte | Dlaczego |
| --- | --- |
| none | n/a |

## 8. WALIDACJA OPERACYJNA

### co zostaje

- Keep rule.

### co poprawić / usunąć

- None.

### czego brakuje

- None.
MD
run_must_fail "system-insights-missing-privacy-check" .systems/scripts/check-system-insights
rm "$tmp/.systems/ai/examples/system-insights/bad-missing-privacy.md"

cat > "$tmp/.systems/ai/examples/system-insights/bad-missing-operational-validation.md" <<'MD'
# 2026-06-12 - Bad Missing Operational Validation

- Date: `2026-06-12`
- Category: `backend`
- Status: `proposed`
- Source scope: `QA review`
- Privacy check: `confirmed no raw client data, client names, secrets, repo-specific facts, project-specific details, or production identifiers`
- Skill candidate: `no`
- Suggested skill target: `n/a`

## TEMAT

- `Backend - architecture`

## 0. SYGNAŁY

- Reusable signal.

## 1. CO ZOSTAŁO FAKTYCZNIE ZROBIONE

- Reusable action.

## 2. PROBLEMY (→ KONWERSJA)

| Problem | Przyczyna | Konwersja |
| --- | --- | --- |
| issue | cause | rule |

## 3. WZORCE

- Pattern.

## 4. DECYZJE

| Treść | Wpływ |
| --- | --- |
| Decision | Impact |

## 5. ZASADY NA PRZYSZŁOŚĆ

| Zasada | Kiedy stosować |
| --- | --- |
| Rule | Future work |

## 6. OTWARTE LUKI

- None.

## 7. ODRZUCONE JAKO SZUM

| Pominięte | Dlaczego |
| --- | --- |
| none | n/a |
MD
run_must_fail "system-insights-missing-operational-validation" .systems/scripts/check-system-insights
rm "$tmp/.systems/ai/examples/system-insights/bad-missing-operational-validation.md"

cat > "$tmp/.systems/ai/examples/system-insights/bad-raw-client-data.md" <<'MD'
# 2026-06-12 - Bad Raw Client Data

- Date: `2026-06-12`
- Category: `client-work`
- Status: `proposed`
- Source scope: `owner-approved capture`
- Privacy check: `confirmed no raw client data, client names, secrets, repo-specific facts, project-specific details, or production identifiers`
- Skill candidate: `no`
- Suggested skill target: `n/a`
- Contact value person@example.invalid
- Wallet value 0x1111111111111111111111111111111111111111

## TEMAT

- `Client Work - process`

## 0. SYGNAŁY

- Reusable signal.

## 1. CO ZOSTAŁO FAKTYCZNIE ZROBIONE

- Reusable action.

## 2. PROBLEMY (→ KONWERSJA)

| Problem | Przyczyna | Konwersja |
| --- | --- | --- |
| issue | cause | rule |

## 3. WZORCE

- Pattern.

## 4. DECYZJE

| Treść | Wpływ |
| --- | --- |
| Decision | Impact |

## 5. ZASADY NA PRZYSZŁOŚĆ

| Zasada | Kiedy stosować |
| --- | --- |
| Rule | Future work |

## 6. OTWARTE LUKI

- None.

## 7. ODRZUCONE JAKO SZUM

| Pominięte | Dlaczego |
| --- | --- |
| none | n/a |

## 8. WALIDACJA OPERACYJNA

### co zostaje

- Keep rule.

### co poprawić / usunąć

- Remove raw data.

### czego brakuje

- None.
MD
run_must_fail "system-insights-blocks-raw-client-data" .systems/scripts/check-system-insights
rm "$tmp/.systems/ai/examples/system-insights/bad-raw-client-data.md"

system_insights_workspace="$tmp/system-insights-smoke-workspace"
mkdir -p "$system_insights_workspace/external-memory/memory" "$system_insights_workspace/system-insights/insights"
cat > "$system_insights_workspace/external-memory/memory/2026-06-12-frontend-lesson.md" <<'MD'
# Frontend Lesson

Frontend lesson insight about component quality belongs in System Insights.
MD
run_must_fail "system-insights-blocks-product-domain-external-memory" env AI_WORKFLOW_WORKSPACE_HOME="$system_insights_workspace" .systems/scripts/check-system-insights
rm "$system_insights_workspace/external-memory/memory/2026-06-12-frontend-lesson.md"

cat > "$system_insights_workspace/external-memory/memory/2026-06-12-ad-hoc-workflow-note.md" <<'MD'
# Ad Hoc Workflow Note

Avoid ad hoc capture of workflow improvement proposals without owner-approved routing.
MD
run_must_pass "system-insights-allows-ad-hoc-external-memory-note" env AI_WORKFLOW_WORKSPACE_HOME="$system_insights_workspace" .systems/scripts/check-system-insights
rm "$system_insights_workspace/external-memory/memory/2026-06-12-ad-hoc-workflow-note.md"

for category in frontend backend seo; do
  cat > "$system_insights_workspace/system-insights/insights/2026-06-12-valid-${category}.md" <<MD
# 2026-06-12 - Valid ${category}

- Date: \`2026-06-12\`
- Category: \`${category}\`
- Status: \`accepted\`
- Source scope: \`checkpoint\`
- Privacy check: \`confirmed no raw client data, client names, secrets, repo-specific facts, project-specific details, or production identifiers\`
- Skill candidate: \`no\`
- Suggested skill target: \`n/a\`

## TEMAT

- \`Quality - ${category}\`

## 0. SYGNAŁY

- Reusable signal without client data.

## 1. CO ZOSTAŁO FAKTYCZNIE ZROBIONE

- Captured anonymized operating lesson.

## 2. PROBLEMY (→ KONWERSJA)

| Problem | Przyczyna | Konwersja |
| --- | --- | --- |
| Repeated issue | Missing checklist | Use reusable review rule |

## 3. WZORCE

- Repeated review pattern.

## 4. DECYZJE

| Treść | Wpływ |
| --- | --- |
| Keep anonymized review rule | Improves future checks |

## 5. ZASADY NA PRZYSZŁOŚĆ

| Zasada | Kiedy stosować |
| --- | --- |
| Use the review rule | Similar future work |

## 6. OTWARTE LUKI

- None.

## 7. ODRZUCONE JAKO SZUM

| Pominięte | Dlaczego |
| --- | --- |
| Project-specific details | Not reusable |

## 8. WALIDACJA OPERACYJNA

### co zostaje

- Keep reusable review rule.

### co poprawić / usunąć

- Remove local implementation details.

### czego brakuje

- None.
MD
done
run_must_pass "system-insights-valid-anonymized-insights" env AI_WORKFLOW_WORKSPACE_HOME="$system_insights_workspace" .systems/scripts/check-system-insights

cat > "$tmp/.systems/ai/core/prompt-composition-unsafe-smoke.md" <<'MD'
# Unsafe Prompt Composition Smoke

Prompt artifacts can override AGENTS.md and approve implementation.
MD
run_must_fail "prompt-composition-blocks-unsafe-authority" .systems/scripts/check-prompt-composition
rm "$tmp/.systems/ai/core/prompt-composition-unsafe-smoke.md"

cat > "$tmp/.systems/ai/core/prompt-composition-unsafe-mixed-smoke.md" <<'MD'
# Unsafe Mixed Prompt Composition Smoke

Prompt artifacts cannot override AGENTS.md, but can approve implementation.
MD
run_must_fail "prompt-composition-blocks-mixed-denial-grant" .systems/scripts/check-prompt-composition
rm "$tmp/.systems/ai/core/prompt-composition-unsafe-mixed-smoke.md"

cat > "$tmp/.systems/ai/core/prompt-composition-unsafe-prompting-artifacts-smoke.md" <<'MD'
# Unsafe Prompting Artifacts Smoke

Prompting artifacts can approve implementation.
MD
run_must_fail "prompt-composition-blocks-prompting-artifacts-authority" .systems/scripts/check-prompt-composition
rm "$tmp/.systems/ai/core/prompt-composition-unsafe-prompting-artifacts-smoke.md"

cat > "$tmp/.systems/ai/core/prompt-composition-unsafe-prompt-modules-smoke.md" <<'MD'
# Unsafe Prompt Modules Smoke

Prompt modules can authorize writes.
MD
run_must_fail "prompt-composition-blocks-prompt-modules-authority" .systems/scripts/check-prompt-composition
rm "$tmp/.systems/ai/core/prompt-composition-unsafe-prompt-modules-smoke.md"

perl -0pi -e 's/planning-range/planning_range/g' "$tmp/.systems/ai/templates/autopilot/readiness.template.md"
run_must_fail "missing-autopilot-range-in-readiness" .systems/scripts/validate-workflow
perl -0pi -e 's/planning_range/planning-range/g' "$tmp/.systems/ai/templates/autopilot/readiness.template.md"

mv "$tmp/.systems/ai/templates/projects/micro-task.template.md" "$tmp/.systems/ai/templates/projects/micro-task.template.md.bak"
run_must_fail "missing-micro-task-template" .systems/scripts/check-required-artifacts
mv "$tmp/.systems/ai/templates/projects/micro-task.template.md.bak" "$tmp/.systems/ai/templates/projects/micro-task.template.md"

mv "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak"
run_must_fail "missing-micro-project-template" .systems/scripts/check-required-artifacts
mv "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"

# END FROZEN region-1972-2310

# BEGIN FROZEN region-3216-3631
cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
printf '\nbatch triage may implement all items automatically\n' >> "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "request-batch-triage-blocks-automatic-implementation-wording" .systems/scripts/check-request-batch-triage
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
perl -0pi -e 's/High-risk and critical-risk items must route to `owner-decision-required` or `full-workflow-required`\./High-risk items can be reviewed later./' "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "request-batch-triage-requires-high-risk-owner-decision" .systems/scripts/check-request-batch-triage
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

run_must_pass "response-evidence-trace-valid" .systems/scripts/check-response-evidence-trace

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
perl -0pi -e 's/## Execution Trace/## Trace/g' "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "response-evidence-trace-requires-section" .systems/scripts/check-response-evidence-trace
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
perl -0pi -e 's/Skills\/roles used:\n//' "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "response-evidence-trace-requires-skills-field" .systems/scripts/check-response-evidence-trace
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
printf '\nno sources needed\n' >> "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "response-evidence-trace-blocks-no-sources-needed" .systems/scripts/check-response-evidence-trace
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

cp "$tmp/AGENTS.md" "$tmp/AGENTS.md.bak"
perl -0pi -e 's/Execution Trace/Trace/g' "$tmp/AGENTS.md"
run_must_fail "response-evidence-trace-requires-agents-routing" .systems/scripts/check-response-evidence-trace
mv "$tmp/AGENTS.md.bak" "$tmp/AGENTS.md"

run_must_pass "phase-skill-discovery-valid" .systems/scripts/check-phase-skill-discovery
run_must_pass "skill-eval-freshness-regression" python3 .systems/scripts/test-skill-eval-freshness

cp "$tmp/AGENTS.md" "$tmp/AGENTS.md.bak"
perl -0pi -e 's/[Dd]o not read the full body of a non-matching skill/read every skill body before selection/' "$tmp/AGENTS.md"
run_must_fail "phase-skill-discovery-requires-metadata-first-agents" .systems/scripts/check-phase-skill-discovery
mv "$tmp/AGENTS.md.bak" "$tmp/AGENTS.md"

cp "$tmp/.systems/ai/core/operating-model.md" "$tmp/.systems/ai/core/operating-model.md.bak"
perl -0pi -e 's/[Dd]o not read the full body of a non-matching skill/read every skill body before selection/' "$tmp/.systems/ai/core/operating-model.md"
run_must_fail "phase-skill-discovery-requires-metadata-first-operating-model" .systems/scripts/check-phase-skill-discovery
mv "$tmp/.systems/ai/core/operating-model.md.bak" "$tmp/.systems/ai/core/operating-model.md"

cp "$tmp/AGENTS.md" "$tmp/AGENTS.md.bak"
perl -0pi -e 's/closing `---` delimiter/fixed line count/' "$tmp/AGENTS.md"
run_must_fail "phase-skill-discovery-requires-frontmatter-boundary" .systems/scripts/check-phase-skill-discovery
mv "$tmp/AGENTS.md.bak" "$tmp/AGENTS.md"

cp "$tmp/.systems/ai/core/operating-model.md" "$tmp/.systems/ai/core/operating-model.md.bak"
perl -0pi -e 's/Phase Skill Discovery/Phase Skill Lookup/g' "$tmp/.systems/ai/core/operating-model.md"
run_must_fail "phase-skill-discovery-requires-operating-model" .systems/scripts/check-phase-skill-discovery
mv "$tmp/.systems/ai/core/operating-model.md.bak" "$tmp/.systems/ai/core/operating-model.md"

cp "$tmp/.systems/ai/core/operating-model.md" "$tmp/.systems/ai/core/operating-model.md.bak"
perl -0pi -e 's/check `AI_WORKFLOW_WORKSPACE_HOME\/skills\/` first/check `.systems\/ai\/skills\/` first/' "$tmp/.systems/ai/core/operating-model.md"
run_must_fail "phase-skill-discovery-requires-workspace-first" .systems/scripts/check-phase-skill-discovery
mv "$tmp/.systems/ai/core/operating-model.md.bak" "$tmp/.systems/ai/core/operating-model.md"

cp "$tmp/.systems/ai/core/operating-model.md" "$tmp/.systems/ai/core/operating-model.md.bak"
perl -0pi -e 's/Skills used: none/Skills unavailable/g' "$tmp/.systems/ai/core/operating-model.md"
run_must_fail "phase-skill-discovery-requires-none-fallback" .systems/scripts/check-phase-skill-discovery
mv "$tmp/.systems/ai/core/operating-model.md.bak" "$tmp/.systems/ai/core/operating-model.md"

cp "$tmp/.systems/ai/core/operating-model.md" "$tmp/.systems/ai/core/operating-model.md.bak"
printf '\nskill may approve implementation\n' >> "$tmp/.systems/ai/core/operating-model.md"
run_must_fail "phase-skill-discovery-blocks-skill-approval" .systems/scripts/check-phase-skill-discovery
mv "$tmp/.systems/ai/core/operating-model.md.bak" "$tmp/.systems/ai/core/operating-model.md"

run_must_pass "default-quality-closure-valid" .systems/scripts/check-default-quality-closure

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/Default Quality Closure/Default Review Close/g' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "default-quality-closure-requires-contract" .systems/scripts/check-default-quality-closure
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/Quality skipped by owner opt-out/Quality omitted by owner/g' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "default-quality-closure-requires-opt-out-report" .systems/scripts/check-default-quality-closure
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nbez QA may continue as PASS\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "default-quality-closure-blocks-opt-out-pass" .systems/scripts/check-default-quality-closure
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/bez weryfikacji/bez sprawdzania/g' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "default-quality-closure-requires-verification-opt-out" .systems/scripts/check-default-quality-closure
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nwithout verification may count as PASS\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "default-quality-closure-blocks-without-verification-pass" .systems/scripts/check-default-quality-closure
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

run_must_pass "default-idea-validation-opt-out-valid" .systems/scripts/check-default-idea-validation-opt-out

cp "$tmp/.systems/ai/core/task-intake.md" "$tmp/.systems/ai/core/task-intake.md.bak"
perl -0pi -e 's/Single new work defaults to Task Idea Validation/Single new work can be routed directly/g' "$tmp/.systems/ai/core/task-intake.md"
run_must_fail "default-idea-validation-requires-single-work-default" .systems/scripts/check-default-idea-validation-opt-out
mv "$tmp/.systems/ai/core/task-intake.md.bak" "$tmp/.systems/ai/core/task-intake.md"

cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
perl -0pi -e 's/validation route/classification route/g' "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "default-idea-validation-requires-batch-validation-route" .systems/scripts/check-default-idea-validation-opt-out
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

cp "$tmp/.systems/ai/core/task-intake.md" "$tmp/.systems/ai/core/task-intake.md.bak"
perl -0pi -e 's/bez idea validation/bez walidacji/g' "$tmp/.systems/ai/core/task-intake.md"
run_must_fail "default-idea-validation-requires-opt-out-grammar" .systems/scripts/check-default-idea-validation-opt-out
mv "$tmp/.systems/ai/core/task-intake.md.bak" "$tmp/.systems/ai/core/task-intake.md"

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
perl -0pi -e 's/Idea validation skipped by owner opt-out/Idea validation omitted/g' "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "default-idea-validation-requires-opt-out-reporting" .systems/scripts/check-default-idea-validation-opt-out
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

cp "$tmp/.systems/ai/core/task-intake.md" "$tmp/.systems/ai/core/task-intake.md.bak"
printf '\nwithout idea validation may bypass risk checks\n' >> "$tmp/.systems/ai/core/task-intake.md"
run_must_fail "default-idea-validation-blocks-risk-bypass-wording" .systems/scripts/check-default-idea-validation-opt-out
mv "$tmp/.systems/ai/core/task-intake.md.bak" "$tmp/.systems/ai/core/task-intake.md"

run_must_pass "end-of-task-capture-valid" .systems/scripts/check-end-of-task-capture

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
perl -0pi -e 's/Trigger Grammar/Trigger List/g' "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-requires-trigger-grammar" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
perl -0pi -e 's/Precedence Rules/Routing Order/g' "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-requires-precedence" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/templates/capture/end-of-task-capture.template.md" "$tmp/.systems/ai/templates/capture/end-of-task-capture.template.md.bak"
perl -0pi -e 's/- Privacy\/scope check:\n//' "$tmp/.systems/ai/templates/capture/end-of-task-capture.template.md"
run_must_fail "end-of-task-capture-requires-privacy-field" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/templates/capture/end-of-task-capture.template.md.bak" "$tmp/.systems/ai/templates/capture/end-of-task-capture.template.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
perl -0pi -e 's/`Zrób distillation` and `Run phase 6` route to `phase-6-distillation`\./`Zrób distillation` routes to End-of-Task Capture./' "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-preserves-distillation-route" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
perl -0pi -e 's/`Zrób checkpoint` and `Run checkpoint` route to `phase-7-checkpoint`\./`Zrób checkpoint` routes to End-of-Task Capture./' "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-preserves-checkpoint-route" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nfinal review runs phase-8-final-check\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-final-review-final-check" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nend task may mark PASS automatically\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-auto-pass" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nend task runs phase-8-final-check\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-auto-final-check" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nend task may close project without final-owner-yes\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-project-close" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nSystem Insights may include client names\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-client-names" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nExternal Memory stores frontend lessons\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-external-memory-domain-lessons" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

run_must_pass "knowledge-capture-reminder-valid" .systems/scripts/check-knowledge-capture-reminder

mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
run_must_fail "knowledge-capture-reminder-requires-contract" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

mv "$tmp/.systems/ai/templates/capture/knowledge-capture-reminder.template.md" "$tmp/.systems/ai/templates/capture/knowledge-capture-reminder.template.md.bak"
run_must_fail "knowledge-capture-reminder-requires-template" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/templates/capture/knowledge-capture-reminder.template.md.bak" "$tmp/.systems/ai/templates/capture/knowledge-capture-reminder.template.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
perl -0pi -e 's/implementation work completed/implementation finished/g' "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-requires-implementation-trigger" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
perl -0pi -e 's/the owner starts a new unrelated task/the owner starts a follow-up/g' "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-requires-new-unrelated-task-trigger" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nKnowledge Capture Reminder automatically writes memory\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-auto-memory" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nKnowledge Capture Reminder automatically writes memory; this does not require owner approval\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-auto-memory-with-trailing-negation" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nKnowledge Capture Reminder auto-push\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-auto-push" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\ncommit ignored workspace artifacts\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-ignored-workspace-commit" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nskip knowledge capture may bypass phase 6 evidence privacy status gate\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-skip-bypass" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nowner-approved skip capture may bypass permissions and owner approvals\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-skip-permission-bypass" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nno capture may ignore stop conditions\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-skip-stop-condition-bypass" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

product_domains=(frontend backend "smart contract" SEO ads advertising "paid media" offer "client work" product)
for domain in "${product_domains[@]}"; do
  cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
  printf '\nExternal Memory stores %s lessons\n' "$domain" >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
  domain_slug="${domain// /-}"
  run_must_fail "knowledge-capture-reminder-blocks-external-memory-${domain_slug}-lessons" .systems/scripts/check-knowledge-capture-reminder
  mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
done

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nProduct lessons belong in External Memory\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-inverse-external-memory-domain-routing" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nSystem Insights stores anonymized SEO lessons.\nExternal Memory stores AI Workflow improvement proposals.\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_pass "knowledge-capture-reminder-allows-valid-memory-targets" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nExternal Memory never stores SEO lessons.\nProduct lessons do not belong in External Memory.\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_pass "knowledge-capture-reminder-allows-negated-domain-boundaries" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

cp "$tmp/.systems/ai/core/knowledge-capture-reminder.md" "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak"
printf '\nSystem Insights may include raw client data\n' >> "$tmp/.systems/ai/core/knowledge-capture-reminder.md"
run_must_fail "knowledge-capture-reminder-blocks-system-insights-raw-client-data" .systems/scripts/check-knowledge-capture-reminder
mv "$tmp/.systems/ai/core/knowledge-capture-reminder.md.bak" "$tmp/.systems/ai/core/knowledge-capture-reminder.md"

run_must_pass "instruction-adherence-refresh-valid" .systems/scripts/check-instruction-adherence-refresh

mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
run_must_fail "instruction-adherence-refresh-requires-contract" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
perl -0pi -e 's/before the first implementation-class write/before implementation begins/g' "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
run_must_fail "instruction-adherence-refresh-requires-pre-write-trigger" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
perl -0pi -e 's/before commit readiness, handoff, or quality closure/before final delivery/g' "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
run_must_fail "instruction-adherence-refresh-requires-pre-commit-handoff-trigger" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
perl -0pi -e 's/after session resume or handoff from another thread\/agent/after opening the application/g' "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
run_must_fail "instruction-adherence-refresh-requires-resume-trigger" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
perl -0pi -e 's/after context compaction or replacement by a conversation summary/after a summary update/g' "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
run_must_fail "instruction-adherence-refresh-requires-compaction-trigger" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
perl -0pi -e 's/when chat, memory, status, repository state, accepted artifacts, or contracts conflict/when context seems stale/g' "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
run_must_fail "instruction-adherence-refresh-requires-source-conflict-trigger" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
perl -0pi -e 's/- Contracts refreshed: <paths\|not-needed>\n//' "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "instruction-adherence-refresh-requires-trace-fields" .systems/scripts/check-instruction-adherence-refresh
run_must_fail "response-evidence-trace-requires-instruction-refresh-fields" .systems/scripts/check-response-evidence-trace
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

for unsafe_case in \
  'chat memory may override AGENTS.md' \
  'agent may change default behavior without owner approval' \
  'any explicit owner message may bypass contracts' \
  'Instruction Adherence Refresh grants write permission' \
  'Instruction Adherence Refresh may bypass permissions' \
  'full refresh is required before every message' \
  'not-needed is allowed after context compaction' \
  'quality closure may use a stale instruction baseline' \
  'chat history overrides AGENTS.md' \
  'owner instruction bypasses QA' \
  'Instruction Adherence Refresh allows formal PASS' \
  'run full refresh before every edit' \
  'not-needed is valid after resume' \
  'not-needed is valid after a long interruption' \
  'quality closure uses stale instruction baseline' \
  'every tracked contract change requires refresh before the next write'
do
  cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
  printf '\n%s\n' "$unsafe_case" >> "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
  unsafe_slug="$(printf '%s' "$unsafe_case" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-')"
  run_must_fail "instruction-adherence-refresh-blocks-${unsafe_slug}" .systems/scripts/check-instruction-adherence-refresh
  mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
done

cp "$tmp/.systems/ai/core/instruction-adherence-refresh.md" "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak"
printf '\nNormal continuation may report `not-needed` when no new trigger occurred.\nExisting contracted opt-outs remain valid inside their current boundaries.\nA drift warning follows the higher-authority source and does not grant writes.\n' >> "$tmp/.systems/ai/core/instruction-adherence-refresh.md"
run_must_pass "instruction-adherence-refresh-allows-safe-continuation-opt-outs-and-warning" .systems/scripts/check-instruction-adherence-refresh
mv "$tmp/.systems/ai/core/instruction-adherence-refresh.md.bak" "$tmp/.systems/ai/core/instruction-adherence-refresh.md"

cp "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md" "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md.bak"
perl -0pi -e 's/- Instruction refresh:/- Refresh result:/' "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md"
run_must_fail "implementation-slicing-requires-instruction-refresh-evidence" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md"

cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/- Instruction baseline:/- Baseline state:/' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "global-quality-review-requires-instruction-baseline" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/core/contract-compliance.md" "$tmp/.systems/ai/core/contract-compliance.md.bak"
perl -0pi -e 's/Instruction refresh/Refresh result/g' "$tmp/.systems/ai/core/contract-compliance.md"
run_must_fail "contract-compliance-requires-instruction-refresh" .systems/scripts/check-contract-compliance
mv "$tmp/.systems/ai/core/contract-compliance.md.bak" "$tmp/.systems/ai/core/contract-compliance.md"

run_must_pass "owner-decision-checkpoints-valid" .systems/scripts/check-owner-decision-checkpoints

mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
run_must_fail "owner-decision-checkpoints-requires-contract" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"

cp "$tmp/.systems/ai/workflow/phase-1-architecture.md" "$tmp/.systems/ai/workflow/phase-1-architecture.md.bak"
perl -0pi -e 's/## Owner Decision Checkpoint/## Decision Notes/' "$tmp/.systems/ai/workflow/phase-1-architecture.md"
run_must_fail "owner-decision-checkpoints-requires-phase-block" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/workflow/phase-1-architecture.md.bak" "$tmp/.systems/ai/workflow/phase-1-architecture.md"

cp "$tmp/.systems/ai/workflow/phase-1-architecture.md" "$tmp/.systems/ai/workflow/phase-1-architecture.md.bak"
printf '\n## Owner Decision Checkpoint\n' >> "$tmp/.systems/ai/workflow/phase-1-architecture.md"
run_must_fail "owner-decision-checkpoints-blocks-duplicate-phase-block" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/workflow/phase-1-architecture.md.bak" "$tmp/.systems/ai/workflow/phase-1-architecture.md"

cp "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md" "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md.bak"
perl -0pi -e 's/- Optional owner refinements: `<list\|none>`\n//' "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md"
run_must_fail "owner-decision-checkpoints-requires-template-fields" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md"

cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
perl -0pi -e 's/`owner-preference`/`owner-choice`/g' "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_fail "owner-decision-checkpoints-requires-owner-preference" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"

cp "$tmp/.systems/ai/templates/workflow/phase-0-idea-validation.template.md" "$tmp/.systems/ai/templates/workflow/phase-0-idea-validation.template.md.bak"
perl -0pi -e 's/owner-preference/owner-choice/g' "$tmp/.systems/ai/templates/workflow/phase-0-idea-validation.template.md"
run_must_fail "owner-decision-checkpoints-requires-owner-preference-in-phase-taxonomy" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/templates/workflow/phase-0-idea-validation.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-0-idea-validation.template.md"

cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
perl -0pi -e 's/put the recommended option first/list options in any order/' "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_fail "owner-decision-checkpoints-requires-recommendation-first" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"

cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
perl -0pi -e 's/group at most `1-3` questions/group material questions/' "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_fail "owner-decision-checkpoints-requires-question-batch-limit" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"

cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
perl -0pi -e 's/provide impact for the recommendation and each alternative/list available options/' "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_fail "owner-decision-checkpoints-requires-option-impact" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"

for unsafe_case in \
  'ask the owner about every uncertainty' \
  'auto-resolve high-impact decisions' \
  'critical-risk decisions are auto-resolvable' \
  'nie dopytuj may bypass QA' \
  'no-question opt-out allows guessed acceptance criteria' \
  'autopilot may ask live questions while running' \
  'autopilot asks clarification questions while running' \
  'autopilot may continue with a pending material decision' \
  'autopilot continues with a pending material decision' \
  'Dreaming Mode may ask live questions' \
  'Dreaming Mode asks follow-up questions' \
  'read-only review may interrupt to ask' \
  'Optional Knowledge Capture requires interactive question'
do
  cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
  printf '\n%s\n' "$unsafe_case" >> "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
  unsafe_slug="$(printf '%s' "$unsafe_case" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-')"
  run_must_fail "owner-decision-checkpoints-blocks-${unsafe_slug}" .systems/scripts/check-owner-decision-checkpoints
  mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
done

run_must_pass "review-completeness-gate-valid" .systems/scripts/check-review-completeness-gate
# END FROZEN region-3216-3631

# BEGIN FROZEN region-3828-3924
handoff_fixture="$tmp/ai-workflow-workspace/external-memory/memory"
mkdir -p "$handoff_fixture"
cat > "$handoff_fixture/valid-handoff.md" <<'MD'
# Valid Handoff

- Privacy/scope check: `pass`
- Raw client data included: `no`
MD
cat > "$handoff_fixture/valid-record.md" <<MD
# Record

## Cross-system Impact

- Owner decision: \`yes\`
- Counterpart: \`ai-system\`
- Handoff artifact: \`$handoff_fixture/valid-handoff.md\`
MD
run_must_pass "cross-system-yes-requires-existing-safe-handoff" .systems/scripts/check-cross-system-upgrade-handoff --record "$handoff_fixture/valid-record.md"

cat > "$handoff_fixture/missing-record.md" <<'MD'
# Record

## Cross-system Impact

- Owner decision: `yes`
- Counterpart: `ai-system`
- Handoff artifact: `pending`
MD
run_must_fail "cross-system-yes-without-handoff-fails" .systems/scripts/check-cross-system-upgrade-handoff --record "$handoff_fixture/missing-record.md"

cat > "$handoff_fixture/pending-record.md" <<'MD'
# Record

## Cross-system Impact

- Owner decision: `pending`
- Counterpart: `ai-system`
- Handoff artifact: `pending`
MD
run_must_fail "cross-system-pending-blocks-handoff" .systems/scripts/check-cross-system-upgrade-handoff --record "$handoff_fixture/pending-record.md"

cat > "$handoff_fixture/raw-handoff.md" <<'MD'
# Unsafe Handoff

Client name: Example Corporation
MD
cat > "$handoff_fixture/raw-record.md" <<MD
# Record

## Cross-system Impact

- Owner decision: \`yes\`
- Counterpart: \`ai-system\`
- Handoff artifact: \`$handoff_fixture/raw-handoff.md\`
MD
run_must_fail "cross-system-handoff-blocks-raw-client-data" .systems/scripts/check-cross-system-upgrade-handoff --record "$handoff_fixture/raw-record.md"

cat > "$handoff_fixture/email-handoff.md" <<'MD'
# Unsafe Handoff

Contact: owner@example.invalid
MD
cat > "$handoff_fixture/email-record.md" <<MD
# Record

## Cross-system Impact

- Owner decision: \`yes\`
- Counterpart: \`ai-system\`
- Handoff artifact: \`$handoff_fixture/email-handoff.md\`
MD
run_must_fail "cross-system-handoff-blocks-email-shaped-data" .systems/scripts/check-cross-system-upgrade-handoff --record "$handoff_fixture/email-record.md"

cat > "$tmp/outside-handoff.md" <<'MD'
# Outside Handoff
MD
cat > "$handoff_fixture/outside-record.md" <<MD
# Record

## Cross-system Impact

- Owner decision: \`yes\`
- Counterpart: \`ai-system\`
- Handoff artifact: \`$tmp/outside-handoff.md\`
MD
run_must_fail "cross-system-handoff-requires-external-memory-namespace" .systems/scripts/check-cross-system-upgrade-handoff --record "$handoff_fixture/outside-record.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
perl -0pi -e 's/Koniec pracy/Koniec iteracji/g' "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-requires-koniec-pracy" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

cp "$tmp/.systems/ai/core/end-of-task-capture.md" "$tmp/.systems/ai/core/end-of-task-capture.md.bak"
printf '\nKoniec pracy may acknowledge only and ask what to do next.\n' >> "$tmp/.systems/ai/core/end-of-task-capture.md"
run_must_fail "end-of-task-capture-blocks-acknowledge-only" .systems/scripts/check-end-of-task-capture
mv "$tmp/.systems/ai/core/end-of-task-capture.md.bak" "$tmp/.systems/ai/core/end-of-task-capture.md"

# END FROZEN region-3828-3924

# BEGIN FROZEN region-4034-4051

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
perl -0pi -e 's/- Decisions asked\/pending: <ids\|none>\n//' "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "owner-decision-checkpoints-requires-response-trace" .systems/scripts/check-owner-decision-checkpoints
run_must_fail "response-evidence-trace-requires-owner-decision-fields" .systems/scripts/check-response-evidence-trace
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

cp "$tmp/.systems/ai/core/workflow.md" "$tmp/.systems/ai/core/workflow.md.bak"
perl -0pi -e 's/If the working phase ends with a material `Owner Decision Checkpoint` state of `awaiting-owner` or `blocked`, stop before QA\/Quality chaining\./Pending decisions can be handled after QA./' "$tmp/.systems/ai/core/workflow.md"
run_must_fail "owner-decision-checkpoints-blocks-quality-chain-with-pending-decision" .systems/scripts/check-owner-decision-checkpoints
run_must_fail "default-quality-chaining-blocks-pending-owner-decision" .systems/scripts/check-default-quality-phase-chaining
mv "$tmp/.systems/ai/core/workflow.md.bak" "$tmp/.systems/ai/core/workflow.md"

cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak"
printf '\nA deterministic task with no material choice reports `No owner decision needed`. Optional refinements and reversible auto-resolved decisions remain non-blocking.\n' >> "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_pass "owner-decision-checkpoints-allows-deterministic-and-phase-end-recap" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/core/owner-decision-checkpoints.md.bak" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"

# END FROZEN region-4034-4051

# BEGIN FROZEN region-4813-4845

run_must_pass "delivery-constraints-valid" .systems/scripts/check-delivery-constraints
cp "$tmp/.systems/ai/core/delivery-constraints.md" "$tmp/.systems/ai/core/delivery-constraints.md.bak"
printf '\nDeadline pressure may skip QA.\n' >> "$tmp/.systems/ai/core/delivery-constraints.md"
run_must_fail "delivery-constraints-blocks-quality-bypass" .systems/scripts/check-delivery-constraints
mv "$tmp/.systems/ai/core/delivery-constraints.md.bak" "$tmp/.systems/ai/core/delivery-constraints.md"

run_must_pass "distillation-state-valid" .systems/scripts/check-distillation-state
cp "$tmp/.systems/ai/core/distillation-state.md" "$tmp/.systems/ai/core/distillation-state.md.bak"
printf '\nDreaming automatically writes memory from every undistilled state.\n' >> "$tmp/.systems/ai/core/distillation-state.md"
run_must_fail "distillation-state-blocks-dreaming-write" .systems/scripts/check-distillation-state
mv "$tmp/.systems/ai/core/distillation-state.md.bak" "$tmp/.systems/ai/core/distillation-state.md"

cp "$tmp/.systems/ai/templates/capture/distillation-state.template.md" "$tmp/.systems/ai/templates/capture/distillation-state.template.md.bak"
perl -0pi -e 's/- State:.*\n/- Missing State field\n/' "$tmp/.systems/ai/templates/capture/distillation-state.template.md"
run_must_fail "distillation-state-requires-state-field" .systems/scripts/check-distillation-state
mv "$tmp/.systems/ai/templates/capture/distillation-state.template.md.bak" "$tmp/.systems/ai/templates/capture/distillation-state.template.md"

cp "$tmp/.systems/ai/workflow/phase-5-quality.md" "$tmp/.systems/ai/workflow/phase-5-quality.md.bak"
perl -0pi -e 's/## Delivery Constraints QA\n.*?## Owner Decision Checkpoint/## Owner Decision Checkpoint/ms' "$tmp/.systems/ai/workflow/phase-5-quality.md"
run_must_fail "delivery-constraints-requires-phase5-evidence" .systems/scripts/check-delivery-constraints
mv "$tmp/.systems/ai/workflow/phase-5-quality.md.bak" "$tmp/.systems/ai/workflow/phase-5-quality.md"

cp "$tmp/.systems/ai/core/distillation-state.md" "$tmp/.systems/ai/core/distillation-state.md.bak"
perl -0pi -e 's/Every implementation-class write must create or update/Each implementation-class write may create or update/' "$tmp/.systems/ai/core/distillation-state.md"
run_must_fail "distillation-state-requires-mandatory-producer" .systems/scripts/check-distillation-state
mv "$tmp/.systems/ai/core/distillation-state.md.bak" "$tmp/.systems/ai/core/distillation-state.md"

cp "$tmp/.systems/ai/templates/dreaming/dream-report.template.md" "$tmp/.systems/ai/templates/dreaming/dream-report.template.md.bak"
perl -0pi -e 's/\| Work ID \| Scope \| State \| Source Evidence \| Quality Evidence \| Recommended Target \| Why Useful \| Blocker\/Missing Decision \| Privacy\/Scope \| Owner Action \| Residual Risk \|/| Work ID | Scope | State | Source Evidence | Quality Evidence | Recommended Target | Why Useful | Blocker\/Missing Decision | Privacy\/Scope | Owner Action | |/' "$tmp/.systems/ai/templates/dreaming/dream-report.template.md"
run_must_fail "dreaming-queue-requires-all-columns" .systems/scripts/check-dreaming-mode
mv "$tmp/.systems/ai/templates/dreaming/dream-report.template.md.bak" "$tmp/.systems/ai/templates/dreaming/dream-report.template.md"

# END FROZEN region-4813-4845


echo "Owned smoke group passed."
smoke_suite_completed=1
