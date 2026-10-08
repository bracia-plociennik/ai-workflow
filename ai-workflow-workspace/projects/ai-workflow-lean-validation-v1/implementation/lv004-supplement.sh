# Dispatcher regressions are additional to the frozen 674-case inventory.
run_must_pass "smoke-partition-manifest-valid" bash .systems/scripts/check-validator-smoke-tests --verify-manifest
for partition_case in missing-id duplicate-id missing-region missing-audit missing-nested-audit wrong-assertion-line wrong-nested-owner wrong-test-region; do
  cp "$tmp/.systems/scripts/smoke/manifest.json" "$tmp/.systems/scripts/smoke/manifest.json.bak"
  python3 - "$tmp/.systems/scripts/smoke/manifest.json" "$partition_case" <<'PARTITION_MUTATION'
import json
from pathlib import Path
import sys
path = Path(sys.argv[1])
data = json.loads(path.read_text())
case = sys.argv[2]
if case == "missing-id":
    data["test_groups"].pop(data["reference_test_ids"][0])
elif case == "duplicate-id":
    data["reference_test_ids"][1] = data["reference_test_ids"][0]
elif case == "missing-region":
    data["regions"] = [region for region in data["regions"] if region["id"] != "region-1512-1544"]
elif case == "missing-audit":
    data["external_assertion_audit"].pop()
elif case == "missing-nested-audit":
    data["nested_python_assertions"].pop()
elif case == "wrong-assertion-line":
    data["external_assertion_audit"][0]["source_line"] += 1
elif case == "wrong-nested-owner":
    data["nested_python_assertions"][0]["group"] = "policy"
elif case == "wrong-test-region":
    data["tests"][0]["region_id"] = "region-1512-1544"
path.write_text(json.dumps(data) + "\n")
PARTITION_MUTATION
  case "$partition_case" in
    missing-id) partition_diagnostic='Smoke manifest error: test ownership' ;;
    duplicate-id) partition_diagnostic='Smoke manifest error: reference ID inventory' ;;
    missing-region) partition_diagnostic='Smoke manifest error: raw region inventory' ;;
    missing-audit) partition_diagnostic='Smoke manifest error: outside assertion semantic audit' ;;
    missing-nested-audit) partition_diagnostic='Smoke manifest error: nested Python assertion inventory' ;;
    wrong-assertion-line) partition_diagnostic='Smoke manifest error: outside assertion line mapping' ;;
    wrong-nested-owner) partition_diagnostic='Smoke manifest error: nested Python assertion line mapping' ;;
    wrong-test-region) partition_diagnostic='Smoke manifest error: test region source call' ;;
  esac
  run_must_fail "smoke-partition-rejects-$partition_case" --expect-literal "$partition_diagnostic" bash .systems/scripts/check-validator-smoke-tests --verify-manifest
  mv "$tmp/.systems/scripts/smoke/manifest.json.bak" "$tmp/.systems/scripts/smoke/manifest.json"
done

cp "$tmp/.systems/scripts/smoke/core.sh" "$tmp/.systems/scripts/smoke/core.sh.bak"
cp "$tmp/.systems/scripts/smoke/manifest.json" "$tmp/.systems/scripts/smoke/manifest.json.bak"
python3 - "$tmp/.systems/scripts/smoke" <<'PARTITION_ASSERTION'
import hashlib
import json
from pathlib import Path
import sys
folder = Path(sys.argv[1])
path = folder / "core.sh"
text = path.read_text()
line = next(line for line in text.splitlines(keepends=True) if 'validate-workflow completion marker count mismatch' in line)
path.write_text(text.replace(line, "", 1))
manifest = folder / "manifest.json"
data = json.loads(manifest.read_text())
data["files_sha256"]["core.sh"] = hashlib.sha256(path.read_bytes()).hexdigest()
manifest.write_text(json.dumps(data) + "\n")
PARTITION_ASSERTION
run_must_fail "smoke-partition-rejects-removed-post-call-assertion" --expect-literal 'Smoke manifest error: changed frozen region: region-0701-1210' bash .systems/scripts/check-validator-smoke-tests --verify-manifest
mv "$tmp/.systems/scripts/smoke/core.sh.bak" "$tmp/.systems/scripts/smoke/core.sh"
mv "$tmp/.systems/scripts/smoke/manifest.json.bak" "$tmp/.systems/scripts/smoke/manifest.json"

cp "$tmp/.systems/ai/core/validation-observability.md" "$tmp/.systems/ai/core/validation-observability.md.bak"
printf '\nNever treat green scripts as PASS.\n' >> "$tmp/.systems/ai/core/validation-observability.md"
run_must_pass "smoke-observability-allows-safe-prohibition" bash .systems/scripts/check-validation-observability
mv "$tmp/.systems/ai/core/validation-observability.md.bak" "$tmp/.systems/ai/core/validation-observability.md"
for observability_case in direct but however period colon unless yet semicolon; do
  cp "$tmp/.systems/ai/core/validation-observability.md" "$tmp/.systems/ai/core/validation-observability.md.bak"
  case "$observability_case" in
    direct) wording='green scripts give PASS' ;;
    but) wording='Never treat green scripts as PASS, but green scripts give PASS' ;;
    however) wording='Never treat green scripts as PASS, however green scripts give PASS' ;;
    period) wording='Never treat green scripts as PASS. green scripts give PASS' ;;
    colon) wording='Never treat green scripts as PASS: green scripts give PASS' ;;
    unless) wording='Never treat green scripts as PASS unless green scripts give PASS' ;;
    yet) wording='Never treat green scripts as PASS, yet green scripts give PASS' ;;
    semicolon) wording='Never treat green scripts as PASS; green scripts give PASS' ;;
  esac
  printf '\n%s\n' "$wording" >> "$tmp/.systems/ai/core/validation-observability.md"
  run_must_fail "smoke-observability-rejects-$observability_case" --expect-literal 'Validation observability weakens coverage or PASS integrity' bash .systems/scripts/check-validation-observability
  mv "$tmp/.systems/ai/core/validation-observability.md.bak" "$tmp/.systems/ai/core/validation-observability.md"
done
mv "$tmp/.systems/ai/core/validation-observability.md" "$tmp/.systems/ai/core/validation-observability.md.bak"
run_must_fail "smoke-observability-rejects-missing-source" --expect-literal 'Policy-boundary scan failed' bash .systems/scripts/check-validation-observability
mv "$tmp/.systems/ai/core/validation-observability.md.bak" "$tmp/.systems/ai/core/validation-observability.md"
