import unittest
from abyssinica import calendar


class TestDates(unittest.TestCase):
    def test_year(self):
        # year 1
        self.assertEqual(calendar.Date._get_year(365 * 0 + 1 + 365), 1)
        self.assertEqual(calendar.Date._get_year(365 * 0 + 365 + 365), 1)

        # year 2
        self.assertEqual(calendar.Date._get_year(365 * 1 + 1 + 365), 2)
        self.assertEqual(calendar.Date._get_year(365 * 1 + 365 + 365), 2)

        # year 3
        # self.assertEqual(calendar._get_year(365 * 2 + 1), 2)
        # self.assertEqual(calendar._get_year(365 * 2 + 365), 2)

        # year 4 ... this is a leap year
        self.assertEqual(calendar.Date._get_year(365 * 2 + 1 + 365), 3)
        self.assertEqual(calendar.Date._get_year(365 * 2 + 365 + 365), 3)
        self.assertEqual(calendar.Date._get_year(365 * 2 + 366 + 365), 3)

        # year 5
        self.assertEqual(calendar.Date._get_year(365.25 * 4 + 1 + 365), 5)
        self.assertEqual(calendar.Date._get_year(365.25 * 4 + 365 + 365), 5)

    def test_day_of_year(self):
        # year 1
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 0 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 0 + 365), 365)

        # year 2
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 1 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 1 + 365), 365)

        # year 3
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 2 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 2 + 365), 365)

        # year 4 ... this is a leap year
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 3 + 1 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 3 + 1 + 365), 365)
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 3 + 1 + 366), 1)

        # year 5
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 3 + 1), 366)
        self.assertEqual(calendar.Date._get_day_of_year(365 + 365 * 3 + 1 + 365), 365)

    def test_month(self):
        # first month
        self.assertEqual(calendar.Date._get_month(365 + 30 * 0 + 1), 1)
        self.assertEqual(calendar.Date._get_month(365 + 30 * 0 + 30), 1)

        # second month
        self.assertEqual(calendar.Date._get_month(365 + 30 * 1 + 1), 2)
        self.assertEqual(calendar.Date._get_month(365 + 30 * 1 + 30), 2)

        # twelfth month
        self.assertEqual(calendar.Date._get_month(365 + 30 * 11 + 1), 12)
        self.assertEqual(calendar.Date._get_month(365 + 30 * 11 + 30), 12)

        # thirteenth month
        self.assertEqual(calendar.Date._get_month(365 + 30 * 12 + 1), 13)
        self.assertEqual(calendar.Date._get_month(365 + 30 * 12 + 5), 13)
        self.assertEqual(calendar.Date._get_month(365 + 30 * 12 + 6), 1)

        # thirteenth month ... leapyear
        self.assertEqual(calendar.Date._get_month(365 + 365 * 3 + 1 - 5), 13)
        self.assertEqual(calendar.Date._get_month(365 + 365 * 3 + 1 - 0), 13)
        self.assertEqual(calendar.Date._get_month(365 + 365 * 3 + 1 + 1), 1)

    def test_day_of_month(self):
        # first month
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 0 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 0 + 30), 30)

        # second month
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 1 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 1 + 30), 30)

        # twelfth month
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 11 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 11 + 30), 30)

        # thirteenth month
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 12 + 1), 1)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 12 + 5), 5)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 30 * 12 + 6), 1)

        # thirteenth month ... leapyear
        self.assertEqual(calendar.Date._get_day_of_month(365 + 365 * 3 + 1 - 5), 1)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 365 * 3 + 1 - 0), 6)
        self.assertEqual(calendar.Date._get_day_of_month(365 + 365 * 3 + 1 + 1), 1)

    def test_gregorian_to_ethoipic(self):
        from datetime import date
        self.assertEqual(calendar.Date.from_gregorian(date(2023, 8, 12)), calendar.Date(2015, 12, 6))
        self.assertEqual(calendar.Date.from_gregorian(date(2023, 7, 11)), calendar.Date(2015, 11, 4))
        self.assertEqual(calendar.Date.from_gregorian(date(2023, 3, 12)), calendar.Date(2015, 7, 3))
        self.assertEqual(calendar.Date.from_gregorian(date(2018, 7, 19)), calendar.Date(2010, 11, 12))
        self.assertEqual(calendar.Date.from_gregorian(date(2017, 2, 16)), calendar.Date(2009, 6, 9))
        self.assertEqual(calendar.Date.from_gregorian(date(2002, 5, 22)), calendar.Date(1994, 9, 14))
        self.assertEqual(calendar.Date.from_gregorian(date(1998, 9, 14)), calendar.Date(1991, 1, 4))

        # test leap year...
        self.assertEqual(calendar.Date.from_gregorian(date(2019, 9, 10)), calendar.Date(2011, 13, 5))
        self.assertEqual(calendar.Date.from_gregorian(date(2019, 9, 11)),  calendar.Date(2011, 13, 6))
        self.assertEqual(calendar.Date.from_gregorian(date(2019, 9, 12)), calendar.Date(2012, 1, 1))

        # test non-leap year... Not a leap year so new years comes on day earlier
        self.assertEqual(calendar.Date.from_gregorian(date(2020, 9, 10)), calendar.Date(2012, 13, 5))
        self.assertEqual(calendar.Date.from_gregorian(date(2020, 9, 11)), calendar.Date(2013, 1, 1))
        self.assertEqual(calendar.Date.from_gregorian(date(2020, 9, 12)), calendar.Date(2013, 1, 2))

        # test the year following a leap year
        self.assertEqual(calendar.Date.from_gregorian(date(2019, 11, 3)),calendar.Date(2012, 2, 23))

        # test 1/1/1
        self.assertEqual(calendar.Date.from_gregorian(date(8, 8, 27)), calendar.Date(1, 1, 1))