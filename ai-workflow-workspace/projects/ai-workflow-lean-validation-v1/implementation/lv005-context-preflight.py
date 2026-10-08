"""Local-only context preview, with an empty config home and synthetic CWD."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

output = Path(__file__).resolve().parent / "lv005-context-preflight-003"
output.mkdir(exist_ok=False)
with tempfile.TemporaryDirectory(prefix="lv005-context-preflight-") as temporary:
    root = Path(temporary).resolve()
    fixture = root / "fixture"
    fixture.mkdir()
    home = root / "empty-codex-home"
    home.mkdir()
    environment = {key: os.environ[key] for key in ("HOME", "PATH", "TMPDIR") if key in os.environ}
    environment["CODEX_HOME"] = str(home)
    settings = {
        "model": "gpt-6-sol", "model_reasoning_effort": "high",
        "approval_policy": "never", "default_permissions": "lv005-fixture",
        "permissions.lv005-fixture.filesystem": {":minimal": "read", ":workspace_roots": {".": "write"}},
        "permissions.lv005-fixture.network.enabled": False,
        "web_search": "disabled", "project_doc_max_bytes": 0,
        "features.code_mode_host": True, "features.skip_host_skill_discovery": True,
        "memories.generate_memories": False, "memories.use_memories": False,
    }
    for feature in ("apps", "plugins", "hooks", "memories", "multi_agent", "multi_agent_v2",
                    "browser_use", "browser_use_external", "computer_use", "view_image",
                    "image_generation", "skill_search", "skill_mcp_dependency_install",
                    "workspace_dependencies", "shell_snapshot", "tool_suggest"):
        settings["features." + feature] = False
    settings["skills.config"] = [{"path": str(home/"skills/.system"/name/"SKILL.md"), "enabled": False}
                                for name in ("imagegen", "openai-docs", "plugin-creator", "skill-creator", "skill-installer")]
    command = ["/Users/jakubplociennik/.local/bin/codex", "debug", "prompt-input"]
    for key, value in settings.items():
        if isinstance(value, dict):
            encoded = '{":minimal"="read",":workspace_roots"={ "."="write" }}'
        elif isinstance(value, list):
            encoded = '[' + ','.join('{path='+json.dumps(item['path'])+',enabled=false}' for item in value) + ']'
        else:
            encoded = json.dumps(value)
        command += ["-c", key + "=" + encoded]
    command.append("Synthetic local context preview only; do not execute tools.")
    result = subprocess.run(command, cwd=fixture, env=environment, capture_output=True,
                            text=True, timeout=60)
    (output / "prompt-input.json").write_text(result.stdout)
    (output / "stderr.txt").write_text(result.stderr)
    data = {"exit_code": result.returncode, "model_called": False,
            "source": "local CLI debug prompt-input with empty CODEX_HOME",
            "settings": settings, "bytes": len(result.stdout.encode()),
            "sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
            "limits": "Local preview is separate from exec; verify exec warnings and actual tools independently."}
    (output / "metadata.json").write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({key:value for key,value in data.items() if key != "settings"}))
    raise SystemExit(result.returncode)
