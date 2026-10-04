#!/usr/bin/env python3
"""Read-only, conservative proposals for one coordinator-owned execution pool."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import unicodedata

ID = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\Z")
SHA = re.compile(r"[0-9a-f]{64}\Z")
STATES = {"planned", "ready", "running", "submitted", "accepted", "rejected", "blocked", "cancelled"}
RUN_KEYS = {"schema", "run_id", "project", "repository_root", "execution_owner",
            "coordinator_id", "revision", "source_snapshot", "capacity",
            "isolation_verified", "checkpoint", "reservations", "units"}
UNIT_KEYS = {"schema", "id", "task_id", "package_id", "slice_id", "goal", "dod",
             "approval_reference", "priority", "dependencies", "expected_inputs",
             "read_set", "write_set", "resources", "state", "accepted_output"}
EXECUTION_KEYS = {"input_hashes", "required_checks", "stop_conditions", "minimal_context"}
OBSERVATION_KEYS = {"backend", "version", "handle", "cwd", "writable_roots",
                    "constraints_verified", "source_snapshot", "kind"}
RESULT_KEYS = {"schema", "run_id", "unit_id", "attempt_id", "handle", "source_snapshot",
               "baseline_digest", "output_digest", "changed_files", "checks", "findings",
               "skipped_checks", "residual_risk"}

class InvalidManifest(ValueError):
    pass

def require(condition, reason):
    if not condition:
        raise InvalidManifest(reason)

def fields(value, keys, label):
    require(type(value) is dict and set(value) == keys, "invalid fields: " + label)

def integer(value, label, minimum=0):
    require(type(value) is int and value >= minimum, "invalid integer: " + label)

def identity(value, label):
    require(type(value) is str and bool(ID.fullmatch(value)), "invalid identity: " + label)

def text(value, label):
    require(type(value) is str and bool(value.strip()) and not any(ord(c) < 32 for c in value),
            "invalid text: " + label)

def unique_ids(value, label):
    require(type(value) is list, "invalid list: " + label)
    for item in value:
        identity(item, label)
    require(len(value) == len(set(value)), "duplicate IDs: " + label)

def relative(value):
    require(type(value) is str and bool(value) and "\\" not in value
            and not any(ord(c) < 32 for c in value), "unsafe relative path")
    p = PurePosixPath(value)
    require(not p.is_absolute() and value == p.as_posix()
            and all(part not in {"..", "."} for part in value.split("/"))
            and value != ".", "unsafe relative path: " + value)
    return p

def physical_path(path):
    path = Path(path).absolute()
    require(".." not in path.parts, "parent traversal in physical path")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        require(not current.is_symlink(), "linked path component: " + str(current))
    return path

def inspect_access_tree(path):
    # Fail closed on inode aliases and unsupported subtrees rather than guessing
    # isolation. This is a bounded metadata scan; no file contents are read.
    pending = [path]
    count = 0
    while pending:
        current = pending.pop()
        count += 1
        require(count <= 10000, "access subtree exceeds safe inventory limit")
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISREG(info.st_mode):
            require(info.st_nlink == 1, "hard-linked access path: " + str(current))
        elif stat.S_ISDIR(info.st_mode):
            with os.scandir(current) as entries:
                for entry in entries:
                    count += 1
                    require(count <= 10000, "access subtree exceeds safe inventory limit")
                    pending.append(Path(entry.path))
        else:
            raise InvalidManifest("linked or special access subtree: " + str(current))

def canonical(root, value):
    relative(value)
    current = root
    for part in value.split("/"):
        current = current / part
        require(not current.is_symlink(), "linked path: " + value)
        if current.exists() and current != root / value:
            require(current.is_dir(), "non-directory path parent: " + value)
        if current.exists():
            require(current.is_dir() or current.is_file(), "special path: " + value)
    resolved = current.resolve()
    require(resolved.is_relative_to(root), "path escaped repository: " + value)
    inspect_access_tree(resolved)
    return resolved

def overlap(left, right):
    if left.exists() and right.exists() and left.samefile(right):
        return True
    # Conservative for case-insensitive targets, including not-yet-created paths.
    a, b = (unicodedata.normalize("NFC", unicodedata.normalize("NFC", p.as_posix()).casefold())
            for p in (left, right))
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")

def resource_conflict(left, right):
    return any(a["name"] == b["name"]
               and (a.get("mode", "exclusive") != "shared-read"
                    or b.get("mode", "exclusive") != "shared-read")
               for a in left for b in right)

def conflicts(left, right, root):
    lr = [canonical(root, p) for p in left["read_set"]]
    lw = [canonical(root, p) for p in left["write_set"]]
    rr = [canonical(root, p) for p in right["read_set"]]
    rw = [canonical(root, p) for p in right["write_set"]]
    return (any(overlap(a, b) for a in lw for b in rr + rw)
            or any(overlap(a, b) for a in lr for b in rw)
            or resource_conflict(left["resources"], right["resources"]))

def validate(manifest):
    require(type(manifest) is dict and set(manifest) in (RUN_KEYS, RUN_KEYS | {"lifecycle"}),
            "invalid fields: run")
    require(type(manifest["schema"]) is int and manifest["schema"] == 1, "unsupported schema")
    for key in ("run_id", "project", "coordinator_id"):
        identity(manifest[key], key)
    integer(manifest["revision"], "revision")
    require(manifest["execution_owner"] in {"ai-workflow", "ai-system"}, "invalid execution owner")
    require(type(manifest["source_snapshot"]) is str
            and bool(SHA.fullmatch(manifest["source_snapshot"])), "invalid source snapshot")
    raw_root = manifest["repository_root"]
    text(raw_root, "repository root")
    require(type(raw_root) is str and Path(raw_root).is_absolute(), "absolute repository root required")
    root = physical_path(raw_root).resolve(strict=True)
    require(root.is_dir(), "repository root is not a directory")
    capacity = manifest["capacity"]
    fields(capacity, {"verified", "total", "active_workers"}, "capacity")
    require(type(capacity["verified"]) is bool, "invalid capacity verification")
    integer(capacity["active_workers"], "active workers")
    if capacity["total"] is not None:
        integer(capacity["total"], "total capacity")
    require(not capacity["verified"] or capacity["total"] is not None,
            "verified capacity requires total")
    require(capacity["total"] is None or capacity["active_workers"] <= capacity["total"],
            "active workers exceed total capacity")
    require(type(manifest["isolation_verified"]) is bool, "invalid isolation observation")
    checkpoint = manifest["checkpoint"]
    fields(checkpoint, {"known", "completed_since_checkpoint", "active_tasks"}, "checkpoint")
    require(type(checkpoint["known"]) is bool, "invalid checkpoint observation")
    integer(checkpoint["completed_since_checkpoint"], "completed task count")
    require(checkpoint["completed_since_checkpoint"] <= 3, "checkpoint cadence exceeded")
    unique_ids(checkpoint["active_tasks"], "active tasks")
    require(checkpoint["completed_since_checkpoint"] + len(checkpoint["active_tasks"]) <= 3,
            "checkpoint reservation exceeded")
    unique_ids(manifest["reservations"], "reservations")
    require(type(manifest["units"]) is list, "units must be a list")
    units = {}
    for unit in manifest["units"]:
        require(type(unit) is dict and set(unit) in (UNIT_KEYS, UNIT_KEYS | {"execution"}), "invalid unit fields")
        if unit.get("execution") is not None:
            execution_contract(unit["execution"])
        require(type(unit["schema"]) is int and unit["schema"] == 1, "invalid unit schema")
        for key in ("id", "task_id", "slice_id"):
            identity(unit[key], key)
        if unit["package_id"] is not None:
            identity(unit["package_id"], "package")
        text(unit["goal"], "goal")
        require(type(unit["dod"]) is list and bool(unit["dod"]), "missing DoD")
        for item in unit["dod"]:
            text(item, "DoD")
        relative(unit["approval_reference"])
        integer(unit["priority"], "priority")
        unique_ids(unit["dependencies"], "dependencies")
        require(unit["state"] in STATES, "invalid unit state")
        require(unit["id"] not in units, "duplicate unit ID")
        for key in ("read_set", "write_set"):
            require(type(unit[key]) is list, "invalid access set")
            for path in unit[key]:
                canonical(root, path)
            require(len(unit[key]) == len(set(unit[key])), "duplicate access path")
        require(type(unit["resources"]) is list, "invalid resources")
        names = set()
        for resource in unit["resources"]:
            require(type(resource) is dict and set(resource) in ({"name"}, {"name", "mode"}),
                    "invalid resource fields")
            identity(resource["name"], "resource")
            require(resource.get("mode", "exclusive") in {"exclusive", "shared-read"},
                    "unknown resource access mode")
            require(resource["name"] not in names, "duplicate resource")
            names.add(resource["name"])
        require(type(unit["expected_inputs"]) is dict, "invalid expected inputs")
        require(set(unit["expected_inputs"]).issubset(set(unit["dependencies"])),
                "input digest without dependency")
        for digest in unit["expected_inputs"].values():
            require(type(digest) is str and bool(SHA.fullmatch(digest)), "invalid dependency digest")
        output = unit["accepted_output"]
        require(output is None or (type(output) is str and bool(SHA.fullmatch(output))),
                "invalid accepted output digest")
        require((unit["state"] == "accepted") == (output is not None),
                "accepted state requires its immutable digest exclusively")
        units[unit["id"]] = unit
    require(set(manifest["reservations"]).issubset(units), "unknown reservation unit")
    running = [u for u in units.values() if u["state"] == "running"]
    require(len(running) <= capacity["active_workers"], "running pool omitted from capacity")
    reserved = {u["id"] for u in units.values() if u["state"] in {"running", "submitted"}}
    require(reserved.issubset(set(manifest["reservations"])), "active unit omitted from reservations")
    require({units[i]["task_id"] for i in manifest["reservations"]}.issubset(set(checkpoint["active_tasks"])),
            "reserved parent omitted from checkpoint state")
    for unit in units.values():
        require(set(unit["dependencies"]).issubset(units), "missing dependency")
        require(unit["id"] not in unit["dependencies"], "self dependency")
    # Kahn order is stable across input list ordering; priority breaks ready ties.
    remaining = set(units)
    ordered = []
    while remaining:
        ready = [units[i] for i in remaining
                 if set(units[i]["dependencies"]).issubset(set(ordered))]
        require(bool(ready), "dependency cycle")
        for unit in sorted(ready, key=lambda u: (-u["priority"], u["id"])):
            ordered.append(unit["id"])
            remaining.remove(unit["id"])
    if manifest.get("lifecycle") is not None:
        lifecycle_schema(manifest, units)
    return root, units, ordered

def plan(manifest):
    root, units, ordered = validate(manifest)
    capacity = manifest["capacity"]
    checkpoint = manifest["checkpoint"]
    result = {"schema": 1, "run_id": manifest["run_id"], "execution_authorized": False,
              "status": "blocked", "mode": "serial", "selected_count": 0,
              "proposed_units": [], "rejected_candidates": [],
              "observed_limits": {"capacity": capacity,
                                  "checkpoint": checkpoint,
                                  "isolation_verified": manifest["isolation_verified"]},
              "required_external_checks": ["current formal task gates and owner permission",
                                           "fresh backend observation and isolation before dispatch"]}
    if integration_pending(manifest):
        result["reason"] = "integration outcome unresolved; reservation retained"
        return result
    if all(unit["state"] == "accepted" for unit in units.values()):
        result["status"] = "complete"
        result["reason"] = "all declared units accepted; this is not task Quality PASS"
        return result
    parallel = capacity["verified"] and manifest["isolation_verified"]
    free = (capacity["total"] - capacity["active_workers"]
            if capacity["verified"] else max(0, 1 - capacity["active_workers"]))
    limit = free if parallel else min(1, free)
    selected = []
    active_tasks = set(checkpoint["active_tasks"])
    reserved = [units[i] for i in manifest["reservations"]]
    for unit_id in ordered:
        unit = units[unit_id]
        if unit["state"] not in {"planned", "ready"}:
            continue
        reasons = []
        for dep_id in sorted(unit["dependencies"]):
            predecessor = units[dep_id]
            if predecessor["state"] != "accepted":
                reasons.append("dependency not accepted: " + dep_id)
            elif unit["expected_inputs"].get(dep_id) != predecessor["accepted_output"]:
                reasons.append("missing or stale immutable dependency: " + dep_id)
            if predecessor["task_id"] != unit["task_id"]:
                reasons.append("cross-task formal Quality/capture gate review required: " + dep_id)
        if not checkpoint["known"]:
            reasons.append("unknown checkpoint state")
        if unit["task_id"] not in active_tasks and (
                checkpoint["completed_since_checkpoint"] + len(active_tasks) >= 3):
            reasons.append("checkpoint task slots exhausted")
        if any(conflicts(unit, other, root) for other in reserved + selected):
            reasons.append("path or resource reservation conflict")
        if len(selected) >= limit:
            reasons.append("free observed capacity exhausted")
        if reasons:
            result["rejected_candidates"].append({"unit_id": unit_id, "reasons": reasons})
        else:
            selected.append(unit)
            active_tasks.add(unit["task_id"])
    result["proposed_units"] = [unit["id"] for unit in selected]
    result["selected_count"] = len(selected)
    if selected:
        result["status"] = "ready"
        result["mode"] = ("parallel-implementation" if any(u["write_set"] for u in selected)
                          else "parallel-read-only") if len(selected) > 1 else "serial"
        result["reason"] = ("conflict-free units within observed limits" if parallel
                            else "serial fallback: unverified capacity or isolation")
    else:
        result["reason"] = "no eligible units; dependent, reserved, failed or unknown work remains"
    return result

def load(path):
    def pairs(items):
        output = {}
        for key, value in items:
            require(key not in output, "duplicate JSON key: " + key)
            output[key] = value
        return output
    path = physical_path(path)
    require(stat.S_ISREG(path.stat().st_mode), "manifest must be a regular file")
    require(path.stat().st_nlink == 1, "linked manifest or evidence inode")
    require(path.stat().st_size <= 8 * 1024 * 1024, "manifest exceeds safe size")
    def invalid_constant(value):
        raise InvalidManifest("non-finite JSON constant: " + value)
    return json.loads(path.read_text(), object_pairs_hook=pairs, parse_constant=invalid_constant)

def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()

def file_inventory(root):
    """Bounded actual worker inventory, including modes; no exclusions hide writes."""
    root = physical_path(root).resolve(strict=True)
    inspect_access_tree(root)
    result = {}
    total_bytes = 0
    for directory, dirs, names in os.walk(root, followlinks=False):
        require(".git" not in dirs and ".git" not in names, "worker Git metadata requires a separately verified adapter")
        if Path(directory) != root:
            result[Path(directory).relative_to(root).as_posix()] = {"sha256": None, "mode": stat.S_IMODE(Path(directory).stat().st_mode)}
        for name in names:
            path = Path(directory) / name
            relative(str(path.relative_to(root)))
            info = path.stat()
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "unsafe worker file type")
            total_bytes += info.st_size
            require(info.st_size <= 8 * 1024 * 1024 and total_bytes <= 64 * 1024 * 1024, "worker inventory exceeds safe size")
            result[path.relative_to(root).as_posix()] = {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "mode": stat.S_IMODE(info.st_mode)}
    return result

def execution_contract(value):
    fields(value, EXECUTION_KEYS, "execution")
    require(type(value["input_hashes"]) is dict, "invalid input hashes")
    for path, digest in value["input_hashes"].items():
        relative(path)
        require(type(digest) is str and bool(SHA.fullmatch(digest)), "invalid input hash")
    for key in ("required_checks", "stop_conditions", "minimal_context"):
        require(type(value[key]) is list and bool(value[key]), "missing execution " + key)
        for item in value[key]:
            text(item, key)
        require(len(value[key]) == len(set(value[key])), "duplicate execution " + key)
    return value

def protected_write(path):
    parts = {unicodedata.normalize("NFC", p.casefold()) for p in relative(path).parts}
    return bool(parts & {"status.md", "memory.md", "decisions", "capture-state", "checkpoints",
                         "distillations", "quality", "orchestration", ".git", "ai-workflow-workspace"})

def unit_digest(unit):
    return digest_json({key: value for key, value in unit.items() if key not in {"state", "accepted_output"}})

def preflight(manifest, unit_id, observation):
    root, units, _ = validate(manifest)
    require(unit_id in units, "unknown unit")
    unit = units[unit_id]
    execution = execution_contract(unit.get("execution"))
    fields(observation, OBSERVATION_KEYS, "backend observation")
    for key in ("backend", "version", "handle"):
        text(observation[key], key)
    require(observation["kind"] in {"native", "synthetic"}, "unknown observation kind")
    require(type(observation["constraints_verified"]) is bool and observation["constraints_verified"],
            "unverified backend write constraints")
    require(observation["source_snapshot"] == manifest["source_snapshot"], "stale backend baseline")
    require(type(observation["cwd"]) is str and Path(observation["cwd"]).is_absolute(), "absolute worker cwd required")
    worker = physical_path(observation["cwd"]).resolve(strict=True)
    require(worker.is_dir() and not overlap(root, worker), "shared or nested worker cwd")
    require(type(observation["writable_roots"]) is list and observation["writable_roots"] == [str(worker)],
            "backend grants broader or ambiguous writable roots")
    require(unit_id in plan(manifest)["proposed_units"], "unit not allocatable")
    for path in unit["write_set"]:
        require(not protected_write(path), "worker write targets coordinator artifact")
        canonical(worker, path)
    baseline = file_inventory(worker)
    for path, expected in execution["input_hashes"].items():
        require(path in baseline and baseline[path]["sha256"] == expected, "missing or stale actual input: " + path)
        require(any(overlap(canonical(worker, path), canonical(worker, scope)) for scope in unit["read_set"]),
                "input outside minimal read scope")
    for path in execution["minimal_context"]:
        relative(path)
        require(path in execution["input_hashes"], "minimal context lacks frozen input hash")
    return {"schema": 1, "unit_id": unit_id, "run_id": manifest["run_id"], "project": manifest["project"],
            "coordinator_id": manifest["coordinator_id"], "execution_owner": manifest["execution_owner"],
            "handle": observation["handle"], "cwd": str(worker),
            "source_snapshot": manifest["source_snapshot"], "baseline_files": baseline,
            "baseline_digest": digest_json(baseline), "unit_digest": unit_digest(unit), "observation": observation,
            "root_mode": stat.S_IMODE(worker.stat().st_mode),
            "root_identity": [worker.stat().st_dev, worker.stat().st_ino],
            "execution_authorized": False}

def verify_result(manifest, unit_id, attempt, result):
    _, units, _ = validate(manifest)
    require(unit_id in units, "unknown result unit")
    unit = units[unit_id]
    require(attempt.get("termination_verified") is True, "worker termination not observed before diff inventory")
    for key in ("run_id", "project", "coordinator_id", "execution_owner"):
        require(attempt[key] == manifest[key], "attempt origin mismatch: " + key)
    require(attempt["unit_id"] == unit_id, "attempt unit mismatch")
    execution = execution_contract(unit.get("execution"))
    require(attempt["unit_digest"] == unit_digest(unit), "unit contract changed after dispatch")
    fields(result, RESULT_KEYS, "result")
    require(type(result["schema"]) is int and result["schema"] == 1, "unsupported result schema")
    for key, expected in (("run_id", manifest["run_id"]), ("unit_id", unit_id),
                          ("attempt_id", attempt["attempt_id"]), ("handle", attempt["handle"]),
                          ("source_snapshot", manifest["source_snapshot"]),
                          ("baseline_digest", attempt["baseline_digest"])):
        require(result[key] == expected, "result provenance mismatch: " + key)
    require(attempt["source_snapshot"] == manifest["source_snapshot"], "stale attempt inputs")
    require(digest_json(attempt["baseline_files"]) == attempt["baseline_digest"], "corrupt baseline inventory")
    worker = physical_path(attempt["cwd"]).resolve(strict=True)
    require(attempt["observation"]["cwd"] == str(worker) and
            attempt["observation"]["handle"] == attempt["handle"], "attempt workspace or handle changed")
    require(attempt["root_mode"] == stat.S_IMODE(worker.stat().st_mode) and
            attempt["root_identity"] == [worker.stat().st_dev, worker.stat().st_ino],
            "worker root metadata changed outside relative write scope")
    actual = file_inventory(worker)
    changed = sorted(p for p in set(actual) | set(attempt["baseline_files"])
                     if actual.get(p) != attempt["baseline_files"].get(p))
    require(result["changed_files"] == changed, "worker actual diff differs from submission")
    for path in changed:
        require(not protected_write(path) and any(
            overlap(canonical(worker, path), canonical(worker, scope)) and
            (path == scope or path.startswith(scope + "/")) for scope in unit["write_set"]),
            "actual worker write outside approved scope")
    require(result["output_digest"] == digest_json(actual), "stale actual output digest")
    require(type(result["checks"]) is list, "missing checks")
    checks = {}
    for check in result["checks"]:
        fields(check, {"id", "result", "evidence"}, "check")
        text(check["id"], "check ID")
        require(check["id"] not in checks and check["result"] in {"pass", "fail", "skipped"}, "invalid check outcome")
        evidence = canonical(worker, check["evidence"])
        require(evidence.is_file(), "missing actual check evidence")
        checks[check["id"]] = check["result"]
    require(set(execution["required_checks"]).issubset(checks), "required check omitted")
    for key in ("findings", "skipped_checks"):
        require(type(result[key]) is list, "invalid result disclosure")
        for item in result[key]:
            text(item, key)
    text(result["residual_risk"], "residual risk")
    return {"schema": 1, "verified_submission": True, "accepted": False,
            "execution_authorized": False, "output_digest": result["output_digest"],
            "changed_files": changed, "quality_ready": all(value == "pass" for value in checks.values())
            and not result["findings"] and not result["skipped_checks"]}


# Canonical records contain hashes and bounded approved metadata, not worker logs.
LIFECYCLE_KEYS = {"schema", "initial_revision", "attempts", "events", "parent_retry_budget",
                  "retry_counts", "completed_tasks", "parent_gates", "checkpoint_epoch", "checkpoint_evidence"}
ATTEMPT_KEYS = {"id", "unit_id", "state", "origin_digest", "preflight_digest", "unit_digest",
                "source_snapshot", "handle", "result_record", "result_digest", "output_digest",
                "cancel_requested", "termination_verified", "reconciliation_digest", "review_digest"}
SANITIZED_RESULT_KEYS = {"schema", "run_id", "unit_id", "attempt_id", "source_snapshot",
                         "baseline_digest", "output_digest", "changed_files", "checks",
                         "findings_count", "skipped_count", "risk_disclosed", "quality_ready", "source_result_digest"}

def sha(value, label):
    require(type(value) is str and bool(SHA.fullmatch(value)), "invalid digest: " + label)

def origin_digest(manifest):
    return digest_json({k: manifest[k] for k in
                        ("run_id", "project", "repository_root", "execution_owner", "coordinator_id")})

def lifecycle_schema(manifest, units):
    life = manifest["lifecycle"]
    require(type(life) is dict and set(life) in (LIFECYCLE_KEYS, LIFECYCLE_KEYS | {"integrations"}),
            "invalid fields: lifecycle")
    require(type(life["schema"]) is int and life["schema"] == 1, "unsupported lifecycle schema")
    integer(life["initial_revision"], "initial revision")
    integer(life["checkpoint_epoch"], "checkpoint epoch")
    unique_ids(life["completed_tasks"], "completed parents")
    require(len(life["completed_tasks"]) == manifest["checkpoint"]["completed_since_checkpoint"],
            "completed parent count mismatch")
    require(not set(life["completed_tasks"]) & set(manifest["checkpoint"]["active_tasks"]),
            "parent both completed and active")
    require(type(life["parent_gates"]) is dict and set(life["parent_gates"]) == set(life["completed_tasks"]),
            "missing completed parent evidence")
    for task in life["completed_tasks"]:
        parent_units = [u for u in units.values() if u["task_id"] == task]
        require(bool(parent_units) and all(u["state"] == "accepted" for u in parent_units),
                "completed parent has unaccepted or missing units")
    for gate in life["parent_gates"].values():
        fields(gate, {"quality", "capture", "source_snapshot"}, "parent gate")
        relative(gate["quality"])
        relative(gate["capture"])
        sha(gate["source_snapshot"], "parent gate baseline")
    fields(life["parent_retry_budget"], {"limit", "reference", "sha256"}, "parent retry budget")
    budget = life["parent_retry_budget"]
    if budget["limit"] is None:
        require(budget["reference"] is None and budget["sha256"] is None, "unknown retry budget has evidence")
    else:
        integer(budget["limit"], "parent retry limit")
        relative(budget["reference"])
        sha(budget["sha256"], "retry evidence")
    require(type(life["retry_counts"]) is dict, "invalid retry counts")
    for key, count in life["retry_counts"].items():
        identity(key, "retry parent")
        integer(count, "parent retries")
        require(budget["limit"] is not None and count <= budget["limit"], "parent retry ceiling exceeded")
    require(type(life["attempts"]) is list and type(life["events"]) is list, "invalid history")
    ids = set()
    for attempt in life["attempts"]:
        fields(attempt, ATTEMPT_KEYS, "attempt")
        identity(attempt["id"], "attempt")
        require(attempt["id"] not in ids and attempt["unit_id"] in units, "duplicate/foreign attempt")
        ids.add(attempt["id"])
        require(attempt["state"] in {"running", "submitted", "accepted", "rejected", "cancelled"},
                "invalid attempt state")
        require(attempt["origin_digest"] == origin_digest(manifest), "attempt origin drift")
        for key in ("origin_digest", "preflight_digest", "unit_digest", "source_snapshot"):
            sha(attempt[key], key)
        identity(attempt["handle"], "handle")
        for key in ("cancel_requested", "termination_verified"):
            require(type(attempt[key]) is bool, "invalid attempt observation")
        for key in ("result_digest", "output_digest", "reconciliation_digest", "review_digest"):
            if attempt[key] is not None:
                sha(attempt[key], key)
        if attempt["result_record"] is not None:
            require(attempt["result_record"] == "results/" + attempt["id"] + ".json", "foreign result record")
            require(attempt["result_digest"] is not None, "missing result digest")
        if attempt["state"] in {"submitted", "accepted"}:
            require(attempt["termination_verified"] and attempt["result_record"] is not None,
                    "submission without terminal evidence")
        if attempt["state"] == "accepted":
            require(attempt["review_digest"] is not None and attempt["output_digest"] is not None,
                    "accepted attempt lacks review")
    latest = {}
    for a in life["attempts"]:
        latest[a["unit_id"]] = a
    for unit in units.values():
        a = latest.get(unit["id"])
        if a and a["state"] in {"running", "submitted"}:
            require(unit["id"] in manifest["reservations"], "attempt reservation lost")
        if unit["state"] in {"running", "submitted", "accepted"}:
            require(a is not None and a["state"] == unit["state"], "unit/attempt state mismatch")
        if unit["state"] == "accepted":
            require(unit["accepted_output"] == a["output_digest"], "accepted snapshot mismatch")
    require(manifest["capacity"]["active_workers"] >= len(manifest["reservations"]),
            "reserved workers omitted from capacity")
    revision = life["initial_revision"]
    for event in life["events"]:
        fields(event, {"revision", "action", "unit_id", "attempt_id", "input_digest"}, "event")
        revision += 1
        require(type(event["revision"]) is int and event["revision"] == revision, "history revision gap")
        identity(event["action"], "event action")
        require(event["unit_id"] is None or event["unit_id"] in units, "unknown event unit")
        require(event["attempt_id"] is None or event["attempt_id"] in ids, "unknown event attempt")
        sha(event["input_digest"], "event input")
    require(revision == manifest["revision"], "event/revision mismatch")
    integration_schema(manifest, units)
    if life["checkpoint_evidence"] is not None:
        fields(life["checkpoint_evidence"], {"path", "sha256"}, "checkpoint evidence")
        relative(life["checkpoint_evidence"]["path"])
        sha(life["checkpoint_evidence"]["sha256"], "checkpoint evidence")

def sanitized_result(record):
    fields(record, SANITIZED_RESULT_KEYS, "sanitized result")
    require(type(record["schema"]) is int and record["schema"] == 1, "unsupported result record")
    for key in ("run_id", "unit_id", "attempt_id"):
        identity(record[key], key)
    for key in ("source_snapshot", "baseline_digest", "output_digest", "source_result_digest"):
        sha(record[key], key)
    require(type(record["changed_files"]) is list, "invalid changed metadata")
    for path in record["changed_files"]:
        relative(path)
        require(not protected_write(path), "protected result metadata")
    require(record["changed_files"] == sorted(set(record["changed_files"])), "duplicate changed metadata")
    require(type(record["checks"]) is list, "invalid check metadata")
    names = []
    for check in record["checks"]:
        fields(check, {"id", "result", "evidence_sha256"}, "sanitized check")
        identity(check["id"], "check")
        require(check["result"] in {"pass", "fail", "skipped"}, "invalid sanitized outcome")
        sha(check["evidence_sha256"], "check evidence")
        names.append(check["id"])
    require(len(names) == len(set(names)), "duplicate sanitized check")
    for key in ("findings_count", "skipped_count"):
        integer(record[key], key)
    require(type(record["risk_disclosed"]) is bool and record["risk_disclosed"], "missing risk disclosure")
    require(type(record["quality_ready"]) is bool, "invalid quality readiness")

def owned_run(path):
    path = physical_path(path).resolve(strict=True)
    require(path.is_dir() and path.parent.name == "runs" and path.parent.parent.name == "orchestration"
            and path.parents[3].name == "projects", "noncanonical run root")
    project = path.parents[2]
    identity(project.name, "project directory")
    identity(path.name, "run directory")
    for parent in (path, path.parent, path.parent.parent, project, project.parent, project.parents[1]):
        require(not (parent / ".git").exists() and not (parent / ".git").is_symlink(),
                "foreign runtime repository")
    return path, project

def inspect_run(path, recovery=False):
    path, project = owned_run(path)
    manifest = load(path / "manifest.json")
    validate(manifest)
    require(manifest.get("lifecycle") is not None, "lifecycle metadata required for persistence")
    require(manifest["run_id"] == path.name and manifest["project"] == project.name, "runtime identity mismatch")
    records = {}
    for attempt in manifest["lifecycle"]["attempts"]:
        if attempt["result_record"] is not None:
            try:
                result_path = canonical(path, attempt["result_record"])
                value = load(result_path)
                sanitized_result(value)
                require(value["run_id"] == manifest["run_id"] and value["unit_id"] == attempt["unit_id"]
                        and value["attempt_id"] == attempt["id"], "stored result origin mismatch")
                require(digest_json(value) == attempt["result_digest"], "stored result drift")
                require(value["output_digest"] == attempt["output_digest"], "stored output mismatch")
                records[attempt["result_record"]] = value
            except (ValueError, OSError):
                if not recovery:
                    raise
                records[attempt["result_record"]] = None  # Damaged evidence is never consumed.
    # No silent exclusion of raw logs, locks, temporary files or foreign checkouts.
    permitted = {"manifest.json"} | set(records)
    for parent, dirs, files in os.walk(path, followlinks=False):
        for name in list(dirs):
            child = Path(parent) / name
            known = not child.is_symlink() and child.relative_to(path).as_posix() == "results"
            if not known and recovery:
                dirs.remove(name)
            else:
                require(known, "unknown canonical runtime directory")
        for name in files:
            child = Path(parent) / name
            local = child.relative_to(path).as_posix()
            if local == ".update.lock":
                require(not child.is_symlink() and stat.S_ISREG(child.stat().st_mode)
                        and child.stat().st_nlink == 1, "unsafe update lock")
                continue  # Explicitly observed in reconciliation, never validation evidence.
            if recovery and (local not in permitted or child.is_symlink()):
                continue
            require(local in permitted and not child.is_symlink(), "unknown canonical runtime file")
            info = child.stat()
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "unsafe canonical runtime file")
    return manifest, records

def recovery_layout(path, records):
    expected = {"manifest.json", "results"} | set(records)
    unknown = []
    for parent, dirs, files in os.walk(path, followlinks=False):
        for name in list(dirs) + files:
            child = Path(parent) / name
            local = child.relative_to(path).as_posix()
            if local not in expected or child.is_symlink():
                unknown.append(digest_json(local))
                if name in dirs:
                    dirs.remove(name)
    return sorted(unknown)

def release_slot(manifest, unit_id):
    if unit_id in manifest["reservations"]:
        manifest["reservations"].remove(unit_id)
        manifest["capacity"]["active_workers"] -= 1
    # A parent task remains active until its formal gates are reviewed.

def private_attempt(manifest, unit_id, stored, value):
    require(digest_json({k: v for k, v in value.items() if k not in
                         {"attempt_id", "termination_verified"}}) == stored["preflight_digest"],
            "private preflight drift")
    require(value.get("attempt_id") == stored["id"], "private attempt identity mismatch")
    require(value["unit_digest"] == stored["unit_digest"] and value["handle"] == stored["handle"],
            "private attempt contract mismatch")
    return value

def reconcile(manifest, observations):
    validate(manifest)
    require(manifest.get("lifecycle") is not None, "missing lifecycle")
    require(type(observations) is list, "invalid reconciliation observations")
    units = {u["id"]: u for u in manifest["units"]}
    rows, seen = [], set()
    for obs in observations:
        fields(obs, {"attempt_id", "handle", "status", "effects_known", "preflight"}, "reconciliation observation")
        identity(obs["attempt_id"], "observed attempt")
        require(obs["attempt_id"] not in seen, "duplicate reconciliation observation")
        seen.add(obs["attempt_id"])
        stored = next((a for a in manifest["lifecycle"]["attempts"] if a["id"] == obs["attempt_id"]), None)
        require(stored is not None and stored["handle"] == obs["handle"], "unknown observed handle")
        require(obs["status"] in {"running", "stopped", "unknown"} and type(obs["effects_known"]) is bool,
                "unknown observation state")
        attempt = private_attempt(manifest, stored["unit_id"], stored, obs["preflight"])
        worker = physical_path(attempt["cwd"]).resolve(strict=True)
        require(attempt["root_mode"] == stat.S_IMODE(worker.stat().st_mode) and
                attempt["root_identity"] == [worker.stat().st_dev, worker.stat().st_ino], "recovery root drift")
        actual = file_inventory(worker)
        changed = sorted(p for p in set(actual) | set(attempt["baseline_files"])
                         if actual.get(p) != attempt["baseline_files"].get(p))
        unit = units[stored["unit_id"]]
        writes_safe = all(not protected_write(p) and any(p == s or p.startswith(s + "/")
                          for s in unit["write_set"]) for p in changed)
        current = stored["source_snapshot"] == manifest["source_snapshot"] and stored["unit_digest"] == unit_digest(unit)
        output_current = stored["output_digest"] is None or stored["output_digest"] == digest_json(actual)
        rows.append({"attempt_id": stored["id"], "termination_verified": obs["status"] == "stopped",
                     "effects_known": obs["effects_known"] and writes_safe and current and output_current,
                     "invalidation_recommended": stored["state"] == "accepted" and not (current and output_current),
                     "actual_digest": digest_json(actual), "reservation_retained":
                     not (obs["status"] == "stopped" and obs["effects_known"] and writes_safe and current and output_current)})
    for stored in manifest["lifecycle"]["attempts"]:
        if stored["state"] in {"running", "submitted"} and stored["id"] not in seen:
            rows.append({"attempt_id": stored["id"], "termination_verified": False,
                         "effects_known": False, "actual_digest": None, "reservation_retained": True,
                         "invalidation_recommended": False})
    return {"schema": 1, "revision": manifest["revision"], "observations_digest": digest_json(observations),
            "rows": rows, "integration_reservations": [r["id"] for r in
                manifest["lifecycle"].get("integrations", []) if r["state"] in {"pending", "blocked"}],
            "execution_authorized": False}


def check_parent_gate(project, manifest, task, quality, capture):
    require(quality.startswith("quality/") and capture.startswith("capture-state/"),
            "parent evidence outside canonical roots")
    here = Path(__file__).resolve().parent
    def imported(name):
        spec = importlib.util.spec_from_file_location(name.replace("-", "_"), here / (name + ".py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    workflow = here.parents[2]
    qa = imported("qa-evidence")
    qa.assess(canonical(project, quality), workflow, project.parents[1], project.name,
              Path(manifest["repository_root"]), "implementation-quality", project.name + ":" + task,
              require_pass=True)
    inventory = imported("capture-state").inventory(project.parents[1], workflow,
                                                    Path(manifest["repository_root"]), project.name)
    require(not inventory["invalid"], "parent capture collection invalid")
    selected = [row for row in inventory["records"]
                if row["path"] == str(canonical(project, capture).relative_to(project.parents[1]))]
    require(len(selected) == 1, "parent capture record missing or ambiguous")
    state = selected[0]
    require(state["work_id"] == task and state["state"] == "completed" and
            state["quality_verification"] == "verified-current", "parent capture not current/completed")

def checkpoint_confirmation(project, manifest, evidence):
    lines = evidence.read_text().splitlines()
    sections, active = {}, None
    for line in lines:
        if line.startswith("## "):
            active = line[3:]
            require(active not in sections, "duplicate checkpoint section")
            sections[active] = []
        elif active is not None:
            sections[active].append(line)
    def values(name):
        result = {}
        for line in sections.get(name, []):
            if line.startswith("- ") and ": " in line:
                key, value = line[2:].split(": ", 1)
                require(key not in result, "duplicate checkpoint field")
                result[key] = value.strip("` ")
        return result
    meta, gate, bound = values("Metadata"), values("Checkpoint Gate"), values("Orchestration Checkpoint Binding")
    require(meta.get("Project") == manifest["project"] and meta.get("Result") in {"completed", "PASS"}
            and meta.get("Workflow phase") in {"phase-7-checkpoint", "7. CHECKPOINT PROJEKTU"},
            "checkpoint not completed for owning project")
    for key in ("Distillations processed atomically", "Memory updated without mechanical copy-paste",
                "Can continue project workflow"):
        require(gate.get(key) == "yes", "checkpoint gate incomplete")
    require(gate.get("Critical drift resolved or escalated") in {"yes", "none"}
            and gate.get("Blocking reason") == "none", "checkpoint blocked")
    expected = {"Run ID": manifest["run_id"], "Coordinator ID": manifest["coordinator_id"],
                "Epoch": str(manifest["lifecycle"]["checkpoint_epoch"]),
                "Source snapshot": manifest["source_snapshot"],
                "Completed tasks": json.dumps(sorted(manifest["lifecycle"]["completed_tasks"]))}
    require(bound == expected, "checkpoint run/epoch/task binding mismatch")


INTEGRATION_KEYS = {"id", "unit_id", "attempt_id", "state", "source_snapshot", "target_scope",
                    "proof_digest", "before_digest", "after_digest", "output_digest",
                    "review_path", "review_sha256", "review_digest", "root_identity"}
INTEGRATION_PROOF_KEYS = {"schema", "run_id", "coordinator_id", "integration_id", "unit_id",
                          "attempt_id", "source_snapshot", "unit_digest", "output_digest",
                          "target_scope", "root_identity", "root_mode", "before_files", "expected_files",
                          "changed_files", "execution_authorized"}

def integration_pending(manifest):
    return any(row["state"] in {"pending", "blocked"}
               for row in (manifest.get("lifecycle") or {}).get("integrations", []))

def integration_schema(manifest, units):
    rows = manifest["lifecycle"].get("integrations", [])
    require(type(rows) is list, "invalid integration history")
    seen = set()
    attempts = {a["id"]: a for a in manifest["lifecycle"]["attempts"]}
    pending = 0
    for row in rows:
        fields(row, INTEGRATION_KEYS, "integration record")
        identity(row["id"], "integration ID")
        require(row["id"] not in seen, "duplicate integration ID")
        seen.add(row["id"])
        require(row["unit_id"] in units and row["attempt_id"] in attempts and
                attempts[row["attempt_id"]]["unit_id"] == row["unit_id"], "foreign integration attempt")
        require(row["state"] in {"pending", "verified", "blocked", "abandoned", "obsolete"},
                "invalid integration state")
        relative(row["target_scope"])
        require(not protected_write(row["target_scope"]), "integration targets coordinator namespace")
        require(type(row["root_identity"]) is list and len(row["root_identity"]) == 2 and
                all(type(n) is int and n >= 0 for n in row["root_identity"]), "invalid integration root identity")
        for key in ("source_snapshot", "proof_digest", "before_digest", "output_digest"):
            sha(row[key], key)
        for key in ("after_digest", "review_sha256", "review_digest"):
            if row[key] is not None:
                sha(row[key], key)
        if row["review_path"] is not None:
            relative(row["review_path"])
        if row["state"] in {"verified", "abandoned"}:
            require(all(row[k] is not None for k in ("after_digest", "review_path", "review_sha256", "review_digest")),
                    "finished integration lacks review")
        if row["state"] == "verified":
            unit, attempt = units[row["unit_id"]], attempts[row["attempt_id"]]
            require(unit["state"] == "accepted" and attempt["state"] == "accepted" and
                    unit["accepted_output"] == row["output_digest"] and
                    row["source_snapshot"] == manifest["source_snapshot"] and
                    attempt["unit_digest"] == unit_digest(unit), "verified integration is stale")
        pending += row["state"] in {"pending", "blocked"}
    require(pending <= 1, "competing integration reservations")

def accepted_snapshot(manifest, unit_id, preflight_value, result, records):
    _, units, _ = validate(manifest)
    require(unit_id in units and units[unit_id]["state"] == "accepted", "unit is not accepted")
    require(manifest.get("lifecycle") is not None, "accepted snapshot needs persistent provenance")
    attempt = next((a for a in reversed(manifest["lifecycle"]["attempts"]) if a["unit_id"] == unit_id), None)
    require(attempt is not None and attempt["state"] == "accepted", "latest attempt not accepted")
    private = private_attempt(manifest, unit_id, attempt, preflight_value)
    record = records.get(attempt["result_record"])
    require(record is not None, "accepted result missing or damaged")
    sanitized_result(record)
    require(digest_json(record) == attempt["result_digest"] and
            digest_json(result) == record["source_result_digest"], "accepted result binding mismatch")
    checked = verify_result(manifest, unit_id, private, result)
    require(checked["quality_ready"] and checked["output_digest"] == units[unit_id]["accepted_output"],
            "accepted output no longer current")
    return attempt, private, file_inventory(Path(private["cwd"]))

def verify_dependency_delivery(manifest, consumer_id, dependency_id, producer_preflight, result,
                               records, observation, paths):
    _, units, _ = validate(manifest)
    require(consumer_id in units and dependency_id in units, "unknown dependency delivery unit")
    consumer, producer = units[consumer_id], units[dependency_id]
    require(dependency_id in consumer["dependencies"] and
            consumer["task_id"] == producer["task_id"], "cross-task dependency needs external formal gates")
    require(consumer["expected_inputs"].get(dependency_id) == producer["accepted_output"],
            "stale dependency binding")
    attempt, private, source = accepted_snapshot(manifest, dependency_id, producer_preflight, result, records)
    delivered = preflight(manifest, consumer_id, observation)
    require(not overlap(Path(private["cwd"]), Path(delivered["cwd"])), "mutable/shared producer delivery")
    require(type(paths) is list and bool(paths) and all(type(p) is str for p in paths) and
            len(paths) == len(set(paths)), "empty/duplicate delivery paths")
    def within(path, scopes):
        return any(path == scope or path.startswith(scope + "/") for scope in scopes)
    hashes = consumer["execution"]["input_hashes"]
    required = {path for path, entry in source.items() if entry["sha256"] is not None and
                (path in hashes or (within(path, producer["write_set"]) and within(path, consumer["read_set"])))}
    require(set(paths) == required, "dependency delivery coverage incomplete")
    for path in delivered["baseline_files"]:
        if within(path, producer["write_set"]) and within(path, consumer["read_set"]):
            require(path in source, "unaccepted extra dependency path: " + path)
    for path, entry in source.items():
        if entry["sha256"] is None and within(path, producer["write_set"]) and any(
                overlap(canonical(Path(delivered["cwd"]), path), canonical(Path(delivered["cwd"]), scope))
                for scope in consumer["read_set"]):
            require(delivered["baseline_files"].get(path) == entry, "dependency directory metadata differs")
    for path in set(private["baseline_files"]) - set(source):
        if within(path, producer["write_set"]) and within(path, consumer["read_set"]):
            require(path not in delivered["baseline_files"], "deleted dependency path resurrected")
    values = {}
    for path in paths:
        relative(path)
        require(path in source and source[path]["sha256"] is not None and
                delivered["baseline_files"].get(path) == source[path] and
                consumer["execution"]["input_hashes"].get(path) == source[path]["sha256"],
                "delivery differs from accepted immutable input")
        values[path] = copy.deepcopy(source[path])
    return {"schema": 1, "producer_attempt": attempt["id"], "producer_output": producer["accepted_output"],
            "consumer_unit": consumer_id, "consumer_contract": delivered["unit_digest"],
            "delivered_preflight": delivered, "files": values, "execution_authorized": False}

def integration_inventory(manifest, project, target_scope):
    root = physical_path(manifest["repository_root"]).resolve(strict=True)
    target = canonical(root, target_scope)
    require(target != root and target.is_dir() and not protected_write(target_scope) and
            not overlap(target, project), "unsafe integration inventory boundary")
    inventory = {target_scope: {"sha256": None, "mode": stat.S_IMODE(target.stat().st_mode)}}
    inventory.update({target_scope + "/" + p: v for p, v in file_inventory(target).items()})
    return target, inventory

def prepare_integration(manifest, project, integration_id, unit_id, attempt_id, preflight_value, result, records, target_scope):
    require(not integration_pending(manifest) and not manifest["reservations"], "integration or worker reservation active")
    check_current_integrations(project, manifest)
    identity(integration_id, "integration ID")
    attempt, private, output = accepted_snapshot(manifest, unit_id, preflight_value, result, records)
    require(attempt["id"] == attempt_id, "integration attempt mismatch")
    target, before = integration_inventory(manifest, project, target_scope)
    unit = next(u for u in manifest["units"] if u["id"] == unit_id)
    require(all(p == target_scope or p.startswith(target_scope + "/") for p in unit["write_set"]),
            "target boundary does not contain whole write set")
    expected = copy.deepcopy(before)
    for path in result["changed_files"]:
        require(path == target_scope or path.startswith(target_scope + "/"), "delta outside integration boundary")
        require(before.get(path) == private["baseline_files"].get(path), "destination conflict: " + path)
        if path in output:
            expected[path] = copy.deepcopy(output[path])
        else:
            expected.pop(path, None)
    return {"schema": 1, "run_id": manifest["run_id"], "coordinator_id": manifest["coordinator_id"],
            "integration_id": integration_id, "unit_id": unit_id, "attempt_id": attempt_id,
            "source_snapshot": manifest["source_snapshot"], "unit_digest": unit_digest(unit),
            "output_digest": result["output_digest"], "target_scope": target_scope,
            "root_identity": [target.stat().st_dev, target.stat().st_ino],
            "root_mode": stat.S_IMODE(target.stat().st_mode), "before_files": before,
            "expected_files": expected, "changed_files": result["changed_files"], "execution_authorized": False}

def integration_proof(manifest, project, row, proof):
    fields(proof, INTEGRATION_PROOF_KEYS, "integration proof")
    require(digest_json(proof) == row["proof_digest"] and proof["execution_authorized"] is False,
            "integration proof changed")
    for key, expected in (("run_id", manifest["run_id"]), ("coordinator_id", manifest["coordinator_id"]),
                          ("integration_id", row["id"]), ("unit_id", row["unit_id"]),
                          ("attempt_id", row["attempt_id"]), ("source_snapshot", manifest["source_snapshot"])):
        require(proof[key] == expected, "integration proof origin/source mismatch")
    target, actual = integration_inventory(manifest, project, proof["target_scope"])
    require([target.stat().st_dev, target.stat().st_ino] == proof["root_identity"], "integration root identity changed")
    return actual

def integration_review(project, review, decision, actual_digest):
    fields(review, {"reviewer", "decision", "diff_checked", "scope_checked", "conflicts_checked",
                    "findings_reviewed", "effects_known", "after_digest", "evidence"}, "integration review")
    identity(review["reviewer"], "integration reviewer")
    require(review["decision"] == decision and review["after_digest"] == actual_digest,
            "integration review decision/baseline mismatch")
    for key in ("diff_checked", "scope_checked", "conflicts_checked", "findings_reviewed", "effects_known"):
        require(type(review[key]) is bool and review[key], "incomplete integration review: " + key)
    evidence = canonical(project, review["evidence"])
    require(evidence.is_file(), "missing integration review evidence")
    return {"review_path": review["evidence"], "review_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
            "review_digest": digest_json(review)}

def invalidate_units(manifest, unit_id):
    _, units, ordered = validate(manifest)
    affected = {unit_id}
    for other_id in ordered:
        if affected & set(units[other_id]["dependencies"]):
            affected.add(other_id)
    life = manifest["lifecycle"]
    for affected_id in affected:
        units[affected_id]["state"], units[affected_id]["accepted_output"] = "blocked", None
        task = units[affected_id]["task_id"]
        if task in life["completed_tasks"]:
            life["completed_tasks"].remove(task)
            life["parent_gates"].pop(task)
            manifest["checkpoint"]["active_tasks"].append(task)
    for row in life.get("integrations", []):
        if row["unit_id"] in affected and row["state"] not in {"abandoned", "obsolete"}:
            row["state"] = "blocked" if row["state"] in {"pending", "blocked"} else "obsolete"
    manifest["checkpoint"]["completed_since_checkpoint"] = len(life["completed_tasks"])

def check_integrated_parent(project, manifest, task):
    require(not integration_pending(manifest), "unresolved integration prevents parent completion")
    rows = manifest["lifecycle"].get("integrations", [])
    for unit in manifest["units"]:
        if unit["task_id"] == task and unit["write_set"]:
            require(any(r["unit_id"] == unit["id"] and r["state"] == "verified" and
                        r["output_digest"] == unit["accepted_output"] for r in rows), "write unit not integrated")
    check_current_integrations(project, manifest)

def check_current_integrations(project, manifest):
    latest = {}
    for row in manifest["lifecycle"].get("integrations", []):
        if row["state"] == "verified":
            evidence = canonical(project, row["review_path"])
            require(hashlib.sha256(evidence.read_bytes()).hexdigest() == row["review_sha256"], "integration review stale")
            latest[row["target_scope"]] = row
    for scope, row in latest.items():
        target, actual = integration_inventory(manifest, project, scope)
        require([target.stat().st_dev, target.stat().st_ino] == row["root_identity"], "integrated destination identity drift")
        require(digest_json(actual) == row["after_digest"], "integrated destination drift")


def apply_transition(manifest, request, project, records):
    value = copy.deepcopy(manifest)
    _, units, _ = validate(value)
    life = value["lifecycle"]
    require(type(request) is dict and "action" in request, "invalid transition")
    action = request["action"]
    if action in {"ready", "start", "retry", "parent-complete", "checkpoint", "integration-prepare"}:
        require(not integration_pending(value), "unresolved integration reservation")
    unit_id = request.get("unit_id")
    unit = units.get(unit_id)
    attempt_id = request.get("attempt_id")
    stored = next((a for a in life["attempts"] if a["id"] == attempt_id), None)
    new_record = None
    private = None
    if action == "ready":
        fields(request, {"action", "unit_id"}, "ready request")
        require(unit is not None and unit["state"] == "planned", "unit not planned")
        require(unit_id in plan(value)["proposed_units"], "unit not ready under current dependencies")
        unit["state"] = "ready"
    elif action == "start":
        require(unit is not None and unit["state"] == "ready", "unit not ready")
        keys = {"action", "unit_id", "attempt_id", "observation"}
        if unit["dependencies"]:
            keys.add("dependency_deliveries")
        fields(request, keys, "start request")
        identity(attempt_id, "new attempt")
        require(stored is None, "attempt ID reused")
        prepared = preflight(value, unit_id, request["observation"])
        if unit["dependencies"]:
            deliveries = request["dependency_deliveries"]
            fields(deliveries, set(unit["dependencies"]), "dependency deliveries")
            for dependency_id, delivery in deliveries.items():
                fields(delivery, {"preflight", "result", "paths"}, "dependency delivery")
                checked = verify_dependency_delivery(value, unit_id, dependency_id,
                    delivery["preflight"], delivery["result"], records,
                    request["observation"], delivery["paths"])
                require(checked["delivered_preflight"] == prepared, "dependency delivery baseline changed")
        private = {**prepared, "attempt_id": attempt_id, "termination_verified": False}
        identity(prepared["handle"], "durable handle")
        stored = {"id": attempt_id, "unit_id": unit_id, "state": "running",
                  "origin_digest": origin_digest(value), "preflight_digest": digest_json(prepared),
                  "unit_digest": prepared["unit_digest"], "source_snapshot": value["source_snapshot"],
                  "handle": prepared["handle"], "result_record": None, "result_digest": None,
                  "output_digest": None, "cancel_requested": False, "termination_verified": False,
                  "reconciliation_digest": None, "review_digest": None}
        life["attempts"].append(stored)
        unit["state"] = "running"
        value["reservations"].append(unit_id)
        value["capacity"]["active_workers"] += 1
        parents = value["checkpoint"]["active_tasks"]
        if unit["task_id"] not in parents:
            parents.append(unit["task_id"])
    elif action == "submit":
        fields(request, {"action", "unit_id", "attempt_id", "preflight", "result"}, "submit request")
        require(unit is not None and stored is not None and stored["unit_id"] == unit_id and
                stored["state"] == "running" and unit["state"] == "running", "attempt not running")
        attempt = private_attempt(value, unit_id, stored, request["preflight"])
        checked = verify_result(value, unit_id, attempt, request["result"])
        worker = Path(attempt["cwd"])
        result = request["result"]
        record = {k: result[k] for k in ("schema", "run_id", "unit_id", "attempt_id", "source_snapshot",
                                         "baseline_digest", "output_digest", "changed_files")}
        record.update(checks=[{"id": c["id"], "result": c["result"],
                              "evidence_sha256": hashlib.sha256(canonical(worker, c["evidence"]).read_bytes()).hexdigest()}
                             for c in result["checks"]],
                      findings_count=len(result["findings"]), skipped_count=len(result["skipped_checks"]),
                      risk_disclosed=bool(result["residual_risk"]), quality_ready=checked["quality_ready"],
                      source_result_digest=digest_json(result))
        sanitized_result(record)
        name = "results/" + attempt_id + ".json"
        require(name not in records, "immutable result already exists")
        new_record = (name, record)
        stored.update(state="submitted", result_record=name, result_digest=digest_json(record),
                      output_digest=checked["output_digest"], termination_verified=True)
        unit["state"] = "submitted"
    elif action == "review":
        fields(request, {"action", "unit_id", "attempt_id", "preflight", "result", "review"}, "review request")
        require(unit is not None and stored is not None and stored["unit_id"] == unit_id and
                unit["state"] == "submitted" and stored["state"] == "submitted", "attempt not submitted")
        attempt = private_attempt(value, unit_id, stored, request["preflight"])
        checked = verify_result(value, unit_id, attempt, request["result"])
        require(digest_json(request["result"]) == records[stored["result_record"]]["source_result_digest"],
                "submission disclosures changed after sealing")
        require(checked["output_digest"] == stored["output_digest"], "submitted output changed")
        review = request["review"]
        fields(review, {"reviewer", "decision", "dod_checked", "scope_checked", "findings_reviewed",
                        "source_snapshot", "output_digest", "evidence"}, "review")
        identity(review["reviewer"], "reviewer")
        relative(review["evidence"])
        require(canonical(project, review["evidence"]).is_file(), "missing review evidence")
        require(review["decision"] in {"accept", "reject"}, "unknown review decision")
        require(review["source_snapshot"] == value["source_snapshot"] and
                review["output_digest"] == stored["output_digest"], "stale review")
        for key in ("dod_checked", "scope_checked", "findings_reviewed"):
            require(type(review[key]) is bool and review[key], "incomplete semantic review: " + key)
        if review["decision"] == "accept":
            require(checked["quality_ready"], "submission not quality-ready")
            stored["state"], unit["state"] = "accepted", "accepted"
            unit["accepted_output"] = stored["output_digest"]
        else:
            stored["state"], unit["state"] = "rejected", "rejected"
        stored["review_digest"] = digest_json({"review": review, "evidence": hashlib.sha256(
            canonical(project, review["evidence"]).read_bytes()).hexdigest()})
        release_slot(value, unit_id)
    elif action == "cancel-request":
        fields(request, {"action", "unit_id", "attempt_id"}, "cancel request")
        require(stored is not None and stored["unit_id"] == unit_id and stored["state"] == "running",
                "cancel requires active attempt")
        require(not stored["cancel_requested"], "cancellation already requested")
        stored["cancel_requested"] = True
    elif action == "cancel":
        fields(request, {"action", "unit_id", "attempt_id", "observations"}, "cancel confirmation")
        require(stored is not None and stored["unit_id"] == unit_id and stored["state"] == "running",
                "attempt not cancellable")
        reconciled = reconcile(value, request["observations"])
        row = next((row for row in reconciled["rows"] if row["attempt_id"] == attempt_id), None)
        require(row is not None and row["termination_verified"] and row["effects_known"],
                "unknown termination or effects")
        stored.update(state="cancelled", termination_verified=True, reconciliation_digest=digest_json(reconciled))
        unit["state"] = "cancelled"
        release_slot(value, unit_id)
    elif action == "retry":
        fields(request, {"action", "unit_id", "observations"}, "retry request")
        require(unit is not None and unit["state"] in {"cancelled", "rejected"}, "retry lacks terminal predecessor")
        terminal = [a for a in life["attempts"] if a["unit_id"] == unit_id][-1]
        reconciled = reconcile(value, request["observations"])
        row = next((row for row in reconciled["rows"] if row["attempt_id"] == terminal["id"]), None)
        require(row is not None and terminal["termination_verified"] and row["termination_verified"] and row["effects_known"],
                "retry requires freshly reconciled effects")
        budget = life["parent_retry_budget"]
        require(budget["limit"] is not None, "unknown parent retry budget")
        proof = load(canonical(project, budget["reference"]))
        fields(proof, {"schema", "project", "coordinator_id", "retry_limit"}, "parent retry evidence")
        require(proof == {"schema": 1, "project": value["project"], "coordinator_id": value["coordinator_id"],
                          "retry_limit": budget["limit"]} and
                hashlib.sha256(canonical(project, budget["reference"]).read_bytes()).hexdigest() == budget["sha256"],
                "parent retry budget drift")
        used = life["retry_counts"].get(unit["task_id"], 0)
        require(used < budget["limit"], "parent retry ceiling reached")
        life["retry_counts"][unit["task_id"]] = used + 1
        unit["state"] = "ready"
    elif action == "invalidate":
        fields(request, {"action", "unit_id", "reason_digest"}, "invalidation")
        require(unit is not None and unit["state"] == "accepted", "invalidation requires accepted unit")
        sha(request["reason_digest"], "invalidation reason")
        invalidate_units(value, unit_id)
        # Finished attempts are untouched; their prior acceptance remains history.
    elif action == "integration-prepare":
        fields(request, {"action", "integration_id", "unit_id", "attempt_id", "preflight", "result", "target_scope"},
               "integration preparation")
        rows = life.setdefault("integrations", [])
        require(not any(r["id"] == request["integration_id"] or
                        (r["attempt_id"] == attempt_id and r["state"] == "verified") for r in rows),
                "integration ID or accepted attempt replay")
        require(all(r["target_scope"] == request["target_scope"] or not overlap(
            canonical(Path(value["repository_root"]), r["target_scope"]),
            canonical(Path(value["repository_root"]), request["target_scope"])) for r in rows),
                "overlapping distinct integration boundaries")
        private = prepare_integration(value, project, request["integration_id"], unit_id, attempt_id,
                                      request["preflight"], request["result"], records, request["target_scope"])
        rows.append({"id": request["integration_id"], "unit_id": unit_id, "attempt_id": attempt_id,
                     "state": "pending", "source_snapshot": value["source_snapshot"],
                     "target_scope": request["target_scope"], "proof_digest": digest_json(private),
                     "root_identity": private["root_identity"],
                     "before_digest": digest_json(private["before_files"]), "after_digest": None,
                     "output_digest": private["output_digest"], "review_path": None,
                     "review_sha256": None, "review_digest": None})
    elif action in {"integration-confirm", "integration-abandon"}:
        needed = {"action", "integration_id", "proof", "review"}
        if action == "integration-confirm":
            needed |= {"preflight", "result"}
        fields(request, needed, "integration conclusion")
        row = next((r for r in life.get("integrations", []) if r["id"] == request["integration_id"]), None)
        require(row is not None and row["state"] in {"pending", "blocked"}, "no pending integration")
        proof = request["proof"]
        actual = integration_proof(value, project, row, proof)
        if action == "integration-confirm":
            _, _, output = accepted_snapshot(value, row["unit_id"], request["preflight"], request["result"], records)
            require(digest_json(output) == proof["output_digest"] and actual == proof["expected_files"],
                    "actual integration differs from intended output")
            state, decision = "verified", "accept"
        else:
            for path in set(actual) | set(proof["before_files"]):
                before, after, observed = proof["before_files"].get(path), proof["expected_files"].get(path), actual.get(path)
                require(observed == before or (path in proof["changed_files"] and observed == after),
                        "unknown integration effects retain reservation")
            state, decision = "abandoned", "abandon"
        review = integration_review(project, request["review"], decision, digest_json(actual))
        row.update(state=state, after_digest=digest_json(actual), **review)
        if state == "abandoned":
            invalidate_units(value, row["unit_id"])
    elif action == "parent-complete":
        fields(request, {"action", "task_id", "quality", "capture"}, "parent completion")
        task = request["task_id"]
        identity(task, "parent task")
        parent_units = [u for u in units.values() if u["task_id"] == task]
        require(task in value["checkpoint"]["active_tasks"] and bool(parent_units) and
                all(u["state"] == "accepted" for u in parent_units),
                "parent units not accepted")
        check_integrated_parent(project, value, task)
        check_parent_gate(project, value, task, request["quality"], request["capture"])
        value["checkpoint"]["active_tasks"].remove(task)
        life["completed_tasks"].append(task)
        value["checkpoint"]["completed_since_checkpoint"] = len(life["completed_tasks"])
        life["parent_gates"][task] = {"quality": request["quality"], "capture": request["capture"],
                                    "source_snapshot": value["source_snapshot"]}
    elif action == "checkpoint":
        fields(request, {"action", "evidence", "sha256"}, "checkpoint completion")
        require(not value["reservations"] and not value["checkpoint"]["active_tasks"] and
                bool(life["completed_tasks"]), "active or unknown parent work prevents checkpoint reset")
        require(request["evidence"].startswith("checkpoints/"), "checkpoint outside owning evidence")
        evidence = canonical(project, request["evidence"])
        sha(request["sha256"], "checkpoint digest")
        require(evidence.is_file() and hashlib.sha256(evidence.read_bytes()).hexdigest() == request["sha256"],
                "checkpoint evidence drift")
        checkpoint_confirmation(project, value, evidence)
        previous = life["checkpoint_evidence"]
        require(previous is None or previous["sha256"] != request["sha256"], "checkpoint evidence replay")
        for task, gate in life["parent_gates"].items():
            require(gate["source_snapshot"] == value["source_snapshot"], "completed parent baseline stale")
            check_integrated_parent(project, value, task)
            check_parent_gate(project, value, task, gate["quality"], gate["capture"])
        life["checkpoint_evidence"] = {"path": request["evidence"], "sha256": request["sha256"]}
        life["checkpoint_epoch"] += 1
        life["completed_tasks"], life["parent_gates"] = [], {}
        value["checkpoint"]["completed_since_checkpoint"] = 0
    else:
        raise InvalidManifest("unsupported lifecycle action")
    value["revision"] += 1
    life["events"].append({"revision": value["revision"], "action": action, "unit_id": unit_id,
                           "attempt_id": attempt_id, "input_digest": digest_json(request)})
    validate(value)
    return value, new_record, private

def update_run(path, coordinator, expected_revision, request):
    path, project = owned_run(path)
    identity(coordinator, "coordinator")
    integer(expected_revision, "expected revision")
    lock = path / ".update.lock"
    fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    lock_info = os.fstat(fd)
    temporary = None
    replaced = False
    try:
        os.write(fd, json.dumps({"coordinator": coordinator, "pid": os.getpid()}).encode())
        os.fsync(fd)
        recovery = request.get("action") == "invalidate" if type(request) is dict else False
        manifest, records = inspect_run(path, recovery=recovery)
        if recovery:
            unknown = recovery_layout(path, records)
            require(set(unknown) <= {digest_json(".update.lock")}, "unknown files block recovery mutation")
        require(manifest["coordinator_id"] == coordinator, "coordinator does not own run")
        require(manifest["revision"] == expected_revision, "revision mismatch")
        value, new_record, private = apply_transition(manifest, request, project, records)
        if new_record:
            name, record = new_record
            directory = path / "results"
            if not directory.exists():
                directory.mkdir(mode=0o700)
            canonical(path, name)
            with open(path / name, "x", encoding="utf-8") as stream:
                json.dump(record, stream, sort_keys=True, allow_nan=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            result_fd = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(result_fd)
            finally:
                os.close(result_fd)
        with tempfile.NamedTemporaryFile(dir=path, prefix=".manifest-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write((json.dumps(value, sort_keys=True, allow_nan=False) + "\n").encode())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path / "manifest.json")
        replaced = True
        directory_fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        response = {"schema": 1, "revision": value["revision"], "committed": True,
                    "dispatch_performed": False, "execution_authorized": False}
        if private is not None:
            response["private_integration" if request["action"] == "integration-prepare" else "private_preflight"] = private
        return response
    except OSError as error:
        if replaced:
            raise InvalidManifest("manifest replaced; durability/ack uncertain, reconcile without replay") from error
        raise
    finally:
        os.close(fd)
        if temporary is not None and temporary.exists():
            temporary.unlink()
        if lock.exists() and not lock.is_symlink():
            info = lock.lstat()
            if (info.st_dev, info.st_ino) == (lock_info.st_dev, lock_info.st_ino):
                lock.unlink()

def lifecycle_main():
    parser = argparse.ArgumentParser(description="Coordinator-owned atomic lifecycle; no worker execution")
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--coordinator-id", required=True)
    parser.add_argument("--expected-revision", type=int)
    parser.add_argument("--request", type=Path)
    parser.add_argument("command", choices=("validate", "transition", "reconcile"))
    args = parser.parse_args()
    try:
        if args.command == "transition":
            require(args.expected_revision is not None and args.request is not None, "transition requires revision/request")
            output = update_run(args.run_root, args.coordinator_id, args.expected_revision, load(args.request))
        else:
            manifest, records = inspect_run(args.run_root, recovery=args.command == "reconcile")
            require(manifest["coordinator_id"] == args.coordinator_id, "coordinator does not own run")
            if args.command == "reconcile":
                output = reconcile(manifest, load(args.request) if args.request else [])
                output["update_lock_present"] = (args.run_root / ".update.lock").exists()
                output["unknown_entry_fingerprints"] = recovery_layout(args.run_root, records)
                output["damaged_result_attempts"] = [a["id"] for a in manifest["lifecycle"]["attempts"]
                                                     if a["result_record"] in records and records[a["result_record"]] is None]
                output["runtime_layout_complete"] = not output["unknown_entry_fingerprints"] and not output["damaged_result_attempts"]
                for attempt_id in output["damaged_result_attempts"]:
                    if not any(row["attempt_id"] == attempt_id for row in output["rows"]):
                        output["rows"].append({"attempt_id": attempt_id, "termination_verified": False,
                                               "effects_known": False, "actual_digest": None,
                                               "reservation_retained": True, "invalidation_recommended": True})
                if output["update_lock_present"] or not output["runtime_layout_complete"]:
                    for row in output["rows"]:
                        row["effects_known"] = False
                        row["reservation_retained"] = True
            else:
                require(not (args.run_root / ".update.lock").exists(), "run has an update lock")
                output = {"schema": 1, "valid": True, "revision": manifest["revision"],
                          "execution_authorized": False}
        print(json.dumps(output, sort_keys=True, allow_nan=False))
        return 0
    except (InvalidManifest, OSError, TypeError, KeyError, UnicodeError, json.JSONDecodeError) as error:
        print("Parallel lifecycle error: " + str(error), file=sys.stderr)
        return 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--format", choices=("json", "human"), default="json")
    args = parser.parse_args()
    try:
        result = plan(load(args.manifest))
        if args.format == "json":
            print(json.dumps(result, sort_keys=True, allow_nan=False))
        else:
            print(result["status"] + ": " + result["mode"] + " (" + str(result["selected_count"]) + ")")
            print(result["reason"])
            print("Execution authorized: false; " + ", ".join(result["proposed_units"]))
            for rejected in result["rejected_candidates"]:
                print(rejected["unit_id"] + ": " + "; ".join(rejected["reasons"]))
        return 0
    except (InvalidManifest, OSError, TypeError, KeyError, UnicodeError, json.JSONDecodeError) as error:
        print("Parallel planning error: " + str(error), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
