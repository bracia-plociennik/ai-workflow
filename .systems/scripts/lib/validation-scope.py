#!/usr/bin/env python3
"""Read-only scope snapshots and explicit dependency planning. No check inference."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
CHECK = re.compile(r"check-[a-z0-9-]+")
PROJECT_DIRS = {
    "architecture", "planning", "specs", "quality", "capture-state", "distillations",
    "checkpoints", "decisions", "escalations", "reviews", "implementation", "autopilot",
    "tasks", "memory", "micro-tasks", "change-requests", "prompting",
}
SENSITIVE = {".env", "secrets", "credentials", "private-key", "raw", "dump"}
RUNTIME_CHECKS = {"check-naming", "check-status-consistency", "check-qa-evidence", "check-distillation-state"}

def strict_json(text):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate JSON field")
            out[key] = value
        return out
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON value")))

def fields(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError("invalid " + label + " fields")

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)

def relative(raw):
    if not isinstance(raw, str) or not raw or "\\" in raw or "\0" in raw:
        raise ValueError("unsafe relative path")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in raw.split("/")):
        raise ValueError("unsafe relative path")
    if any(part.lower() in SENSITIVE or part.lower().startswith(".env") for part in path.parts):
        raise ValueError("sensitive input path is not authorized")
    return raw

def contained(root, raw, exists=True):
    relative(raw)
    path = root / raw
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("escaping scope path")
    # Reject links even when they happen to point inside this root.
    current = root
    for part in PurePosixPath(raw).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("symlink scope input")
    if exists and not path.is_file():
        raise ValueError("missing scope input")
    return path

def digest(path):
    if not path.stat().st_mode & 0o444:
        raise ValueError("unreadable scope input")
    return hashlib.sha256(path.read_bytes()).hexdigest()

def owned_root(workspace, raw):
    if not (raw == "repo/core" or re.fullmatch(r"projects/[a-z0-9]+(?:-[a-z0-9]+)*", raw)):
        raise ValueError("unknown owned runtime root")
    path = contained(workspace, raw, False)
    if not path.is_dir():
        raise ValueError("missing runtime root")
    if not path.stat().st_mode & 0o444 or not path.stat().st_mode & 0o111:
        raise ValueError("unreadable runtime root")
    if (path / ".git").exists() or (path / ".git").is_symlink():
        raise ValueError("foreign repository in owned runtime root")
    return path

def runtime_files(workspace, raw):
    root = owned_root(workspace, raw)
    legacy = workspace / "repo/core/legacy-qa-evidence-v1.md"
    if legacy.exists() or legacy.is_symlink():
        digest(contained(workspace, "repo/core/legacy-qa-evidence-v1.md"))
    files = []
    for item in sorted(root.iterdir()):
        if item.is_symlink():
            raise ValueError("symlink runtime input")
        if item.is_file() and (item.suffix == ".md" or item.name == "quality-assessments.json"):
            relative(str(item.relative_to(workspace)))
            files.append(item)
        elif item.is_dir() and raw.startswith("projects/") and item.name in PROJECT_DIRS:
            def unreadable(_):
                raise ValueError("unreadable runtime directory")
            for directory, dirs, names in os.walk(item, followlinks=False, onerror=unreadable):
                parent = Path(directory)
                if not parent.stat().st_mode & 0o444 or not parent.stat().st_mode & 0o111:
                    raise ValueError("unreadable runtime directory")
                if (parent / ".git").exists():
                    raise ValueError("foreign repository in owned runtime artifacts")
                for name in dirs:
                    if (parent / name).is_symlink():
                        raise ValueError("symlink runtime directory")
                for name in sorted(names):
                    file = parent / name
                    if file.is_symlink():
                        raise ValueError("symlink runtime input")
                    if file.is_file():
                        relative(str(file.relative_to(workspace)))
                        files.append(file)
    # Raw context/eval/legacy/dump trees are supporting data, not active producers.
    return sorted(files)

def inventory_runtime(workspace, roots):
    if not isinstance(roots, list) or any(not isinstance(root, str) for root in roots) or len(roots) != len(set(roots)):
        raise ValueError("duplicate or invalid runtime roots")
    return [{"root": raw, "files": [{"path": str(p.relative_to(workspace)), "sha256": digest(p)}
             for p in runtime_files(workspace, raw)]} for raw in sorted(roots)]

def git_changes(repo, base):
    rows = []
    for area, args in [
        ("committed", ["diff", "--name-status", "-z", "--find-renames", base, "HEAD"]),
        ("staged", ["diff", "--cached", "--name-status", "-z", "--find-renames"]),
        ("unstaged", ["diff", "--name-status", "-z", "--find-renames"]),
    ]:
        tokens = git(repo, *args).decode("utf-8", "surrogateescape").split("\0")
        index = 0
        while index < len(tokens) and tokens[index]:
            status = tokens[index]
            index += 1
            old = None
            if status[0] in "RC":
                old = tokens[index]
                index += 1
            path = tokens[index]
            index += 1
            rows.append({"area": area, "status": status, "path": path, "old_path": old})
    for path in git(repo, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8", "surrogateescape").split("\0"):
        if path:
            rows.append({"area": "untracked", "status": "?", "path": path, "old_path": None})
    return sorted(rows, key=lambda row: (row["area"], row["path"], row["old_path"] or "", row["status"]))

def covered(path, scopes):
    return any(path == scope or path.startswith(scope + "/") for scope in scopes)

def framework_snapshot(workflow):
    workflow = workflow.resolve(strict=True)
    if Path(os.fsdecode(git(workflow, "rev-parse", "--show-toplevel").strip())).resolve() != workflow:
        raise ValueError("workflow identity is not its canonical Git root")
    head = git(workflow, "rev-parse", "HEAD").decode().strip()
    names = set(os.fsdecode(git(workflow, "ls-files", "-z")).split("\0"))
    names.update(os.fsdecode(git(workflow, "ls-files", "--others", "--exclude-standard", "-z")).split("\0"))
    relevant = lambda raw: raw.startswith((".systems/", ".github/")) or raw in {"AGENTS.md", "HUMANS.md", "README.md"}
    entries = []
    for raw in sorted(name for name in names if name and relevant(name)):
        path = contained(workflow, raw, False)
        supporting = raw.startswith(".systems/ai/skills/legacy/") or "/context/" in raw
        entries.append((raw, "supporting-data" if supporting else digest(path) if path.is_file() else None))
    for required in (".systems/scripts/validate-workflow", ".systems/scripts/lib/validation-scope.py", ".systems/scripts/lib/validation-checks.json",
                     ".systems/scripts/resolve-workflow-env", ".systems/scripts/run-with-timeout",
                     ".systems/scripts/lib/policy-boundaries.sh", ".systems/scripts/lib/qa-evidence.py",
                     ".systems/scripts/lib/validation-timing.py"):
        contained(workflow, required)
    changes = git_changes(workflow, head)
    dirty = any(relevant(row["path"]) or (row["old_path"] and relevant(row["old_path"])) for row in changes)
    return {"repository": str(workflow), "head": head, "dirty": dirty,
            "sha256": hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()}

def snapshot(repo, workspace, base, scopes, roots, intent, workflow):
    repo = repo.resolve(strict=True)
    if Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel").strip())).resolve() != repo:
        raise ValueError("repository identity is not its canonical Git root")
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    base_id = git(repo, "rev-parse", "--verify", base + "^{commit}").decode().strip()
    if not isinstance(scopes, list) or not scopes or any(not isinstance(scope, str) for scope in scopes) or len(scopes) != len(set(scopes)):
        raise ValueError("empty or duplicate implementation scope")
    for scope in scopes:
        relative(scope)
    changes = git_changes(repo, base_id)
    for row in changes:
        for path in (row["path"], row["old_path"]):
            if path and not covered(path, scopes):
                raise ValueError("Git change outside declared implementation scope")
    paths = sorted({path for row in changes for path in (row["path"], row["old_path"]) if path})
    inputs = []
    for raw in paths:
        path = contained(repo, raw, False)
        content = digest(path) if path.is_file() else None
        staged = git(repo, "ls-files", "--stage", "-z", "--", raw)
        # index metadata covers staged deletions and staged/worktree divergence without a payload read.
        base_blob = git(repo, "ls-tree", "-z", base_id, "--", raw)
        inputs.append({"path": raw, "sha256": content,
                       "index_sha256": hashlib.sha256(staged).hexdigest(),
                       "base_sha256": hashlib.sha256(base_blob).hexdigest()})
    ancillary = workspace / "repo/core/legacy-qa-evidence-v1.md"
    supporting = []
    if ancillary.exists() or ancillary.is_symlink():
        supporting.append({"path": "repo/core/legacy-qa-evidence-v1.md", "sha256": digest(contained(workspace, "repo/core/legacy-qa-evidence-v1.md"))})
    return {"schema_version": 1, "repository": str(repo), "base": base_id, "head": head,
            "implementation_scope": scopes, "changes": changes, "inputs": inputs,
            "workspace": str(workspace.resolve()), "runtime": inventory_runtime(workspace, roots), "intent": intent,
            "framework": framework_snapshot(workflow), "supporting_inputs": supporting}

def validate_manifest(path, repo, workspace, workflow):
    if path.is_symlink() or any(part.lower() in SENSITIVE or part.lower().startswith(".env") for part in path.parts):
        raise ValueError("unsafe scope manifest source")
    digest(path)
    document = strict_json(path.read_text())
    fields(document, {"schema_version", "repository", "base", "head", "implementation_scope", "changes", "inputs", "workspace", "runtime", "intent", "framework", "supporting_inputs"}, "scope manifest")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise ValueError("unknown scope schema")
    if document["intent"] not in {"iteration", "checkpoint"}:
        raise ValueError("invalid scope intent")
    if document["repository"] != str(repo.resolve()) or document["workspace"] != str(workspace.resolve()):
        raise ValueError("scope repository/workspace identity mismatch")
    for key in ("base", "head"):
        if not isinstance(document[key], str) or not re.fullmatch(r"[0-9a-f]{40}", document[key]):
            raise ValueError("invalid source revision")
    if not isinstance(document["runtime"], list):
        raise ValueError("invalid runtime inventory")
    fields(document["framework"], {"repository", "head", "dirty", "sha256"}, "framework inventory")
    if type(document["framework"]["dirty"]) is not bool:
        raise ValueError("invalid framework dirty flag")
    roots = []
    for entry in document["runtime"]:
        fields(entry, {"root", "files"}, "runtime inventory")
        roots.append(entry["root"])
    actual = snapshot(repo, workspace, document["base"], document["implementation_scope"], roots, document["intent"], workflow)
    if actual != document:
        raise ValueError("stale or incomplete scope manifest")
    return document

def registry(path, workflow):
    data = strict_json(path.read_text())
    fields(data, {"schema_version", "checks", "runtime_required"}, "check registry")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1 or not isinstance(data["checks"], dict):
        raise ValueError("invalid check registry")
    for name, row in data["checks"].items():
        if not CHECK.fullmatch(name):
            raise ValueError("unsafe registry check name")
        fields(row, {"dependencies", "scope"}, "registry check")
        if row["scope"] not in {"framework", "runtime"} or not isinstance(row["dependencies"], list) or any(not isinstance(name, str) for name in row["dependencies"]):
            raise ValueError("invalid registry check")
        if len(row["dependencies"]) != len(set(row["dependencies"])):
            raise ValueError("duplicate dependency")
        source = contained(workflow, ".systems/scripts/" + name)
        if not os.access(source, os.X_OK):
            raise ValueError("non-executable required check source")
    if not isinstance(data["runtime_required"], list) or any(not isinstance(name, str) or name not in data["checks"] for name in data["runtime_required"]):
        raise ValueError("unknown runtime-required check")
    if len(data["runtime_required"]) != len(set(data["runtime_required"])):
        raise ValueError("duplicate runtime-required check")
    if not (RUNTIME_CHECKS | {"check-contract-compliance", "check-full-qa-verification"}) <= set(data["runtime_required"]):
        raise ValueError("missing runtime-required consumer")
    for name, row in data["checks"].items():
        if (row["scope"] == "runtime") != (name in RUNTIME_CHECKS):
            raise ValueError("invalid runtime consumer scope")
    def visit(name, stack, done):
        if name not in data["checks"]:
            raise ValueError("unknown dependency check")
        if name in stack:
            raise ValueError("dependency cycle")
        if name in done:
            return
        for dependency in data["checks"][name]["dependencies"]:
            visit(dependency, stack + [name], done)
        done.append(name)
    for name in data["checks"]:
        visit(name, [], [])
    return data

def closure(names, data):
    done = []
    def visit(name):
        if name in done:
            return
        if name not in data["checks"]:
            raise ValueError("unknown scoped check")
        for dependency in data["checks"][name]["dependencies"]:
            visit(dependency)
        done.append(name)
    for name in names:
        visit(name)
    return done

def owned_runtime_input(repo, workspace, roots, row):
    # Tracked target-owned runtime is not framework code. Missing/deleted inputs
    # remain conservative: a complete scoped claim cannot hide an absent artifact.
    if row["sha256"] is None:
        return False
    path = repo / row["path"]
    if not path.is_relative_to(workspace):
        return False
    local = path.relative_to(workspace)
    for raw in roots:
        root = Path(raw)
        if not local.is_relative_to(root):
            continue
        parts = local.relative_to(root).parts
        if len(parts) == 1 and local.suffix == ".md":
            return True
        if raw.startswith("projects/") and len(parts) > 1 and parts[0] in PROJECT_DIRS:
            return True
    return False

def plan(args):
    workflow, repo, workspace = args.workflow.resolve(), args.repo.resolve(), args.workspace.resolve()
    data = registry(args.registry, workflow)
    requested = [name.strip() for name in args.checks.split(",")]
    if any(not CHECK.fullmatch(name) for name in requested):
        raise ValueError("empty or unsafe scoped check")
    names = closure(requested, data)
    manifest = validate_manifest(args.manifest, repo, workspace, workflow) if args.manifest else None
    roots = [entry["root"] for entry in manifest["runtime"]] if manifest else []
    if args.project:
        if not SLUG.fullmatch(args.project):
            raise ValueError("unsafe project")
        if roots and roots != ["projects/" + args.project]:
            raise ValueError("project option conflicts with manifest roots")
    invocations = []
    for name in names:
        scopes = roots if data["checks"][name]["scope"] == "runtime" and roots else [""]
        for root in scopes:
            project = root.removeprefix("projects/") if root.startswith("projects/") else ""
            if not root:
                project = (args.project or "") if data["checks"][name]["scope"] == "runtime" else ""
            normalized = name + ":" + root + ":" + project
            identifier = name + "-scope-" + hashlib.sha256(normalized.encode()).hexdigest()[:16] if root or project else name
            invocations.append({"check": name, "root": root, "project": project, "id": identifier})
    coverage, reason, eligible = "unverified", "no-manifest", False
    if manifest:
        shared = any(path["path"].startswith((".systems/", ".github/")) or path["path"] in {"AGENTS.md", "HUMANS.md", "README.md"} for path in manifest["inputs"])
        unknown = any(not owned_runtime_input(repo, workspace, roots, row) for row in manifest["inputs"])
        required = closure(data["runtime_required"], data)
        missing = [name for name in required if name not in names]
        coverage, reason = "incomplete", "missing-required-checks" if missing else "runtime-scope-required"
        if shared or unknown or manifest["framework"]["dirty"]:
            reason = "full-required-source-impact"
        elif roots and not missing:
            coverage, reason = "complete", "owned-runtime-required-dependencies"
            eligible = manifest["intent"] == "checkpoint"
            if "repo/core" in roots:
                status = contained(workspace, "repo/core/status.md").read_text()
                active = re.findall(r"^active-project:\s*(\S+)\s*$", status, re.M)
                active += re.findall(r"^\|\s*`?active-project`?\s*\|\s*`?([a-z0-9-]+)`?\s*\|", status, re.M)
                if len(active) != 1 or (active[0] not in {"none", "not-applicable"} and "projects/" + active[0] not in roots):
                    coverage, reason, eligible = "incomplete", "active-project-scope-required", False
    return {"schema_version": 1, "requested": list(dict.fromkeys(requested)), "required": names,
            "invocations": invocations, "coverage_result": coverage, "reason": reason,
            "final_evidence_eligible": eligible, "manifest": str(args.manifest.resolve()) if args.manifest else None,
            "manifest_sha256": digest(args.manifest) if args.manifest else None,
            "registry_sha256": digest(args.registry), "registry": str(args.registry.resolve()), "workflow": str(workflow)}

def validate_distillation(workspace, raw, workflow, repo):
    root = owned_root(workspace, raw)
    files = [p for p in runtime_files(workspace, raw) if p.parent == root / "capture-state" and p.suffix == ".md"]
    required = {"Work ID", "Work mode", "Project/repo scope", "Source artifact", "Quality artifact", "State", "Distillation artifact", "Last reminder", "Owner disposition", "Privacy/scope check", "Residual risk"}
    for file in files:
        values = {}
        text = file.read_text()
        for key, value in re.findall(r"^- ([^:\n]+):\s*([^\n]+)$", text, re.M):
            key, value = key.strip("` "), value.strip("` ")
            if key in values:
                raise ValueError("duplicate distillation field")
            values[key] = value
        if not required <= values.keys() or any(not values[key] or "<" in values[key] for key in required):
            raise ValueError("incomplete distillation state")
        state = values["State"]
        if state not in {"pending-quality", "ready", "completed", "deferred", "owner-skipped", "blocked", "not-applicable"}:
            raise ValueError("invalid distillation state")
        if values.get("is_distilled` derived value", values.get("is_distilled derived value")) != ("true" if state == "completed" else "false"):
            raise ValueError("distillation derived boolean mismatch")
        if state in {"ready", "completed"} and not re.fullmatch(r"pass(?: for [^<>\n]+)?", values["Privacy/scope check"]):
            raise ValueError("distillation privacy check is not pass")
        for key in ("Source artifact", "Quality artifact", "Distillation artifact"):
            values[key] = values[key].split(";", 1)[0].strip()
            if values[key] != "none":
                contained(root, values[key])
        if state in {"ready", "completed"}:
            if values["Quality artifact"] == "none":
                raise ValueError("distillation lacks quality evidence")
            if not raw.startswith("projects/"):
                raise ValueError("formal distillation requires a project scope")
            qa = workflow / ".systems/scripts/lib/qa-evidence.py"
            checked = subprocess.run([sys.executable, str(qa), str(root / values["Quality artifact"]),
                            "--workflow-root", str(workflow), "--workspace-root", str(workspace),
                            "--project", raw.split("/")[1], "--approved-target-root", str(repo),
                            "--expected-kind", "implementation-quality",
                            "--expected-identity", raw.split("/")[1] + ":" + values["Work ID"],
                            "--require-pass"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if checked.returncode:
                raise ValueError("distillation current QA evidence invalid")
        if state == "completed" and values["Distillation artifact"] == "none":
            raise ValueError("completed distillation lacks artifact")
        if state == "completed":
            distilled = contained(root, values["Distillation artifact"]).read_text()
            ids = re.findall(r"^- Task/package ID:\s*([^\n]+)$", distilled, re.M)
            if ids != [values["Work ID"]]:
                raise ValueError("distillation artifact identity mismatch")
            if not re.search(r"^## Distillation Gate\s*$", distilled, re.M) or not re.search(r"^- Ready for checkpoint processing:\s*yes(?:[;,].*)?$", distilled, re.M):
                raise ValueError("distillation artifact lacks accepted gate evidence")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("snapshot", "plan", "finish"):
        p = sub.add_parser(command)
        p.add_argument("--repo", type=Path, default=Path.cwd())
        p.add_argument("--workspace", type=Path, required=True)
        p.add_argument("--workflow", type=Path, default=Path(__file__).resolve().parents[3])
        if command == "snapshot":
            p.add_argument("--base", required=True)
            p.add_argument("--scope", action="append", required=True)
            p.add_argument("--runtime-root", action="append", default=[])
            p.add_argument("--intent", choices=["iteration", "checkpoint"], default="iteration")
        elif command == "plan":
            p.add_argument("--registry", type=Path, default=Path(__file__).with_name("validation-checks.json"))
            p.add_argument("--checks", required=True)
            p.add_argument("--manifest", type=Path)
            p.add_argument("--project", default="")
        else:
            p.add_argument("--plan", required=True)
            p.add_argument("--status", type=int, required=True)
            p.add_argument("--executed", default="")
    sub.add_parser("lines").add_argument("--plan", required=True)
    p = sub.add_parser("runtime-files")
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--root", required=True)
    p = sub.add_parser("resolve-artifact")
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--root", required=True)
    p.add_argument("--path", required=True)
    p = sub.add_parser("distillation")
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--root", required=True)
    p.add_argument("--workflow", type=Path, default=Path(__file__).resolve().parents[3])
    p.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.command == "snapshot":
        result = snapshot(args.repo, args.workspace, args.base, args.scope, args.runtime_root, args.intent, args.workflow)
    elif args.command == "plan":
        result = plan(args)
    elif args.command == "lines":
        for row in strict_json(args.plan)["invocations"]:
            # Nonempty sentinels keep Bash IFS whitespace from collapsing empty columns.
            print("\t".join(row[key] or "-" for key in ("check", "root", "project", "id")))
        return
    elif args.command == "runtime-files":
        for path in runtime_files(args.workspace.resolve(), args.root):
            sys.stdout.buffer.write(os.fsencode(path) + b"\0")
        return
    elif args.command == "resolve-artifact":
        root = owned_root(args.workspace.resolve(), args.root)
        path = Path(args.path)
        if path.is_absolute() and not path.is_relative_to(root):
            raise ValueError("artifact outside owned runtime root")
        raw = str(path.relative_to(root)) if path.is_absolute() else args.path
        print(contained(root, raw))
        return
    elif args.command == "distillation":
        validate_distillation(args.workspace.resolve(), args.root, args.workflow.resolve(), args.repo.resolve())
        return
    else:
        planned = strict_json(args.plan)
        fields(planned, {"schema_version", "requested", "required", "invocations", "coverage_result", "reason",
                         "final_evidence_eligible", "manifest", "manifest_sha256", "registry_sha256", "registry", "workflow"}, "execution plan")
        if planned["manifest"]:
            path = Path(planned["manifest"])
            if digest(path) != planned["manifest_sha256"]:
                raise ValueError("scope manifest changed during validation")
        if digest(Path(planned["registry"])) != planned["registry_sha256"]:
            raise ValueError("check registry changed during validation")
        projects = {row["project"] for row in planned["invocations"] if row["project"] and not row["root"]}
        if len(projects) > 1:
            raise ValueError("invalid execution project options")
        actual_plan = plan(argparse.Namespace(workflow=args.workflow, repo=args.repo, workspace=args.workspace,
                           registry=Path(planned["registry"]), checks=",".join(planned["requested"]),
                           manifest=Path(planned["manifest"]) if planned["manifest"] else None,
                           project=next(iter(projects), "")))
        if planned != actual_plan:
            raise ValueError("stale or fabricated execution plan")
        executed = args.executed.split(",") if args.executed else []
        expected = [row["id"] for row in planned["invocations"]]
        complete_execution = executed == expected and args.status == 0
        if args.status == 0 and not complete_execution:
            raise ValueError("requested invocation execution is incomplete")
        result = {"execution_result": "pass" if args.status == 0 else "fail",
                  "coverage_result": planned["coverage_result"] if complete_execution else "incomplete",
                  "final_evidence_eligible": planned["final_evidence_eligible"] and complete_execution,
                  "requested": planned["requested"], "required": expected, "executed": executed,
                  "skipped": [item for item in expected if item not in executed],
                  "reason": planned["reason"] if complete_execution else "requested-check-failed-or-incomplete"}
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError, TypeError, KeyError) as error:
        # Do not expose private path names or source payloads in scope diagnostics.
        message = str(error) if isinstance(error, ValueError) else type(error).__name__
        print("Validation scope rejected: " + message, file=sys.stderr)
        sys.exit(1)
