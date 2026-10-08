"""Offline LV005 recovery. Synthetic local sink, no auth or model response.

Persist only fixed classifications, inventory hashes and synthetic check results.
Never persist raw CLI output, request text, headers or environment values.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


BASE = Path(__file__).resolve().parent
CLI = Path('/Users/jakubplociennik/.codex/packages/standalone/releases/0.156.1-aarch64-apple-darwin/bin/codex')
SANDBOX = '/usr/bin/sandbox-exec'
PROMPT = 'LV005_SYNTHETIC_REQUEST: local packaging probe only. No work or tools requested.'
MAX_BODY = 4_000_000
ALLOWED_TOOLS = {'function', 'custom'}
ALLOWED_TOOL_NAMES = {'exec_command', 'write_stdin', 'apply_patch', 'update_plan', 'code_mode'}


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def summarize(payload, headers=()):
    """Fail closed on unknown schema/context. Output never includes context strings."""
    errors = []
    if not isinstance(payload, dict):
        return {'errors': ['malformed-payload']}
    instructions = payload.get('instructions')
    items = payload.get('input')
    tools = payload.get('tools')
    if not isinstance(instructions, str) or not instructions.strip():
        errors.append('missing-instructions')
        instructions = ''
    if not isinstance(items, list) or not items:
        errors.append('missing-input')
        items = []
    texts, roles = [], []
    for item in items:
        if not isinstance(item, dict) or item.get('role') not in ('user', 'developer', 'system'):
            errors.append('invalid-input-item')
            continue
        roles.append(item['role'])
        content = item.get('content')
        if not isinstance(content, list) or not content:
            errors.append('invalid-content')
            continue
        for part in content:
            if not isinstance(part, dict) or part.get('type') not in ('input_text', 'text') or not isinstance(part.get('text'), str):
                errors.append('unexpected-content-type')
            else:
                texts.append(part['text'])
    combined = instructions + '\n' + '\n'.join(texts)
    for marker, classification in (
        ('<skills_instructions>', 'ambient-skills'),
        ('# AGENTS.md instructions', 'ambient-agents'),
        ('<memory', 'ambient-memory'),
        ('<app-context>', 'ambient-app-context'),
        ('/Users/', 'host-path'),
        ('LV005_FOREIGN_CONTEXT_CANARY', 'foreign-context'),
    ):
        if marker in combined:
            errors.append(classification)
    # A familiar tag is not authority: unknown permission/environment blocks
    # need an explicit future synthetic-source adapter, not a prefix exemption.
    for text in texts:
        if text != PROMPT:
            errors.append('unclassified-context')
    if texts.count(PROMPT) != 1:
        errors.append('missing-or-duplicate-prompt')
    inventory = []
    if not isinstance(tools, list):
        errors.append('missing-tools')
        tools = []
    for tool in tools:
        if not isinstance(tool, dict):
            errors.append('invalid-tool')
            continue
        kind = tool.get('type')
        name = tool.get('name', tool.get('function', {}).get('name') if isinstance(tool.get('function'), dict) else None)
        if kind not in ALLOWED_TOOLS or name not in ALLOWED_TOOL_NAMES:
            errors.append('unexpected-tool')
        inventory.append({'type': kind if kind in ALLOWED_TOOLS else 'unexpected',
                          'name': name if name in ALLOWED_TOOL_NAMES else 'unexpected',
                          'schema_sha256': digest(tool)})
    if len({(t['type'], t['name']) for t in inventory}) != len(inventory):
        errors.append('duplicate-tool')
    if any(str(h).lower() in ('authorization', 'proxy-authorization', 'x-api-key', 'api-key', 'cookie') for h in headers):
        errors.append('authentication-header')
    if payload.get('model') != 'gpt-6-sol':
        errors.append('unexpected-model')
    reasoning = payload.get('reasoning')
    if not isinstance(reasoning, dict) or reasoning.get('effort') != 'high':
        errors.append('unexpected-reasoning')
    return {'errors': sorted(set(errors)), 'context_sha256': digest(combined.encode()),
            'instructions_sha256': digest(instructions.encode()), 'context_bytes': len(combined.encode()),
            'role_inventory': roles, 'input_count': len(items), 'tools': inventory,
            'request_sha256': digest(payload)}


def compare(preview, actual):
    errors = list(preview.get('errors', [])) + list(actual.get('errors', []))
    for key in ('context_sha256', 'instructions_sha256', 'role_inventory', 'tools'):
        if key not in preview or key not in actual or preview[key] != actual[key]:
            errors.append('preview-exec-mismatch:' + key)
    return sorted(set(errors))


def result_errors(code, output_present, timed_out=False):
    errors = []
    if timed_out:
        errors.append('process-timeout')
    if code != 0:
        errors.append('nonzero-exit')
    if not output_present:
        errors.append('missing-actual-result')
    return errors


def run(command, cwd, env, timeout=45):
    process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        try:
            out, err = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                out, err = process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                out, err = process.communicate(timeout=5)
    finally:
        # Also kill descendants of a successfully exited leader, never unrelated PIDs.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)
    summary = {'exit_code': 124 if timed_out else process.returncode, 'timed_out': timed_out,
               'stdout_bytes': len(out), 'stderr_bytes': len(err),
               'stdout_sha256': digest(out), 'stderr_sha256': digest(err),
               'sandbox_unavailable': b'sandbox_apply' in err or b'failed to initialize sandbox' in err,
               'unknown_config': b'unknown field' in err or b'unrecognized' in err,
               'operation_denied': b'Operation not permitted' in err or b'Permission denied' in err}
    syntax = re.search(rb'unbound variable: ([a-zA-Z0-9_*-]+)', err)
    if syntax:
        summary['sandbox_unbound_symbol'] = syntax.group(1).decode('ascii')
    summary['diagnostic_categories'] = [label for token, label in (
        (b'compilation', 'policy-compilation'), (b'syntax', 'policy-syntax'),
        (b'posix_spawn', 'spawn-failure'), (b'dyld', 'runtime-loader'),
        (b'No such file', 'missing-runtime-file'), (b'not permitted', 'permission-denied'),
        (b'unbound', 'policy-unbound-symbol')) if token in err]
    return summary, out, err


def policy(root, port):
    # No broad home, /tmp, /Users, keychain, Unix-socket or network access.
    read_paths = ['/System/Library', '/usr/lib', '/usr/share', '/usr/bin', '/bin',
                  '/private/var/db/dyld', str(CLI)]
    lines = ['(version 1)', '(deny default)', '(allow process*)', '(allow sysctl-read)',
             '(allow signal (target self))', '(allow file-read-metadata)',
             '(allow mach-lookup (global-name "com.apple.system.logger"))']
    for path in read_paths:
        lines.append('(allow file-read* file-map-executable (subpath ' + json.dumps(path) + '))')
    # The Apple system profile treats executable mappings separately from reads.
    # Inherited descriptors here are only /dev/null and our stdout/stderr pipes.
    lines.append('(allow file-read-data file-write-data (subpath "/dev/fd"))')
    for path in ['/dev/null', '/dev/random', '/dev/urandom', '/dev/tty']:
        lines.append('(allow file-read* file-write* (literal ' + json.dumps(path) + '))')
    for name in ('home', 'codex-home', 'temp', 'fixture'):
        lines.append('(allow file-read* file-write* (subpath ' + json.dumps(str(root / name)) + '))')
    # macOS SBPL requires the loopback token "localhost", not numeric 127.0.0.1.
    lines.append('(allow network-outbound (remote ip "localhost:' + str(port) + '"))')
    return '\n'.join(lines) + '\n'


def settings(root, port):
    values = {
        'model': '"gpt-6-sol"', 'model_reasoning_effort': '"high"',
        'approval_policy': '"never"', 'sandbox_mode': '"workspace-write"',
        'sandbox_workspace_write.network_access': 'false', 'web_search': '"disabled"',
        'project_doc_max_bytes': '0', 'features.code_mode_host': 'true',
        'features.skip_host_skill_discovery': 'true',
        'memories.generate_memories': 'false', 'memories.use_memories': 'false',
        'model_provider': '"lv005-local-sink"',
        'model_providers.lv005-local-sink.name': '"Rejecting local sink, no model"',
        'model_providers.lv005-local-sink.base_url': json.dumps('http://127.0.0.1:' + str(port) + '/v1'),
        'model_providers.lv005-local-sink.requires_openai_auth': 'false',
        'model_providers.lv005-local-sink.wire_api': '"responses"',
        'model_providers.lv005-local-sink.supports_websockets': 'false',
        'model_providers.lv005-local-sink.request_max_retries': '0',
        'model_providers.lv005-local-sink.stream_max_retries': '0',
    }
    for feature in ('apps', 'plugins', 'hooks', 'memories', 'multi_agent', 'multi_agent_v2',
                    'browser_use', 'browser_use_external', 'computer_use', 'view_image',
                    'image_generation', 'skill_search', 'skill_mcp_dependency_install',
                    'workspace_dependencies', 'shell_snapshot', 'tool_suggest'):
        values['features.' + feature] = 'false'
    names = ('imagegen', 'openai-docs', 'plugin-creator', 'skill-creator', 'skill-installer')
    values['skills.config'] = '[' + ','.join('{path=' + json.dumps(str(root/'codex-home'/'skills'/'.system'/name/'SKILL.md')) + ',enabled=false}' for name in names) + ']'
    return values


def make_sink():
    observations = []
    class Sink(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'LV005_LOCAL_SINK_OK')

        def do_POST(self):
            self.connection.settimeout(3)
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= MAX_BODY or self.path != '/v1/responses':
                    observations.append({'errors': ['invalid-transport']})
                else:
                    body = self.rfile.read(length)
                    if len(body) != length:
                        observations.append({'errors': ['truncated-request']})
                    else:
                        observations.append(summarize(json.loads(body), self.headers.keys()))
            except (ValueError, UnicodeDecodeError, TimeoutError, OSError):
                observations.append({'errors': ['malformed-request']})
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            try:
                self.wfile.write(b'{"error":{"message":"intentional local sink rejection; no model response","type":"invalid_request_error"}}')
            except (BrokenPipeError, ConnectionResetError):
                pass
    server = HTTPServer(('127.0.0.1', 0), Sink)
    server.timeout = 3
    return server, observations


def main():
    output = BASE / 'runs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + str(os.getpid()))
    output.mkdir(parents=True, exist_ok=False)
    report = {'scope': 'offline-preparation-only', 'model_calls': 0, 'login_performed': False,
              'credentials_read_or_copied': False, 'hosted_provider_equivalence': 'not-tested',
              'behavioral_eval_ready': False, 'LV005_disposition': 'deferred',
              'checks': {}, 'blockers': [], 'result': 'blocked',
              'harness_sha256': digest(Path(__file__).read_bytes())}
    server = None
    thread = None
    temporary = None
    root = None
    try:
        report['active_stage'] = 'freeze-and-setup'
        if not CLI.is_file() or not Path(SANDBOX).is_file():
            raise RuntimeError('missing-frozen-runtime-or-sandbox')
        report['binary_sha256'] = digest(CLI.read_bytes())
        temporary = tempfile.TemporaryDirectory(prefix='lv005-offline-', dir='/private/tmp')
        root = Path(temporary.name).resolve()
        for name in ('home', 'codex-home', 'temp', 'fixture'):
            (root / name).mkdir(mode=0o700)
        (root/'fixture'/'visible.txt').write_text('synthetic-visible\n')
        (root/'sibling-canary.txt').write_text('LV005_FOREIGN_CONTEXT_CANARY\n')
        environment = {'HOME': str(root/'home'), 'CODEX_HOME': str(root/'codex-home'),
                       'TMPDIR': str(root/'temp'), 'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}
        report['environment_keys'] = sorted(environment)
        report['active_stage'] = 'loopback-sink-start'
        server, received = make_sink()
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        profile = policy(root, server.server_port)
        config = settings(root, server.server_port)
        report['sandbox_policy_sha256'] = digest(profile.encode())
        report['config_sha256'] = digest(config)
        report['config_keys'] = sorted(config)
        # Policy uses -p text, so no broad read exemption is needed for a policy file.
        prefix = [SANDBOX, '-p', profile]
        report['active_stage'] = 'timeout-cleanup'
        timeout_script = '(printf LV005_CHILD_STARTED; /bin/sleep 2; printf orphan > orphan.txt) & wait'
        cleanup, out, _ = run(prefix + ['/bin/sh', '-c', timeout_script], root/'fixture', environment, timeout=0.2)
        time.sleep(2.3)
        cleanup['delayed_descendant_write_absent'] = not (root/'fixture'/'orphan.txt').exists()
        cleanup['child_started_observed'] = b'LV005_CHILD_STARTED' in out
        report['checks']['timeout-cleanup'] = cleanup
        if not cleanup['timed_out'] or not cleanup['child_started_observed'] or not cleanup['delayed_descendant_write_absent']:
            raise RuntimeError('timeout-cleanup-not-proven')
        # Independent real command: synthetic outputs, OS-denied sibling read and
        # external network denial diagnostic; no model/CLI tool claim is accepted.
        shell = '''test "$(/bin/cat visible.txt)" = synthetic-visible || exit 10
if /bin/cat "$1" >/dev/null; then exit 11; fi
printf synthetic-write > written.txt || exit 12
test "$(/usr/bin/curl --noproxy '*' --connect-timeout 2 -s "$2")" = LV005_LOCAL_SINK_OK || exit 13
/usr/bin/curl --noproxy '*' --connect-timeout 2 -sS http://192.0.2.1:9 > network.out 2> network.err
code=$?
test "$code" -ne 0 || exit 14
/usr/bin/grep -q 'Operation not permitted\\|Permission denied' network.err || exit 15
printf 'VISIBLE_OK OUTSIDE_DENIED WRITE_OK LOOPBACK_OK NETWORK_DENIED\\n'
'''
        report['active_stage'] = 'os-permissions'
        probe, out, _ = run(prefix + ['/bin/sh', '-c', shell, 'probe', str(root/'sibling-canary.txt'),
                                    'http://127.0.0.1:' + str(server.server_port) + '/health'], root/'fixture', environment)
        probe['actual_result'] = out.strip() == b'VISIBLE_OK OUTSIDE_DENIED WRITE_OK LOOPBACK_OK NETWORK_DENIED' and (root/'fixture'/'written.txt').read_text() == 'synthetic-write'
        report['checks']['os-permissions'] = probe
        if result_errors(probe['exit_code'], probe['actual_result'], probe['timed_out']):
            raise RuntimeError('permission-probe-incomplete')
        report['active_stage'] = 'runtime-version'
        version, out, _ = run(prefix + [str(CLI), '--version'], root/'fixture', environment)
        version['expected_version'] = out.strip() == b'codex-cli 0.156.1'
        report['checks']['runtime-version'] = version
        if version['exit_code'] != 0 or not version['expected_version']:
            raise RuntimeError('sandbox-or-frozen-runtime-unavailable')
        flags = [part for key, value in config.items() for part in ('-c', key + '=' + value)]
        report['active_stage'] = 'preview'
        preview, out, _ = run(prefix + [str(CLI), 'debug', 'prompt-input'] + flags + [PROMPT], root/'fixture', environment)
        try:
            parsed = json.loads(out)
            report['preview_required_keys_present'] = {key: isinstance(parsed, dict) and key in parsed
                                                       for key in ('instructions', 'input', 'tools', 'model', 'reasoning')}
            # Only the actual documented wire shape is admitted. No fallback
            # treating arbitrary stdout or a missing field as a clean context.
            preview_summary = summarize(parsed)
        except (ValueError, UnicodeDecodeError):
            preview_summary = {'errors': ['malformed-preview']}
        report['checks']['preview'] = {**preview, 'summary': preview_summary}
        if preview['exit_code'] != 0 or preview_summary['errors']:
            raise RuntimeError('preview-context-not-proven')
        report['active_stage'] = 'exec-local-sink'
        executed, _, _ = run(prefix + [str(CLI), 'exec', '--ephemeral', '--ignore-user-config', '--ignore-rules',
                                      '--strict-config', '--json', '--skip-git-repo-check', '-C', str(root/'fixture')]
                               + flags + [PROMPT], root/'fixture', environment)
        report['checks']['exec-sink'] = executed
        report['requests'] = received
        if len(received) != 1:
            raise RuntimeError('missing-or-duplicate-exec-request')
        mismatches = compare(preview_summary, received[0])
        if executed['timed_out'] or executed['exit_code'] == 0 or mismatches:
            report['comparison_errors'] = mismatches
            raise RuntimeError('exec-context-not-proven')
        report['result'] = 'offline-preflight-ready'
    except RuntimeError as error:
        report['blockers'].append(str(error))
    except Exception as error:
        # Never include exception text (it can contain payloads or host paths).
        report['blockers'].append('unexpected-error:' + type(error).__name__)
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()
        if thread is not None:
            thread.join(timeout=5)
            report['sink_stopped'] = not thread.is_alive()
        else:
            report['sink_stopped'] = True
            report['sink_not_started'] = True
        if temporary is not None:
            temporary.cleanup()
            report['temporary_root_removed'] = not root.exists()
        report['runtime_hash_unchanged'] = CLI.is_file() and digest(CLI.read_bytes()) == report.get('binary_sha256')
        report['harness_hash_unchanged'] = digest(Path(__file__).read_bytes()) == report['harness_sha256']
        report['no_raw_context_persisted'] = True
        if not report.get('temporary_root_removed') or not report.get('sink_stopped'):
            report['result'] = 'blocked'
            report['blockers'].append('cleanup-incomplete')
        if not report['runtime_hash_unchanged'] or not report['harness_hash_unchanged']:
            report['result'] = 'blocked'
            report['blockers'].append('frozen-source-changed')
        (output/'summary.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'report': str(output/'summary.json'), 'result': report['result'], 'blockers': report['blockers']}))
    return 0 if report['result'] == 'offline-preflight-ready' else 1


if __name__ == '__main__':
    raise SystemExit(main())
