import unittest

from math_utils import clamp, normalize_bounds


class ClampTests(unittest.TestCase):
    def test_middle(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_below(self):
        self.assertEqual(clamp(-2, 0, 10), 0)

    def test_above(self):
        self.assertEqual(clamp(12, 0, 10), 10)

    def test_normalize_bounds(self):
        self.assertEqual(normalize_bounds(0, 10), (0, 10))

    def test_reversed_bounds_rejected(self):
        with self.assertRaises(ValueError):
            normalize_bounds(10, 0)


if __name__ == "__main__":
    unittest.main()
