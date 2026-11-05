"""Evidence-bound retrospective support for an explicitly selected task."""
import argparse
import hashlib
import json
from pathlib import Path


def analyze(value):
    if set(value) != {'task_id', 'events'} or not value['task_id']:
        raise ValueError('task identity and observed events required')
    seen, findings = set(), []
    for event in value['events']:
        required = {'action', 'source_fingerprint', 'environment_fingerprint',
                    'mandatory', 'reason', 'evidence', 'category'}
        if set(event) != required or type(event['mandatory']) is not bool:
            raise ValueError('invalid retrospective event')
        if any(not isinstance(event[k], str) or not event[k] for k in required - {'mandatory'}):
            raise ValueError('incomplete observed event')
        key = (event['action'], event['source_fingerprint'], event['environment_fingerprint'])
        if key in seen and not event['mandatory'] and event['reason'] == 'no-new-input':
            findings.append(dict(category='potential-redundancy', evidence=event['evidence'],
                                 finding='Repeated action with identical declared inputs',
                                 improvement='Reuse eligible evidence or state the changed verification question',
                                 verification='Review the next comparable task for justified repetitions'))
        if event['category'] in {'executor-error', 'missing-contract', 'environment-constraint'}:
            findings.append(dict(category=event['category'], evidence=event['evidence'],
                                 finding=event['reason'], improvement='Address the observed cause before another expensive attempt',
                                 verification='Exercise the affected command or input with a focused preview'))
        seen.add(key)
    return dict(task_id=value['task_id'], findings=findings,
                result='findings' if findings else 'no-significant-inefficiency-observed-in-supplied-events',
                coverage='supplied-observations-only', savings=None, execution_authorized=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        raw = args.input.read_bytes()
        result = analyze(json.loads(raw))
        result['source_sha256'] = hashlib.sha256(raw).hexdigest()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, 'Retrospective: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
