import argparse
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

root = Path.cwd()
tool = root / '.systems/scripts/report-validation-comparison'
loader = importlib.machinery.SourceFileLoader('comparison', str(tool))
module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(module)
source = module.source_digest()
with tempfile.TemporaryDirectory(dir='/tmp', prefix='lv002-comparison-probe-') as raw:
    base = Path(raw)
    manifests = []
    for index, duration in enumerate((100, 101, 102, 80, 81, 82), 1):
        timing = base / f'run-{index}.tsv'
        run = f'{source}-probe-{index}'
        timing.write_text(module.timing.HEADER + ''.join(
            '\t'.join((check, group, str(seconds), 'pass', profile, '2', run, kind, parent)) + '\n'
            for check, group, seconds, profile, kind, parent in (
                ('check-validator-smoke-tests', 'smoke', 7, 'full', 'child', 'validation-wall'),
                ('one-smoke', 'core', 3, 'smoke-all', 'child', 'smoke-suite-wall'),
                ('smoke-suite-wall', 'smoke', 6, 'smoke-all', 'wall', 'validation-wall'),
                ('validation-wall', 'wall', duration, 'full', 'wall', 'none'),
            )))
        manifest = base / f'run-{index}.json'
        module.capture(argparse.Namespace(timing=str(timing), output=str(manifest), scope_fingerprint='synthetic', input_fingerprint='synthetic', setup_regime='ordinary'))
        manifests.append(str(manifest))
    command = [str(tool), 'compare', '--baseline', *manifests[:3], '--candidate', *manifests[3:]]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    assert json.loads(result.stdout)['result'] == 'qualified-improvement'
    print('separated synthetic ranges qualify with limitations: pass')
    result = subprocess.run([str(tool), 'compare', '--baseline', *manifests[:3], '--candidate', *manifests[:3]], capture_output=True, text=True)
    assert result.returncode == 2 and 'reuse a run ID' in result.stderr
    print('baseline/candidate run reuse rejected: pass')
    result = subprocess.run([str(tool), 'summarize', *manifests[:2]], capture_output=True, text=True)
    assert result.returncode == 2 and 'at least three runs' in result.stderr
    print('fewer than three baseline runs rejected: pass')
print('LV002 comparison probes: 3 pass; synthetic only, no real speed claim')
