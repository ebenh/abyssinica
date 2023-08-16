import math
from datetime import date, datetime
from typing import Tuple


class Date:
    _LEAP_YEAR_CYCLE_DAYS = 1461
    """
    This constant represents a full leap year cycle consisting of four years of 365 days each plus one extra leap day. 
    This figure can be derived from (365 * 4) + 1 or 365.25 * 4.
    """

    _GREGORIAN_OFFSET_DAYS = 2430
    """
    The difference in days between 1/1/-1 (Ethiopic) and 1/1/1 (Gregorian).
    """

    def __init__(self, year: int, month: int, day: int):
        assert year >= 1, 'Dates before 1/1/1 are not supported'
        assert 1 <= month <= 13

        if month <= 12:
            assert 1 <= day <= 30
        elif Date.is_leap_year(year):
            assert 1 <= day <= 6
        else:
            assert 1 <= day <= 5

        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def fromtimestamp(cls, t) -> 'Date':
        return cls.from_gregorian(date.fromtimestamp(t))

    @classmethod
    def today(cls) -> 'Date':
        return cls.from_gregorian(date.today())

    @classmethod
    def fromordinal(cls, ethiopic_day_number) -> 'Date':
        """
        :param ethiopic_day_number: The cumulative count of days since 1/1/-1.
        :return: A `Date` object corresponding to the Ethoipic day number
        """
        return Date.from_gregorian(date.fromordinal(ethiopic_day_number + Date._GREGORIAN_OFFSET_DAYS))

    def weekday(self) -> int:
        # Return day of the week, where Monday == 0 ... Sunday == 6
        return self.toordinal() % 7

    @staticmethod
    def is_leap_year(year: int) -> bool:
        assert year >= 1, 'Dates before 1/1/1 are not supported'
        return (year + 1) % 4 == 0

    def toordinal(self) -> int:
        """
        :return: The cumulative count of days since 1/1/-1.
        """
        full_leap_year_cycle_count, remainder_years = divmod(self.year, 4)
        num_days_before_year = (full_leap_year_cycle_count * self._LEAP_YEAR_CYCLE_DAYS) + (remainder_years * 365)
        num_days_before_month = (self.month - 1) * 30
        return num_days_before_year + num_days_before_month + self.day

    def to_gregorian(self) -> date:
        gregorian_day_number = self.toordinal() + Date._GREGORIAN_OFFSET_DAYS
        return date.fromordinal(gregorian_day_number)

    @classmethod
    def from_gregorian(cls, gregorian_date: date) -> 'Date':
        assert gregorian_date >= date(8, 8, 27), 'Dates before 1/1/1 are not supported'

        ethiopic_day_number = gregorian_date.toordinal() - Date._GREGORIAN_OFFSET_DAYS

        year, month, day = Date._ethiopic_day_number_to_ymd(ethiopic_day_number)

        return cls(year, month, day)

    @staticmethod
    def _ethiopic_day_number_to_ymd(ethiopic_day_number: int) -> Tuple[int, int, int]:
        """
        :param ethiopic_day_number: The cumulative count of days since 1/1/-1.
        :return: A three-tuple consisting of the year, month and day corresponding to the Ethiopic day number
        """
        full_leap_year_cycle_count, remainder_days = Date._get_leap_year_cycles(ethiopic_day_number)

        year = Date._get_year(full_leap_year_cycle_count, remainder_days)

        day_of_year = Date._get_day_of_year(remainder_days)

        month = Date._get_month(day_of_year)
        day = Date._get_day_of_month(day_of_year)

        return year, month, day

    @staticmethod
    def _get_leap_year_cycles(ethiopic_day_number: int):
        """
        :param ethiopic_day_number: The cumulative count of days since 1/1/-1.
        :return: A two-tuple consisting of (1) An integer representing the count of full leap year cycles that have
                 occurred, and (2) An integer representing the remaining fraction of a leap year cycle expressed in
                 days.
        """
        assert ethiopic_day_number > 365, 'Dates before 1/1/1 are not supported'
        return divmod(ethiopic_day_number, Date._LEAP_YEAR_CYCLE_DAYS)

    @staticmethod
    def _get_year(full_leap_year_cycle_count: int, remainder_days: int) -> int:
        assert full_leap_year_cycle_count >= 0
        assert 0 <= remainder_days < Date._LEAP_YEAR_CYCLE_DAYS
        if full_leap_year_cycle_count == 0:
            assert remainder_days > 365, 'Dates before 1/1/1 are not supported'
        return (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365) - 1

    @staticmethod
    def _get_day_of_year(remainder_days: int) -> int:
        assert 0 <= remainder_days < Date._LEAP_YEAR_CYCLE_DAYS
        return 366 if remainder_days == 0 else Date._circular_index(remainder_days, 365)

    @staticmethod
    def _get_month(day_of_year: int) -> int:
        assert 1 <= day_of_year <= 366
        return math.ceil(day_of_year / 30) if day_of_year <= 360 else 13

    @staticmethod
    def _get_day_of_month(day_of_year: int) -> int:
        assert 1 <= day_of_year <= 366
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

    def __str__(self):
        return f'{self.month}/{self.day}/{self.year}'

    def __eq__(self, other: 'Date'):
        return self.month == other.month and self.day == other.day and self.year == other.year


if __name__ == '__main__':
    print(datetime.now().date().weekday())
    print(Date.from_gregorian(datetime.now().date()).weekday())
    print(Date(1,1,1).weekday())
    # import locale
    # locale.setlocale(locale.LC_TIME, 'am_ET.UTF-8')
    # print(datetime.now().strftime('%B %a %A %U/%d/%Y'))
    # import locale
    # d = datetime.now().date()

    # available_locales = []
    # for l in locale.locale_alias.items():
    #     try:
    #         locale.setlocale(locale.LC_ALL, l[1])
    #         available_locales.append(l)
    #     except:
    #         pass
    #
    #
    # print(available_locales)
