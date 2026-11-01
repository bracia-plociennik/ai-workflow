#!/usr/bin/env python3
"""Conservative task resource lifecycle. No field is authority or a QA verdict."""
import argparse
import copy
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
CACHE_PROFILE = 'next-webpack-cache-v1'


def manifest_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def cache_profile(resource):
    profile = resource.get('profile')
    if profile is not None and (profile != CACHE_PROFILE or resource.get('kind') != 'cache'):
        raise ValueError('unsupported cache profile')
    return profile == CACHE_PROFILE


def checked_stat(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def fd_inventory(fd, path, *, exclude=()):
    """Descriptor-bound, exhaustive closure. Exclusions are exact relative paths."""
    device = os.fstat(fd).st_dev
    found = {}

    def walk(parent, prefix):
        before = os.fstat(parent)
        for name in sorted(os.listdir(parent)):
            rel = (prefix / name).as_posix()
            if rel in exclude:
                continue
            if (name == '.env' or name.startswith('.env.') or name.lower() in
                    {'secrets', 'credentials', '.aws', 'id_rsa', 'id_ed25519'}
                    or name.lower().endswith(('.pem', '.key'))):
                raise ValueError('secret-bearing content cannot be inventoried for cache eviction')
            info = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if info.st_dev != device or os.path.ismount(path / rel):
                raise ValueError('mounted resource content')
            if stat.S_ISDIR(info.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
                try:
                    if checked_stat(info) != checked_stat(os.fstat(child)):
                        raise ValueError('directory changed during inventory')
                    found[rel] = ['dir', stat.S_IMODE(info.st_mode), info.st_dev, info.st_ino]
                    walk(child, Path(rel))
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                child = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
                with os.fdopen(child, 'rb') as stream:
                    if checked_stat(info) != checked_stat(os.fstat(stream.fileno())):
                        raise ValueError('file changed during inventory')
                    sha = hashlib.file_digest(stream, 'sha256').hexdigest()
                    if checked_stat(info) != checked_stat(os.fstat(stream.fileno())):
                        raise ValueError('file changed during hashing')
                found[rel] = ['file', stat.S_IMODE(info.st_mode), info.st_size, sha,
                              info.st_dev, info.st_ino, info.st_blocks * 512]
            else:
                raise ValueError('linked, special or hardlinked resource content')
        if checked_stat(before) != checked_stat(os.fstat(parent)):
            raise ValueError('directory changed during inventory')
    walk(fd, Path())
    return found


def profile_inventory(path, *, exclude=()):
    path = runtime.unlinked(path)
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        return fd_inventory(fd, path, exclude=exclude)
    finally:
        os.close(fd)


def webpack_inventory(path):
    items = profile_inventory(path)
    sensitive(items)
    compiler = r'(client|server|edge-server)-(production|development)'
    for name, entry in items.items():
        pattern = compiler if entry[0] == 'dir' else compiler + r'/(index|[0-9]+)\.pack(?:\.(?:gz|br))?(?:\.old)?'
        if not re.fullmatch(pattern, name):
            raise ValueError('unknown webpack generated content; cache retained')
    return items


def remove_profile(path, resource, snapshot, proof):
    """Remove approved entries only, through identity-checked directory descriptors."""
    source = Path(proof['source']['root'])
    descriptors = []
    try:
        fd = os.open(source, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(fd)
        if [os.fstat(fd).st_dev, os.fstat(fd).st_ino] != proof['source']['identity']:
            raise ValueError('source root changed at removal')
        for name in ('.next', 'cache'):
            fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            descriptors.append(fd)
        parent = fd
        root = os.open('webpack', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        descriptors.append(root)
        if [os.fstat(root).st_dev, os.fstat(root).st_ino] != resource['identity']:
            raise ValueError('cache identity changed at removal')
        if fd_inventory(root, path) != snapshot:
            raise ValueError('cache inventory changed at removal')

        def open_parent(relative):
            current = os.dup(root)
            prefix = Path()
            try:
                for name in relative.parts[:-1]:
                    prefix /= name
                    child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
                    os.close(current)
                    current = child
                    info = os.fstat(current)
                    if snapshot[prefix.as_posix()] != ['dir', stat.S_IMODE(info.st_mode), info.st_dev, info.st_ino]:
                        raise ValueError('approved cache directory changed')
                return current
            except BaseException:
                os.close(current)
                raise

        for name, entry in sorted(snapshot.items(), key=lambda item: (-len(Path(item[0]).parts), item[0])):
            relative = Path(name)
            fd = open_parent(relative)
            try:
                info = os.stat(relative.name, dir_fd=fd, follow_symlinks=False)
                if entry[0] == 'dir':
                    if not stat.S_ISDIR(info.st_mode) or entry != ['dir', stat.S_IMODE(info.st_mode), info.st_dev, info.st_ino]:
                        raise ValueError('approved cache directory changed')
                    os.rmdir(relative.name, dir_fd=fd)  # Unknown/new contents are never traversed/deleted.
                else:
                    child = os.open(relative.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                    with os.fdopen(child, 'rb') as stream:
                        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or checked_stat(info) != checked_stat(os.fstat(stream.fileno())):
                            raise ValueError('approved cache file changed')
                        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
                        if entry != ['file', stat.S_IMODE(info.st_mode), info.st_size, sha, info.st_dev, info.st_ino, info.st_blocks * 512] or checked_stat(info) != checked_stat(os.fstat(stream.fileno())):
                            raise ValueError('approved cache file changed')
                    os.unlink(relative.name, dir_fd=fd)
            finally:
                os.close(fd)
        info = os.stat('webpack', dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISDIR(info.st_mode) or [info.st_dev, info.st_ino] != resource['identity']:
            raise ValueError('cache root changed before final removal')
        os.rmdir('webpack', dir_fd=parent)
    finally:
        for fd in reversed(descriptors):
            os.close(fd)


def task_fingerprint(path, work_id, resource_id):
    value = copy.deepcopy(runtime.read_json(path))
    if not isinstance(value, dict):
        raise ValueError('task evidence must be an object')
    if value.get('work_id') == work_id:
        policy = value.get('task_resource_cleanup', {})
        if not isinstance(policy, dict) or not isinstance(policy.get('resources', []), list):
            raise ValueError('invalid owning task policy')
        policy.pop('receipts', None)
        policy['resources'] = [r for r in policy.get('resources', []) if r['id'] != resource_id]
    return manifest_digest(value)


def read_cache_proof(policy, resource, value):
    expected = {'schema', 'kind', 'work_id', 'reviewed_by', 'state', 'profile', 'path',
                'identity', 'manifest', 'source', 'source_manifest', 'index_sha256',
                'reports', 'dependencies', 'task_records', 'workers', 'claims',
                'reconstruction', 'dependency_review', 'review_revision'}
    if (set(value) != expected or type(value['schema']) is not int or value['schema'] != 1
            or value['kind'] != 'reviewed-cache-eviction-v1' or value['state'] != 'complete'
            or value['work_id'] != policy['work_id'] or value['profile'] != CACHE_PROFILE
            or not isinstance(value['reviewed_by'], str) or not value['reviewed_by'].strip()
            or not isinstance(value['reconstruction'], str) or not value['reconstruction'].strip()):
        raise ValueError('invalid reviewed cache eviction proof')
    review = value['dependency_review']
    if (not isinstance(review, dict) or set(review) != {'complete', 'cache_required', 'evidence'}
            or review['complete'] is not True or review['cache_required'] is not False
            or not isinstance(review['evidence'], str) or not review['evidence'].strip()):
        raise ValueError('cache dependency review is incomplete or requires cache')
    for key, state in (('workers', 'terminated'), ('claims', 'released')):
        if not isinstance(value[key], list) or any(not isinstance(v, dict) or set(v) != {'state', 'evidence'}
                or v['state'] != state or not isinstance(v['evidence'], str) or not v['evidence'].strip() for v in value[key]):
            raise ValueError('cache worker/claim termination is unknown')
    path = locate(policy, resource)
    if (value['review_revision'] != resource.get('review_revision')
            or not isinstance(value['review_revision'], str)
            or not re.fullmatch(r'[0-9a-f]{32}', value['review_revision'])):
        raise ValueError('cache review revision invalidated by claim/resume')
    if value['path'] != str(path) or value['identity'] != resource['identity']:
        raise ValueError('cache proof target identity mismatch')
    repo = Path(git(path, 'rev-parse', '--show-toplevel'))
    activity = observe(repo)
    if not activity['complete'] or activity['busy']:
        raise ValueError(activity['reason'])
    if value['manifest'] != resource['manifest'] or webpack_inventory(path) != value['manifest']:
        raise ValueError('cache content changed since review/enrollment')
    source = {**runtime.identity(repo), 'head': git(repo, 'rev-parse', 'HEAD'),
              'identity': [repo.stat().st_dev, repo.stat().st_ino]}
    if value['source'] != source:
        raise ValueError('cache source HEAD/identity changed')
    index = runtime.unlinked(git(repo, 'rev-parse', '--path-format=absolute', '--git-path', 'index'))
    if digest(index) != value['index_sha256']:
        raise ValueError('cache source index changed')
    actual = profile_inventory(repo, exclude=('.git', path.relative_to(repo).as_posix()))
    if any('.git' in Path(name).parts for name in actual):
        raise ValueError('nested repository in cache source closure')
    if not isinstance(value['source_manifest'], dict) or actual != value['source_manifest']:
        raise ValueError('complete cache source input inventory changed')
    if git(repo, 'ls-files', '--', path.relative_to(repo).as_posix()):
        raise ValueError('cache contains tracked input')
    own_records, recorded = [], set()
    for key in ('reports', 'dependencies', 'task_records'):
        entries = value[key]
        if not isinstance(entries, list) or (key != 'dependencies' and not entries):
            raise ValueError('current cache review reports/tasks missing')
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {'path', 'sha256'}:
                raise ValueError('unknown cache evidence fields')
            file = runtime.unlinked(entry['path'])
            if (str(file) in seen or runtime.temporary(file) or not file.is_relative_to(Path(policy['workspace']))):
                raise ValueError('cache evidence must be unique and in durable owning runtime')
            seen.add(str(file))
            sha = task_fingerprint(file, policy['work_id'], resource['id']) if key == 'task_records' else digest(file)
            if sha != entry['sha256']:
                raise ValueError('current cache review dependency/task changed')
            if key == 'task_records':
                recorded.add(str(file))
                record = runtime.read_json(file)
                if record.get('work_id') == policy['work_id']:
                    other = record.get('task_resource_cleanup')
                    if not other or any(other.get(k) != policy[k] for k in ('canonical', 'workspace', 'work_id', 'schema')):
                        raise ValueError('cache owning task mismatch')
                    own_records.append(str(file))
            elif any(ref.encode() in file.read_bytes() for ref in (str(path), '.next/cache/webpack')):
                raise ValueError('current cache review dependency references cache')
    if len(own_records) != 1:
        raise ValueError('exact owning cache task must be reviewed')
    owners = runtime.unlinked(Path(policy['canonical']['git_common']) / 'task-resource-owners', exists=False)
    if owners.exists():
        for marker in owners.iterdir():
            pointer = runtime.read_json(marker)
            if set(pointer) != {'path', 'record', 'id'} or pointer['record'] not in recorded:
                raise ValueError('registered task dependency closure is incomplete')
            record = runtime.read_json(pointer['record'])
            other = record.get('task_resource_cleanup', {})
            if other.get('canonical') != policy['canonical'] or not any(r['id'] == pointer['id'] and r['path'] == pointer['path'] for r in other.get('resources', [])):
                raise ValueError('registered task ownership is ambiguous')
            otherpath = Path(pointer['path'])
            if pointer['record'] != own_records[0] and (path == otherpath or path.is_relative_to(otherpath) or otherpath.is_relative_to(path)):
                raise ValueError('cache overlaps another owning task')
    return value


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
    if not isinstance(policy, dict) or set(policy) != expected or type(policy['schema']) is not int or policy['schema'] not in {1, 2}:
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
    for resource in resources:
        if 'profile' in resource or 'enrollment_review' in resource:
            fields = {'id', 'kind', 'path', 'state', 'keep', 'released_at', 'closure',
                      'identity', 'manifest', 'profile', 'enrollment_review', 'review_revision'}
            if policy['schema'] != 2 or set(resource) != fields or not cache_profile(resource):
                raise ValueError('unsupported versioned cache resource')
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
    profiled = cache_profile(resource)
    if profiled and policy['schema'] != 2:
        raise ValueError('webpack cache profile requires explicit policy schema2')
    if resource['kind'] == 'cache':
        tail = ('.next', 'cache', 'webpack') if profiled else ('.next', 'cache')
        if tuple(path.parts[-len(tail):]) != tail:
            raise ValueError('cache path does not match exact supported profile')
    if resource['kind'] != 'scratch' and path.exists():
        repo = Path(git(path, 'rev-parse', '--show-toplevel'))
        if repo == Path(policy['canonical']['root']) or not repo.is_relative_to(root / '.worktrees'):
            raise ValueError('cache/worktree is not an auxiliary repository')
        if runtime.identity(repo)['git_common'] != policy['canonical']['git_common']:
            raise ValueError('resource belongs to another repository')
        if profiled and path != repo / '.next/cache/webpack':
            raise ValueError('webpack cache must be directly under auxiliary source root')
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
    if cache_profile(resource) and (not isinstance(proof, dict) or set(proof) != {'path', 'sha256'}):
        raise ValueError('unknown cache proof reference fields')
    file = runtime.unlinked(proof['path'])
    if not file.is_relative_to(Path(policy['workspace'])) or digest(file) != proof['sha256']:
        raise ValueError('closure evidence changed or is outside owning runtime')
    value = runtime.read_json(file)
    if cache_profile(resource):
        if proof != resource.get('enrollment_review'):
            raise ValueError('cache proof differs from explicit enrollment review')
        return read_cache_proof(policy, resource, value)
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
            actual = webpack_inventory(path) if cache_profile(resource) else inventory(path)
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
        result = {'id': resource['id'], 'eligible': True, 'path': str(path), 'reason': 'closed, preserved, unused and in scope'}
        if cache_profile(resource):
            result.update(profile=CACHE_PROFILE, bytes=sum(v[2] for v in actual.values() if v[0] == 'file'),
                          allocated_bytes=sum(v[6] for v in actual.values() if v[0] == 'file'),
                          manifest_sha256=manifest_digest(actual))
        return result
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        return {'id': resource.get('id'), 'eligible': False, 'reason': str(exc)}


def init_record(record, canonical, workspace, collection, schema=1):
    # Record must already exist; preserve all unrelated owning work fields.
    value = runtime.read_json(record)
    if not isinstance(value, dict) or not isinstance(value.get('work_id'), str) or not SLUG.fullmatch(value['work_id']):
        raise ValueError('existing owning work record with stable work_id is required')
    canonical, workspace, collection = runtime.unlinked(canonical), runtime.durable(workspace), runtime.durable(collection)
    if not runtime.unlinked(record).is_relative_to(workspace) or runtime.temporary(canonical):
        raise ValueError('owning record/canonical source is not durable')
    if type(schema) is not int or schema not in {1, 2}:
        raise ValueError('unsupported resource policy schema')
    policy = {'schema': schema, 'enabled': True, 'work_id': value['work_id'], 'canonical': runtime.identity(canonical),
              'workspace': str(workspace), 'collection': str(collection), 'resources': [], 'receipts': []}
    if 'task_resource_cleanup' in value:
        _, existing = load(record)
        if any(existing[k] != policy[k] for k in ('schema', 'work_id', 'canonical', 'workspace', 'collection')):
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
            if getattr(args, 'profile', None):
                if not getattr(args, 'cache_review', None):
                    raise ValueError('cache profile requires explicit reviewed enrollment')
                resource.update(profile=args.profile, enrollment_review={
                    'path': str(runtime.unlinked(args.cache_review)), 'sha256': digest(args.cache_review)})
                resource['review_revision'] = runtime.read_json(args.cache_review).get('review_revision')
            elif getattr(args, 'cache_review', None):
                raise ValueError('cache enrollment review requires explicit profile')
            path = locate(policy, resource)
            for other in policy['resources']:
                otherpath = Path(other['path'])
                if path == otherpath:
                    raise ValueError('resource path already registered')
            if args.kind != 'worktree':
                resource['manifest'] = webpack_inventory(path) if cache_profile(resource) else inventory(path)
                sensitive(resource['manifest'])
            resource['identity'] = [path.stat().st_dev, path.stat().st_ino]
            if cache_profile(resource):
                resource['closure'] = resource['enrollment_review']
                read_proof(policy, resource)
                resource['closure'] = None
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
            if action in {'release','apply'} and 'sprint_iteration' in value:
                import sprint_iteration
                sprint_iteration.guard_record(record, HERE.parents[1])
            resource = next((r for r in policy['resources'] if r['id'] == args.id), None)
            if not resource:
                raise ValueError('unknown resource identity')
            if action in {'claim', 'resume'}:
                if resource['state'] in {'deleted', 'deleting'}:
                    raise ValueError('deleted/uncertain resource cannot be reclaimed')
                locate(policy, resource)
                resource.update(state='active', keep=False, released_at=None, closure=None)
                if cache_profile(resource):
                    resource.update(enrollment_review=None, review_revision=uuid.uuid4().hex)
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
                if getattr(args, 'cache_review', None):
                    if not cache_profile(resource) or runtime.unlinked(args.cache_review) != runtime.unlinked(args.closure):
                        raise ValueError('cache review renewal requires the same explicit cache closure')
                    path = locate(policy, resource)
                    resource['manifest'] = webpack_inventory(path)
                    resource['enrollment_review'] = {'path': str(runtime.unlinked(args.cache_review)), 'sha256': digest(args.cache_review)}
                resource['closure'] = {'path': str(runtime.unlinked(args.closure)), 'sha256': digest(args.closure)}
                read_proof(policy, resource)
                path = locate(policy, resource)
                activity = observe(Path(git(path, 'rev-parse', '--show-toplevel')) if cache_profile(resource) else path)
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
                snapshot = webpack_inventory(path) if cache_profile(resource) else inventory(path)
                size = sum(v[2] for v in snapshot.values() if v[0] == 'file')
                resource['state'] = 'deleting'
                policy['receipts'].append({'id': resource['id'], 'at': timestamp(), 'action': 'delete-intent', 'bytes': size})
                save(record, value)
                try:
                    locate(policy, resource)
                    if (webpack_inventory(path) if cache_profile(resource) else inventory(path)) != snapshot:
                        raise ValueError('resource changed immediately before removal')
                    activity = observe(Path(git(path, 'rev-parse', '--show-toplevel')) if resource['kind'] == 'cache' else path)
                    if not activity['complete'] or activity['busy']:
                        raise ValueError(activity['reason'])
                    if cache_profile(resource):
                        # Re-read all source/evidence/task dependencies after the journal and observation.
                        current_proof = read_proof(policy, resource)
                        remove_profile(path, resource, snapshot, current_proof)
                    elif resource['kind'] == 'worktree':
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


def review_cache(record, path, profile, review=None):
    """Read-only legacy qualification; never enroll, release or authorize removal."""
    _, policy = load(record)
    result = {'schema': 1, 'eligible': False, 'execution_authorized': False, 'authority': 'none',
              'path': str(path.absolute()), 'profile': profile, 'reasons': []}
    try:
        if policy is None:
            raise ValueError('no resource policy; candidate is unregistered')
        disabled = runtime.unlinked(Path(policy['canonical']['git_common']) / 'task-resource-cleanup.disabled', exists=False)
        if not policy['enabled'] or disabled.exists():
            result['reasons'].append('cleanup disabled; current policy/stop marker preserved')
        resource = {'id': 'review-candidate', 'kind': 'cache', 'path': str(path.absolute()), 'profile': profile}
        # Geometry may be inspected under the proposed capability without migrating the actual policy.
        target = locate(dict(policy, schema=2), resource)
        actual = webpack_inventory(target)
        result.update(bytes=sum(v[2] for v in actual.values() if v[0] == 'file'),
                      allocated_bytes=sum(v[6] for v in actual.values() if v[0] == 'file'),
                      manifest_sha256=manifest_digest(actual),
                      identity=[target.stat().st_dev, target.stat().st_ino])
        matches = [r for r in policy['resources'] if r['path'] == str(target) and r.get('profile') == profile]
        if len(matches) == 1:
            decision = eligible(policy, matches[0])
            value = runtime.read_json(record)
            if 'sprint_iteration' in value:
                import sprint_iteration
                if not sprint_iteration.inspect(record, HERE.parents[1])['closure_allowed']:
                    decision = {'eligible': False, 'reason': 'Sprint has pending/stale Quality'}
            result.update(decision)
            if not decision['eligible']:
                result['reasons'].append(decision['reason'])
        else:
            result['reasons'].append('candidate is not explicitly registered/released with this profile')
            if policy['schema'] != 2:
                result['reasons'].append('existing policy schema1 remains unchanged; explicit schema2 enrollment required')
            if review is None:
                result['reasons'].append('reviewed-cache-eviction-v1 proof missing; reconstructibility/dependency closure unverified')
            else:
                result['reasons'].append('unregistered candidate proof cannot supply enrollment/release authority')
        activity = observe(Path(git(target, 'rev-parse', '--show-toplevel')))
        result['activity'] = activity
        if not activity['complete'] or activity['busy']:
            result['eligible'] = False
            result['reasons'].append(activity['reason'])
        for other in policy['resources']:
            otherpath = Path(other['path'])
            if (target == otherpath or target.is_relative_to(otherpath) or otherpath.is_relative_to(target)) and (other.get('keep') or other['state'] not in {'released', 'deleted'}):
                result['eligible'] = False
                result['reasons'].append('overlapping resource is active, kept or uncertain')
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        result['eligible'] = False
        result['reasons'].append(str(exc))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['list','init','bind-runtime','register','claim','resume','release','keep','inspect','plan','review-cache','apply','enable','disable'])
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
    p.add_argument('--schema', type=int, choices=[1, 2], default=1, help='Explicit init schema; never migrates existing policies')
    p.add_argument('--profile')
    p.add_argument('--cache-review', type=Path)
    a = p.parse_args()
    try:
        if a.action == 'list':
            if not a.canonical or not a.workspace:
                raise ValueError('list requires explicit selected canonical and workspace roots')
            print(json.dumps(discover(a.canonical, a.workspace), sort_keys=True, indent=2))
            return 0
        if not a.record:
            raise ValueError('owning work record is required')
        if a.action == 'review-cache':
            if not a.path or a.profile != CACHE_PROFILE:
                raise ValueError('review-cache requires exact path and supported explicit profile')
            result = review_cache(a.record, a.path, a.profile, a.cache_review)
        elif a.action in {'inspect','plan'}:
            value, policy = load(a.record)
            if policy is None:
                result = {'schema': 1, 'state': 'legacy-inspect-only', 'candidates': [], 'authority': 'none'}
            elif a.action == 'inspect':
                result = {'schema': 1, 'policy': policy, 'authority': 'none'}
            else:
                sprint_pinned = False
                if 'sprint_iteration' in value:
                    import sprint_iteration
                    sprint_pinned = not sprint_iteration.inspect(a.record, HERE.parents[1])['closure_allowed']
                candidates = ([{'id':r['id'],'eligible':False,'reason':'Sprint has pending/stale Quality'} for r in policy['resources']]
                              if sprint_pinned else [eligible(policy,r) for r in policy['resources']])
                result = {'schema': 1, 'candidates': candidates, 'authority': 'none'}
        else:
            if a.action == 'apply' and os.geteuid() == 0:
                raise ValueError('deletion engine must run unprivileged; elevate read-only observer only')
            if not a.approved:
                raise ValueError('mutation requires independently verified scoped approval and --approved')
            if a.action == 'init':
                if not all((a.canonical,a.workspace,a.collection)):
                    raise ValueError('init requires canonical, workspace and collection')
                init_record(a.record,a.canonical,a.workspace,a.collection,schema=a.schema)
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
