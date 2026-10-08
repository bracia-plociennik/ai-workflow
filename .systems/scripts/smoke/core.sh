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

python3 .systems/scripts/lib/smoke-fixture.py --repo "$(pwd -P)" --output "$tmp"

source "$(pwd -P)/.systems/scripts/smoke/common.sh"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md" "$tmp/example-status.orig"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/tasks.md" "$tmp/example-tasks.orig"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/example-phase5-quality.orig"
# BEGIN FROZEN region-0701-1210

synthetic_source_digest="$(.systems/scripts/report-validation-comparison source-digest)"
run_must_fail "validation-timing-rejects-existing-output" --expect-literal 'File exists' python3 "$timing_helper" init "$tmp/AGENTS.md"
run_must_fail "validation-timing-rejects-escaping-output" --expect-literal 'must be under ignored workspace or tmp' python3 "$timing_helper" init "$(pwd -P)/.systems/scripts/invalid-timing.tsv"
# Avoid macOS developer-tool wrappers writing their cache into the hostile TMPDIR.
timing_python="$(python3 -c 'import sys; print(sys.executable)')"
timing_git="$(command -v git)"
if [[ "$(uname -s)" == Darwin ]]; then
  timing_git="$(xcrun --find git)"
fi
run_must_fail "validation-timing-rejects-tmpdir-override" --expect-literal 'must be under ignored workspace or tmp' env TMPDIR="$(pwd -P)" PATH="$(dirname "$timing_git"):$PATH" "$timing_python" "$timing_helper" init "$(pwd -P)/.systems/scripts/invalid-tmpdir-timing.tsv"
ln -s "$tmp/AGENTS.md" "$tmp/lv002-timing-link.tsv"
run_must_fail "validation-timing-rejects-symlink" --expect-literal 'must not be a symlink' python3 "$timing_helper" init "$tmp/lv002-timing-link.tsv"
python3 "$timing_helper" init "$tmp/lv002-precision.tsv"
mkdir -p "$tmp/lv002-tracked-output"
git init -q "$tmp/lv002-tracked-output"
cp "$tmp/lv002-precision.tsv" "$tmp/lv002-tracked-output/tracked.tsv"
git -C "$tmp/lv002-tracked-output" add tracked.tsv
run_must_fail "validation-timing-rejects-tracked-temporary-output" --expect-literal 'tracked by git' bash -c 'cd "$1" && shift && exec "$@"' _ "$tmp/lv002-tracked-output" python3 "$timing_helper" init "$tmp/lv002-tracked-output/tracked.tsv"
run_must_fail "validation-timing-rejects-unignored-temporary-repo-output" --expect-literal 'must be under ignored workspace or tmp' bash -c 'cd "$1" && shift && exec "$@"' _ "$tmp/lv002-tracked-output" python3 "$timing_helper" init "$tmp/lv002-tracked-output/unignored.tsv"
run_must_fail "validation-timing-rejects-foreign-tracked-output" --expect-literal 'tracked by git' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" python3 "$timing_helper" init "$tmp/lv002-tracked-output/tracked.tsv"
rm "$tmp/lv002-tracked-output/tracked.tsv"
run_must_fail "validation-timing-rejects-foreign-deleted-tracked-output" --expect-literal 'tracked by git' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" python3 "$timing_helper" init "$tmp/lv002-tracked-output/tracked.tsv"
run_must_fail "validation-timing-rejects-foreign-unignored-output" --expect-literal 'must be under ignored workspace or tmp' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" python3 "$timing_helper" init "$tmp/lv002-tracked-output/unignored.tsv"
precision_start="$(python3 "$timing_helper" now)"
sleep 0.02
python3 "$timing_helper" record "$tmp/lv002-precision.tsv" precision-run short-check core pass full child validation-wall "$precision_start"
awk -F '\t' 'NR == 2 { if ($3 <= 0 || $3 >= 1) exit 1; found=1 } END { if (!found) exit 1 }' "$tmp/lv002-precision.tsv" || { echo "LV002 sub-second duration was not recorded precisely"; exit 1; }

for synthetic_run in 1 2 3 4 5 6; do
  synthetic_timing="$tmp/lv002-synthetic-$synthetic_run.tsv"
  {
    printf 'command/check_id\tgroup\tduration_seconds\tresult\tprofile\tschema_version\trun_id\trecord_kind\tparent_id\n'
    printf 'check-required-artifacts\tvalidator\t2.000000\tpass\tfull\t2\t%s-synthetic-%s\tchild\tvalidation-wall\n' "$synthetic_source_digest" "$synthetic_run"
    printf 'check-validator-smoke-tests\tsmoke\t7.000000\tpass\tfull\t2\t%s-synthetic-%s\tchild\tvalidation-wall\n' "$synthetic_source_digest" "$synthetic_run"
    printf 'one-smoke\tcore\t3.000000\tpass\tsmoke-all\t2\t%s-synthetic-%s\tchild\tsmoke-suite-wall\n' "$synthetic_source_digest" "$synthetic_run"
    printf 'smoke-suite-wall\tsmoke\t6.000000\tpass\tsmoke-all\t2\t%s-synthetic-%s\twall\tvalidation-wall\n' "$synthetic_source_digest" "$synthetic_run"
    printf 'validation-wall\twall\t10.000000\tpass\tfull\t2\t%s-synthetic-%s\twall\tnone\n' "$synthetic_source_digest" "$synthetic_run"
  } > "$synthetic_timing"
  run_must_pass "validation-comparison-captures-$synthetic_run" bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$synthetic_timing" --output "$tmp/lv002-synthetic-$synthetic_run.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
done
python3 - "$tmp/lv002-synthetic-1.json" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if manifest["schema_version"] != 2 or manifest["timing_file"] != "lv002-synthetic-1.tsv":
    raise SystemExit("LV002 manifest leaked an absolute timing path")
PY
run_must_pass "validation-comparison-summarizes-complete" .systems/scripts/report-validation-comparison summarize "$tmp/lv002-synthetic-1.json" "$tmp/lv002-synthetic-2.json" "$tmp/lv002-synthetic-3.json"
run_must_pass "validation-comparison-preserves-inconclusive" .systems/scripts/report-validation-comparison compare --baseline "$tmp/lv002-synthetic-1.json" "$tmp/lv002-synthetic-2.json" "$tmp/lv002-synthetic-3.json" --candidate "$tmp/lv002-synthetic-4.json" "$tmp/lv002-synthetic-5.json" "$tmp/lv002-synthetic-6.json"
rg -q '"result": "complete-baseline"' "$tmp/validation-comparison-summarizes-complete.out" || { echo "LV002 complete baseline summary missing"; exit 1; }
rg -q '"result": "inconclusive"' "$tmp/validation-comparison-preserves-inconclusive.out" || { echo "LV002 no-gain comparison claimed improvement"; exit 1; }
rg -v '^smoke-suite-wall' "$tmp/lv002-synthetic-1.tsv" | sed 's/synthetic-1/synthetic-incomplete/g' > "$tmp/lv002-incomplete.tsv"
run_must_pass "validation-comparison-captures-incomplete" bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-incomplete.tsv" --output "$tmp/lv002-incomplete.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
run_must_fail "validation-comparison-rejects-incomplete" --expect-literal 'incomplete or failed run cannot be a baseline' .systems/scripts/report-validation-comparison summarize "$tmp/lv002-synthetic-1.json" "$tmp/lv002-synthetic-2.json" "$tmp/lv002-incomplete.json"
sed "s/$synthetic_source_digest/0000000000000000000000000000000000000000000000000000000000000000/g" "$tmp/lv002-synthetic-1.tsv" > "$tmp/lv002-wrong-source.tsv"
run_must_fail "validation-comparison-rejects-source-mismatch" --expect-literal 'source does not match the timed run identity' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-wrong-source.tsv" --output "$tmp/lv002-wrong-source.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
cp "$tmp/lv002-synthetic-1.tsv" "$tmp/lv002-duplicate.tsv"
rg '^one-smoke' "$tmp/lv002-synthetic-1.tsv" >> "$tmp/lv002-duplicate.tsv"
run_must_fail "validation-comparison-rejects-duplicate-record" --expect-literal 'duplicate timing identity' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-duplicate.tsv" --output "$tmp/lv002-duplicate.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
awk -F '\t' '$1 != "check-validator-smoke-tests"' "$tmp/lv002-synthetic-1.tsv" > "$tmp/lv002-missing-smoke-check.tsv"
run_must_fail "validation-comparison-rejects-missing-smoke-check" --expect-literal 'smoke wall has no top-level smoke check' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-missing-smoke-check.tsv" --output "$tmp/lv002-missing-smoke-check.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
sed 's/10.000000/Infinity/' "$tmp/lv002-synthetic-1.tsv" > "$tmp/lv002-nonfinite.tsv"
run_must_fail "validation-comparison-rejects-nonfinite-duration" --expect-literal 'invalid timing duration' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-nonfinite.tsv" --output "$tmp/lv002-nonfinite.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
run_must_fail "validation-comparison-rejects-separate-output" --expect-literal 'must share a directory' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-synthetic-1.tsv" --output "$tmp/lv002-manifests/separate.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
sed 's/6.000000/8.000000/' "$tmp/lv002-synthetic-1.tsv" > "$tmp/lv002-oversized-smoke-wall.tsv"
run_must_fail "validation-comparison-rejects-oversized-smoke-wall" --expect-literal 'smoke wall exceeds its top-level check' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-oversized-smoke-wall.tsv" --output "$tmp/lv002-oversized-smoke-wall.json" --scope-fingerprint synthetic-full --input-fingerprint synthetic-input --setup-regime ordinary
run_must_fail "validation-comparison-rejects-private-fingerprint" --expect-literal 'unsafe field' bash -c 'cd "$1" && shift && exec "$@"' _ "$(pwd -P)" .systems/scripts/report-validation-comparison capture --timing "$tmp/lv002-synthetic-1.tsv" --output "$tmp/lv002-private-fingerprint.json" --scope-fingerprint synthetic-full --input-fingerprint '/private/client/path' --setup-regime ordinary

for infrastructure_case in unexpected-timeout missing-source wrong-error-code wrong-diagnostic; do
  case "$infrastructure_case" in
    unexpected-timeout)
      infrastructure_command=(.systems/scripts/run-with-timeout --timeout-seconds 1 python3 -c 'import time; time.sleep(3)')
      ;;
    missing-source)
      infrastructure_command=(.systems/scripts/no-such-validator)
      ;;
    wrong-error-code)
      infrastructure_command=(python3 -c 'import sys; print("wrong rejection"); sys.exit(2)')
      ;;
    wrong-diagnostic)
      infrastructure_command=(python3 -c 'import sys; print("unrelated error"); sys.exit(1)')
      ;;
  esac
  if (AI_WORKFLOW_TIMING_OUTPUT='' run_must_fail "smoke-helper-rejects-$infrastructure_case" --expect-literal 'intended policy violation' "${infrastructure_command[@]}") > "$tmp/smoke-helper-$infrastructure_case.out" 2>&1; then
    echo "Negative smoke helper accepted $infrastructure_case as a policy rejection"
    exit 1
  fi
  expected_failure='instead of expected 1'
  if [[ "$infrastructure_case" == missing-source ]]; then
    expected_failure='infrastructure error instead of the intended rejection'
  elif [[ "$infrastructure_case" == wrong-diagnostic ]]; then
    expected_failure='lacks the intended rejected clause'
  fi
  grep -q "$expected_failure" "$tmp/smoke-helper-$infrastructure_case.out" || {
    echo "Negative smoke helper did not report the wrong exit status for $infrastructure_case"
    cat "$tmp/smoke-helper-$infrastructure_case.out"
    exit 1
  }
done


# LV003 uses isolated synthetic Git fixtures; checks are stubs only for dispatch
# identity, while canonical consumer tests below exercise the real validators.
cat > "$tmp/lv003-scope-probes.py" <<'LV3PY'
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

source = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("case")
parser.add_argument("--source", type=Path, default=source)
args = parser.parse_args()
source = args.source.resolve()
helper_source = source / ".systems/scripts/lib/validation-scope.py"
spec = importlib.util.spec_from_file_location("scope", helper_source)
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)

def reject(call, fragment):
    try:
        call()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        assert fragment in str(error), (fragment, str(error))
    else:
        raise AssertionError("expected rejection: " + fragment)

def invoke(command, cwd, ok=True, env=None):
    run = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    assert (run.returncode == 0) == ok, (run.returncode, run.stdout, run.stderr)
    return run

with tempfile.TemporaryDirectory(prefix="lv003-scope-") as directory:
    repo = Path(directory) / "repo"
    repo.mkdir()
    scripts = repo / ".systems/scripts"
    lib = scripts / "lib"
    lib.mkdir(parents=True)
    for name in ("validation-scope.py", "validation-checks.json", "validation-timing.py", "policy-boundaries.sh", "qa-evidence.py"):
        shutil.copy2(source / ".systems/scripts/lib" / name, lib / name)
    for name in ("validate-workflow", "resolve-workflow-env", "run-with-timeout"):
        shutil.copy2(source / ".systems/scripts" / name, scripts / name)
    registry_path = lib / "validation-checks.json"
    registry = json.loads(registry_path.read_text())
    for name in registry["checks"]:
        path = scripts / name
        path.write_text('#!/usr/bin/env bash\nprintf "EXEC %s %s\\n" "' + name + '" "$*"\n')
        path.chmod(0o755)
    (repo / ".gitignore").write_text("workspace/\n")
    invoke(["git", "init", "-q", str(repo)], repo)
    invoke(["git", "add", "."], repo)
    invoke(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], repo)
    workspace = repo / "workspace"
    for name in ("a", "b"):
        root = workspace / "projects" / name
        root.mkdir(parents=True)
        (root / "status.md").write_text("current-phase: phase-4-implementation\n")
    manifest_path = Path(directory) / "manifest.json"

    def manifest(roots=("projects/a",), intent="checkpoint", scopes=("product",)):
        value = scope.snapshot(repo, workspace, "HEAD", list(scopes), list(roots), intent, repo)
        manifest_path.write_text(json.dumps(value))
        return value

    def planned(checks=",".join(registry["runtime_required"]), path=manifest_path):
        return scope.plan(argparse.Namespace(workflow=repo, repo=repo, workspace=workspace,
                         registry=registry_path, checks=checks, manifest=path, project=""))

    case = args.case
    if case == "dedup":
        plan = planned("check-status-consistency,check-qa-evidence,check-status-consistency", None)
        assert len(plan["invocations"]) == len(set(row["id"] for row in plan["invocations"]))
        assert plan["required"].count("check-qa-evidence") == 1
        assert plan["coverage_result"] == "unverified" and not plan["final_evidence_eligible"]
        env = dict(os.environ, AI_WORKFLOW_MODE="official", AI_WORKFLOW_WORKSPACE_HOME=str(workspace))
        out = invoke([str(scripts / "validate-workflow"), "--profile", "scoped", "--checks",
                      "check-status-consistency,check-status-consistency", "--progress", "quiet"], repo, env=env).stdout
        assert out.count("EXEC check-status-consistency") == 1
        assert "EXEC check-required-artifacts" not in out and "EXEC check-branch-policy" not in out
        assert out.count("AI_WORKFLOW_VALIDATE_COMPLETE ") == 1
    elif case == "projects":
        manifest(("projects/a", "projects/b"))
        plan = planned()
        ids = [row["id"] for row in plan["invocations"]]
        assert len(ids) == len(set(ids))
        assert sum(row["check"] == "check-qa-evidence" for row in plan["invocations"]) == 2
        assert sum(row["check"] == "check-full-qa-verification" for row in plan["invocations"]) == 1
    elif case == "graph":
        reject(lambda: planned("check-unknown", None), "unknown scoped check")
        reject(lambda: planned("check-naming,", None), "empty or unsafe")
        registry_text = registry_path.read_text()
        registry_path.write_text('{"schema_version":1,"schema_version":1}')
        reject(lambda: planned(path=None), "duplicate JSON field")
        registry_path.write_text(registry_text)
        registry["checks"]["check-naming"]["dependencies"] = ["check-status-consistency"]
        registry_path.write_text(json.dumps(registry))
        reject(lambda: planned(path=None), "dependency cycle")
    elif case == "git":
        product = repo / "product"
        product.mkdir()
        old = product / "old file.md"
        old.write_text("base")
        invoke(["git", "add", "."], repo)
        invoke(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "product"], repo)
        base = scope.git(repo, "rev-parse", "HEAD").decode().strip()
        invoke(["git", "mv", "product/old file.md", "product/new file.md"], repo)
        (product / "new file.md").write_text("modified")
        weird = product / "line\nbreak.md"
        weird.write_text("untracked")
        snap = scope.snapshot(repo, workspace, base, ["product"], ["projects/a"], "iteration", repo)
        assert any(row["old_path"] == "product/old file.md" for row in snap["changes"])
        assert any(row["area"] == "unstaged" for row in snap["changes"])
        assert any(row["path"] == "product/line\nbreak.md" for row in snap["changes"])
        assert {row["path"] for row in snap["inputs"]} >= {"product/old file.md", "product/new file.md", "product/line\nbreak.md"}
        (product / "new file.md").unlink()
        assert any(row["status"] == "D" for row in scope.git_changes(repo, base))
        (scripts / "check-naming").unlink()
        reject(lambda: planned(path=None), "missing scope input")
    elif case == "freshness":
        manifest()
        (workspace / "projects/a/status.md").write_text("changed")
        reject(lambda: planned(), "stale or incomplete")
        manifest()
        value = json.loads(manifest_path.read_text())
        value["runtime"][0]["files"] = []
        manifest_path.write_text(json.dumps(value))
        reject(lambda: planned(), "stale or incomplete")
        manifest(scopes=(".systems", "product"))
        (scripts / "check-naming").write_text("#!/bin/sh\nexit 1\n")
        reject(lambda: planned(), "stale or incomplete")
    elif case == "ownership":
        foreign = workspace / "projects/a/context/foreign"
        foreign.mkdir(parents=True)
        (foreign / ".git").mkdir()
        (foreign / "STATE.md").write_text("raw")
        files = scope.runtime_files(workspace, "projects/a")
        assert all("context" not in file.parts for file in files)
        owned = workspace / "projects/a/reviews/nested"
        owned.mkdir(parents=True)
        (owned / ".git").mkdir()
        reject(lambda: scope.runtime_files(workspace, "projects/a"), "foreign repository")
    elif case == "paths":
        reject(lambda: scope.owned_root(workspace, "projects/missing"), "missing runtime root")
        reject(lambda: scope.owned_root(workspace, "../repo"), "unknown owned")
        bad = workspace / "projects/a/link.md"
        bad.symlink_to(repo / ".gitignore")
        reject(lambda: manifest(), "symlink runtime")
        bad.unlink()
        sensitive = workspace / "projects/a/.env.md"
        sensitive.write_text("synthetic private source")
        reject(lambda: manifest(), "sensitive input path")
        sensitive.unlink()
        status = workspace / "projects/a/status.md"
        status.chmod(0)
        try:
            reject(lambda: manifest(), "unreadable")
        finally:
            status.chmod(0o644)
        unreadable = workspace / "projects/a/reviews"
        unreadable.mkdir()
        unreadable.chmod(0)
        try:
            reject(lambda: manifest(), "unreadable runtime directory")
        finally:
            unreadable.chmod(0o755)
        (repo / "outside.txt").write_text("out of scope")
        reject(lambda: manifest(), "outside declared")
    elif case == "checkpoint":
        manifest()
        plan = planned()
        assert plan["coverage_result"] == "complete" and plan["final_evidence_eligible"]
        manifest(intent="iteration")
        assert planned()["coverage_result"] == "complete" and not planned()["final_evidence_eligible"]
        manifest()
        assert planned("check-naming")["coverage_result"] == "incomplete"
        core = workspace / "repo/core"
        core.mkdir(parents=True)
        (core / "status.md").write_text("active-project: b\n")
        manifest(("repo/core", "projects/a"))
        assert planned()["reason"] == "active-project-scope-required"
        invoke(["git", "add", "-f", "workspace/projects/a/status.md"], repo)
        invoke(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "tracked runtime"], repo)
        tracked = workspace / "projects/a/status.md"
        tracked.write_text("current-phase: phase-7-checkpoint\n")
        manifest(scopes=("workspace/projects/a",))
        assert planned()["coverage_result"] == "complete" and planned()["final_evidence_eligible"]
        tracked.unlink()
        manifest(scopes=("workspace/projects/a",))
        assert not planned()["final_evidence_eligible"]
        tracked.write_text("current-phase: phase-7-checkpoint\n")
        invoke(["git", "add", "-f", "workspace/projects/b/status.md"], repo)
        manifest(scopes=("workspace/projects",))
        assert planned()["reason"] == "full-required-source-impact"
    elif case == "source":
        (repo / "AGENTS.md").write_text("source")
        manifest(scopes=("AGENTS.md",))
        assert planned()["reason"] == "full-required-source-impact"
        assert not planned()["final_evidence_eligible"]
        invoke(["git", "add", "."], repo)
        invoke(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "source"], repo)
        (scripts / "check-naming").write_text("#!/bin/sh\nexit 0\n")
        manifest(scopes=(".systems",))
        assert planned()["reason"] == "full-required-source-impact"
    elif case == "finish":
        manifest()
        plan = planned()
        argv = [sys.executable, str(lib / "validation-scope.py"), "finish", "--repo", str(repo),
                "--workspace", str(workspace), "--workflow", str(repo), "--plan", json.dumps(plan), "--status", "0"]
        rejected = invoke(argv, repo, ok=False)
        assert "execution is incomplete" in rejected.stderr
        done = ",".join(row["id"] for row in plan["invocations"])
        result = json.loads(invoke(argv + ["--executed", done], repo).stdout)
        assert result["execution_result"] == "pass" and result["coverage_result"] == "complete"
        fake = dict(plan, final_evidence_eligible=False)
        forged = [*argv]
        forged[forged.index("--plan") + 1] = json.dumps(fake)
        assert "fabricated execution plan" in invoke(forged + ["--executed", done], repo, ok=False).stderr
        (workspace / "projects/a/status.md").write_text("stale")
        assert "stale or incomplete" in invoke(argv + ["--executed", done], repo, ok=False).stderr
    elif case == "consumers":
        env = dict(os.environ, AI_WORKFLOW_MODE="official", AI_WORKFLOW_WORKSPACE_HOME=str(workspace))
        root = workspace / "projects/a"
        status = (source / ".systems/ai/examples/projects/EXAMPLE/status.md").read_text()
        (root / "status.md").write_text(status.replace(".systems/ai/examples/projects/EXAMPLE", str(root)))
        (root / "context.md").write_text("# Accepted Context\n")
        (root / "tasks.md").write_text("| Task ID | Title | Risk | Status | Task Card | Spec | Quality | Notes |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| A-DOCS-001-fixture | Fixture | low | ready | none | none | none | fixture |\n")
        (workspace / "projects/b/status.md").write_text("invalid unrelated project")
        foreign = root / "context/foreign"
        foreign.mkdir(parents=True)
        (foreign / ".git").mkdir()
        (foreign / "STATE.md").write_text("data")
        state_dir = root / "capture-state"
        state_dir.mkdir()
        state = state_dir / "work.md"
        text = "# Distillation State\n" + "\n".join("- " + key + ": " + value for key, value in {
            "Work ID": "A-DOCS-001-fixture", "Work mode": "workflow-maintenance", "Project/repo scope": "a",
            "Source artifact": "context.md", "Quality artifact": "none", "State": "pending-quality",
            "Distillation artifact": "none", "Last reminder": "none", "Owner disposition": "not-requested",
            "Privacy/scope check": "pass", "Residual risk": "none", "is_distilled derived value": "false"
        }.items()) + "\n"
        state.write_text(text)
        def check(name, ok=True, fragment=""):
            result = invoke([str(source / ".systems/scripts" / name), "--runtime-only", "--scope-root", "projects/a"],
                            source, ok=ok, env=env)
            assert fragment in result.stdout + result.stderr
        for name in sorted(scope.RUNTIME_CHECKS):
            check(name)
        state.write_text(text.replace("value: false", "value: true"))
        check("check-distillation-state", False, "derived boolean mismatch")
        state.write_text(text)
        (root / "WRONG.md").write_text("# Invalid name\n")
        check("check-naming", False, "Invalid Markdown filename")
        (root / "WRONG.md").unlink()
        (root / "status.md").write_text(status.replace("next-phase", "invalid-phase-field"))
        check("check-status-consistency", False, "missing status key: next-phase")
        (root / "status.md").write_text(status)
        quality = root / "quality"
        quality.mkdir()
        (quality / "phase-5-a-001-quality.md").write_text("# Quality\n\n## Metadata\n\n- Result: PASS\n")
        check("check-qa-evidence", False, "missing ## Evidence section")
        (quality / "phase-5-a-001-quality.md").unlink()
        (root / "tasks.md").write_text((root / "tasks.md").read_text().replace("| none | none | none |", "| ../b/status.md | none | none |"))
        check("check-status-consistency", False, "unsafe relative path")

    else:
        raise AssertionError("unknown probe")
print("LV003 " + args.case + " verified")

LV3PY
for scope_case in dedup projects graph git freshness ownership paths checkpoint source finish consumers; do
  run_must_pass "validation-scope-$scope_case" python3 "$tmp/lv003-scope-probes.py" "$scope_case"
done


run_must_pass "validation-completion-validator-valid" .systems/scripts/check-validation-completion

run_must_pass "validate-workflow-emits-one-completion-marker" env AI_WORKFLOW_SKIP_SMOKE_TESTS=1 .systems/scripts/validate-workflow --profile fast --progress summary --timeout-seconds 60
test "$(rg -c '^AI_WORKFLOW_VALIDATE_START ' "$tmp/validate-workflow-emits-one-completion-marker.out")" -eq 1 || { echo "validate-workflow start marker count mismatch"; exit 1; }
test "$(rg -c '^AI_WORKFLOW_VALIDATE_COMPLETE ' "$tmp/validate-workflow-emits-one-completion-marker.out")" -eq 1 || { echo "validate-workflow completion marker count mismatch"; exit 1; }

cat > "$tmp/.systems/scripts/check-smoke-failure" <<'SH'
#!/usr/bin/env bash
exit 7
SH
chmod +x "$tmp/.systems/scripts/check-smoke-failure"
cp "$tmp/.systems/scripts/lib/validation-checks.json" "$tmp/check-registry.backup"
python3 - "$tmp/.systems/scripts/lib/validation-checks.json" <<'PY'
import json, pathlib, sys
path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())
data['checks']['check-smoke-failure'] = {'dependencies': [], 'scope': 'framework'}
path.write_text(json.dumps(data))
PY
run_must_fail "validate-workflow-emits-failure-marker" .systems/scripts/validate-workflow --profile scoped --checks check-smoke-failure --progress quiet --timeout-seconds 60
mv "$tmp/check-registry.backup" "$tmp/.systems/scripts/lib/validation-checks.json"
rm "$tmp/.systems/scripts/check-smoke-failure"
grep -q '^AI_WORKFLOW_VALIDATE_COMPLETE .*result=fail ' "$tmp/validate-workflow-emits-failure-marker.out" || { echo "validate-workflow failure marker missing"; exit 1; }

run_must_fail "timeout-wrapper-returns-124" .systems/scripts/run-with-timeout --timeout-seconds 1 python3 -c 'import time; time.sleep(3)'
grep -q '^AI_WORKFLOW_TIMEOUT ' "$tmp/timeout-wrapper-returns-124.out" || { echo "timeout marker missing"; exit 1; }

cat > "$tmp/timeout-process-tree.py" <<'PY'
import os
import pathlib
import sys
import time

pid_file = pathlib.Path(sys.argv[1])
child_pid = os.fork()
if child_pid == 0:
    pid_file.write_text(str(os.getpid()))
    time.sleep(10)
else:
    pid_file.write_text(str(child_pid))
    time.sleep(10)
PY
timeout_tree_pid_file="$tmp/timeout-process-tree.pid"
run_must_fail "timeout-wrapper-kills-process-group" .systems/scripts/run-with-timeout --timeout-seconds 1 python3 "$tmp/timeout-process-tree.py" "$timeout_tree_pid_file"
test -s "$timeout_tree_pid_file" || { echo "timeout process tree did not publish child pid"; exit 1; }
timeout_tree_pid="$(cat "$timeout_tree_pid_file")"
if kill -0 "$timeout_tree_pid" 2>/dev/null; then
  echo "timeout wrapper left an orphan process"
  kill "$timeout_tree_pid" 2>/dev/null || true
  exit 1
fi

update_fixture_root="$tmp/update-lifecycle-fixture"
update_remote="$update_fixture_root/remote.git"
update_target="$update_fixture_root/target"
update_ai="$update_target/ai-workflow"
mkdir -p "$update_fixture_root" "$update_ai/.systems/scripts" "$update_target/ai-workflow-workspace/repo/core"
git init -q --bare "$update_remote"
cp "$tmp/.systems/scripts/update-from-upstream" "$update_ai/.systems/scripts/update-from-upstream"
printf '%s\n' '#!/usr/bin/env bash' 'printf "stub validation args: %s\\n" "$*"' 'exit "${STUB_VALIDATE_STATUS:-0}"' > "$update_ai/.systems/scripts/validate-workflow"
chmod +x "$update_ai/.systems/scripts/update-from-upstream" "$update_ai/.systems/scripts/validate-workflow"
git -C "$update_ai" init -q
git -C "$update_ai" config user.email "smoke@example.invalid"
git -C "$update_ai" config user.name "AI Workflow Smoke"
git -C "$update_ai" add .
git -C "$update_ai" commit -q -m "fixture baseline"
git -C "$update_ai" branch -M main
git -C "$update_ai" remote add origin "$update_remote"
git -C "$update_ai" push -q -u origin main

run_must_pass "update-equal-canonical" env AI_WORKFLOW_WORKSPACE_HOME="$update_target/ai-workflow-workspace" "$update_ai/.systems/scripts/update-from-upstream" --remote origin --branch main
grep -q '^AI_WORKFLOW_UPSTREAM_STATE relation=equal ' "$tmp/update-equal-canonical.out" || { echo "equal relation marker missing"; exit 1; }
grep -q '^AI_WORKFLOW_UPDATE_VALIDATION_COMPLETE result=pass$' "$tmp/update-equal-canonical.out" || { echo "equal validation marker missing"; exit 1; }
grep -q '^AI_WORKFLOW_UPDATE_COMPLETE result=pass ' "$tmp/update-equal-canonical.out" || { echo "equal completion marker missing"; exit 1; }

run_must_fail "update-validation-failure" env STUB_VALIDATE_STATUS=7 AI_WORKFLOW_WORKSPACE_HOME="$update_target/ai-workflow-workspace" "$update_ai/.systems/scripts/update-from-upstream" --remote origin --branch main
grep -q '^AI_WORKFLOW_UPDATE_VALIDATION_COMPLETE result=fail exit_code=7$' "$tmp/update-validation-failure.out" || { echo "update validation failure marker missing"; exit 1; }
grep -q '^AI_WORKFLOW_UPDATE_COMPLETE result=fail exit_code=7 ' "$tmp/update-validation-failure.out" || { echo "update failure completion marker missing"; exit 1; }
if grep -q '^update-from-upstream completed\.$' "$tmp/update-validation-failure.out"; then
  echo "failed update printed success completion"
  exit 1
fi
if grep -q "ai-workflow/.systems/scripts/update-workspace" "$tmp/update-validation-failure.out"; then
  echo "failed update printed update-workspace recommendation"
  exit 1
fi

run_must_fail "update-validation-timeout" env STUB_VALIDATE_STATUS=124 AI_WORKFLOW_WORKSPACE_HOME="$update_target/ai-workflow-workspace" "$update_ai/.systems/scripts/update-from-upstream" --remote origin --branch main
grep -q '^AI_WORKFLOW_UPDATE_VALIDATION_COMPLETE result=timeout exit_code=124$' "$tmp/update-validation-timeout.out" || { echo "update timeout validation marker missing"; exit 1; }
grep -q '^AI_WORKFLOW_UPDATE_COMPLETE result=timeout exit_code=124 ' "$tmp/update-validation-timeout.out" || { echo "update timeout completion marker missing"; exit 1; }
if grep -q "ai-workflow/.systems/scripts/update-workspace" "$tmp/update-validation-timeout.out"; then
  echo "timed out update printed update-workspace recommendation"
  exit 1
fi

update_remote_work="$update_fixture_root/remote-work"
git clone -q --branch main "$update_remote" "$update_remote_work"
git -C "$update_remote_work" config user.email "smoke@example.invalid"
git -C "$update_remote_work" config user.name "AI Workflow Smoke"
printf '%s\n' 'REMOTE_ADVANCE' >> "$update_remote_work/README.md"
git -C "$update_remote_work" add README.md
git -C "$update_remote_work" commit -q -m "remote advance"
git -C "$update_remote_work" push -q origin main

run_must_pass "update-behind-canonical" env AI_WORKFLOW_WORKSPACE_HOME="$update_target/ai-workflow-workspace" "$update_ai/.systems/scripts/update-from-upstream" --remote origin --branch main
grep -q '^AI_WORKFLOW_UPSTREAM_STATE relation=behind ' "$tmp/update-behind-canonical.out" || { echo "behind relation marker missing"; exit 1; }
test "$(git -C "$update_ai" rev-parse HEAD)" = "$(git -C "$update_ai" rev-parse origin/main)" || { echo "behind update did not fast-forward"; exit 1; }

printf '%s\n' 'LOCAL_AHEAD' >> "$update_ai/README.md"
git -C "$update_ai" add README.md
git -C "$update_ai" commit -q -m "local noncanonical commit"
printf '%s\n' 'WORKSPACE_MUST_SURVIVE' > "$update_target/ai-workflow-workspace/repo/core/status.md"
run_must_fail "update-ahead-stops" env AI_WORKFLOW_WORKSPACE_HOME="$update_target/ai-workflow-workspace" "$update_ai/.systems/scripts/update-from-upstream" --remote origin --branch main
grep -q '^AI_WORKFLOW_UPSTREAM_STATE relation=ahead ' "$tmp/update-ahead-stops.out" || { echo "ahead relation marker missing"; exit 1; }
if grep -q '^AI_WORKFLOW_UPDATE_VALIDATION_START' "$tmp/update-ahead-stops.out"; then
  echo "ahead update incorrectly ran validation"
  exit 1
fi
grep -q 'WORKSPACE_MUST_SURVIVE' "$update_target/ai-workflow-workspace/repo/core/status.md" || { echo "ahead update touched workspace"; exit 1; }

printf '%s\n' 'REMOTE_DIVERGENCE' >> "$update_remote_work/README.md"
git -C "$update_remote_work" add README.md
git -C "$update_remote_work" commit -q -m "second remote advance"
git -C "$update_remote_work" push -q origin main
run_must_fail "update-diverged-stops" env AI_WORKFLOW_WORKSPACE_HOME="$update_target/ai-workflow-workspace" "$update_ai/.systems/scripts/update-from-upstream" --remote origin --branch main
grep -q '^AI_WORKFLOW_UPSTREAM_STATE relation=diverged ' "$tmp/update-diverged-stops.out" || { echo "diverged relation marker missing"; exit 1; }

# END FROZEN region-0701-1210

# BEGIN FROZEN region-4867-4872
run_must_pass "validation-observability-validator-valid" .systems/scripts/check-validation-observability
cp "$tmp/.systems/ai/core/validation-observability.md" "$tmp/.systems/ai/core/validation-observability.md.bak"
printf '\nGreen scripts = PASS.\n' >> "$tmp/.systems/ai/core/validation-observability.md"
run_must_fail "validation-observability-preserves-pass-integrity" .systems/scripts/check-validation-observability
mv "$tmp/.systems/ai/core/validation-observability.md.bak" "$tmp/.systems/ai/core/validation-observability.md"

# END FROZEN region-4867-4872

# Dispatcher regressions are additional to the frozen 674-case inventory.
run_must_pass "validation-scope-dependencies" python3 .systems/scripts/tests/runtime-dependency-scope.py
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

run_must_pass "runtime-integrity-synthetic-regressions" bash .systems/scripts/check-runtime-integrity

# Exercise the actual assertion consumer without depending on host rg wording.
for diagnostic_case in short long missing-marker wrong-status-zero wrong-status-two; do
  run_must_pass "smoke-diagnostic-contract-$diagnostic_case" bash -lc '
    set -euo pipefail
    fixture_root="$1"
    diagnostic_case="$2"
    tmp="$(mktemp -d)"
    trap '\''rm -rf "$tmp"'\'' EXIT
    unset AI_WORKFLOW_TIMING_OUTPUT AI_WORKFLOW_SMOKE_DIAGNOSTICS_OUTPUT
    source "$fixture_root/.systems/scripts/smoke/common.sh"
    should_run_smoke_test() { return 0; }
    progress=quiet
    test_timeout_seconds=10
    timeout_runner="$fixture_root/.systems/scripts/run-with-timeout"

    set +e
    (
      run_must_fail "policy-boundaries-fails-missing-source" bash -c '\''
        diagnostic_case="$1"
        case "$diagnostic_case" in
          short|long)
            rg() {
              if [[ "$diagnostic_case" == short ]]; then
                echo "rg: /definitely/missing/policy-source.md: No such file or directory (os error 2)" >&2
              else
                echo "rg: /definitely/missing/policy-source.md: IO error for operation on /definitely/missing/policy-source.md: No such file or directory (os error 2)" >&2
              fi
              return 2
            }
            source "$2/.systems/scripts/lib/policy-boundaries.sh"
            fail=0
            policy_reject_unsafe_pattern "unsafe policy wording" "missing source test" /definitely/missing/policy-source.md
            exit "$fail"
            ;;
          missing-marker)
            echo "rg: /definitely/missing/policy-source.md: No such file or directory (os error 2)"
            exit 1
            ;;
          wrong-status-zero|wrong-status-two)
            echo "Policy-boundary scan failed: missing source test"
            [[ "$diagnostic_case" != wrong-status-zero ]] || exit 0
            exit 2
            ;;
        esac
      '\'' _ "$diagnostic_case" "$fixture_root"
    ) > "$tmp/assertion.out" 2>&1
    assertion_status=$?
    set -e
    case "$diagnostic_case" in
      short|long)
        expected_status=0
        expected_message=""
        ;;
      missing-marker)
        expected_status=1
        expected_message="Validator smoke test lacks expected diagnostic: policy-boundaries-fails-missing-source"
        ;;
      wrong-status-zero|wrong-status-two)
        expected_status=1
        expected_message="Validator smoke test returned"
        ;;
    esac
    if [[ "$assertion_status" -ne "$expected_status" ]]; then
      cat "$tmp/assertion.out"
      echo "Diagnostic assertion regression failed: $diagnostic_case"
      exit 1
    fi
    if [[ -n "$expected_message" ]] && ! grep -Fq "$expected_message" "$tmp/assertion.out"; then
      cat "$tmp/assertion.out"
      echo "Diagnostic assertion rejected for the wrong reason: $diagnostic_case"
      exit 1
    fi
  ' _ "$tmp" "$diagnostic_case"
done

run_must_pass "execution-efficiency-behavioral" python3 "$(pwd -P)/.systems/scripts/tests/execution-efficiency.py"
cp "$tmp/.systems/ai/core/execution-efficiency.md" "$tmp/eff-contract.orig"
printf '\nReuse must not replace semantic review, but reuse may replace semantic review.\n' >> "$tmp/.systems/ai/core/execution-efficiency.md"
run_must_fail "execution-efficiency-compound-boundary" --expect-literal 'Unsafe execution efficiency wording' bash .systems/scripts/check-execution-efficiency
mv "$tmp/eff-contract.orig" "$tmp/.systems/ai/core/execution-efficiency.md"
mv "$tmp/.systems/ai/core/execution-efficiency.md" "$tmp/eff-contract.orig"
run_must_fail "execution-efficiency-missing-contract" --expect-literal 'Missing execution efficiency artifact' bash .systems/scripts/check-execution-efficiency
mv "$tmp/eff-contract.orig" "$tmp/.systems/ai/core/execution-efficiency.md"

run_must_pass "parallel-task-orchestration-valid" bash .systems/scripts/check-parallel-task-orchestration
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nWorkers may not bypass QA.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_pass "parallel-task-orchestration-may-not-prohibition" bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nWorkers can skip Phase 7.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_fail "parallel-task-orchestration-phase-seven-bypass" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nTwo implementation-range autopilots can run in the same project.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_fail "parallel-task-orchestration-dual-owners" --expect-literal 'Unsafe parallel orchestration acceptance' bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
for pto_consumer in parallel-work-policy autopilot implementation-slicing command-routing operating-model workflow; do
  cp "$tmp/.systems/ai/core/$pto_consumer.md" "$tmp/pto-consumer.orig"
  printf '\nDelegation may bypass QA.\n' >> "$tmp/.systems/ai/core/$pto_consumer.md"
  run_must_fail "parallel-task-orchestration-consumer-$pto_consumer" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
  mv "$tmp/pto-consumer.orig" "$tmp/.systems/ai/core/$pto_consumer.md"
done
for pto_artifact in project-plan readiness state; do
  case "$pto_artifact" in
    project-plan) pto_path='.systems/ai/workflow/phase-2-project-plan.md' ;;
    readiness) pto_path='.systems/ai/templates/autopilot/readiness.template.md' ;;
    state) pto_path='.systems/ai/templates/autopilot/state.template.md' ;;
  esac
  cp "$tmp/$pto_path" "$tmp/pto-consumer.orig"
  printf '\nDelegation may bypass QA.\n' >> "$tmp/$pto_path"
  run_must_fail "parallel-task-orchestration-artifact-$pto_artifact" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
  mv "$tmp/pto-consumer.orig" "$tmp/$pto_path"
done
for pto_unsafe in recursive scope phase-eight; do
  case "$pto_unsafe" in
    recursive) pto_claim='Workers may delegate recursively.' ;;
    scope) pto_claim='Workers may expand scope.' ;;
    phase-eight) pto_claim='Workers may run Phase 8.' ;;
  esac
  cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
  printf '\n%s\n' "$pto_claim" >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
  run_must_fail "parallel-task-orchestration-authority-$pto_unsafe" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
  mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
done
for pto_equivalent in auto-push completion-capacity unlimited-capacity; do
  case "$pto_equivalent" in
    auto-push) pto_claim='Workers may automatically push.'; pto_diagnostic='Unsafe parallel orchestration wording' ;;
    completion-capacity) pto_claim='Worker completion is sufficient for PASS.'; pto_diagnostic='Unsafe parallel orchestration acceptance' ;;
    unlimited-capacity) pto_claim='Unknown capacity allows unlimited workers.'; pto_diagnostic='Unsafe parallel orchestration acceptance' ;;
  esac
  cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
  printf '\n%s\n' "$pto_claim" >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
  run_must_fail "parallel-task-orchestration-equivalent-$pto_equivalent" --expect-literal "$pto_diagnostic" bash .systems/scripts/check-parallel-task-orchestration
  mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
done
for pto_reverse in but however period colon semicolon unless yet; do
  case "$pto_reverse" in
    but) pto_join=', but ' ;;
    however) pto_join=', however ' ;;
    period) pto_join='. ' ;;
    colon) pto_join=': ' ;;
    semicolon) pto_join='; ' ;;
    unless) pto_join=' unless ' ;;
    yet) pto_join=', yet ' ;;
  esac
  cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
  printf '\nDelegation may bypass QA%sworkers must not bypass approvals.\n' "$pto_join" >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
  run_must_fail "parallel-task-orchestration-reverse-$pto_reverse" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
  mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
done
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nDelegation must not bypass QA.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_pass "parallel-task-orchestration-safe-prohibition" bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nDelegation may bypass QA.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_fail "parallel-task-orchestration-direct-boundary" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
for pto_separator in however period colon semicolon unless yet; do
  case "$pto_separator" in
    however) pto_join=', however ' ;;
    period) pto_join='. ' ;;
    colon) pto_join=': ' ;;
    semicolon) pto_join='; ' ;;
    unless) pto_join=' unless ' ;;
    yet) pto_join=', yet ' ;;
  esac
  cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
  printf '\nDelegation must not bypass QA%sdelegation may bypass QA.\n' "$pto_join" >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
  run_must_fail "parallel-task-orchestration-separator-$pto_separator" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
  mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
done
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nDelegation must not bypass QA, but delegation may bypass QA.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_fail "parallel-task-orchestration-compound-boundary" --expect-literal 'Unsafe parallel orchestration wording' bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
cp "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
printf '\nSubmitted may count as accepted.\n' >> "$tmp/.systems/ai/core/parallel-task-orchestration.md"
run_must_fail "parallel-task-orchestration-submitted-is-not-accepted" --expect-literal 'Unsafe parallel orchestration acceptance' bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"
mv "$tmp/.systems/ai/core/parallel-task-orchestration.md" "$tmp/pto-contract.orig"
run_must_fail "parallel-task-orchestration-missing-contract" --expect-literal 'Missing parallel orchestration contract' bash .systems/scripts/check-parallel-task-orchestration
mv "$tmp/pto-contract.orig" "$tmp/.systems/ai/core/parallel-task-orchestration.md"

run_must_pass "parallel-planner-offline-regressions" python3 .systems/scripts/lib/parallel-orchestration-tests.py --case planner
run_must_pass "parallel-protocol-offline-regressions" python3 .systems/scripts/lib/parallel-orchestration-tests.py --case protocol
run_must_pass "parallel-lifecycle-offline-regressions" python3 .systems/scripts/lib/parallel-orchestration-tests.py --case lifecycle
run_must_pass "parallel-integration-offline-regressions" python3 .systems/scripts/lib/parallel-orchestration-tests.py --case integration
run_must_pass "parallel-compatibility-offline-regressions" python3 .systems/scripts/lib/parallel-orchestration-tests.py --case compatibility

run_must_pass "phase-commit-policy-valid" bash .systems/scripts/check-phase-commit-policy
run_must_pass "phase-commit-policy-offline-regressions" python3 .systems/scripts/tests/phase-commit-policy.py
cp "$tmp/.systems/ai/core/phase-commit-policy.md" "$tmp/phase-commit.orig"
printf '\nBinding must not bypass QA.\n' >> "$tmp/.systems/ai/core/phase-commit-policy.md"
run_must_pass "phase-commit-policy-safe-prohibition" bash .systems/scripts/check-phase-commit-policy
mv "$tmp/phase-commit.orig" "$tmp/.systems/ai/core/phase-commit-policy.md"
for phase_join in direct but however period colon semicolon unless yet; do
  case "$phase_join" in
    direct) phase_prefix='' ;;
    but) phase_prefix='Binding must not bypass QA, but ' ;;
    however) phase_prefix='Binding must not bypass QA, however ' ;;
    period) phase_prefix='Binding must not bypass QA. ' ;;
    colon) phase_prefix='Binding must not bypass QA: ' ;;
    semicolon) phase_prefix='Binding must not bypass QA; ' ;;
    unless) phase_prefix='Binding must not bypass QA unless ' ;;
    yet) phase_prefix='Binding must not bypass QA, yet ' ;;
  esac
  cp "$tmp/.systems/ai/core/phase-commit-policy.md" "$tmp/phase-commit.orig"
  printf '\n%sbinding may bypass QA.\n' "$phase_prefix" >> "$tmp/.systems/ai/core/phase-commit-policy.md"
  run_must_fail "phase-commit-policy-boundary-$phase_join" --expect-literal 'Unsafe phase commit authority wording' bash .systems/scripts/check-phase-commit-policy
  mv "$tmp/phase-commit.orig" "$tmp/.systems/ai/core/phase-commit-policy.md"
done
mv "$tmp/.systems/ai/core/phase-commit-policy.md" "$tmp/phase-commit.orig"
run_must_fail "phase-commit-policy-missing-source" --expect-literal 'Policy-boundary scan failed' bash .systems/scripts/check-phase-commit-policy
mv "$tmp/phase-commit.orig" "$tmp/.systems/ai/core/phase-commit-policy.md"

run_must_pass "parallel-cross-system-offline-regressions" python3 .systems/scripts/tests/parallel-compatibility.py

run_must_pass "execution-modes-valid" bash .systems/scripts/check-execution-modes
run_must_pass "execution-modes-behavioral" python3 .systems/scripts/tests/execution-modes.py
cp "$tmp/.systems/ai/core/owner-decision-checkpoints.md" "$tmp/owner-mode.orig"
printf '\nautopilot may continue only verified independent units while a pending material decision blocks excluded units and dependents.\n' >> "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_pass "execution-modes-qualified-independent-policy" bash .systems/scripts/check-owner-decision-checkpoints
printf '\nAuto may dispatch a unit blocked by a pending material decision.\n' >> "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
run_must_fail "execution-modes-blocked-unit-policy" --expect-literal 'Unsafe owner decision checkpoint wording' bash .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/owner-mode.orig" "$tmp/.systems/ai/core/owner-decision-checkpoints.md"
cp "$tmp/.systems/ai/core/execution-modes.md" "$tmp/execution-mode.orig"
printf '\nAuto must not bypass QA.\n' >> "$tmp/.systems/ai/core/execution-modes.md"
run_must_pass "execution-modes-safe-prohibition" bash .systems/scripts/check-execution-modes
mv "$tmp/execution-mode.orig" "$tmp/.systems/ai/core/execution-modes.md"
for em_join in direct but however period colon semicolon unless yet; do
  case "$em_join" in
    direct) em_prefix='' ;;
    but) em_prefix='Auto must not bypass QA, but ' ;;
    however) em_prefix='Auto must not bypass QA, however ' ;;
    period) em_prefix='Auto must not bypass QA. ' ;;
    colon) em_prefix='Auto must not bypass QA: ' ;;
    semicolon) em_prefix='Auto must not bypass QA; ' ;;
    unless) em_prefix='Auto must not bypass QA unless ' ;;
    yet) em_prefix='Auto must not bypass QA, yet ' ;;
  esac
  cp "$tmp/.systems/ai/core/execution-modes.md" "$tmp/execution-mode.orig"
  printf '\n%sAuto may bypass QA.\n' "$em_prefix" >> "$tmp/.systems/ai/core/execution-modes.md"
  run_must_fail "execution-modes-boundary-$em_join" --expect-literal 'Unsafe execution mode authority wording' bash .systems/scripts/check-execution-modes
  mv "$tmp/execution-mode.orig" "$tmp/.systems/ai/core/execution-modes.md"
done
cp "$tmp/.systems/ai/core/execution-modes.md" "$tmp/execution-mode.orig"
printf '\nAuto may mark completed with incomplete DoD.\n' >> "$tmp/.systems/ai/core/execution-modes.md"
run_must_fail "execution-modes-false-completion" --expect-literal 'Unsafe execution mode completion wording' bash .systems/scripts/check-execution-modes
mv "$tmp/execution-mode.orig" "$tmp/.systems/ai/core/execution-modes.md"
mv "$tmp/.systems/ai/core/execution-modes.md" "$tmp/execution-mode.orig"
run_must_fail "execution-modes-missing-contract" --expect-literal 'Execution modes contract missing' bash .systems/scripts/check-execution-modes
mv "$tmp/execution-mode.orig" "$tmp/.systems/ai/core/execution-modes.md"
cp "$tmp/.systems/ai/templates/autopilot/state.template.md" "$tmp/execution-state.orig"
perl -0pi -e 's/  approval-reference: <actual-owner-scope-reference>\n//' "$tmp/.systems/ai/templates/autopilot/state.template.md"
run_must_fail "execution-modes-missing-producer-field" --expect-literal 'Execution modes producer field missing' bash .systems/scripts/check-execution-modes
mv "$tmp/execution-state.orig" "$tmp/.systems/ai/templates/autopilot/state.template.md"

echo "Owned smoke group passed."
smoke_suite_completed=1
