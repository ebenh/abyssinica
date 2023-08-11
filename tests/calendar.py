import unittest
from abyssinica import calendar


class TestDates(unittest.TestCase):
    def test_year(self):
        # year 1
        self.assertEqual(calendar.get_year(365 * 0 + 1), 1)
        self.assertEqual(calendar.get_year(365 * 0 + 365), 1)
        self.assertEqual(calendar.get_year(365 * 0 + 366), 2)
        # year 2
        self.assertEqual(calendar.get_year(365 * 1 + 1), 2)
        self.assertEqual(calendar.get_year(365 * 1 + 365), 2)
        self.assertEqual(calendar.get_year(365 * 1 + 366), 3)

        # year 3
        self.assertEqual(calendar.get_year(365 * 2 + 1), 3)
        self.assertEqual(calendar.get_year(365 * 2 + 365), 3)
        self.assertEqual(calendar.get_year(365 * 2 + 366), 4)

        # year 4 ... this is a leap year
        self.assertEqual(calendar.get_year(365 * 3 + 1), 4)
        self.assertEqual(calendar.get_year(365 * 3 + 365), 4)
        self.assertEqual(calendar.get_year(365 * 3 + 366), 4)

        # year 5
        self.assertEqual(calendar.get_year(365.25 * 4 + 1), 5)
        self.assertEqual(calendar.get_year(365.25 * 4 + 365), 5)
        self.assertEqual(calendar.get_year(365.25 * 4 + 366), 6)

    def test_day(self):
        self.assertTrue(True)

