#!/usr/bin/env python3
"""Read-only Linux process/container/mount observer; emits no process arguments."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def observe(raw):
    target = os.path.abspath(raw)
    if sys.platform != 'linux' or not Path('/proc/self/mountinfo').exists():
        return {'complete': False, 'busy': True, 'reason': 'unsupported activity inspector'}
    roots = (target, target.rstrip('/') + '/')
    def touches(raw):
        raw = raw.removesuffix(' (deleted)')
        return raw == roots[0] or raw.startswith(roots[1])
    ancestors = set()
    pid = os.getpid()
    while pid and pid not in ancestors:
        ancestors.add(pid)
        try:
            text = Path(f'/proc/{pid}/stat').read_text()
            pid = int(text[text.rfind(')') + 2:].split()[1])
        except FileNotFoundError:
            break
    try:
        for proc in Path('/proc').iterdir():
            if not proc.name.isdecimal():
                continue
            try:
                if touches(os.readlink(proc / 'cwd')):
                    return {'complete': True, 'busy': True, 'reason': 'process cwd in resource'}
                args = (proc / 'cmdline').read_bytes()
                if int(proc.name) not in ancestors and target.encode() in args:
                    return {'complete': True, 'busy': True, 'reason': 'process references resource'}
                for fd in (proc / 'fd').iterdir():
                    try:
                        if touches(os.readlink(fd)):
                            return {'complete': True, 'busy': True, 'reason': 'open resource descriptor'}
                    except FileNotFoundError:
                        pass
                if any(touches(line.split(None, 5)[-1]) for line in (proc / 'maps').read_text().splitlines()):
                    return {'complete': True, 'busy': True, 'reason': 'mapped resource file'}
                for line in (proc / 'mountinfo').read_text().splitlines():
                    fields = line.split()
                    # Linux mountinfo escapes whitespace/backslashes as octal.
                    for field in fields[3:5]:
                        for code, char in [('040',' '),('011','\t'),('012','\n'),('134','\\')]:
                            field = field.replace('\\' + code, char)
                        if touches(field):
                            return {'complete': True, 'busy': True, 'reason': 'mount references resource'}
            except (FileNotFoundError, ProcessLookupError):
                continue
        docker = shutil.which('docker')
        if docker and Path('/var/run/docker.sock').exists():
            run = subprocess.run([docker, '--host', 'unix:///var/run/docker.sock', 'ps', '-q'], capture_output=True, text=True, timeout=20)
            if run.returncode:
                return {'complete': False, 'busy': True, 'reason': 'container inventory unavailable'}
            ids = run.stdout.split()
            if ids:
                run = subprocess.run([docker, '--host', 'unix:///var/run/docker.sock', 'inspect', *ids], capture_output=True, text=True, timeout=20)
                if run.returncode:
                    return {'complete': False, 'busy': True, 'reason': 'container mounts unavailable'}
                for value in json.loads(run.stdout):
                    for mount in value.get('Mounts', []):
                        source = mount.get('Source', '')
                        if source and (touches(source) or target.startswith(source.rstrip('/') + '/')):
                            return {'complete': True, 'busy': True, 'reason': 'active container mount'}
        elif Path('/var/run/docker.sock').exists():
            return {'complete': False, 'busy': True, 'reason': 'container socket without inspector'}
        return {'complete': True, 'busy': False, 'reason': 'no process, open descriptor or mount found'}
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        return {'complete': False, 'busy': True, 'reason': 'incomplete activity visibility: ' + type(error).__name__}


if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isabs(sys.argv[1]):
        raise SystemExit(2)
    print(json.dumps(observe(sys.argv[1])))
