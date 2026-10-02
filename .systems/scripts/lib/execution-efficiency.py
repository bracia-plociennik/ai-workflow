#!/usr/bin/env python3
"""Explicit execution plans, authenticated evidence and privacy-minimal timing."""
import argparse
import hashlib
import hmac
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import uuid

HERE = Path(__file__).resolve().parent
WORKFLOW = HERE.parents[2]
REUSE_CHECKS = {"check-required-artifacts", "check-full-qa-verification"}
PHASES = {"discovery-refresh", "implementation", "review", "product-tests",
          "artifact-work", "artifact-rework", "owner-waiting", "publication"}
CAPABILITIES = ("source-bound-check-reuse", "project-artifact-validation", "bounded-defect",
                "historical-qa-lifecycle", "quality-record-producer", "selective-refresh", "process-timing")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load_module("eff_scope", HERE / "validation-scope.py")
timing = load_module("eff_timing", HERE / "validation-timing.py")


def read_json(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("JSON input must be an unlinked regular file")
    return scope.strict_json(path.read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def contained(root, relative):
    relative = scope.relative(relative)
    root = Path(root).resolve(strict=True)
    path = root / relative
    for item in (path, *path.parents):
        if item == root:
            break
        if item.is_symlink():
            raise ValueError("linked input is not approved")
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("input escapes approved root")
    return resolved


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def key_bytes(path):
    path = Path(path)
    if path.is_symlink():
        raise ValueError("reuse key must not be linked")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or info.st_uid != os.getuid():
            raise ValueError("reuse key must be owner-only")
        value = stream.read()
    if len(value) < 32:
        raise ValueError("reuse key must have at least 32 bytes")
    return value


def sign(record, key):
    body = {k: v for k, v in record.items() if k != "authentication"}
    return hmac.new(key, digest(body).encode(), hashlib.sha256).hexdigest()


def verify_record(record, key):
    if not isinstance(record, dict) or record.get("schema") != 1:
        raise ValueError("unsupported evidence schema")
    if not hmac.compare_digest(str(record.get("authentication", "")), sign(record, key)):
        raise ValueError("evidence authentication mismatch")
    if record.get("state") != "completed" or record.get("exit_code") != 0:
        raise ValueError("incomplete or failed source evidence")
    return record


def publish(path, value):
    path = canonical_path(timing.safe_output(str(path)))
    # Reject linked parents rather than resolving them into a permitted output.
    if any(parent.is_symlink() for parent in (path, *path.parents)):
        raise ValueError("linked evidence output")
    if path.exists():
        raise ValueError("evidence output already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".eff-", delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write((json.dumps(value, indent=2, allow_nan=False) + "\n").encode())
            stream.flush()
            os.fsync(stream.fileno())
            os.link(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def canonical_path(raw):
    path = Path(raw).expanduser().absolute()
    # macOS /tmp and /var are platform aliases, not owner-supplied links.
    for alias in (Path("/tmp"), Path("/var")):
        if alias.is_symlink() and path.is_relative_to(alias):
            path = alias.resolve() / path.relative_to(alias)
            break
    if any(parent.is_symlink() for parent in (path, *path.parents)):
        raise ValueError("linked path is not approved")
    return path


def source_identity(root):
    root = Path(root).resolve(strict=True)
    result = subprocess.run([str(root / ".systems/scripts/report-validation-comparison"), "source-digest"],
                            cwd=root, capture_output=True, text=True, check=True)
    value = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("invalid source identity")
    return value


def environment_identity():
    tools = {}
    for name, argv in (("python3", [sys.executable, "--version"]), ("git", ["git", "--version"]),
                       ("rg", ["rg", "--version"]), ("bash", ["bash", "--version"])):
        executable = shutil.which(argv[0])
        if not executable:
            raise ValueError("missing tool: " + name)
        result = subprocess.run(argv, capture_output=True, check=True)
        tools[name] = digest([str(Path(executable).resolve()), file_hash(Path(executable).resolve()), result.stdout.decode(errors="replace"),
                              result.stderr.decode(errors="replace")])
    # Values never leave this digest. Shell bookkeeping does not affect checks.
    bookkeeping = {"_", "SHLVL", "AI_WORKFLOW_HOME", "AI_WORKFLOW_WORKSPACE_HOME",
                   "AI_WORKFLOW_MODE_RESOLVED", "TARGET_REPO_ROOT", "AI_WORKFLOW_TIMING_RUN_ID",
                   "AI_WORKFLOW_TIMING_OUTPUT"}
    env = {k: v for k, v in os.environ.items() if k not in bookkeeping}
    return digest({"tools": tools, "environment": env, "platform": sys.platform})


def preflight(root, output=None, process_metadata=True):
    root = Path(root).resolve(strict=True)
    if not (root / "AGENTS.md").is_file() or not (root / ".systems/scripts/run-with-timeout").is_file():
        raise ValueError("workflow root/capability missing")
    environment_identity()
    if process_metadata:
        result = subprocess.run(["ps", "-p", str(os.getpid()), "-o", "pid=", "-o", "ppid="],
                                capture_output=True)
        if result.returncode or not result.stdout.strip():
            raise ValueError("process metadata unavailable before expensive work")
    if output:
        path = canonical_path(timing.safe_output(str(output)))
        if path.exists() or any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError("unsafe or existing output")
        parent = path.parent
        while not parent.exists():
            parent = parent.parent
        if not os.access(parent, os.W_OK):
            raise ValueError("output parent is not writable")
    return {"state": "ready", "environment": environment_identity(), "root": digest(str(root))}


def execute_bound(argv, binding, previous, key, *, cwd, timeout):
    if previous:
        verify_record(previous, key)
        if previous.get("binding") == binding:
            return {"schema": 1, "run_id": uuid.uuid4().hex, "state": "completed", "exit_code": 0,
                    "binding": binding, "execution": "reused", "duration_ns": 0,
                    "source_run_id": previous["run_id"], "reason": "identical declared inputs"}
    start = time.monotonic_ns()
    process = subprocess.Popen(argv, cwd=cwd, start_new_session=True)
    def stop_child():
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
    try:
        code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        stop_child()
        code = 124
    except KeyboardInterrupt:
        stop_child()
        code = 130
    return {"schema": 1, "run_id": uuid.uuid4().hex,
            "state": "completed" if code == 0 else "failed", "exit_code": code,
            "binding": binding, "execution": "invalidated" if previous else "executed",
            "duration_ns": time.monotonic_ns() - start,
            "reason": "changed binding" if previous else "fresh execution"}


def execute_plan(plan_path, output, key_path, previous_path=None, progress="summary"):
    plan = read_json(plan_path)
    scope.fields(plan, {"schema", "purpose", "checks", "scope_manifest", "workflow_root"}, "check plan")
    if plan["schema"] != 1 or plan["purpose"] != "iteration":
        raise ValueError("execution reuse is iteration-only; full/CI/updater must execute fresh")
    if os.environ.get("CI", "").lower() in {"1", "true"}:
        raise ValueError("CI requires fresh full validation")
    root = Path(plan["workflow_root"]).resolve(strict=True)
    if root != WORKFLOW:
        raise ValueError("plan workflow root differs from executing helper")
    preflight(root, output)
    key = key_bytes(key_path)
    previous = verify_record(read_json(previous_path), key) if previous_path else None
    registry_path = root / ".systems/scripts/lib/validation-checks.json"
    registry = read_json(registry_path)["checks"]
    if not isinstance(plan["checks"], list) or not plan["checks"]:
        raise ValueError("empty check plan")
    IDs = [item.get("id") for item in plan["checks"] if isinstance(item, dict)]
    if len(IDs) != len(plan["checks"]) or len(set(IDs)) != len(IDs):
        raise ValueError("invalid or duplicate check IDs")
    # The existing planner owns dependency coverage. Only iteration evidence is returned here.
    for check_id in IDs:
        if check_id not in registry:
            raise ValueError("unknown check")
        if any(dependency not in IDs for dependency in registry[check_id]["dependencies"]):
            raise ValueError("missing declared check dependency")
    before = source_identity(root)
    env = environment_identity()
    records = []
    status = 0
    previous_checks = {item["id"]: item for item in previous.get("checks", [])} if previous else {}
    if previous and (len(previous_checks) != len(previous.get("checks", []))
                     or set(previous_checks) != set(previous.get("planned", []))):
        raise ValueError("incomplete source check inventory")
    for item in plan["checks"]:
        scope.fields(item, {"id", "category", "inputs", "arguments", "coverage"}, "planned check")
        check_id = item["id"]
        if item["category"] not in {"product", "runtime-artifact", "integration", "environment"}:
            raise ValueError("unknown applicability category")
        if not isinstance(item["coverage"], list) or not item["coverage"] or not all(
                isinstance(x, str) and re.fullmatch(r"[a-z0-9-]+", x) for x in item["coverage"]):
            raise ValueError("missing coverage declaration")
        if not isinstance(item["inputs"], list) or len(set(item["inputs"])) != len(item["inputs"]):
            raise ValueError("invalid input inventory")
        # Runtime/foreign inputs require the existing manifest route, never guessed closure.
        if item["arguments"] or plan["scope_manifest"] is not None:
            raise ValueError("runtime scope uses validate-workflow --scope-manifest, not iteration reuse")
        hashes = {raw: file_hash(contained(root, raw)) for raw in item["inputs"]}
        reusable = check_id in REUSE_CHECKS and item["category"] == "product"
        binding = digest({"root": str(root), "source": before, "inputs": hashes,
                          "command": check_id, "args": item["arguments"], "coverage": item["coverage"],
                          "registry": file_hash(registry_path), "environment": env})
        prior = previous_checks.get(check_id) if reusable else None
        if prior:
            if prior.get("state") != "completed" or prior.get("exit_code") != 0:
                raise ValueError("failed check cannot be reused")
            prior = dict(prior)
            prior["authentication"] = sign(prior, key)
        if progress != "quiet":
            print("AI_WORKFLOW_CHECK_START check=" + check_id, flush=True)
        argv = [str(root / ".systems/scripts/run-with-timeout"), "--timeout-seconds", "1200",
                str(root / ".systems/scripts" / check_id)]
        record = execute_bound(argv, binding, prior, key, cwd=root, timeout=1210)
        record["id"] = check_id
        record["reusable"] = reusable
        records.append(record)
        if progress != "quiet":
            print("AI_WORKFLOW_CHECK_COMPLETE check=" + check_id + " execution=" + record["execution"]
                  + " exit_code=" + str(record["exit_code"]), flush=True)
        if record["exit_code"]:
            status = record["exit_code"]
            break
    if source_identity(root) != before or environment_identity() != env:
        status = 1
    result = {"schema": 1, "run_id": uuid.uuid4().hex, "purpose": "iteration",
              "source": before, "state": "completed" if status == 0 else "failed",
              "exit_code": status, "planned": IDs, "checks": records,
              "coverage_result": "unverified", "final_evidence_eligible": False}
    result["authentication"] = sign(result, key)
    publish(output, result)
    return status


def source_run_start(output, key_path):
    preflight(WORKFLOW, output)
    key = key_bytes(key_path)
    value = {"schema": 1, "run_id": uuid.uuid4().hex, "purpose": "full-source-start",
             "source": source_identity(WORKFLOW), "environment": environment_identity(),
             "root": digest(str(WORKFLOW)), "state": "started", "exit_code": None}
    value["authentication"] = sign(value, key)
    publish(output, value)


def source_run_finish(start_path, output, key_path, status, checks):
    key = key_bytes(key_path)
    start = read_json(start_path)
    if not hmac.compare_digest(str(start.get("authentication", "")), sign(start, key)):
        raise ValueError("source-start authentication mismatch")
    if (start.get("purpose") != "full-source-start" or start.get("state") != "started"
            or start.get("root") != digest(str(WORKFLOW))):
        raise ValueError("invalid source-start record")
    registry = read_json(HERE / "validation-checks.json")
    complete = set(registry["checks"]).issubset(set(checks))
    valid = (status == 0 and complete and start["source"] == source_identity(WORKFLOW)
             and start["environment"] == environment_identity())
    result = {**start, "purpose": "full-source-verification",
              "state": "completed" if valid else "failed", "exit_code": 0 if valid else 1,
              "source_exit_code": status,
              "checks": checks, "supporting_only": True}
    result["authentication"] = sign(result, key)
    publish(output, result)
    if not valid:
        raise ValueError("full source receipt is incomplete or changed")


def verify_source(receipt, key_path):
    record = verify_record(read_json(receipt), key_bytes(key_path))
    required = set(read_json(HERE / "validation-checks.json")["checks"])
    if (record.get("purpose") != "full-source-verification"
            or record.get("source") != source_identity(WORKFLOW)
            or record.get("environment") != environment_identity()
            or record.get("root") != digest(str(WORKFLOW))
            or not required.issubset(set(record.get("checks", [])))):
        raise ValueError("source gate receipt is stale or incomplete")
    return record


def artifact_closure(workspace, project, receipt, key_path, output):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project):
        raise ValueError("unsafe artifact project")
    source_record = verify_source(receipt, key_path)
    workspace = canonical_path(workspace)
    if any(parent.is_symlink() for parent in (workspace, *workspace.parents)):
        raise ValueError("linked workspace")
    workspace = workspace.resolve(strict=True)
    preflight(WORKFLOW, output)
    owner = workspace / "projects" / project
    def runtime_binding():
        legacy = workspace / "repo/core/legacy-qa-evidence-v1.md"
        ancillary = file_hash(contained(workspace, "repo/core/legacy-qa-evidence-v1.md")) if legacy.exists() or legacy.is_symlink() else None
        return digest({"runtime": scope.inventory_runtime(workspace, ["projects/" + project]), "legacy": ancillary})
    before = runtime_binding()
    checks = []
    result = 0
    for check_id in ("check-naming", "check-qa-evidence", "check-status-consistency", "check-distillation-state"):
        argv = [str(WORKFLOW / ".systems/scripts/run-with-timeout"), "--timeout-seconds", "1200",
                str(WORKFLOW / ".systems/scripts" / check_id), "--runtime-only", "--scope-root", "projects/" + project]
        env = {**os.environ, "AI_WORKFLOW_WORKSPACE_HOME": str(workspace)}
        code = subprocess.run(argv, cwd=WORKFLOW, env=env, check=False).returncode
        checks.append({"id": check_id, "state": "executed", "exit_code": code})
        if code:
            result = code
            break
    if before != runtime_binding():
        result = 1
    verify_source(receipt, key_path)
    report = {"schema": 1, "purpose": "artifact-closure", "source_run_id": source_record["run_id"],
              "source_checks": "previous-fresh-full-current", "runtime_checks": checks,
              "runtime_fingerprint": before, "semantic_qa_required": True,
              "approval_granted": False, "exit_code": result,
              "coverage": "complete" if result == 0 else "incomplete"}
    publish(output, report)
    return result


def bounded_defect(record):
    scope.fields(record, {"risk", "scope", "dod", "consumers", "reversible", "approval",
                          "regressions", "semantic_review", "impacts", "capture"}, "bounded defect")
    if record["risk"] not in {"low", "medium"} or record["reversible"] is not True:
        raise ValueError("defect is not safely bounded")
    for field in ("scope", "approval", "semantic_review", "capture"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError("missing bounded defect evidence: " + field)
    for field in ("dod", "consumers", "regressions"):
        if not isinstance(record[field], list) or not record[field] or not all(
                isinstance(value, str) and value.strip() for value in record[field]):
            raise ValueError("missing bounded defect evidence: " + field)
    if record["impacts"] != []:
        raise ValueError("security/permission/billing/migration/production/architecture or unknown impact excludes bounded route")
    return {"eligible": True, "permission_granted": False, "quality_required": True,
            "route": "bounded-defect", "scope_fingerprint": digest(record)}


def process_timing(record):
    scope.fields(record, {"schema", "clock", "intervals", "unknown"}, "process timing")
    if record["schema"] != 1 or record["clock"] != "monotonic":
        raise ValueError("unsupported process clock")
    intervals = []
    for item in record["intervals"]:
        scope.fields(item, {"phase", "start", "end", "measurement", "reason", "input_fingerprint"}, "interval")
        if item["phase"] not in PHASES or item["measurement"] not in {"observed", "estimate"}:
            raise ValueError("unknown process phase or measurement")
        if not item["reason"] or not re.fullmatch(r"[0-9a-f]{64}", item["input_fingerprint"]):
            raise ValueError("missing rerun reason or inputs")
        if any(isinstance(item[x], bool) or not isinstance(item[x], (int, float))
               or not math.isfinite(item[x]) for x in ("start", "end")):
            raise ValueError("invalid interval time")
        if item["start"] < 0 or item["end"] < item["start"]:
            raise ValueError("reversed process interval")
        if item["measurement"] == "observed":
            intervals.append((item["start"], item["end"]))
    if not isinstance(record["unknown"], list) or not all(isinstance(x, str) for x in record["unknown"]) or not set(record["unknown"]).issubset(PHASES):
        raise ValueError("unknown phase classification")
    observed_phases = {item["phase"] for item in record["intervals"] if item["measurement"] == "observed"}
    unmeasured = sorted(PHASES - observed_phases)
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return {"observed_union_seconds": sum(end-start for start, end in merged),
            "unmeasured_phases": sorted(set(record["unknown"]) | set(unmeasured)), "estimates_included_in_wall": False}


def refresh(snapshot, root, scope_id, trigger):
    scope.fields(snapshot, {"schema", "scope", "stage", "approval_reference", "contracts",
                            "repository", "baseline", "authority_inputs"}, "refresh snapshot")
    if snapshot["schema"] != 1 or snapshot["scope"] != scope_id or not snapshot["approval_reference"]:
        raise ValueError("refresh scope/approval conflict")
    if snapshot["repository"] != digest(str(Path(root).resolve())) or not re.fullmatch(r"[0-9a-f]{40}", snapshot["baseline"]):
        raise ValueError("refresh repository/baseline conflict")
    live_head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if snapshot["baseline"] != live_head:
        raise ValueError("refresh HEAD conflict; reread current repository baseline")
    if trigger not in {"continuation", "resume", "compaction", "scope-change", "quality", "commit", "source-conflict"}:
        raise ValueError("unknown refresh trigger")
    changed = []
    if not isinstance(snapshot["contracts"], dict) or not snapshot["contracts"] or "AGENTS.md" not in snapshot["contracts"]:
        raise ValueError("refresh snapshot missing authority")
    if not isinstance(snapshot["stage"], str) or not snapshot["stage"].strip():
        raise ValueError("refresh stage missing")
    authority_changed = []
    if not isinstance(snapshot["authority_inputs"], dict) or not snapshot["authority_inputs"]:
        raise ValueError("refresh requires accepted scope/status/decision inputs")
    if set(snapshot["contracts"]) & set(snapshot["authority_inputs"]):
        raise ValueError("duplicate authority fingerprint")
    for path, checksum in {**snapshot["contracts"], **snapshot["authority_inputs"]}.items():
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise ValueError("invalid contract fingerprint")
        if file_hash(contained(root, path)) != checksum:
            changed.append(path)
            if path in snapshot["authority_inputs"]:
                authority_changed.append(path)
    return {"status": "blocked" if authority_changed else "verification-complete",
            "required_refresh": "full" if trigger in {"resume", "compaction", "scope-change", "source-conflict"} else "targeted",
            "re_read": changed, "required_relevant_sources": True,
            "stage": snapshot["stage"], "permission_granted": False}


def benchmark_check(root, check, source, stage):
    key = b"synthetic-benchmark-key-32-bytes-only"
    receipt = root / "receipt.json"
    previous = read_json(receipt) if stage else None
    binding = digest({"implementation": file_hash(check), "input": file_hash(source),
                      "python": sys.version, "coverage": ["intent", "consumer", "failure", "regression"]})
    result = execute_bound([sys.executable, str(check), str(source)], binding, previous, key,
                           cwd=root, timeout=10)
    result["authentication"] = sign(result, key)
    # Disposable fixture receipt; never production authentication key.
    if stage:
        receipt.unlink()
    publish(receipt, result)
    if result["exit_code"]:
        raise ValueError("benchmark check failed")
    return "reused" if result["execution"] == "reused" else "executed"


def main():
    def interrupt(_number, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupt)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    execute = sub.add_parser("execute")
    execute.add_argument("--plan", required=True)
    execute.add_argument("--output", required=True)
    execute.add_argument("--key-file", required=True)
    execute.add_argument("--reuse")
    execute.add_argument("--progress", choices=("quiet", "summary", "verbose"), default="summary")
    pre = sub.add_parser("preflight")
    pre.add_argument("--output")
    for action in ("bounded-defect", "timing"):
        child = sub.add_parser(action)
        child.add_argument("record")
    ref = sub.add_parser("refresh")
    ref.add_argument("snapshot")
    ref.add_argument("--scope", required=True)
    ref.add_argument("--trigger", required=True)
    sub.add_parser("capabilities")
    start = sub.add_parser("source-start")
    start.add_argument("--output", required=True)
    start.add_argument("--key-file", required=True)
    finish = sub.add_parser("source-finish")
    finish.add_argument("--start", required=True)
    finish.add_argument("--output", required=True)
    finish.add_argument("--key-file", required=True)
    finish.add_argument("--status", required=True, type=int)
    finish.add_argument("--checks", required=True)
    source_check = sub.add_parser("verify-source")
    source_check.add_argument("--receipt", required=True)
    source_check.add_argument("--key-file", required=True)
    artifact = sub.add_parser("artifact-closure")
    artifact.add_argument("--workspace", required=True)
    artifact.add_argument("--project", required=True)
    artifact.add_argument("--receipt", required=True)
    artifact.add_argument("--key-file", required=True)
    artifact.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.action == "execute":
            return execute_plan(args.plan, args.output, args.key_file, args.reuse, args.progress)
        if args.action == "source-start":
            source_run_start(args.output, args.key_file)
            return 0
        if args.action == "source-finish":
            source_run_finish(args.start, args.output, args.key_file, args.status, args.checks.split(","))
            return 0
        if args.action == "verify-source":
            result = {"source_gate_satisfied": True, "run_id": verify_source(args.receipt, args.key_file)["run_id"],
                      "semantic_qa_required": True, "approval_granted": False}
        elif args.action == "artifact-closure":
            return artifact_closure(args.workspace, args.project, args.receipt, args.key_file, args.output)
        elif args.action == "preflight":
            result = preflight(WORKFLOW, args.output)
        elif args.action == "bounded-defect":
            result = bounded_defect(read_json(args.record))
        elif args.action == "timing":
            result = process_timing(read_json(args.record))
        elif args.action == "refresh":
            result = refresh(read_json(args.snapshot), WORKFLOW, args.scope, args.trigger)
        else:
            result = read_json(WORKFLOW / ".systems/ai/capabilities/execution-efficiency-v1.json")
        print(json.dumps(result, sort_keys=True))
        return 0
    except KeyboardInterrupt:
        print("Execution efficiency interrupted", file=sys.stderr)
        return 130
    except (ValueError, OSError, subprocess.SubprocessError, KeyError, TypeError) as error:
        print("Execution efficiency error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
