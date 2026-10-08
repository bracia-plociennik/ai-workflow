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
