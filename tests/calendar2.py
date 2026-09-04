import unittest
from datetime import date, datetime

from abyssinica.calendar.date2 import Date as EthiopicDate


class TestDate(unittest.TestCase):

    def test_is_leap_year(self):
        # Pagume 6 exists in years where year % 4 == 3
        self.assertTrue(EthiopicDate.is_leap_year(3))
        self.assertTrue(EthiopicDate.is_leap_year(7))
        self.assertTrue(EthiopicDate.is_leap_year(11))
        self.assertTrue(EthiopicDate.is_leap_year(-1))
        self.assertTrue(EthiopicDate.is_leap_year(-5))

        self.assertFalse(EthiopicDate.is_leap_year(1))
        self.assertFalse(EthiopicDate.is_leap_year(2))
        self.assertFalse(EthiopicDate.is_leap_year(4))
        self.assertFalse(EthiopicDate.is_leap_year(0))

    def test_constructor_validation(self):
        # Valid dates
        EthiopicDate(1, 1, 1)
        EthiopicDate(1, 12, 30)
        EthiopicDate(1, 13, 5)
        EthiopicDate(3, 13, 6)  # Leap year, Pagume 6

        # Invalid month
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 0, 1)
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 14, 1)

        # Invalid day for regular month
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 1, 0)
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 1, 31)

        # Pagume 6 in a non-leap year
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 13, 6)

        # Pagume 7 even in a leap year
        with self.assertRaises(AssertionError):
            EthiopicDate(3, 13, 7)

    def test_to_jdn_known_epoch(self):
        # Meskerem 1, Year 1 EC = JDN 1724221
        self.assertEqual(1724221, EthiopicDate(1, 1, 1).to_jdn())

    def test_jdn_round_trip(self):
        test_dates = [
            (-4720, 1, 1),
            (-1, 1, 1),
            (0, 1, 1),
            (1, 1, 1),
            (3, 13, 5),
            (3, 13, 6),   # Leap day
            (4, 1, 1),
            (7, 13, 6),   # Another leap day
            (2016, 1, 1),
            (2017, 6, 15),
        ]
        for y, m, d in test_dates:
            with self.subTest(date=(y, m, d)):
                jdn = EthiopicDate(y, m, d).to_jdn()
                result = EthiopicDate.from_jdn(jdn)
                self.assertEqual(y, result.year)
                self.assertEqual(m, result.month)
                self.assertEqual(d, result.day)

    def test_jdn_matches_cryptic_algorithm(self):
        from abyssinica.calendar.uitl import to_julian_day

        test_dates = [
            (-4720, 1, 1),
            (-1, 1, 1),
            (0, 1, 1),
            (1, 1, 1),
            (3, 13, 6),
            (4, 1, 1),
            (2016, 1, 1),
            (2017, 13, 5),
        ]
        for y, m, d in test_dates:
            with self.subTest(date=(y, m, d)):
                expected = to_julian_day(y, m, d, 'ETHIOPIC')
                actual = EthiopicDate(y, m, d).to_jdn()
                self.assertEqual(expected, actual)

    def test_from_jdn_matches_cryptic_algorithm(self):
        from abyssinica.calendar.uitl import to_calendar

        test_jdns = [
            -124,        # Meskerem 1, -4720 EC
            0,           # Julian epoch
            1724221,     # Meskerem 1, Year 1 EC
            1725316,     # Pagume 6, Year 3 EC
            2460200,     # Meskerem 1, Year 2016 EC
        ]
        for jdn in test_jdns:
            with self.subTest(jdn=jdn):
                ey, em, ed = to_calendar(jdn, 'ETHIOPIC')
                result = EthiopicDate.from_jdn(jdn)
                self.assertEqual(ey, result.year)
                self.assertEqual(em, result.month)
                self.assertEqual(ed, result.day)

    def test_consecutive_days_at_year_boundary(self):
        # Non-leap year boundary (year 1 -> year 2)
        last_day = EthiopicDate(1, 13, 5)
        first_day = EthiopicDate(2, 1, 1)
        self.assertEqual(last_day.to_jdn() + 1, first_day.to_jdn())

        # Leap year boundary (year 3 -> year 4)
        last_day = EthiopicDate(3, 13, 6)
        first_day = EthiopicDate(4, 1, 1)
        self.assertEqual(last_day.to_jdn() + 1, first_day.to_jdn())

        # BC year boundary (year -1 -> year 0)
        last_day = EthiopicDate(-1, 13, 6)  # -1 is a leap year (-1 % 4 == 3)
        first_day = EthiopicDate(0, 1, 1)
        self.assertEqual(last_day.to_jdn() + 1, first_day.to_jdn())

    def test_year_lengths(self):
        # Non-leap year: 365 days
        self.assertEqual(
            365,
            EthiopicDate(2, 1, 1).to_jdn() - EthiopicDate(1, 1, 1).to_jdn()
        )

        # Leap year: 366 days
        self.assertEqual(
            366,
            EthiopicDate(4, 1, 1).to_jdn() - EthiopicDate(3, 1, 1).to_jdn()
        )

    def test_from_gregorian(self):
        # Test random dates
        self.assertEqual(EthiopicDate(2015, 12, 6), EthiopicDate.from_gregorian(date(2023, 8, 12)))
        self.assertEqual(EthiopicDate(2015, 11, 4), EthiopicDate.from_gregorian(date(2023, 7, 11)))
        self.assertEqual(EthiopicDate(2015, 7, 3), EthiopicDate.from_gregorian(date(2023, 3, 12)))
        self.assertEqual(EthiopicDate(2010, 11, 12), EthiopicDate.from_gregorian(date(2018, 7, 19)))
        self.assertEqual(EthiopicDate(2009, 6, 9), EthiopicDate.from_gregorian(date(2017, 2, 16)))
        self.assertEqual(EthiopicDate(1994, 9, 14), EthiopicDate.from_gregorian(date(2002, 5, 22)))
        self.assertEqual(EthiopicDate(1991, 1, 4), EthiopicDate.from_gregorian(date(1998, 9, 14)))

        # Test new years (leap year)
        self.assertEqual(EthiopicDate(2011, 13, 5), EthiopicDate.from_gregorian(date(2019, 9, 10)))
        self.assertEqual(EthiopicDate(2011, 13, 6), EthiopicDate.from_gregorian(date(2019, 9, 11)))
        self.assertEqual(EthiopicDate(2012, 1, 1), EthiopicDate.from_gregorian(date(2019, 9, 12)))

        # Test new years (non leap years)
        self.assertEqual(EthiopicDate(2012, 13, 5), EthiopicDate.from_gregorian(date(2020, 9, 10)))
        self.assertEqual(EthiopicDate(2013, 1, 1), EthiopicDate.from_gregorian(date(2020, 9, 11)))
        self.assertEqual(EthiopicDate(2013, 1, 2), EthiopicDate.from_gregorian(date(2020, 9, 12)))

        # Test a random date in the year following a leap year
        self.assertEqual(EthiopicDate(2012, 2, 23), EthiopicDate.from_gregorian(date(2019, 11, 3)))

        # Test the Beginning of the Incarnation Era (i.e. 1/1/1 AD)
        self.assertEqual(EthiopicDate(1, 1, 1), EthiopicDate.from_gregorian(date(8, 8, 27)))

        # Test the Annunciation
        self.assertEqual(EthiopicDate(1, 7, 29), EthiopicDate.from_gregorian(date(9, 3, 23)))

        # Test the Nativity (i.e. the first Christmas)
        self.assertEqual(EthiopicDate(2, 4, 29), EthiopicDate.from_gregorian(date(9, 12, 23)))

    def test_to_gregorian(self):
        # Test random dates
        self.assertEqual(date(2023, 8, 12), EthiopicDate(2015, 12, 6).to_gregorian())
        self.assertEqual(date(2023, 7, 11), EthiopicDate(2015, 11, 4).to_gregorian())
        self.assertEqual(date(2023, 3, 12), EthiopicDate(2015, 7, 3).to_gregorian())
        self.assertEqual(date(2018, 7, 19), EthiopicDate(2010, 11, 12).to_gregorian())
        self.assertEqual(date(2017, 2, 16), EthiopicDate(2009, 6, 9).to_gregorian())
        self.assertEqual(date(2002, 5, 22), EthiopicDate(1994, 9, 14).to_gregorian())
        self.assertEqual(date(1998, 9, 14), EthiopicDate(1991, 1, 4).to_gregorian())

        # Test new years (leap year)
        self.assertEqual(date(2019, 9, 10), EthiopicDate(2011, 13, 5).to_gregorian())
        self.assertEqual(date(2019, 9, 11), EthiopicDate(2011, 13, 6).to_gregorian())
        self.assertEqual(date(2019, 9, 12), EthiopicDate(2012, 1, 1).to_gregorian())

        # Test new years (non leap years)
        self.assertEqual(date(2020, 9, 10), EthiopicDate(2012, 13, 5).to_gregorian())
        self.assertEqual(date(2020, 9, 11), EthiopicDate(2013, 1, 1).to_gregorian())
        self.assertEqual(date(2020, 9, 12), EthiopicDate(2013, 1, 2).to_gregorian())

        # Test a random date in the year following a leap year
        self.assertEqual(date(2019, 11, 3), EthiopicDate(2012, 2, 23).to_gregorian())

        # Test the Beginning of the Incarnation Era (i.e. 1/1/1 AD)
        self.assertEqual(date(8, 8, 27), EthiopicDate(1, 1, 1).to_gregorian())

        # Test the Annunciation
        self.assertEqual(date(9, 3, 23), EthiopicDate(1, 7, 29).to_gregorian())

        # Test the Nativity (i.e. the first Christmas)
        self.assertEqual(date(9, 12, 23), EthiopicDate(2, 4, 29).to_gregorian())

    def test_weekday(self):
        # Year 0 in date2 = year -1 (1 BC) in date.py
        # First Tuesday
        self.assertEqual(1, EthiopicDate(0, 13, 5).weekday())

        # First Wednesday
        self.assertEqual(2, EthiopicDate(1, 1, 1).weekday())

        # First Thursday
        self.assertEqual(3, EthiopicDate(1, 1, 2).weekday())

        # First Friday
        self.assertEqual(4, EthiopicDate(1, 1, 3).weekday())

        # First Saturday
        self.assertEqual(5, EthiopicDate(1, 1, 4).weekday())

        # First Sunday
        self.assertEqual(6, EthiopicDate(1, 1, 5).weekday())

        # First Monday
        self.assertEqual(0, EthiopicDate(1, 1, 6).weekday())

        # First Tuesday
        self.assertEqual(1, EthiopicDate(1, 1, 7).weekday())

        # Make sure the Ethiopic and Gregorian calendars have the same day of the week
        today_gregorian = datetime.now().date()
        self.assertEqual(EthiopicDate.from_gregorian(today_gregorian).weekday(), today_gregorian.weekday())

    def test_equality(self):
        self.assertEqual(EthiopicDate(2017, 1, 1), EthiopicDate(2017, 1, 1))
        self.assertNotEqual(EthiopicDate(2017, 1, 1), EthiopicDate(2017, 1, 2))

    def test_comparison(self):
        self.assertLess(EthiopicDate(2017, 1, 1), EthiopicDate(2017, 1, 2))
        self.assertLessEqual(EthiopicDate(2017, 1, 1), EthiopicDate(2017, 1, 1))
        self.assertGreater(EthiopicDate(2017, 1, 2), EthiopicDate(2017, 1, 1))
        self.assertGreaterEqual(EthiopicDate(2017, 1, 1), EthiopicDate(2017, 1, 1))

    def test_isoformat(self):
        self.assertEqual('2017-01-01', EthiopicDate(2017, 1, 1).isoformat())
        self.assertEqual('0001-01-01', EthiopicDate(1, 1, 1).isoformat())

    def test_str(self):
        self.assertEqual('2017-01-01', str(EthiopicDate(2017, 1, 1)))

    def test_repr(self):
        d = EthiopicDate(2017, 1, 1)
        self.assertIn('Date', repr(d))
        self.assertIn('2017', repr(d))

    def test_today(self):
        eth_today = EthiopicDate.today()
        greg_today = datetime.now().date()
        self.assertEqual(eth_today, EthiopicDate.from_gregorian(greg_today))

    def test_matches_v1_for_ce_dates(self):
        """Verify date2 produces identical results to date.py for all CE dates in a range."""
        from abyssinica.calendar.date import Date as DateV1
        from datetime import timedelta

        d = date(1900, 1, 1)
        end = date(2025, 12, 31)
        while d <= end:
            v1 = DateV1.from_gregorian(d)
            v2 = EthiopicDate.from_gregorian(d)
            self.assertEqual(
                str(v1), str(v2),
                f'Mismatch for Gregorian {d}: v1={v1}, v2={v2}'
            )
            d += timedelta(days=1)
