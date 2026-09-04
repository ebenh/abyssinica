import unittest
from datetime import date, datetime

from abyssinica.calendar.date import Date as EthiopicDate


class TestDate(unittest.TestCase):

    def test_is_leap_year(self):
        # A sixth day of month 13 exists in years where year % 4 == 3
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
        # There should be 30 days in months 1 to 12, and 5 in month 13,
        # or 6 when the year is a leap year
        EthiopicDate(1, 1, 1)
        EthiopicDate(1, 12, 30)
        EthiopicDate(1, 13, 5)
        EthiopicDate(3, 13, 6)  # leap day

        # There should be no month outside 1 to 13
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 0, 1)
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 14, 1)

        # There should be no day outside 1 to 30 in months 1 to 12
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 1, 0)
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 1, 31)

        # There should be no sixth day of month 13 in a non-leap year
        with self.assertRaises(AssertionError):
            EthiopicDate(1, 13, 6)

        # There should be no seventh day of month 13, even in a leap year
        with self.assertRaises(AssertionError):
            EthiopicDate(3, 13, 7)

    def test_to_jdn_known_epoch(self):
        # 01/01/0001 (Ethiopic) is JDN 1,724,221
        self.assertEqual(1_724_221, EthiopicDate(1, 1, 1).to_jdn())

    def test_jdn_round_trip(self):
        test_dates = [
            (-4720, 1, 1),
            (-1, 1, 1),
            (0, 1, 1),
            (1, 1, 1),
            (3, 13, 5),
            (3, 13, 6),   # leap day
            (4, 1, 1),
            (7, 13, 6),   # another leap day
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

    def test_to_jdn_matches_reference(self):
        """The util module is a separate implementation, used here as an oracle."""
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

    def test_from_jdn_matches_reference(self):
        """The util module is a separate implementation, used here as an oracle."""
        from abyssinica.calendar.uitl import to_calendar

        test_jdns = [
            -124,        # EDN 0, which is 01/01/-4720 (Ethiopic)
            0,           # the Julian period epoch, 05/05/-4720 (Ethiopic)
            1_724_221,   # 01/01/0001 (Ethiopic)
            1_725_316,   # 13/06/0003 (Ethiopic), a leap day
            2_460_200,   # 01/01/2016 (Ethiopic)
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

        # Negative leap year boundary (year -1 -> year 0)
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
        # Random dates
        self.assertEqual(EthiopicDate(2015, 12, 6), EthiopicDate.from_gregorian(date(2023, 8, 12)))
        self.assertEqual(EthiopicDate(2015, 11, 4), EthiopicDate.from_gregorian(date(2023, 7, 11)))
        self.assertEqual(EthiopicDate(2015, 7, 3), EthiopicDate.from_gregorian(date(2023, 3, 12)))
        self.assertEqual(EthiopicDate(2010, 11, 12), EthiopicDate.from_gregorian(date(2018, 7, 19)))
        self.assertEqual(EthiopicDate(2009, 6, 9), EthiopicDate.from_gregorian(date(2017, 2, 16)))
        self.assertEqual(EthiopicDate(1994, 9, 14), EthiopicDate.from_gregorian(date(2002, 5, 22)))
        self.assertEqual(EthiopicDate(1991, 1, 4), EthiopicDate.from_gregorian(date(1998, 9, 14)))

        # New year's day following a leap year, when month 13 has six days
        self.assertEqual(EthiopicDate(2011, 13, 5), EthiopicDate.from_gregorian(date(2019, 9, 10)))
        self.assertEqual(EthiopicDate(2011, 13, 6), EthiopicDate.from_gregorian(date(2019, 9, 11)))
        self.assertEqual(EthiopicDate(2012, 1, 1), EthiopicDate.from_gregorian(date(2019, 9, 12)))

        # New year's day following a non-leap year, when month 13 has five days
        self.assertEqual(EthiopicDate(2012, 13, 5), EthiopicDate.from_gregorian(date(2020, 9, 10)))
        self.assertEqual(EthiopicDate(2013, 1, 1), EthiopicDate.from_gregorian(date(2020, 9, 11)))
        self.assertEqual(EthiopicDate(2013, 1, 2), EthiopicDate.from_gregorian(date(2020, 9, 12)))

        # A random date in the year following a leap year
        self.assertEqual(EthiopicDate(2012, 2, 23), EthiopicDate.from_gregorian(date(2019, 11, 3)))

        # The beginning of the Incarnation Era, 01/01/0001 (Ethiopic)
        self.assertEqual(EthiopicDate(1, 1, 1), EthiopicDate.from_gregorian(date(8, 8, 27)))

        # The Annunciation
        self.assertEqual(EthiopicDate(1, 7, 29), EthiopicDate.from_gregorian(date(9, 3, 23)))

        # The Nativity, the first Christmas
        self.assertEqual(EthiopicDate(2, 4, 29), EthiopicDate.from_gregorian(date(9, 12, 23)))

    def test_to_gregorian(self):
        # Random dates
        self.assertEqual(date(2023, 8, 12), EthiopicDate(2015, 12, 6).to_gregorian())
        self.assertEqual(date(2023, 7, 11), EthiopicDate(2015, 11, 4).to_gregorian())
        self.assertEqual(date(2023, 3, 12), EthiopicDate(2015, 7, 3).to_gregorian())
        self.assertEqual(date(2018, 7, 19), EthiopicDate(2010, 11, 12).to_gregorian())
        self.assertEqual(date(2017, 2, 16), EthiopicDate(2009, 6, 9).to_gregorian())
        self.assertEqual(date(2002, 5, 22), EthiopicDate(1994, 9, 14).to_gregorian())
        self.assertEqual(date(1998, 9, 14), EthiopicDate(1991, 1, 4).to_gregorian())

        # New year's day following a leap year, when month 13 has six days
        self.assertEqual(date(2019, 9, 10), EthiopicDate(2011, 13, 5).to_gregorian())
        self.assertEqual(date(2019, 9, 11), EthiopicDate(2011, 13, 6).to_gregorian())
        self.assertEqual(date(2019, 9, 12), EthiopicDate(2012, 1, 1).to_gregorian())

        # New year's day following a non-leap year, when month 13 has five days
        self.assertEqual(date(2020, 9, 10), EthiopicDate(2012, 13, 5).to_gregorian())
        self.assertEqual(date(2020, 9, 11), EthiopicDate(2013, 1, 1).to_gregorian())
        self.assertEqual(date(2020, 9, 12), EthiopicDate(2013, 1, 2).to_gregorian())

        # A random date in the year following a leap year
        self.assertEqual(date(2019, 11, 3), EthiopicDate(2012, 2, 23).to_gregorian())

        # The beginning of the Incarnation Era, 01/01/0001 (Ethiopic)
        self.assertEqual(date(8, 8, 27), EthiopicDate(1, 1, 1).to_gregorian())

        # The Annunciation
        self.assertEqual(date(9, 3, 23), EthiopicDate(1, 7, 29).to_gregorian())

        # The Nativity, the first Christmas
        self.assertEqual(date(9, 12, 23), EthiopicDate(2, 4, 29).to_gregorian())

    def test_weekday(self):
        # Eight consecutive days across the start of year 1, which begins
        # on a Wednesday. The first is the last day of year 0, so it covers
        # every weekday once.
        self.assertEqual(1, EthiopicDate(0, 13, 5).weekday())  # Tuesday
        self.assertEqual(2, EthiopicDate(1, 1, 1).weekday())   # Wednesday
        self.assertEqual(3, EthiopicDate(1, 1, 2).weekday())   # Thursday
        self.assertEqual(4, EthiopicDate(1, 1, 3).weekday())   # Friday
        self.assertEqual(5, EthiopicDate(1, 1, 4).weekday())   # Saturday
        self.assertEqual(6, EthiopicDate(1, 1, 5).weekday())   # Sunday
        self.assertEqual(0, EthiopicDate(1, 1, 6).weekday())   # Monday
        self.assertEqual(1, EthiopicDate(1, 1, 7).weekday())   # Tuesday

        # The Ethiopic and Gregorian calendars should agree on the current day of the week
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

    def test_matches_reference_over_modern_range(self):
        # Every day from 01/01/1900 to 12/31/2025 (Gregorian), checked
        # against the util module rather than against a sibling
        from abyssinica.calendar.uitl import to_calendar
        from datetime import timedelta

        d = date(1900, 1, 1)
        end = date(2025, 12, 31)
        while d <= end:
            expected = to_calendar(d.toordinal() + 1_721_425, 'ETHIOPIC')
            actual = EthiopicDate.from_gregorian(d)
            self.assertEqual(
                expected, (actual.year, actual.month, actual.day),
                f'Mismatch for Gregorian {d}'
            )
            d += timedelta(days=1)
