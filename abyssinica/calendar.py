import math
from datetime import date


class Date:
    _LEAP_YEAR_CYCLE_DAYS = 1461
    """
    This constant represents a full leap year cycle consisting of four years of 365 days each plus one extra leap day. 
    This figure can be derived from (365 * 4) + 1 or 365.25 * 4.
    """

    _GREGORIAN_OFFSET_DAYS = 2430
    """
    The difference in days between first day of the first month of the year 1 AD of the Gregorian calendar, and the first 
    day of the first month of the year 1 BC of the Ethiopic calendar.
    """

    def __init__(self, year: int, month: int, day: int):
        self._year = year
        self._month = month
        self._day = day

    @staticmethod
    def _get_leap_year_cycles(ethiopic_day_number: int):
        """
        :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC
                                    of the Ethiopic calendar.
        :return: A two-tuple consisting of (1) An integer representing the count of full leap year cycles that have
                 occurred, and (2) An integer representing the remaining fraction of a leap year cycle expressed in
                 days.
        """
        assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
        return divmod(ethiopic_day_number, Date._LEAP_YEAR_CYCLE_DAYS)

    @staticmethod
    def _get_year(ethiopic_day_number: int) -> int:
        """
        :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC
                                    of the Ethiopic calendar.
        :return: An integer representing the year in the range [1, inf)
        """
        assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
        full_leap_year_cycle_count, remainder_days = Date._get_leap_year_cycles(ethiopic_day_number)
        return (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365) - 1

    @staticmethod
    def _get_day_of_year(ethiopic_day_number: int) -> int:
        """
        :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC
                                    of the Ethiopic calendar.
        :return: The cumulative count of days since the start of the year. This value falls in the range [1, 365] for
                 non-leap years, and [1, 366] for leap years.
        """
        assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
        _, remainder_days = Date._get_leap_year_cycles(ethiopic_day_number)
        return 366 if remainder_days == 0 else Date._circular_index(remainder_days, 365)

    @staticmethod
    def _get_month(ethiopic_day_number: int) -> int:
        """
        :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC
                                    of the Ethiopic calendar.
        :return: An integer representing the month of the year in the range [1, 13].
        """
        assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
        day_of_year = Date._get_day_of_year(ethiopic_day_number)
        return math.ceil(day_of_year / 30) if day_of_year <= 360 else 13

    @staticmethod
    def _get_day_of_month(ethiopic_day_number: int) -> int:
        """
        :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC
                                    of the Ethiopic calendar.
        :return: An integer representing the day of the month in the range [1, 30].
        """
        assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
        day_of_year = Date._get_day_of_year(ethiopic_day_number)
        return Date._circular_index(day_of_year, 30)

    @staticmethod
    def _circular_index(idx, k):
        """
        Cycles the index `idx` within the range [1, k]
        :param idx: The index
        :param k: The upper bound for the circular range
        :return: The index `idx` wrapped around within the range [1, k]
        """
        return ((idx - 1) % k) + 1

    @staticmethod
    def from_gregorian(gregorian_date: date):
        """
        Create an Ethiopic `Date` object from a Gregorian `date` object
        :param gregorian_date: The Gregorian date.
        :return: The Ethiopic date.
        """
        assert gregorian_date >= date(8, 8, 27), 'Dates before 1 AD of the Ethiopic calendar are not supported'
        ethiopic_day_number = gregorian_date.toordinal() - Date._GREGORIAN_OFFSET_DAYS
        year = Date._get_year(ethiopic_day_number)
        month = Date._get_month(ethiopic_day_number)
        day = Date._get_day_of_month(ethiopic_day_number)
        return Date(year, month, day)

    def __str__(self):
        return f'{self._month}/{self._day}/{self._year}'

    def __eq__(self, other: 'Date'):
        return self._month == other._month and self._day == other._day and self._year == other._year


if __name__ == '__main__':
    pass
