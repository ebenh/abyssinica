import unittest
from abyssinica import calendar


class TestDates(unittest.TestCase):
    def test_year(self):
        # year 1
        self.assertEqual(calendar._get_year(365 * 0 + 1), 1)
        self.assertEqual(calendar._get_year(365 * 0 + 365), 1)

        # year 2
        self.assertEqual(calendar._get_year(365 * 1 + 1), 2)
        self.assertEqual(calendar._get_year(365 * 1 + 365), 2)

        # year 3
        self.assertEqual(calendar._get_year(365 * 2 + 1), 3)
        self.assertEqual(calendar._get_year(365 * 2 + 365), 3)

        # year 4 ... this is a leap year
        self.assertEqual(calendar._get_year(365 * 3 + 1), 4)
        self.assertEqual(calendar._get_year(365 * 3 + 365), 4)
        self.assertEqual(calendar._get_year(365 * 3 + 366), 4)

        # year 5
        self.assertEqual(calendar._get_year(365.25 * 4 + 1), 5)
        self.assertEqual(calendar._get_year(365.25 * 4 + 365), 5)

    def test_day_of_year(self):
        # year 1
        self.assertEqual(calendar._get_day_of_year(365 * 0 + 1), 1)
        self.assertEqual(calendar._get_day_of_year(365 * 0 + 365), 365)

        # year 2
        self.assertEqual(calendar._get_day_of_year(365 * 1 + 1), 1)
        self.assertEqual(calendar._get_day_of_year(365 * 1 + 365), 365)

        # year 3
        self.assertEqual(calendar._get_day_of_year(365 * 2 + 1), 1)
        self.assertEqual(calendar._get_day_of_year(365 * 2 + 365), 365)

        # year 4 ... this is a leap year
        self.assertEqual(calendar._get_day_of_year(365 * 3 + 1), 1)
        self.assertEqual(calendar._get_day_of_year(365 * 3 + 365), 365)
        self.assertEqual(calendar._get_day_of_year(365 * 3 + 366), 366)

        # year 5
        self.assertEqual(calendar._get_day_of_year(365.25 * 4 + 1), 1)
        self.assertEqual(calendar._get_day_of_year(365.25 * 4 + 365), 365)

    def test_month(self):
        # first month
        self.assertEqual(calendar._get_month(30 * 0 + 1), 1)
        self.assertEqual(calendar._get_month(30 * 0 + 30), 1)

        # second month
        self.assertEqual(calendar._get_month(30 * 1 + 1), 2)
        self.assertEqual(calendar._get_month(30 * 1 + 30), 2)

        # twelfth month
        self.assertEqual(calendar._get_month(30 * 11 + 1), 12)
        self.assertEqual(calendar._get_month(30 * 11 + 30), 12)

        # thirteenth month
        self.assertEqual(calendar._get_month(30 * 12 + 1), 13)
        self.assertEqual(calendar._get_month(30 * 12 + 5), 13)
        self.assertEqual(calendar._get_month(30 * 12 + 6), 1)

        # thirteenth month ... leapyear
        self.assertEqual(calendar._get_month(365.25 * 4 - 5), 13)
        self.assertEqual(calendar._get_month(365.25 * 4 - 0), 13)
        self.assertEqual(calendar._get_month(365.25 * 4 + 1), 1)

    def test_day_of_month(self):
        # first month
        self.assertEqual(calendar._get_day_of_month(30 * 0 + 1), 1)
        self.assertEqual(calendar._get_day_of_month(30 * 0 + 30), 30)

        # second month
        self.assertEqual(calendar._get_day_of_month(30 * 1 + 1), 1)
        self.assertEqual(calendar._get_day_of_month(30 * 1 + 30), 30)

        # twelfth month
        self.assertEqual(calendar._get_day_of_month(30 * 11 + 1), 1)
        self.assertEqual(calendar._get_day_of_month(30 * 11 + 30), 30)

        # thirteenth month
        self.assertEqual(calendar._get_day_of_month(30 * 12 + 1), 1)
        self.assertEqual(calendar._get_day_of_month(30 * 12 + 5), 5)
        self.assertEqual(calendar._get_day_of_month(30 * 12 + 6), 1)

        # thirteenth month ... leapyear
        self.assertEqual(calendar._get_day_of_month(365.25 * 4 - 5), 1)
        self.assertEqual(calendar._get_day_of_month(365.25 * 4 - 0), 6)
        self.assertEqual(calendar._get_day_of_month(365.25 * 4 + 1), 1)

    def test_gregorian_to_ethoipic(self):
        from datetime import date
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2023, 8, 12)), '12/6/2015')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2023, 7, 11)), '11/4/2015')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2023, 3, 12)), '7/3/2015')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2018, 7, 19)), '11/12/2010')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2017, 2, 16)), '6/9/2009')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2002, 5, 22)), '9/14/1994')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(1998, 9, 14)), '1/4/1991')

        # test leap year...
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2019, 9, 10)), '13/5/2011')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2019, 9, 11)),  '13/6/2011')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2019, 9, 12)), '1/1/2012')

        # test non-leap year... Not a leap year so new years comes on day earlier
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2020, 9, 10)), '13/5/2012')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2020, 9, 11)), '1/1/2013')
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2020, 9, 12)), '1/2/2013')

        # test the year following a leap year
        self.assertEqual(calendar.gregorian_to_ethiopic(date(2019, 11, 3)),'2/23/2012')