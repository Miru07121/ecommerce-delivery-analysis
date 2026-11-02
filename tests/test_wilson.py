"""Count contracts and numerical reference cases for review-rate intervals."""
import unittest
from analyze import wilson


class WilsonTests(unittest.TestCase):
    def test_reference_interval(self):
        low, high = wilson(5, 10)
        self.assertAlmostEqual(low, .236593090512564, places=12)
        self.assertAlmostEqual(high, .763406909487436, places=12)

    def test_zero_and_all_successes(self):
        self.assertEqual(wilson(0, 0), (None, None))
        self.assertAlmostEqual(wilson(0, 10)[0], 0)
        self.assertAlmostEqual(wilson(10, 10)[1], 1)
        self.assertGreater(wilson(0, 10)[1], 0)
        self.assertLess(wilson(10, 10)[0], 1)

    def test_complement_symmetry(self):
        for k in range(21):
            low, high = wilson(k, 20)
            other_low, other_high = wilson(20 - k, 20)
            self.assertAlmostEqual(low, 1 - other_high)
            self.assertAlmostEqual(high, 1 - other_low)
            self.assertTrue(0 <= low <= high <= 1)

    def test_invalid_counts(self):
        for k, n in [(-1, 10), (11, 10), (1, 0), (0, -1),
                     (.5, 10), (1, 10.0), (True, 10), (1, False),
                     (float('nan'), 10), (0, float('inf')), ('1', 10)]:
            with self.subTest(k=k, n=n):
                with self.assertRaises(ValueError):
                    wilson(k, n)


if __name__ == '__main__':
    unittest.main()
