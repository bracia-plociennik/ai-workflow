import unittest

from math_utils import clamp


class ClampTests(unittest.TestCase):
    def test_within_range(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_below_range(self):
        self.assertEqual(clamp(-2, 0, 10), 0)

    def test_above_range(self):
        self.assertEqual(clamp(12, 0, 10), 10)


if __name__ == "__main__":
    unittest.main()
