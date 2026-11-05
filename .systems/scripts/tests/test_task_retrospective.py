from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from task_retrospective import analyze


class RetrospectiveTests(unittest.TestCase):
    def test_required_repeat_and_unnecessary_repeat(self):
        event = dict(action='full', source_fingerprint='s', environment_fingerprint='e',
                     mandatory=True, reason='release-gate', evidence='report.json', category='validation')
        value = dict(task_id='task', events=[event, event])
        self.assertEqual(analyze(value)['findings'], [])
        value['events'].append(dict(event, mandatory=False, reason='no-new-input'))
        self.assertEqual(len(analyze(value)['findings']), 1)

    def test_unknown_quality_is_not_inferred(self):
        result = analyze(dict(task_id='task', events=[]))
        self.assertIsNone(result['savings'])
        self.assertEqual(result['coverage'], 'supplied-observations-only')


if __name__ == '__main__':
    unittest.main()
