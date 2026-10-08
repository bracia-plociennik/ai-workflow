import unittest

from runtime_guard import require_owner_index
from task_summary import summarize_runs


class RunSummaryTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(summarize_runs([]), {"total": 0, "ok": 0, "failed": 0})

    def test_invalid_state(self):
        with self.assertRaises(ValueError):
            summarize_runs([{"state": "pending"}])

    def test_missing_state(self):
        with self.assertRaises(ValueError):
            summarize_runs([{}])

    def test_input_unchanged(self):
        events = [{"state": "ok"}]
        self.assertEqual(summarize_runs(events), {"total": 1, "ok": 1, "failed": 0})
        self.assertEqual(events, [{"state": "ok"}])

    def test_summary_and_owner_state(self):
        result = summarize_runs([{"state": "ok"}, {"state": "failed"}, {"state": "ok"}])
        self.assertEqual(result, {"total": 3, "ok": 2, "failed": 1})
        require_owner_index()


if __name__ == "__main__":
    unittest.main()
