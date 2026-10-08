"""Synthetic negative controls; no CLI, auth or network use."""
import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest
from datetime import datetime, timezone

spec = importlib.util.spec_from_file_location('preflight', Path(__file__).with_name('preflight.py'))
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def fixture():
    return {'instructions': 'Synthetic fixed base.', 'model': 'gpt-6-sol', 'reasoning': {'effort': 'high'},
            'input': [{'role': 'user', 'content': [{'type': 'input_text', 'text': p.PROMPT}]}],
            'tools': [{'type': 'function', 'name': 'exec_command', 'parameters': {'type': 'object'}}]}


class Detectors(unittest.TestCase):
    def test_clean(self):
        value = p.summarize(fixture())
        self.assertEqual(value['errors'], [])
        self.assertEqual(p.compare(value, value), [])

    def test_missing_malformed(self):
        for value in (None, [], {}, {'instructions': 3, 'input': [None], 'tools': ['bad']}):
            with self.subTest(shape=type(value).__name__):
                self.assertTrue(p.summarize(value)['errors'])

    def test_required_fields(self):
        for field in ('input', 'instructions', 'tools', 'model', 'reasoning'):
            value = fixture()
            del value[field]
            with self.subTest(field=field):
                self.assertTrue(p.summarize(value)['errors'])

    def test_ambient(self):
        for text in ('LV005_FOREIGN_CONTEXT_CANARY', '<skills_instructions>', '# AGENTS.md instructions',
                     '<memory>', '<app-context>', '/Users/synthetic/private', 'Unknown guidance',
                     '<environment_context>Unknown guidance</environment_context>',
                     '<permissions instructions>Unknown guidance</permissions instructions>'):
            value = fixture()
            value['input'].append({'role': 'developer', 'content': [{'type': 'input_text', 'text': text}]})
            with self.subTest(marker=text):
                self.assertTrue(p.summarize(value)['errors'])

    def test_auth(self):
        for header in ('Authorization', 'authorization', 'Proxy-Authorization', 'X-API-Key', 'Cookie'):
            self.assertIn('authentication-header', p.summarize(fixture(), [header])['errors'])

    def test_tools(self):
        for tool in ({'type': 'web_search'}, {'type': 'function', 'name': 'unknown'}, 'malformed'):
            value = fixture()
            value['tools'].append(tool)
            self.assertTrue(p.summarize(value)['errors'])
        value = fixture()
        value['tools'] *= 2
        self.assertIn('duplicate-tool', p.summarize(value)['errors'])

    def test_invalid_roles_and_content(self):
        for item in ({'role': 'assistant', 'content': []},
                     {'role': 'user', 'content': [{'type': 'image', 'text': p.PROMPT}]},
                     {'role': 'user', 'content': 'unknown'},
                     {'role': 'user', 'content': [{'type': 'text', 'text': None}]}):
            value = fixture()
            value['input'] = [item]
            self.assertTrue(p.summarize(value)['errors'])

    def test_policy_is_default_deny(self):
        policy = p.policy(Path('/private/tmp/synthetic-lv005'), 12345)
        self.assertIn('(deny default)', policy)
        self.assertIn('localhost:12345', policy)
        self.assertNotIn('(allow network*)', policy)
        self.assertNotIn('(subpath "/Users")', policy)
        self.assertNotIn('(subpath "/private/tmp")', policy)
        self.assertNotIn('securityd', policy)
        self.assertNotIn('(allow syscall*)', policy)
        self.assertNotIn('(allow mach*)', policy)

    def test_config_is_unauthenticated_local_sink(self):
        values = p.settings(Path('/private/tmp/synthetic-lv005'), 12345)
        self.assertEqual(values['model_providers.lv005-local-sink.requires_openai_auth'], 'false')
        self.assertIn('127.0.0.1:12345', values['model_providers.lv005-local-sink.base_url'])
        self.assertEqual(values['model_providers.lv005-local-sink.request_max_retries'], '0')

    def test_mismatch(self):
        baseline = p.summarize(fixture())
        value = fixture()
        value['instructions'] += ' Changed.'
        self.assertTrue(p.compare(baseline, p.summarize(value)))
        self.assertTrue(p.compare({}, {}))

    def test_zero_exit_missing_result(self):
        self.assertEqual(p.result_errors(0, False), ['missing-actual-result'])
        self.assertEqual(p.result_errors(0, True), [])
        self.assertIn('process-timeout', p.result_errors(124, False, True))

    def test_redaction(self):
        value = fixture()
        value['input'][0]['content'][0]['text'] = 'LV005_FOREIGN_CONTEXT_CANARY'
        encoded = str(p.summarize(value, ['Authorization']))
        self.assertNotIn('LV005_FOREIGN_CONTEXT_CANARY', encoded)
        self.assertNotIn('Synthetic fixed base.', encoded)

    def test_timeout_wrapper_real_synthetic_child(self):
        # Wrapper test only: no CLI/model/network. It does not certify OS isolation.
        with tempfile.TemporaryDirectory(prefix='lv005-wrapper-', dir='/private/tmp') as temporary:
            root = Path(temporary)
            environment = {'HOME': temporary, 'PATH': '/usr/bin:/bin', 'TMPDIR': temporary}
            result, out, _ = p.run(['/bin/sh', '-c', '(printf LV005_CHILD_STARTED; /bin/sleep 1; printf orphan > orphan.txt) & wait'],
                                 root, environment, timeout=0.1)
            time.sleep(1.2)
            self.assertEqual(result['exit_code'], 124)
            self.assertTrue(result['timed_out'])
            self.assertIn(b'LV005_CHILD_STARTED', out)
            self.assertFalse((root/'orphan.txt').exists())

    def test_wrapper_actual_output(self):
        with tempfile.TemporaryDirectory(prefix='lv005-wrapper-', dir='/private/tmp') as temporary:
            result, out, _ = p.run(['/bin/sh', '-c', 'printf LV005_SYNTHETIC_OUTPUT'],
                                   Path(temporary), {'HOME': temporary, 'PATH': '/usr/bin:/bin'})
            self.assertEqual(result['exit_code'], 0)
            self.assertEqual(out, b'LV005_SYNTHETIC_OUTPUT')
            self.assertEqual(p.result_errors(result['exit_code'], bool(out)), [])


if __name__ == '__main__':
    started = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Detectors))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    output = Path(__file__).parent/'runs'/('detectors-' + stamp)
    output.mkdir(parents=True, exist_ok=False)
    summary = {'scope': 'synthetic-detectors-and-wrapper-only', 'model_calls': 0, 'CLI_called': False,
               'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
               'successful': result.wasSuccessful(), 'duration_seconds': round(time.monotonic() - started, 3),
               'harness_sha256': p.digest(Path(__file__).with_name('preflight.py').read_bytes()),
               'tests_sha256': p.digest(Path(__file__).read_bytes()),
               'runtime_isolation_proven': False, 'behavioral_eval_ready': False}
    (output/'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('Evidence: ' + str(output/'summary.json'))
    raise SystemExit(0 if result.wasSuccessful() else 1)
