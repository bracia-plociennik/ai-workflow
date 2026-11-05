"""Cooperating filesystem capacity reservations for managed operations."""
import argparse
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import subprocess
import signal
import stat
import uuid

from durable_runtime import unlinked

GIB = 1024 ** 3


def estimate(value):
    if type(value) is not int or value < 0:
        raise ValueError('an explicit nonnegative integer estimate is required')
    return value


def filesystem(path):
    path = unlinked(path)
    info = path.stat()
    fs = os.statvfs(path)
    return dict(device=info.st_dev, total=fs.f_blocks * fs.f_frsize,
                available=fs.f_bavail * fs.f_frsize, inodes=fs.f_favail)


def records(directory):
    values = []
    for path in sorted(directory.glob('*.json')):
        path = unlinked(path)
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > 65536:
            raise ValueError('unsupported reservation file')
        value = json.loads(path.read_text())
        required = {'schema', 'id', 'work_id', 'device', 'bytes', 'inodes', 'path'}
        if (set(value) != required or type(value['schema']) is not int or
                value['schema'] != 1 or path.stem != value['id']):
            raise ValueError('unknown reservation record; inspect before allocation')
        for key in ('device', 'bytes', 'inodes'):
            estimate(value[key])
        if not isinstance(value['work_id'], str) or not value['work_id']:
            raise ValueError('invalid reservation owner')
        if not isinstance(value['path'], str):
            raise ValueError('invalid reservation path')
        values.append(value)
    return values


def assess(snapshot, existing, requested_bytes, requested_inodes):
    requested_bytes, requested_inodes = estimate(requested_bytes), estimate(requested_inodes)
    matching = [v for v in existing if v['device'] == snapshot['device']]
    floor = max(10 * GIB, (snapshot['total'] + 9) // 10)
    usable = snapshot['available'] - floor - sum(v['bytes'] for v in matching)
    nodes = snapshot['inodes'] - 1024 - sum(v['inodes'] for v in matching)
    return dict(allowed=requested_bytes <= usable and requested_inodes <= nodes,
                available=snapshot['available'], device=snapshot['device'],
                reserve_floor=floor, unreserved_bytes=max(0, usable),
                unreserved_inodes=max(0, nodes), estimated_bytes=requested_bytes,
                estimated_inodes=requested_inodes, execution_authorized=False)


@contextmanager
def locked(directory):
    directory = unlinked(directory)
    fd = os.open(directory / '.capacity.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError('unsupported capacity lock')
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def reserve(directory, path, work_id, size, inodes):
    if not work_id or not isinstance(work_id, str):
        raise ValueError('stable work ID required')
    with locked(directory):
        snapshot = filesystem(path)
        result = assess(snapshot, records(directory), size, inodes)
        if not result['allowed']:
            raise ValueError('insufficient unreserved bytes or inodes: ' + json.dumps(result))
        identity = uuid.uuid4().hex
        value = dict(schema=1, id=identity, work_id=work_id, device=snapshot['device'],
                     bytes=size, inodes=inodes, path=str(unlinked(path)))
        output = directory / (identity + '.json')
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream)
            stream.flush()
            os.fsync(stream.fileno())
        sync_directory(directory)
        return value


def sync_directory(directory):
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def release(directory, identity, work_id):
    if not isinstance(identity, str) or len(identity) != 32 or any(c not in '0123456789abcdef' for c in identity):
        raise ValueError('invalid reservation ID')
    with locked(directory):
        values = {v['id']: v for v in records(directory)}
        value = values.get(identity)
        if value is None:
            return dict(released=False, reason='already-absent')
        if value['work_id'] != work_id:
            raise ValueError('reservation belongs to another work')
        (directory / (identity + '.json')).unlink()
        sync_directory(directory)
        return dict(released=True, id=identity)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inspect', 'plan', 'reserve', 'release', 'run'])
    parser.add_argument('--state-dir', required=True, type=Path)
    parser.add_argument('--path', type=Path)
    parser.add_argument('--work-id')
    parser.add_argument('--bytes', type=int)
    parser.add_argument('--inodes', type=int)
    parser.add_argument('--id')
    parser.add_argument('--approved', action='store_true')
    import sys
    arguments = sys.argv[1:]
    split = arguments.index('--') if '--' in arguments else len(arguments)
    args = parser.parse_args(arguments[:split])
    args.command = arguments[split + 1:]
    try:
        directory = unlinked(args.state_dir)
        if args.action == 'inspect':
            result = dict(reservations=records(directory), execution_authorized=False)
        elif args.action == 'plan':
            result = assess(filesystem(args.path), records(directory), args.bytes, args.inodes)
        else:
            if not args.approved:
                raise ValueError('caller must verify actual scoped authority')
            if args.action == 'release':
                result = release(directory, args.id, args.work_id)
            else:
                command = args.command[1:] if args.command[:1] == ['--'] else args.command
                if args.action == 'run' and not command:
                    raise ValueError('explicit command argv required')
                result = reserve(directory, args.path, args.work_id, args.bytes, args.inodes)
                if args.action == 'run':
                    process = None
                    try:
                        with subprocess.Popen(command, start_new_session=True) as process:
                            try:
                                status = process.wait()
                            except BaseException:
                                os.killpg(process.pid, signal.SIGTERM)
                                try:
                                    process.wait(timeout=10)
                                except subprocess.TimeoutExpired:
                                    os.killpg(process.pid, signal.SIGKILL)
                                    process.wait()
                                raise
                    finally:
                        try:
                            if process is None:
                                raise ProcessLookupError
                            os.killpg(process.pid, 0)
                        except ProcessLookupError:
                            release(directory, result['id'], args.work_id)
                        else:
                            print('Capacity reservation retained for live process group: ' + result['id'])
                    return status
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, 'Capacity: ' + str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
