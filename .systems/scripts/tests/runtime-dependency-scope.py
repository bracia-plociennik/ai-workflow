#!/usr/bin/env python3
"""Offline fixed dependency exclusion and fail-closed consumer regressions."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parents[3]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, SOURCE / ".systems/scripts/lib" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load("scope", "validation-scope.py")
qa = load("qa", "qa-evidence.py")


def reject(call, fragment):
    try:
        call()
    except ValueError as error:
        assert fragment in str(error), str(error)
    else:
        raise AssertionError("expected rejection: " + fragment)


with tempfile.TemporaryDirectory(prefix="dependency-scope-") as directory:
    workspace = Path(directory) / "workspace"
    root = workspace / "projects/probe"
    artifacts = root / "quality/artifacts"
    artifacts.mkdir(parents=True)
    status = (SOURCE / ".systems/ai/examples/projects/EXAMPLE/status.md").read_text()
    status = status.replace(".systems/ai/examples/projects/EXAMPLE", str(root))
    (root / "status.md").write_text(status)
    (root / "context.md").write_text("# Context\n")
    (root / "tasks.md").write_text("| Task ID | Title | Risk | Status | Task Card | Spec | Quality | Notes |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| PROBE-DOCS-001-fixture | Fixture | low | ready | none | none | none | synthetic |\n")
    state = root / "capture-state/work.md"
    state.parent.mkdir()
    state_text = "# Distillation State\n" + "\n".join("- " + key + ": " + value for key, value in {
        "Work ID": "PROBE-DOCS-001-fixture", "Work mode": "workflow-maintenance", "Project/repo scope": "probe",
        "Source artifact": "context.md", "Quality artifact": "none", "State": "pending-quality",
        "Distillation artifact": "none", "Last reminder": "none", "Owner disposition": "not-requested",
        "Privacy/scope check": "pass", "Residual risk": "none", "is_distilled derived value": "false"
    }.items()) + "\n"
    state.write_text(state_text)
    target = Path(directory) / "dependencies"
    target.mkdir()
    (target / ".git").mkdir()
    (target / ".env.md").write_text("synthetic forbidden evidence")
    (target / "WRONG.md").write_text("not active evidence")
    link = artifacts / "node_modules"
    link.symlink_to(target, target_is_directory=True)
    inode, destination = link.lstat().st_ino, os.readlink(link)
    adjacent = artifacts / "accepted.md"
    adjacent.write_text("owned evidence")
    files = scope.runtime_files(workspace, "projects/probe")
    assert adjacent in files and all("node_modules" not in p.parts for p in files)
    assert link.lstat().st_ino == inode and os.readlink(link) == destination
    for reader in (scope.contained, qa.contained):
        reject(lambda: reader(root, "quality/artifacts/node_modules/WRONG.md"), "not evidence")
        reject(lambda: reader(workspace, "projects/probe/quality/artifacts/node_modules/WRONG.md"), "not evidence")

    env = dict(os.environ, AI_WORKFLOW_MODE="official", AI_WORKFLOW_WORKSPACE_HOME=str(workspace))

    def check(name, ok=True, fragment=""):
        result = subprocess.run([str(SOURCE / ".systems/scripts" / name), "--runtime-only", "--scope-root", "projects/probe"],
                                cwd=SOURCE, env=env, capture_output=True, text=True)
        assert (result.returncode == 0) == ok, (name, result.stdout, result.stderr)
        assert fragment in result.stdout + result.stderr

    for name in sorted(scope.RUNTIME_CHECKS):
        check(name, fragment="not evidence; no traversal")
    state.write_text(state_text.replace("value: false", "value: true"))
    check("check-distillation-state", False, "derived boolean mismatch")
    state.write_text(state_text)
    (root / "WRONG.md").write_text("invalid owned filename")
    check("check-naming", False, "Invalid Markdown filename")
    (root / "WRONG.md").unlink()
    (root / "status.md").write_text(status.replace("next-phase", "invalid-phase-field"))
    check("check-status-consistency", False, "missing status key: next-phase")
    (root / "status.md").write_text(status)
    bad_qa = root / "quality/phase-5-probe-quality.md"
    bad_qa.write_text("# Quality\n\n## Metadata\n\n- Result: PASS\n")
    check("check-qa-evidence", False, "missing ## Evidence section")
    bad_qa.unlink()
    assert link.lstat().st_ino == inode and os.readlink(link) == destination

    link.unlink()
    link.symlink_to(Path(directory) / "missing-target", target_is_directory=True)
    scope.runtime_files(workspace, "projects/probe")
    for name in sorted(scope.RUNTIME_CHECKS):
        check(name)
    link.unlink()
    link.mkdir()
    (link / "readme.md").write_text("not evidence")
    assert link / "readme.md" not in scope.runtime_files(workspace, "projects/probe")
    for reader in (scope.contained, qa.contained):
        reject(lambda: reader(root, "quality/artifacts/node_modules/readme.md"), "not evidence")
    (link / "readme.md").unlink()
    link.rmdir()
    link.write_text("not a directory")
    reject(lambda: scope.runtime_files(workspace, "projects/probe"), "not a directory or symlink")
    link.unlink()
    for path in (root / "node_modules", artifacts / "other-dependencies", root / "reviews/node_modules"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target, target_is_directory=True)
        reject(lambda: scope.runtime_files(workspace, "projects/probe"), "symlink runtime")
        path.unlink()
    parent = root / "quality/linked-artifacts"
    parent.symlink_to(target, target_is_directory=True)
    reject(lambda: scope.runtime_files(workspace, "projects/probe"), "symlink runtime")

print("Fixed dependency exclusion and all runtime consumers verified.")
