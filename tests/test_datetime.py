import unittest


class TestDate(unittest.TestCase):
    @staticmethod
    def _get_n_years(n: int) -> int:
        return 365 * n

    @staticmethod
    def _get_n_months(n: int) -> int:
        return 30 * n

    def test_get_year(self):
        from abyssinica.datetime import Date

        # Test 1 AD
        self.assertEqual(1, Date._get_year(0, TestDate._get_n_years(1) + 1))
        self.assertEqual(1, Date._get_year(0, TestDate._get_n_years(1) + 365))

        # Test 2 AD
        self.assertEqual(2, Date._get_year(0, TestDate._get_n_years(2) + 1))
        self.assertEqual(2, Date._get_year(0, TestDate._get_n_years(2) + 365))

        # Test 3 AD (leap year)
        self.assertEqual(3, Date._get_year(0, TestDate._get_n_years(3) + 1))
        self.assertEqual(3, Date._get_year(0, TestDate._get_n_years(3) + 365))
        self.assertEqual(3, Date._get_year(1, TestDate._get_n_years(0)))

        # Test 4 AD
        self.assertEqual(4, Date._get_year(1, TestDate._get_n_years(0) + 1))
        self.assertEqual(4, Date._get_year(1, TestDate._get_n_years(0) + 365))

        # Test 5 AD
        self.assertEqual(5, Date._get_year(1, TestDate._get_n_years(1) + 1))
        self.assertEqual(5, Date._get_year(1, TestDate._get_n_years(1) + 365))

    def test_get_day_of_year(self):
        from abyssinica.datetime import Date

        # Year 1
        self.assertEqual(1, Date._get_day_of_year(TestDate._get_n_years(0) + 1))
        self.assertEqual(365, Date._get_day_of_year(TestDate._get_n_years(0) + 365))

        # Year 2
        self.assertEqual(1, Date._get_day_of_year(TestDate._get_n_years(1) + 1))
        self.assertEqual(365, Date._get_day_of_year(TestDate._get_n_years(1) + 365))

        # Year 3 (leap year)
        self.assertEqual(1, Date._get_day_of_year(TestDate._get_n_years(2) + 1))
        self.assertEqual(365, Date._get_day_of_year(TestDate._get_n_years(2) + 365))

        # Year 4
        self.assertEqual(1, Date._get_day_of_year(TestDate._get_n_years(3) + 1))
        self.assertEqual(365, Date._get_day_of_year(TestDate._get_n_years(3) + 365))
        self.assertEqual(366, Date._get_day_of_year(TestDate._get_n_years(0)))

    def test_get_month(self):
        from abyssinica.datetime import Date

        # First month
        self.assertEqual(1, Date._get_month(TestDate._get_n_months(0) + 1))
        self.assertEqual(1, Date._get_month(TestDate._get_n_months(0) + 30))

        # Second month
        self.assertEqual(2, Date._get_month(TestDate._get_n_months(1) + 1))
        self.assertEqual(2, Date._get_month(TestDate._get_n_months(1) + 30))

        # Twelfth month
        self.assertEqual(12, Date._get_month(TestDate._get_n_months(11) + 1))
        self.assertEqual(12, Date._get_month(TestDate._get_n_months(11) + 30))

        # Thirteenth month
        self.assertEqual(13, Date._get_month(TestDate._get_n_months(12) + 1))
        self.assertEqual(13, Date._get_month(TestDate._get_n_months(12) + 5))
        self.assertEqual(13, Date._get_month(TestDate._get_n_months(12) + 6))

    def test_get_day_of_month(self):
        from abyssinica.datetime import Date

        # First month
        self.assertEqual(1, Date._get_day_of_month(TestDate._get_n_months(0) + 1))
        self.assertEqual(30, Date._get_day_of_month(TestDate._get_n_months(0) + 30))

        # Second month
        self.assertEqual(1, Date._get_day_of_month(TestDate._get_n_months(1) + 1))
        self.assertEqual(30, Date._get_day_of_month(TestDate._get_n_months(1) + 30))

        # Twelfth month
        self.assertEqual(1, Date._get_day_of_month(TestDate._get_n_months(11) + 1))
        self.assertEqual(30, Date._get_day_of_month(TestDate._get_n_months(11) + 30))

        # Thirteenth month
        self.assertEqual(1, Date._get_day_of_month(TestDate._get_n_months(12) + 1))
        self.assertEqual(5, Date._get_day_of_month(TestDate._get_n_months(12) + 5))
        self.assertEqual(6, Date._get_day_of_month(TestDate._get_n_months(12) + 6))

    def test_from_gregorian(self):
        from abyssinica.datetime import Date as EthiopicDate
        from datetime import date

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

        # Test 1/1/1
        self.assertEqual(EthiopicDate(1, 1, 1), EthiopicDate.from_gregorian(date(8, 8, 27)))

    def test_to_gregorian(self):
            from abyssinica.datetime import Date as EthiopicDate
            from datetime import date

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

            # Test 1/1/1
            self.assertEqual(date(8, 8, 27), EthiopicDate(1, 1, 1).to_gregorian())
