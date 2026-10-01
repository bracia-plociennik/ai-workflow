#!/usr/bin/env python3
"""Classify read evidence conservatively. Aggregate shell text is not an execution trace."""
import argparse
import json
import re
import shlex
from pathlib import Path

READERS = {'cat', 'sed', 'head', 'tail', 'nl', 'awk', 'less', 'rg'}
PATH = re.compile(r'(?:[^\s\"\';&|()]+/)?(?:\.systems/ai/[A-Za-z0-9_./-]+\.md|AGENTS\.md|SKILL\.md)')


def classify(item):
    command = item.get('command', '')
    if not isinstance(command, str):
        return []
    try:
        outer = shlex.split(command)
        script = outer[-1] if len(outer) >= 3 and Path(outer[0]).name in {'bash', 'zsh', 'sh'} and outer[1] in {'-c', '-lc'} else command
        lexer = shlex.shlex(script, posix=True, punctuation_chars=';&|()<>')
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return [{'path': p, 'state': 'unknown', 'reason': 'unparseable-shell'} for p in PATH.findall(command)]
    paths = list(dict.fromkeys(PATH.findall(script)))
    if not paths:
        return []
    completed = item.get('type') == 'command_execution' and item.get('status') == 'completed' and type(item.get('exit_code')) is int
    complex_shell = any(t in {';', '&&', '||', '|', '&', '(', ')', '>', '>>', '<', '<<'} for t in tokens) or '\n' in script or any(t in {'if', 'for', 'while', 'case', 'eval', 'source'} for t in tokens)
    # The literal false builtin has a deterministic short-circuit boundary.
    if completed and item['exit_code'] == 1 and tokens[:2] == ['false', '&&'] and not any(t in {';', '||', '|', '&', '\n'} for t in tokens[2:]):
        return [{'path': p, 'state': 'not-executed', 'reason': 'literal-false-short-circuit'} for p in paths]
    reader = tokens and Path(tokens[0]).name in READERS and not (Path(tokens[0]).name == 'rg' and '--files' in tokens)
    literal = all(not any(c in t for c in '$`*?{}') for t in tokens) and not any(t in {'--help', '--version'} for t in tokens)
    if reader and not complex_shell and literal:
        arguments = [t for t in tokens[1:] if not t.startswith('-')]
        if Path(tokens[0]).name in {'sed', 'awk', 'rg'}:
            # Expression/pattern tokens are not input files. Complex option forms
            # remain unknown rather than treating a script name as read evidence.
            if any(t in {'-e', '-f', '--file', '--regexp'} or t.startswith(('-e', '-f', '--regexp=', '--file=')) for t in tokens[1:]):
                literal = False
            else:
                arguments = arguments[1:]
        paths = [p for p in paths if p in arguments]
    state = 'unknown' if complex_shell or not reader or not literal else 'confirmed' if completed and item['exit_code'] == 0 else 'attempted'
    return [{'path': p, 'state': state, 'reason': 'completed-simple-reader' if state == 'confirmed' else 'aggregate-or-incomplete-trace'} for p in paths]


def summarize(events):
    rows = []
    for event in events:
        if event.get('type') in {'item.completed', 'item.started'}:
            item = dict(event.get('item', {}))
            if event['type'] != 'item.completed':
                item['status'] = 'in_progress'
            for row in classify(item):
                rows.append({**row, 'event_type': event['type']})
    # Retain separate attempts: a later failed command does not erase an earlier read.
    return {'schema_version': 1, 'reads': rows, 'confirmed_paths': sorted({r['path'] for r in rows if r['state'] == 'confirmed'}),
            'limits': 'Compound/pipeline/branch commands remain unknown without per-command trace; no historic eval is rewritten.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('trace', type=Path)
    a = p.parse_args()
    events = [json.loads(line) for line in a.trace.read_text().splitlines() if line.strip()]
    print(json.dumps(summarize(events), sort_keys=True))


if __name__ == '__main__':
    main()
