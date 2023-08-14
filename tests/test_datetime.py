import unittest


class TestDate(unittest.TestCase):
    @staticmethod
    def _get_n_years(n):
        return 365 * n

    @staticmethod
    def _get_n_months(n):
        return 30 * n

    def test_year(self):
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

    def test_day_of_year(self):
        from abyssinica.datetime import Date

        # Year 1
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(0) + 1), 1)
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(0) + 365), 365)

        # Year 2
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(1) + 1), 1)
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(1) + 365), 365)

        # Year 3 (leap year)
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(2) + 1), 1)
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(2) + 365), 365)

        # Year 4
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(3) + 1), 1)
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(3) + 365), 365)
        self.assertEqual(Date._get_day_of_year(TestDate._get_n_years(0)), 366)

    def test_month(self):
        from abyssinica.datetime import Date

        # First month
        self.assertEqual(Date._get_month(TestDate._get_n_months(0) + 1), 1)
        self.assertEqual(Date._get_month(TestDate._get_n_months(0) + 30), 1)

        # Second month
        self.assertEqual(Date._get_month(TestDate._get_n_months(1) + 1), 2)
        self.assertEqual(Date._get_month(TestDate._get_n_months(1) + 30), 2)

        # Twelfth month
        self.assertEqual(Date._get_month(TestDate._get_n_months(11) + 1), 12)
        self.assertEqual(Date._get_month(TestDate._get_n_months(11) + 30), 12)

        # Thirteenth month
        self.assertEqual(Date._get_month(TestDate._get_n_months(12) + 1), 13)
        self.assertEqual(Date._get_month(TestDate._get_n_months(12) + 5), 13)
        self.assertEqual(Date._get_month(TestDate._get_n_months(12) + 6), 13)

    def test_day_of_month(self):
        from abyssinica.datetime import Date

        # First month
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(0) + 1), 1)
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(0) + 30), 30)

        # Second month
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(1) + 1), 1)
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(1) + 30), 30)

        # Twelfth month
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(11) + 1), 1)
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(11) + 30), 30)

        # Thirteenth month
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(12) + 1), 1)
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(12) + 5), 5)
        self.assertEqual(Date._get_day_of_month(TestDate._get_n_months(12) + 6), 6)

    def test_gregorian_to_ethoipic(self):
        from abyssinica.datetime import Date as EthiopicDate
        from datetime import date as GregorianDate

        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2023, 8, 12)), EthiopicDate(2015, 12, 6))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2023, 7, 11)), EthiopicDate(2015, 11, 4))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2023, 3, 12)), EthiopicDate(2015, 7, 3))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2018, 7, 19)), EthiopicDate(2010, 11, 12))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2017, 2, 16)), EthiopicDate(2009, 6, 9))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2002, 5, 22)), EthiopicDate(1994, 9, 14))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(1998, 9, 14)), EthiopicDate(1991, 1, 4))

        # test leap year...
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2019, 9, 10)), EthiopicDate(2011, 13, 5))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2019, 9, 11)), EthiopicDate(2011, 13, 6))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2019, 9, 12)), EthiopicDate(2012, 1, 1))

        # test non-leap year... Not a leap year so new years comes on day earlier
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2020, 9, 10)), EthiopicDate(2012, 13, 5))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2020, 9, 11)), EthiopicDate(2013, 1, 1))
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2020, 9, 12)), EthiopicDate(2013, 1, 2))

        # test the year following a leap year
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(2019, 11, 3)),EthiopicDate(2012, 2, 23))

        # test 1/1/1
        self.assertEqual(EthiopicDate.from_gregorian(GregorianDate(8, 8, 27)), EthiopicDate(1, 1, 1))