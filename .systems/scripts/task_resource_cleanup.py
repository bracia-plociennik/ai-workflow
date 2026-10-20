#!/usr/bin/env python3
"""Conservative task resource lifecycle. No field is authority or a QA verdict."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid

import durable_runtime as runtime

RETENTION = 7 * 24 * 3600
HERE = Path(__file__).resolve().parent
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0')).decode().strip()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def instant(value):
    result = datetime.fromisoformat(value)
    if result.utcoffset() is None:
        raise ValueError('release time must include timezone')
    return result.timestamp()


def save(path, value):
    path = runtime.unlinked(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.resource-record-', delete=False) as out:
        temp = Path(out.name)
        try:
            os.chmod(temp, 0o600)
            out.write((json.dumps(value, sort_keys=True, indent=2) + '\n').encode())
            out.flush()
            os.fsync(out.fileno())
            os.replace(temp, path)
            fd = os.open(path.parent, os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        finally:
            temp.unlink(missing_ok=True)


def load(record):
    record = runtime.unlinked(record)
    value = runtime.read_json(record)
    policy = value.get('task_resource_cleanup')
    if policy is None:
        return value, None
    expected = {'schema', 'enabled', 'work_id', 'canonical', 'workspace', 'collection', 'resources', 'receipts'}
    if not isinstance(policy, dict) or set(policy) != expected or type(policy['schema']) is not int or policy['schema'] != 1:
        raise ValueError('unsupported task resource record')
    if not SLUG.fullmatch(policy['work_id']) or type(policy['enabled']) is not bool:
        raise ValueError('invalid task resource identity/policy')
    if policy['canonical'] != runtime.identity(policy['canonical']['root']):
        raise ValueError('canonical repository identity changed')
    workspace = runtime.durable(policy['workspace'])
    collection = runtime.durable(policy['collection'])
    if not record.is_relative_to(workspace) or workspace.is_relative_to(collection / '.tmp'):
        raise ValueError('work record is outside persistent runtime')
    resources = policy['resources']
    if not isinstance(resources, list) or not isinstance(policy['receipts'], list):
        raise ValueError('invalid task resource inventory')
    if len({r['id'] for r in resources}) != len(resources):
        raise ValueError('duplicate resource identity')
    return value, policy


@contextmanager
def lock(policy):
    # Same lock is used for register, claim/resume, release and apply across records.
    root = Path(policy['canonical']['git_common'])
    path = runtime.unlinked(root / 'task-resource-cleanup.lock', exists=False)
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(fd)


def inventory(path):
    """Full content/type/mode closure, including ignored files. Never follow links."""
    path = runtime.unlinked(path)
    device = path.stat().st_dev
    found = {}
    for root, dirs, files in os.walk(path, followlinks=False):
        for name in sorted(dirs + files):
            item = Path(root) / name
            info = item.lstat()
            if info.st_dev != device or item.is_symlink() or os.path.ismount(item):
                raise ValueError('linked or mounted resource content')
            rel = item.relative_to(path).as_posix()
            if stat.S_ISDIR(info.st_mode):
                found[rel] = ['dir', stat.S_IMODE(info.st_mode)]
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                found[rel] = ['file', stat.S_IMODE(info.st_mode), info.st_size, digest(item)]
            else:
                raise ValueError('special or hardlinked resource content')
    return found


def sensitive(items):
    for name in items:
        parts = set(Path(name).parts)
        if ('.git' in parts or any(p == '.env' or p.startswith('.env.') for p in parts)
                or any(p.lower() in {'secrets', 'credentials', 'id_rsa', 'id_ed25519'} for p in parts)
                or any(p.lower() in {'quality', 'capture-state', 'checkpoints'} for p in parts)
                or name.lower().endswith(('.md', '.pem', '.key', '.sqlite', '.db'))
                or re.search(r'(^|[/_.-])(qa|quality|capture|checkpoint|evidence|report)([/_.-]|$)', name.lower())):
            raise ValueError('resource contains source, secrets, data or durable evidence')


def locate(policy, resource, exists=True):
    path = runtime.unlinked(resource['path'], exists=exists)
    if not Path(policy['collection']).is_dir():
        raise ValueError('approved collection disappeared')
    root = Path(policy['collection'])
    if path == Path(policy['canonical']['root']):
        raise ValueError('canonical repository cannot be disposable')
    if resource['kind'] == 'scratch':
        allowed = root / '.tmp' / policy['work_id']
        if not path.is_relative_to(allowed) or path == allowed.parent:
            raise ValueError('scratch is outside owning task .tmp namespace')
    elif resource['kind'] in {'cache', 'worktree'}:
        trees = root / '.worktrees'
        if not path.is_relative_to(trees) or path == trees:
            raise ValueError('resource is outside auxiliary worktree collection')
    else:
        raise ValueError('unknown resource kind')
    if path.exists():
        if not path.is_dir() or os.path.ismount(path):
            raise ValueError('resource must be an unmounted directory')
        actual = [path.stat().st_dev, path.stat().st_ino]
        if resource.get('identity') is not None and actual != resource['identity']:
            raise ValueError('resource directory identity changed')
    if resource['kind'] == 'cache' and tuple(path.parts[-2:]) != ('.next', 'cache'):
        raise ValueError('only .next/cache profile is supported')
    if resource['kind'] != 'scratch' and path.exists():
        repo = Path(git(path, 'rev-parse', '--show-toplevel'))
        if repo == Path(policy['canonical']['root']) or not repo.is_relative_to(root / '.worktrees'):
            raise ValueError('cache/worktree is not an auxiliary repository')
        if runtime.identity(repo)['git_common'] != policy['canonical']['git_common']:
            raise ValueError('resource belongs to another repository')
        for block in git(repo, 'worktree', 'list', '--porcelain').split('\n\n'):
            if block.startswith('worktree ' + str(repo) + '\n') and any(line == 'locked' or line.startswith('locked ') for line in block.splitlines()):
                raise ValueError('Git worktree is explicitly locked')
        if resource['kind'] == 'worktree' and repo != path:
            raise ValueError('whole worktree requires exact root')
    return path


def read_proof(policy, resource):
    proof = resource.get('closure')
    if not proof:
        raise ValueError('reviewed task closure is missing')
    file = runtime.unlinked(proof['path'])
    if not file.is_relative_to(Path(policy['workspace'])) or digest(file) != proof['sha256']:
        raise ValueError('closure evidence changed or is outside owning runtime')
    value = runtime.read_json(file)
    expected = {'schema', 'kind', 'work_id', 'reviewed_by', 'state', 'workers', 'claims',
                'reports', 'dependencies', 'source_roots', 'commit', 'ref', 'push_required', 'remote', 'remote_ref'}
    if (set(value) != expected or type(value['schema']) is not int or value['schema'] != 1 or value['kind'] != 'reviewed-task-closure-v1'
            or value['work_id'] != policy['work_id'] or value['state'] != 'complete'
            or not isinstance(value['reviewed_by'], str) or not value['reviewed_by'].strip()):
        raise ValueError('invalid reviewed task closure')
    if not isinstance(value['workers'], list) or any(w.get('state') != 'terminated' or not w.get('evidence') for w in value['workers']):
        raise ValueError('worker termination is not confirmed')
    if not isinstance(value['claims'], list) or any(c.get('state') != 'released' or not c.get('evidence') for c in value['claims']):
        raise ValueError('resource claims remain active or unknown')
    if not isinstance(value['source_roots'], list) or not value['source_roots']:
        raise ValueError('current source dependency closure is missing')
    target = Path(resource['path'])
    for raw in value['source_roots']:
        source = runtime.unlinked(raw)
        if source == target or source.is_relative_to(target) or target.is_relative_to(source):
            raise ValueError('current QA still requires this execution environment')
    if not value['reports'] or type(value['push_required']) is not bool:
        raise ValueError('current QA/Capture reports or publication requirement missing')
    for is_report, entries in ((True, value['reports']), (False, value['dependencies'])):
        if not isinstance(entries, list):
            raise ValueError('invalid evidence collection')
        for entry in entries:
            allowed = {'path', 'sha256'}
            if not isinstance(entry, dict) or set(entry) not in (allowed, allowed | {'role'}):
                raise ValueError('unknown evidence reference fields')
            role = entry.get('role', 'required')
            if role not in {'required', 'archive'} or (is_report and role != 'required'):
                raise ValueError('archival data cannot supply current QA/Capture')
            path = runtime.unlinked(entry['path'])
            if runtime.temporary(path) or not path.is_relative_to(Path(policy['workspace'])):
                raise ValueError('evidence is not in durable owning runtime')
            if digest(path) != entry['sha256']:
                raise ValueError('required QA/Capture dependency changed')
            # Historical run provenance can name its old location without requiring it live.
            # Current reports and complete source_roots remain independently mandatory.
            if role != 'archive' and str(target).encode() in path.read_bytes():
                raise ValueError('current report still references the disposable source')
    repo = Path(policy['canonical']['root'])
    if not re.fullmatch(r'[0-9a-f]{40}', value['commit']) or not value['ref'].startswith('refs/'):
        raise ValueError('invalid preserved source reference')
    git(repo, 'check-ref-format', value['ref'])
    git(repo, 'cat-file', '-e', value['commit'] + '^{commit}')
    subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', value['commit'], value['ref']], check=True, capture_output=True)
    if value['push_required']:
        if value['remote'] not in git(repo, 'remote').splitlines() or not value['remote_ref'].startswith('refs/'):
            raise ValueError('publication reference is unknown')
        actual = git(repo, 'ls-remote', '--exit-code', value['remote'], value['remote_ref']).split()
        if len(actual) != 2 or actual[1] != value['remote_ref'] or not re.fullmatch(r'[0-9a-f]{40}', actual[0]):
            raise ValueError('required pushed result not confirmed')
        if actual[0] != value['commit']:
            # A later remote commit is fine only with independently verifiable local ancestry.
            # No fetch or tracking-ref mutation is performed by inspect/plan.
            git(repo, 'cat-file', '-e', actual[0] + '^{commit}')
            subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', value['commit'], actual[0]], check=True, capture_output=True)
    return value


def observe(path):
    helper = HERE / 'lib/task-resource-activity.py'
    command = [sys.executable, '-I', str(helper), str(path)]
    # Only the small read-only observer is elevated; never the deletion engine.
    if os.geteuid() != 0:
        command = ['sudo', '-n', *command]
    try:
        value = json.loads(subprocess.check_output(command, stderr=subprocess.PIPE, timeout=50))
        if set(value) != {'complete', 'busy', 'reason'} or type(value['complete']) is not bool or type(value['busy']) is not bool:
            raise ValueError('invalid activity observation')
        return value
    except (OSError, ValueError, subprocess.SubprocessError):
        return {'complete': False, 'busy': True, 'reason': 'complete read-only activity inspector unavailable'}


def eligible(policy, resource, *, now=None):
    try:
        disabled = runtime.unlinked(Path(policy['canonical']['git_common']) / 'task-resource-cleanup.disabled', exists=False)
        if disabled.exists() or not policy['enabled']:
            raise ValueError('cleanup disabled')
        if resource['state'] != 'released':
            raise ValueError('resource is active, kept, deleted or requires recovery')
        if resource.get('keep'):
            raise ValueError('resource is explicitly kept')
        path = locate(policy, resource)
        if HERE.is_relative_to(path):
            raise ValueError('cleanup executor itself resides in this environment; use canonical installed Workflow')
        for other in policy['resources']:
            if other['id'] == resource['id']:
                continue
            otherpath = Path(other['path'])
            overlap = path == otherpath or path.is_relative_to(otherpath) or otherpath.is_relative_to(path)
            if overlap and (other.get('keep') or other['state'] not in {'released', 'deleted'}):
                raise ValueError('overlapping resource is active, kept or uncertain')
        proof = read_proof(policy, resource)
        if resource['kind'] == 'worktree':
            if (datetime.now(timezone.utc).timestamp() if now is None else now) - instant(resource['released_at']) < RETENTION:
                raise ValueError('seven-day retention has not elapsed')
            # No force removal, no unknown ignored or untracked files, no submodules.
            if subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain=v1', '--untracked-files=all', '--ignored=matching', '-z'], env=dict(os.environ, GIT_OPTIONAL_LOCKS='0')):
                raise ValueError('worktree has modified/untracked/ignored contents')
            if git(path, 'ls-files', '--stage').find('160000 ') >= 0:
                raise ValueError('worktree contains submodules')
            if git(path, 'rev-parse', 'HEAD') != proof['commit']:
                raise ValueError('worktree result differs from preserved canonical result')
            inventory(path)  # lstat full closure catches untracked races/links/mounts.
        else:
            actual = inventory(path)
            sensitive(actual)
            if resource['kind'] == 'scratch' and actual != resource['manifest']:
                raise ValueError('generated scratch contents changed')
            if resource['kind'] == 'cache':
                repo = Path(git(path, 'rev-parse', '--show-toplevel'))
                if git(repo, 'ls-files', '--', path.relative_to(repo).as_posix()):
                    raise ValueError('cache contains tracked input')
        activity_root = path
        if resource['kind'] == 'cache':
            activity_root = Path(git(path, 'rev-parse', '--show-toplevel'))
        activity = observe(activity_root)
        if not activity['complete'] or activity['busy']:
            raise ValueError(activity['reason'])
        return {'id': resource['id'], 'eligible': True, 'path': str(path), 'reason': 'closed, preserved, unused and in scope'}
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        return {'id': resource.get('id'), 'eligible': False, 'reason': str(exc)}


def init_record(record, canonical, workspace, collection):
    # Record must already exist; preserve all unrelated owning work fields.
    value = runtime.read_json(record)
    if not isinstance(value, dict) or not isinstance(value.get('work_id'), str) or not SLUG.fullmatch(value['work_id']):
        raise ValueError('existing owning work record with stable work_id is required')
    canonical, workspace, collection = runtime.unlinked(canonical), runtime.durable(workspace), runtime.durable(collection)
    if not runtime.unlinked(record).is_relative_to(workspace) or runtime.temporary(canonical):
        raise ValueError('owning record/canonical source is not durable')
    policy = {'schema': 1, 'enabled': True, 'work_id': value['work_id'], 'canonical': runtime.identity(canonical),
              'workspace': str(workspace), 'collection': str(collection), 'resources': [], 'receipts': []}
    if 'task_resource_cleanup' in value:
        _, existing = load(record)
        if any(existing[k] != policy[k] for k in ('work_id', 'canonical', 'workspace', 'collection')):
            raise ValueError('conflicting existing resource policy')
        return
    with lock(policy):
        # Re-read under lock so competing activation cannot overwrite a resource.
        value = runtime.read_json(record)
        if 'task_resource_cleanup' in value:
            raise ValueError('resource policy initialized concurrently; inspect before retry')
        value['task_resource_cleanup'] = policy
        save(record, value)


def mutate(record, action, args):
    _, policy = load(record)
    if policy is None:
        raise ValueError('legacy work record is inspect-only until explicit activation')
    with lock(policy):
        value, policy = load(record)
        if action == 'bind-runtime':
            return runtime.bind(args.target, policy['canonical']['root'], policy['workspace'], record)
        if action in {'enable', 'disable'}:
            policy['enabled'] = action == 'enable'
            disabled = runtime.unlinked(Path(policy['canonical']['git_common']) / 'task-resource-cleanup.disabled', exists=False)
            if action == 'disable':
                disabled.touch(mode=0o600, exist_ok=True)
            else:
                disabled.unlink(missing_ok=True)
        elif action == 'register':
            if not SLUG.fullmatch(args.id):
                raise ValueError('invalid resource id')
            if any(r['id'] == args.id for r in policy['resources']):
                raise ValueError('resource id already registered; never reset retention')
            resource = {'id': args.id, 'kind': args.kind, 'path': str(runtime.unlinked(args.path)),
                        'state': 'active', 'keep': False, 'released_at': None, 'closure': None, 'identity': None, 'manifest': None}
            path = locate(policy, resource)
            for other in policy['resources']:
                otherpath = Path(other['path'])
                if path == otherpath:
                    raise ValueError('resource path already registered')
            if args.kind != 'worktree':
                resource['manifest'] = inventory(path)
                sensitive(resource['manifest'])
            resource['identity'] = [path.stat().st_dev, path.stat().st_ino]
            # Ownership pointers contain no lifecycle state; the existing work record stays authoritative.
            owners = Path(policy['canonical']['git_common']) / 'task-resource-owners'
            runtime.unlinked(owners, exists=False)
            owners.mkdir(exist_ok=True, mode=0o700)
            for marker in owners.glob('*.json'):
                prior = runtime.read_json(marker)
                priorpath = Path(prior['path'])
                overlap = path == priorpath or path.is_relative_to(priorpath) or priorpath.is_relative_to(path)
                if overlap and prior['record'] != str(runtime.unlinked(record)):
                    raise ValueError('resource overlaps another owning work record')
            marker = owners / (hashlib.sha256(str(path).encode()).hexdigest() + '.json')
            pointer = {'path': str(path), 'record': str(runtime.unlinked(record)), 'id': args.id}
            if marker.exists() and runtime.read_json(marker) != pointer:
                raise ValueError('resource ownership is ambiguous')
            if not marker.exists():
                with marker.open('x') as out:
                    json.dump(pointer, out, sort_keys=True)
            policy['resources'].append(resource)
        else:
            resource = next((r for r in policy['resources'] if r['id'] == args.id), None)
            if not resource:
                raise ValueError('unknown resource identity')
            if action in {'claim', 'resume'}:
                if resource['state'] in {'deleted', 'deleting'}:
                    raise ValueError('deleted/uncertain resource cannot be reclaimed')
                locate(policy, resource)
                resource.update(state='active', keep=False, released_at=None, closure=None)
            elif action == 'keep':
                if resource['state'] in {'deleted', 'deleting'}:
                    raise ValueError('deleted/uncertain resource cannot be kept')
                resource['keep'] = True
                resource['state'] = 'kept'
            elif action == 'release':
                if resource['state'] == 'released':
                    return {'status': 'already-released', 'released_at': resource['released_at']}
                if resource['state'] != 'active':
                    raise ValueError('only an active resource can be safely released')
                resource['closure'] = {'path': str(runtime.unlinked(args.closure)), 'sha256': digest(args.closure)}
                read_proof(policy, resource)
                activity = observe(locate(policy, resource))
                if not activity['complete'] or activity['busy']:
                    raise ValueError(activity['reason'])
                resource['state'] = 'released'
                resource['released_at'] = timestamp()
            elif action == 'apply':
                decision = eligible(policy, resource)
                if not decision['eligible']:
                    policy['receipts'].append({**decision, 'at': timestamp(), 'action': 'retained'})
                    save(record, value)
                    return decision
                path = locate(policy, resource)
                # Journal before deleting, and never automatically replay an uncertain deletion.
                snapshot = inventory(path)
                size = sum(v[2] for v in snapshot.values() if v[0] == 'file')
                resource['state'] = 'deleting'
                policy['receipts'].append({'id': resource['id'], 'at': timestamp(), 'action': 'delete-intent', 'bytes': size})
                save(record, value)
                try:
                    locate(policy, resource)
                    if inventory(path) != snapshot:
                        raise ValueError('resource changed immediately before removal')
                    activity = observe(Path(git(path, 'rev-parse', '--show-toplevel')) if resource['kind'] == 'cache' else path)
                    if not activity['complete'] or activity['busy']:
                        raise ValueError(activity['reason'])
                    if resource['kind'] == 'worktree':
                        subprocess.run(['git', '-C', policy['canonical']['root'], 'worktree', 'remove', str(path)], check=True, capture_output=True)
                    else:
                        if not shutil.rmtree.avoids_symlink_attacks:
                            raise ValueError('fd-safe removal unavailable')
                        # Bind parent descriptor, verify directory identity, never follow a swapped parent.
                        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                        try:
                            info = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
                            if [info.st_dev, info.st_ino] != resource['identity']:
                                raise ValueError('resource identity changed at removal')
                            shutil.rmtree(path.name, dir_fd=fd)
                        finally:
                            os.close(fd)
                    resource['state'] = 'deleted'
                    result = {'id': resource['id'], 'action': 'deleted', 'bytes': size, 'at': timestamp()}
                    policy['receipts'].append(result)
                    save(record, value)
                    return result
                except BaseException:
                    # State remains deleting; a future run must inspect/reconcile explicitly.
                    raise
        save(record, value)
        return {'status': action, 'authority': 'none'}


def discover(canonical, workspace):
    """Read only registered ownership pointers, never scan/adopt old environments."""
    canonical = runtime.identity(canonical)
    workspace = runtime.durable(workspace)
    pointers = runtime.unlinked(Path(canonical['git_common']) / 'task-resource-owners', exists=False)
    records, retained = {}, []
    if pointers.exists():
        if not pointers.is_dir():
            raise ValueError('invalid resource ownership pointer namespace')
        for file in sorted(pointers.iterdir()):
            try:
                pointer = runtime.read_json(file)
                if set(pointer) != {'path', 'record', 'id'}:
                    raise ValueError('unknown ownership pointer fields')
                record = runtime.unlinked(pointer['record'], exists=False)
                if not record.is_relative_to(workspace):
                    raise ValueError('foreign owning runtime; pointer retained without reading it')
                _, policy = load(record)
                if not policy or policy['canonical'] != canonical or policy['workspace'] != str(workspace):
                    raise ValueError('ownership pointer does not match selected repository/runtime')
                matches = [r for r in policy['resources'] if r['id'] == pointer['id'] and r['path'] == pointer['path']]
                if len(matches) != 1:
                    raise ValueError('ownership pointer lacks its exact resource record')
                if any(r['state'] != 'deleted' for r in policy['resources']):
                    records[str(record)] = policy['work_id']
            except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
                retained.append({'pointer': file.name, 'reason': str(exc)})
    return {'schema': 1, 'records': [{'record': key, 'work_id': value} for key, value in sorted(records.items())],
            'retained': retained, 'authority': 'none'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['list','init','bind-runtime','register','claim','resume','release','keep','inspect','plan','apply','enable','disable'])
    p.add_argument('--record', type=Path)
    p.add_argument('--approved', action='store_true', help='Caller has independently verified actual scoped owner authority')
    p.add_argument('--canonical', type=Path)
    p.add_argument('--workspace', type=Path)
    p.add_argument('--collection', type=Path)
    p.add_argument('--target', type=Path)
    p.add_argument('--id')
    p.add_argument('--kind', choices=['cache','scratch','worktree'])
    p.add_argument('--path', type=Path)
    p.add_argument('--closure', type=Path)
    a = p.parse_args()
    try:
        if a.action == 'list':
            if not a.canonical or not a.workspace:
                raise ValueError('list requires explicit selected canonical and workspace roots')
            print(json.dumps(discover(a.canonical, a.workspace), sort_keys=True, indent=2))
            return 0
        if not a.record:
            raise ValueError('owning work record is required')
        if a.action in {'inspect','plan'}:
            value, policy = load(a.record)
            if policy is None:
                result = {'schema': 1, 'state': 'legacy-inspect-only', 'candidates': [], 'authority': 'none'}
            elif a.action == 'inspect':
                result = {'schema': 1, 'policy': policy, 'authority': 'none'}
            else:
                result = {'schema': 1, 'candidates': [eligible(policy,r) for r in policy['resources']], 'authority': 'none'}
        else:
            if a.action == 'apply' and os.geteuid() == 0:
                raise ValueError('deletion engine must run unprivileged; elevate read-only observer only')
            if not a.approved:
                raise ValueError('mutation requires independently verified scoped approval and --approved')
            if a.action == 'init':
                if not all((a.canonical,a.workspace,a.collection)):
                    raise ValueError('init requires canonical, workspace and collection')
                init_record(a.record,a.canonical,a.workspace,a.collection)
                result = {'status': 'initialized', 'authority': 'none'}
            else:
                if a.action in {'register','claim','resume','release','keep','apply'} and not a.id:
                    raise ValueError('resource id required')
                if a.action == 'register' and not all((a.path,a.kind)):
                    raise ValueError('register requires path and kind')
                if a.action == 'release' and not a.closure:
                    raise ValueError('release requires reviewed current closure')
                result = mutate(a.record,a.action,a)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,StopIteration,subprocess.SubprocessError) as exc:
        print('Task resources: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
