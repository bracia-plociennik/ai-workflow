"""Offline containment probe using synthetic canaries only; no model execution."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

project = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="lv005-isolation-") as temp:
    root = Path(temp).resolve()
    fixture = root / "fixture"
    fixture.mkdir()
    (fixture / "visible.txt").write_text("synthetic-visible")
    (root / "outside-canary.txt").write_text("synthetic-outside")
    command = [
        "/Users/jakubplociennik/.local/bin/codex", "sandbox",
        "--permission-profile", "lv005-fixture",
        "-c", 'permissions.lv005-fixture.filesystem={":minimal"="read",":workspace_roots"={ "."="write" }}',
        "-c", 'permissions.lv005-fixture.network.enabled=false',
        "-C", str(fixture), "--", "/bin/sh", "-c",
        'test "$(cat visible.txt)" = synthetic-visible || exit 10; '
        'if cat "$1" >/dev/null 2>&1; then exit 11; fi; '
        'printf synthetic-write > written.txt || exit 12; '
        'printf "VISIBLE_OK OUTSIDE_DENIED WRITE_OK\n"', "probe", str(root / "outside-canary.txt")]
    environment = {k: os.environ[k] for k in ("HOME","PATH","CODEX_HOME","TMPDIR") if k in os.environ}
    result = subprocess.run(command, cwd=fixture, env=environment, text=True,
                            capture_output=True, timeout=30)
    data = {"kind": "offline-synthetic-containment-probe", "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr,
            "fixture_write": (fixture / "written.txt").exists(),
            "model_called": False, "private_files_read": False,
            "limits": "Tests a harmless sibling canary, not secrets; runtime/model context must be audited separately."}
    (project / "lv005-isolation-preflight-result.json").write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(data))
    raise SystemExit(result.returncode)
