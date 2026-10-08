import unittest

from task_summary import summarize_tasks


class TaskSummaryTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(summarize_tasks([]), {"todo": 0, "in-progress": 0, "done": 0})

    def test_canonical_counts(self):
        rows = [{"state": "todo"}, {"state": "in-progress"}, {"state": "done"}, {"state": "done"}]
        self.assertEqual(summarize_tasks(rows), {"todo": 1, "in-progress": 1, "done": 2})

    def test_alias_counts(self):
        rows = [{"state": "in_progress"}, {"state": "in progress"}, {"state": " IN-PROGRESS "}]
        self.assertEqual(summarize_tasks(rows), {"todo": 0, "in-progress": 3, "done": 0})

    def test_invalid_state(self):
        with self.assertRaises(ValueError):
            summarize_tasks([{"state": "blocked"}])

    def test_missing_state(self):
        with self.assertRaises(ValueError):
            summarize_tasks([{}])

    def test_input_unchanged(self):
        rows = [{"state": "todo"}]
        self.assertEqual(summarize_tasks(rows), {"todo": 1, "in-progress": 0, "done": 0})
        self.assertEqual(rows, [{"state": "todo"}])


if __name__ == "__main__":
    unittest.main()
