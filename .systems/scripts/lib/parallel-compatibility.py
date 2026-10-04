#!/usr/bin/env python3
"""Inspect a closed counterpart envelope; never dispatch or publish transitions."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import unicodedata

sys.dont_write_bytecode = True


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p, coordinator = load('parallel-orchestration'), load('coordinator-status')
RUN = {'contract', 'run_id', 'coordinator_id', 'approval_ref', 'baseline', 'source_manifest',
       'retired_attempt_ids', 'retired_agent_ids', 'runtime_capacity', 'dispatch_count',
       'checkpoint_open', 'workflow_parallel_supported', 'units'}
UNIT = {'id', 'goal', 'dod', 'dependencies', 'mode', 'system', 'write_paths', 'resources',
        'worktree', 'status', 'attempt_id', 'agent_id', 'termination_confirmed', 'result'}
MAPPING = {'schema', 'peer_contract', 'workflow_protocol', 'run_id', 'coordinator_id',
           'project', 'unit_mapping', 'capacity'}
DISPOSITIONS = {'pending': 'planned', 'ready': 'ready-for-local-review', 'running': 'running-observed',
                'submitted': 'submitted-unaccepted', 'accepted': 'accepted-needs-local-receipt',
                'failed': 'rejected-needs-reconciliation', 'blocked': 'blocked',
                'cancel-requested': 'cancellation-reserved', 'cancelled': 'cancelled-observed'}
FORBIDDEN = {'.git', 'ai-workflow', 'ai-workflow-workspace', 'capture-state', 'credentials',
             'secrets', 'private', 'raw', 'dump', '.ssh', '.aws', '.codex', 'private-key'}


def require(condition):
    if not condition:
        raise ValueError('invalid compatibility input')


def fields(value, keys):
    require(type(value) is dict and set(value) == keys)


def number(value, minimum=1):
    require(type(value) is int and minimum <= value <= 10000)


def ids(values):
    require(type(values) is list and len(values) <= 1000)
    for value in values:
        p.identity(value, 'identity')
    require(len(set(values)) == len(values))


def boolean(value):
    require(type(value) is bool)


def safe_path(root, relative):
    p.relative(relative)
    require(not any(unicodedata.normalize('NFC', part).casefold() in FORBIDDEN
                    or part.casefold().startswith(('.env', 'id_rsa', 'id_ed25519', 'id_ecdsa'))
                    or part.casefold().endswith(('.pem', '.key', '.p12', '.pfx'))
                    for part in relative.split('/')))
    return p.canonical(root, relative)


def paths_unique(paths):
    require(type(paths) is list and len(paths) <= 1000 and all(type(path) is str for path in paths))
    require(len(paths) == len({unicodedata.normalize('NFC', path).casefold() for path in paths}))


def signature(path):
    path = p.physical_path(path)
    info = path.stat()
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_nlink)


def read_file(path, limit=1048576, observations=None):
    path = p.physical_path(path)
    raw = coordinator.bounded_bytes(path.parent, path.name, limit)
    if observations is not None:
        stamp = signature(path)
        require(path not in observations or observations[path] == stamp)
        observations[path] = stamp
    return raw, (hashlib.sha256(raw).hexdigest(), stat.S_IMODE(path.stat().st_mode))


def read_json(path, observations=None):
    raw, fingerprint = read_file(path, observations=observations)
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value)
            value[key] = item
        return value
    def invalid_constant(_):
        raise ValueError('nonfinite JSON')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant), fingerprint


def head(root):
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
    # Explicit root/HEAD queries only; no counterpart commands or shell evaluation.
    top = subprocess.check_output(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                                  env=env, stderr=subprocess.DEVNULL, timeout=10).decode().strip()
    require(Path(top).resolve() == root)
    value = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                                    env=env, stderr=subprocess.DEVNULL, timeout=10).decode().strip()
    require(re.fullmatch('[0-9a-f]{40}', value) is not None)
    return value


def manifest(entries, root, observed_paths=None):
    require(type(entries) is list and 0 < len(entries) <= 1000)
    seen, observations, total = set(), {}, 0
    for entry in entries:
        fields(entry, {'path', 'sha256'})
        path = safe_path(root, entry['path'])
        alias = unicodedata.normalize('NFC', entry['path']).casefold()
        require(alias not in seen)
        seen.add(alias)
        raw, observed = read_file(path, observations=observed_paths)
        total += len(raw)
        require(total <= 16 * 1024 * 1024 and observed[0] == entry['sha256'])
        observations[entry['path']] = observed
    digest = hashlib.sha256(''.join(sorted(e['path'] + '=' + e['sha256'] + '\n' for e in entries)).encode()).hexdigest()
    return digest, observations


def inspect(workflow, repo, run_path, mapping_path):
    workflow, repo = (p.physical_path(path).resolve(strict=True) for path in (workflow, repo))
    initial_head = head(repo)
    observed_paths = {}
    run, run_hash = read_json(run_path, observed_paths)
    mapping, mapping_hash = read_json(mapping_path, observed_paths)
    fields(run, RUN)
    fields(mapping, MAPPING)
    for value in (run['contract'], mapping['schema'], mapping['peer_contract'], mapping['workflow_protocol']):
        require(type(value) is int and value == 1)
    for key in ('run_id', 'coordinator_id'):
        p.identity(run[key], key)
        require(run[key] == mapping[key])
    p.identity(mapping['project'], 'project')
    p.text(run['approval_ref'], 'approval reference')
    fields(run['baseline'], {'commit', 'source_digest'})
    require(run['baseline']['commit'] == initial_head)
    digest, sources = manifest(run['source_manifest'], repo, observed_paths)
    require(digest == run['baseline']['source_digest'])
    for key in ('runtime_capacity', 'dispatch_count'):
        number(run[key])
    require(run['dispatch_count'] <= run['runtime_capacity'])
    for key in ('checkpoint_open', 'workflow_parallel_supported'):
        boolean(run[key])
    # Peer asserted support cannot negotiate an unverified operational backend.
    require(run['workflow_parallel_supported'] is False)
    for key in ('retired_attempt_ids', 'retired_agent_ids'):
        ids(run[key])
    require(type(run['units']) is list and 0 < len(run['units']) <= 100)
    require(type(mapping['unit_mapping']) is list and len(mapping['unit_mapping']) == len(run['units']))
    by_id, maps, agents, attempts, result_observations = {}, {}, set(), set(), []
    for entry in mapping['unit_mapping']:
        fields(entry, {'unit_id', 'task_id', 'slice_id', 'read_paths'})
        for key in ('unit_id', 'task_id', 'slice_id'):
            p.identity(entry[key], key)
        require(entry['unit_id'] not in maps)
        ids_paths = entry['read_paths']
        paths_unique(ids_paths)
        for path in ids_paths:
            safe_path(repo, path)
            require(path in sources)
        maps[entry['unit_id']] = entry
    for unit in run['units']:
        fields(unit, UNIT)
        p.identity(unit['id'], 'unit')
        require(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', unit['id']) is not None)
        require(unit['id'] not in by_id and unit['id'] in maps)
        by_id[unit['id']] = unit
        for key in ('goal', 'dod'):
            p.text(unit[key], key)
        ids(unit['dependencies'])
        ids(unit['resources'])
        require(unit['mode'] in {'read-only', 'implementation'} and unit['system'] in {'ai-system', 'ai-workflow'})
        require(unit['status'] in DISPOSITIONS)
        boolean(unit['termination_confirmed'])
        paths = unit['write_paths']
        paths_unique(paths)
        for path in paths:
            safe_path(repo, path)
        if unit['mode'] == 'read-only':
            require(not paths and unit['worktree'] is None)
        else:
            require(paths and type(unit['worktree']) is str and Path(unit['worktree']).is_absolute())
            p.physical_path(unit['worktree'])
        for key, seen, retired in (('agent_id', agents, run['retired_agent_ids']), ('attempt_id', attempts, run['retired_attempt_ids'])):
            value = unit[key]
            if value is not None:
                p.identity(value, key)
                require(value not in seen and value not in retired)
                seen.add(value)
        state = unit['status']
        if state in {'pending', 'ready', 'blocked'}:
            require(unit['agent_id'] is None and unit['attempt_id'] is None and unit['result'] is None
                    and not unit['termination_confirmed'])
        else:
            require(unit['agent_id'] is not None and unit['attempt_id'] is not None)
        if state in {'running', 'cancel-requested'}:
            require(not unit['termination_confirmed'])
        if state == 'cancelled':
            require(unit['termination_confirmed'])
        result = unit['result']
        if state in {'submitted', 'accepted'} or result is not None:
            require(state in {'submitted', 'accepted', 'failed', 'cancel-requested', 'cancelled'})
            keys = {'baseline', 'attempt_id', 'evidence', 'test_summary', 'findings'}
            if state == 'accepted' or type(result) is dict and 'verified_by' in result:
                keys |= {'verified_by', 'verified_checks'}
            fields(result, keys)
            require(result['attempt_id'] == unit['attempt_id'] and result['baseline'] == run['baseline'])
            p.text(result['test_summary'], 'test summary')
            require(type(result['findings']) is list and all(type(item) is str for item in result['findings']))
            result_observations.append((result['evidence'], manifest(result['evidence'], repo, observed_paths)))
            if state == 'accepted':
                require(result['verified_by'] == run['coordinator_id'] and not result['findings'])
                ids(result['verified_checks'])
                require(set(result['verified_checks']) >= {'intent', 'diff', 'tests', 'privacy'})
        else:
            require(result is None)
    visiting, visited = set(), set()
    def visit(key):
        require(key not in visiting)
        if key in visited:
            return
        visiting.add(key)
        unit = by_id[key]
        require(set(unit['dependencies']) <= set(by_id))
        for dependency in unit['dependencies']:
            visit(dependency)
        if unit['status'] in {'running', 'submitted', 'accepted', 'cancel-requested'}:
            require(all(by_id[d]['status'] == 'accepted' for d in unit['dependencies']))
        visiting.remove(key)
        visited.add(key)
    for key in by_id:
        visit(key)
    capacity = mapping['capacity']
    fields(capacity, {'known', 'complete', 'total', 'actors'})
    require(capacity['known'] is True and capacity['complete'] is True)
    number(capacity['total'])
    require(capacity['total'] == run['runtime_capacity'])
    require(type(capacity['actors']) is list and len(capacity['actors']) <= 1000)
    observed, live = set(), 0
    for actor in capacity['actors']:
        fields(actor, {'agent_id', 'role', 'system', 'unit_id', 'termination_confirmed'})
        p.identity(actor['agent_id'], 'actor')
        require(actor['agent_id'] not in observed and actor['agent_id'] not in run['retired_agent_ids'])
        observed.add(actor['agent_id'])
        require(actor['role'] in {'worker', 'reviewer'} and actor['system'] in {'ai-system', 'ai-workflow'})
        boolean(actor['termination_confirmed'])
        if actor['unit_id'] is not None:
            require(actor['role'] == 'worker' and actor['unit_id'] in by_id)
            unit = by_id[actor['unit_id']]
            require(actor['agent_id'] == unit['agent_id'] and actor['system'] == unit['system']
                    and actor['termination_confirmed'] == unit['termination_confirmed'])
        else:
            require(actor['agent_id'] not in agents)
        live += not actor['termination_confirmed']
    require(agents <= observed and live <= capacity['total'])
    active = [u for u in run['units'] if u['agent_id'] and not u['termination_confirmed']]
    require(not any(u['system'] == 'ai-workflow' for u in active) or len(active) == 1)
    def local(u):
        return {'read_set': maps[u['id']]['read_paths'], 'write_set': u['write_paths'],
                'resources': [{'name': name, 'mode': 'exclusive'} for name in u['resources']]}
    for index, unit in enumerate(active):
        for other in active[index+1:]:
            require(not p.conflicts(local(unit), local(other), repo))
            if unit['mode'] == other['mode'] == 'implementation':
                require(not p.overlap(Path(unit['worktree']), Path(other['worktree'])))
    capability = coordinator.parallel_capability(workflow)
    require(capability['state'] == 'installed')
    require(head(repo) == initial_head and manifest(run['source_manifest'], repo, observed_paths) == (digest, sources))
    for entries, observation in result_observations:
        require(manifest(entries, repo, observed_paths) == observation)
    require(read_file(run_path, observations=observed_paths)[1] == run_hash
            and read_file(mapping_path, observations=observed_paths)[1] == mapping_hash)
    # Closing content reads and Git queries are followed by a whole-input sweep.
    require(all(signature(path) == stamp for path, stamp in observed_paths.items()))
    require(head(repo) == initial_head)
    require(all(signature(path) == stamp for path, stamp in observed_paths.items()))
    return {'schema': 1, 'result': 'compatible-inspection', 'execution_authorized': False,
            'operational_support': False, 'capacity_evidence': 'caller-supplied-not-native-proof',
            'occupied': live, 'free_observed': capacity['total'] - live,
            'source_digest_kind': 'declared-sorted-path-sha256-newline', 'source_digest': digest,
            'capability_state': capability['state'],
            'units': [{'unit_id': u['id'], 'task_id': maps[u['id']]['task_id'], 'slice_id': maps[u['id']]['slice_id'],
                       'disposition': DISPOSITIONS[u['status']]} for u in run['units']],
            'required_local_actions': ['approval-and-phase-gates', 'current-local-evidence-receipt',
                                       'cross-task-quality-capture-checkpoint'],
            'unsupported': ['native-dispatch', 'git-worktree-executor', 'logical-rebase']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('workflow', 'repo', 'run', 'mapping'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.workflow, args.repo, args.run, args.mapping), sort_keys=True))
        return 0
    except (ValueError, OSError, UnicodeError, TypeError, KeyError, RecursionError, subprocess.SubprocessError):
        print(json.dumps({'schema': 1, 'result': 'blocked', 'reason': 'invalid-or-unsupported-compatibility-input',
                          'execution_authorized': False, 'operational_support': False}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
