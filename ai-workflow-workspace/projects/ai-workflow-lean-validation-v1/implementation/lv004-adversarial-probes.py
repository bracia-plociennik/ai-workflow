"""Isolated lifecycle/integrity probes, never an equivalence certificate alone."""
import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time

parser = argparse.ArgumentParser()
parser.add_argument("--candidate", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
candidate = args.candidate.resolve()
if not candidate.is_relative_to(Path("/tmp").resolve()):
    raise SystemExit("Candidate must be isolated under tmp")
script = candidate / ".systems/scripts/check-validator-smoke-tests"
embedded = script.read_text().split("<<'SMOKE_DISPATCH'\n", 1)[1].rsplit("\nSMOKE_DISPATCH", 1)[0]
definitions = embedded.rsplit("raise SystemExit(main())", 1)[0]
namespace = {"__name__": "isolated_probe"}
exec(compile(definitions, str(script), "exec"), namespace)
results = []

def copy_fixture(parent, name):
    root = parent / name
    shutil.copytree(candidate, root, ignore=shutil.ignore_patterns(".git"))
    return root.resolve()

def update_group_digest(root):
    path = root / ".systems/scripts/smoke/manifest.json"
    data = json.loads(path.read_text())
    group = root / ".systems/scripts/smoke/core.sh"
    data["files_sha256"]["core.sh"] = hashlib.sha256(group.read_bytes()).hexdigest()
    path.write_text(json.dumps(data) + "\n")

def inject(root, command):
    path = root / ".systems/scripts/smoke/core.sh"
    text = path.read_text()
    anchor = "tar --exclude='.git'"
    start = text.index(anchor)
    path.write_text(text[:start] + command + "\n" + text[start:])
    update_group_digest(root)

def assert_marker(text, result, code):
    rows = [line for line in text.splitlines() if line.startswith("AI_WORKFLOW_SMOKE_COMPLETE ")]
    assert len(rows) == 1, rows
    assert f"result={result} " in rows[0] and f"exit_code={code} " in rows[0], rows

with tempfile.TemporaryDirectory(prefix="lv004-adversarial-") as temporary:
    parent = Path(temporary)
    baseline = namespace["load_manifest"](candidate)
    results.append({"case": "complete-live-manifest", "result": "pass", "ids": len(baseline["tests"])})
    for case, expected in (
        ("duplicate-json-key", "duplicate JSON key"),
        ("missing-source", "common.sh"),
        ("source-drift", "source digest"),
        ("missing-test-contract", "test contract inventory"),
        ("wrong-coverage-command", "coverage index command"),
    ):
        root = copy_fixture(parent, case)
        manifest = root / ".systems/scripts/smoke/manifest.json"
        data = json.loads(manifest.read_text())
        if case == "duplicate-json-key":
            text = manifest.read_text().replace('"schema": 2,', '"schema": 2, "schema": 2,', 1)
            manifest.write_text(text)
        elif case == "missing-source":
            (root / ".systems/scripts/smoke/common.sh").unlink()
        elif case == "source-drift":
            path = root / ".systems/scripts/smoke/common.sh"
            path.write_text(path.read_text() + "\n")
        elif case == "missing-test-contract":
            data["tests"].pop()
            manifest.write_text(json.dumps(data) + "\n")
        elif case == "wrong-coverage-command":
            # Hold source/digests intact: exercise the live index consumer itself.
            old = namespace["COVERAGE_INDEX"]["contract-compliance"]
            namespace["COVERAGE_INDEX"]["contract-compliance"] = (old[0], "no-such-live-command")
        try:
            namespace["load_manifest"](root)
        except (ValueError, OSError) as error:
            assert expected in str(error), (case, str(error))
            results.append({"case": case, "result": "pass", "diagnostic": expected})
        else:
            raise AssertionError("Mutation accepted: " + case)
        finally:
            if case == "wrong-coverage-command":
                namespace["COVERAGE_INDEX"]["contract-compliance"] = old
    for case, injection, expected in (
        ("early-zero-no-cases", "smoke_suite_completed=1; exit 0", 1),
        ("child-failure-seven", "exit 7", 7),
    ):
        root = copy_fixture(parent, case)
        inject(root, injection)
        command = ["bash", str(root / ".systems/scripts/check-validator-smoke-tests"), "--group", "core", "--progress", "quiet"]
        run = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
        assert run.returncode == expected, run.stdout
        assert_marker(run.stdout, "fail", expected)
        if case == "early-zero-no-cases":
            assert "executed ID/group coverage" in run.stdout
        results.append({"case": case, "result": "pass", "exit_code": run.returncode})
    for case in ("interrupt-owned-tree", "timeout-owned-tree", "failure-owned-tree"):
        root = copy_fixture(parent, case)
        pids = parent / (case + ".pids")
        payload = parent / (case + ".py")
        payload.write_text("import os, subprocess, sys, time\n"
                           "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(90)'], start_new_session=True)\n"
                           "open(sys.argv[1], 'w').write(str(os.getpid()) + '\\n' + str(child.pid) + '\\n')\n"
                           "time.sleep(90)\n")
        injection = f"python3 '{payload}' '{pids}'"
        if case == "failure-owned-tree":
            injection += " &\nsleep 1\nexit 7"
        inject(root, injection)
        command = ["bash", str(root / ".systems/scripts/check-validator-smoke-tests"), "--group", "core", "--progress", "quiet"]
        if case == "timeout-owned-tree":
            command = [str(candidate / ".systems/scripts/run-with-timeout"), "--timeout-seconds", "3", *command]
        process = subprocess.Popen(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
        deadline = time.monotonic() + 10
        while not pids.exists() and time.monotonic() < deadline and process.poll() is None:
            time.sleep(0.05)
        assert pids.exists(), case
        if case == "interrupt-owned-tree":
            process.send_signal(signal.SIGTERM)
        try:
            output, _ = process.communicate(timeout=15)
        except subprocess.TimeoutExpired as error:
            print(json.dumps({"failed_case": case, "parent_status": process.poll(),
                              "partial_output": (error.output or b"").decode() if isinstance(error.output, bytes) else error.output}), flush=True)
            # Probe-owned PIDs are exact, not a broad process-name match.
            for pid in map(int, pids.read_text().splitlines()):
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
            process.communicate(timeout=5)
            raise
        expected = {"interrupt-owned-tree": 143, "timeout-owned-tree": 124, "failure-owned-tree": 7}[case]
        assert process.returncode == expected, output
        assert_marker(output, "fail" if case == "failure-owned-tree" else "interrupted", 7 if case == "failure-owned-tree" else 143)
        for pid in map(int, pids.read_text().splitlines()):
            state = subprocess.run(["ps", "-p", str(pid), "-o", "stat="], text=True, stdout=subprocess.PIPE).stdout.strip()
            assert not state or state.startswith("Z"), (case, pid, state)
        # Every parent-owned fixture is removed, including nested-session payloads.
        results.append({"case": case, "result": "pass", "exit_code": process.returncode, "live_orphans": 0})
    root = copy_fixture(parent, "cleanup-failure")
    inject(root, "exit 7")
    saved_cwd, saved_argv = Path.cwd(), namespace["sys"].argv
    original_remove = namespace["shutil"].rmtree
    failed_paths = []
    def failing_remove(path):
        failed_paths.append(path)
        raise OSError("synthetic cleanup failure")
    try:
        os.chdir(root)
        namespace["sys"].argv = ["probe", "--group", "core", "--progress", "quiet"]
        namespace["shutil"].rmtree = failing_remove
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = namespace["main"]()
        assert code == 1 and "synthetic cleanup failure" in output.getvalue()
        assert_marker(output.getvalue(), "fail", 1)
        results.append({"case": "cleanup-failure", "result": "pass", "exit_code": code})
    finally:
        namespace["shutil"].rmtree = original_remove
        namespace["sys"].argv = saved_argv
        os.chdir(saved_cwd)
        for path in failed_paths:
            original_remove(path)
args.output.write_text(json.dumps({"candidate_dispatcher_sha256": hashlib.sha256(script.read_bytes()).hexdigest(), "probes": results,
                                   "limits": "Synthetic fault paths and manifest integrity only; full old/new behavior, repetitions and source QA are separate."}, indent=2) + "\n")
print(json.dumps({"probes": len(results), "result": "pass"}))
