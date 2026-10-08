import csv
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time

source = Path.cwd()
checks = ['check-required-artifacts', 'check-branch-policy', 'check-naming', 'check-status-consistency', 'check-qa-evidence', 'check-full-qa-verification', 'check-contract-compliance']
cases = [('failure', '#!/usr/bin/env bash\nexit 7\n', 7, 'fail', '60'), ('timeout', '#!/usr/bin/env python3\nimport time\ntime.sleep(2)\n', 124, 'timeout', '0.1'), ('source-drift', '#!/usr/bin/env bash\nprintf changed > probe-drift.txt\n', 1, 'fail', '60'), ('interrupt', '#!/usr/bin/env python3\nimport time\nfrom pathlib import Path\nPath("child-started").touch()\ntime.sleep(2)\n', 143, 'interrupted', '60'), ('success', '#!/usr/bin/env bash\nexit 0\n', 0, 'pass', '60')]
for name, script, expected, verdict, timeout in cases:
    with tempfile.TemporaryDirectory(prefix='lv002-lifecycle-', dir='/tmp') as directory:
        parent = Path(directory)
        repository = parent / 'repo'
        subprocess.run(['git', 'init', '-q', str(repository)], check=True)
        if name == 'interrupt':
            script = script.replace('Path("child-started")', 'Path(' + repr(str(parent / 'child-started')) + ')')
        for relative in ['.systems/scripts/validate-workflow', '.systems/scripts/resolve-workflow-env', '.systems/scripts/run-with-timeout', '.systems/scripts/report-validation-comparison', '.systems/scripts/lib/validation-timing.py']:
            target = repository / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, target)
        for check in checks:
            target = repository / '.systems/scripts' / check
            target.write_text(script if check == 'check-required-artifacts' else '#!/usr/bin/env bash\nexit 0\n')
            target.chmod(0o755)
        output = parent / 'timing.tsv'
        command = ['.systems/scripts/validate-workflow', '--profile', 'fast', '--progress', 'quiet', '--timeout-seconds', timeout, '--timing-output', str(output)]
        if name == 'interrupt':
            process = subprocess.Popen(command, cwd=repository, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
            deadline = time.monotonic() + 10
            while not (parent / 'child-started').exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(0.05)
            assert (parent / 'child-started').exists(), 'validator child did not start before signal'
            os.kill(process.pid, signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=10)
            result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
        else:
            result = subprocess.run(command, cwd=repository, capture_output=True, text=True)
        assert result.returncode == expected, (name, result.returncode, result.stdout, result.stderr)
        markers = [line for line in result.stdout.splitlines() if line.startswith('AI_WORKFLOW_VALIDATE_COMPLETE ')]
        assert len(markers) == 1 and f'result={verdict} ' in markers[0] and f'exit_code={expected} ' in markers[0], (name, markers)
        with output.open() as stream:
            rows = list(csv.DictReader(stream, delimiter='\t'))
        wall = [row for row in rows if row['command/check_id'] == 'validation-wall']
        assert len(wall) == 1 and wall[0]['result'] == verdict, (name, rows)
        print(f'{name}: exit {expected}, one completion marker, timing wall {verdict}')
print('LV002 lifecycle probes: 5 pass')
