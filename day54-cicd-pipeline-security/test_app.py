"""Unit tests for the Day 54 pipeline demo."""
import unittest

from app import calculate_total


class CalculateTotalTests(unittest.TestCase):
    def test_calculates_total(self):
        self.assertEqual(calculate_total(10, 3), 30)

    def test_rounds_to_two_decimal_places(self):
        self.assertEqual(calculate_total(2.555, 2), 5.11)

    def test_rejects_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_total(-1, 2)

    def test_rejects_negative_quantity(self):
        with self.assertRaises(ValueError):
            calculate_total(10, -1)


if __name__ == "__main__":
    unittest.main()
