import math
from datetime import date
from abyssinica.calendar.uitl import to_julian_day


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

    _JULIAN_DAY_OFFSET = 124

    _MIN_YEAR = -4721

    def __init__(self, year: int, month: int, day: int):
        assert year != 0, '0 is not a valid year'
        assert year >= -4721, 'Dates before 01/01/4721 BC are not supported'
        assert 1 <= month <= 13

        if month <= 12:
            assert 1 <= day <= 30
        elif Date.is_leap_year(year+1):
            # Leap days are added in years preceding leap years
            assert 1 <= day <= 6
        else:
            assert 1 <= day <= 5

        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls) -> 'Date':
        return cls.from_gregorian(date.today())

    @classmethod
    def fromtimestamp(cls, t: int) -> 'Date':
        return cls.from_gregorian(date.fromtimestamp(t))

    @classmethod
    def fromordinal(cls, ethiopic_day: int) -> 'Date':
        """
        :param ethiopic_day: The cumulative count of days since 1/1/-1.
        :return: A `Date` object corresponding to the Ethiopic day number
        """
        return Date.from_gregorian(date.fromordinal(ethiopic_day + Date._GREGORIAN_OFFSET_DAYS))

    def toordinal(self) -> int:
        """
        :return: The cumulative count of days since 1/1/-1.
        """
        assert self.year >= 1, 'This method is only supported for dates greater than or equal to 1/1/1'
        full_leap_year_cycle_count, remainder_years = divmod(self.year, 4)
        num_days_before_year = (full_leap_year_cycle_count * self._LEAP_YEAR_CYCLE_DAYS) + (remainder_years * 365)
        num_days_before_month = (self.month - 1) * 30
        return num_days_before_year + num_days_before_month + self.day

    def to_julian_day(self) -> int:
        year_count = abs(self._MIN_YEAR + 1) + self.year
        full_leap_year_cycle_count, remainder_years = divmod(year_count, 4)
        num_days_before_year = (full_leap_year_cycle_count * self._LEAP_YEAR_CYCLE_DAYS) + (remainder_years * 365)
        num_days_before_month = (self.month - 1) * 30
        ethiopic_day = num_days_before_year + num_days_before_month + self.day
        julian_day = ethiopic_day - self._JULIAN_DAY_OFFSET - 1
        return julian_day

    @classmethod
    def from_gregorian(cls, gregorian_date: date) -> 'Date':
        # ethiopic_day = gregorian_date.toordinal() - Date._GREGORIAN_OFFSET_DAYS

        julian_day = to_julian_day(gregorian_date.year, gregorian_date.month, gregorian_date.day, 'GREGORIAN')

        ethiopic_day = julian_day + Date._JULIAN_DAY_OFFSET + 1  # added 125

        full_leap_year_cycle_count, remainder_days = Date._get_leap_year_cycles(ethiopic_day)

        year = Date._get_year(full_leap_year_cycle_count, remainder_days)

        day_of_year = Date._get_day_of_year(remainder_days)

        month = Date._get_month(day_of_year)
        day = Date._get_day_of_month(day_of_year)

        return cls(year, month, day)

    def to_gregorian(self) -> date:
        gregorian_day = self.toordinal() + Date._GREGORIAN_OFFSET_DAYS
        return date.fromordinal(gregorian_day)

    @staticmethod
    def _get_leap_year_cycles(ethiopic_day: int):
        """
        :param ethiopic_day: The cumulative count of days since 1/1/-1.
        :return: A two-tuple consisting of (1) An integer representing the count of full leap year cycles that have
                 occurred, and (2) An integer representing the remaining fraction of a leap year cycle expressed in
                 days.
        """
        # assert ethiopic_day > 365, 'Dates before 1/1/1 are not supported'
        return divmod(ethiopic_day, Date._LEAP_YEAR_CYCLE_DAYS)

    @staticmethod
    def _get_year(full_leap_year_cycle_count: int, remainder_days: int) -> int:
        assert full_leap_year_cycle_count >= 0
        assert 0 <= remainder_days < Date._LEAP_YEAR_CYCLE_DAYS
        if full_leap_year_cycle_count == 0:
            assert remainder_days > 0, 'Invalid arguments'
        year_count = (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365)
        year = Date._MIN_YEAR + year_count
        year = year - 1 if year <= 0 else year  # Make the year look right 0 -> 1 BC, 1 -> 2 BC
        return year

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
    def _circular_index(idx: int, k: int):
        """
        Cycles the index `idx` within the range [1, k]
        :param idx: The index
        :param k: The upper bound for the circular range
        :return: The index `idx` wrapped around within the range [1, k]
        """
        return ((idx - 1) % k) + 1

    def weekday(self) -> int:
        """
        :return: Return day of the week, where Monday == 0 ... Sunday == 6
        """
        return self.toordinal() % 7

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Years divisible by four are designated as leap years, keep in mind that leap days are added in the years
        preceding leap years.
        :param year: The Ethiopic year
        :return: Whether the year is a leap year.
        """
        assert year != 0, '0 is not a valid year'
        assert year >= -4721, 'Dates before 01/01/4721 BC are not supported'
        return year % 4 == 0

    def isoformat(self):
        """Return the date formatted according to ISO.

        This is 'YYYY-MM-DD'.

        References:
        - http://www.w3.org/TR/NOTE-datetime
        - http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        """
        return "%04d-%02d-%02d" % (self.year, self.month, self.day)

    def __str__(self) -> str:
        return self.isoformat()

    def __eq__(self, other: 'Date') -> bool:
        if isinstance(other, Date):
            return (self.year, self.month, self.day) == (other.year, other.month, other.day)
        else:
            return NotImplemented

    def __lt__(self, other: 'Date') -> bool:
        if isinstance(other, Date):
            return (self.year, self.month, self.day) < (other.year, other.month, other.day)
        else:
            return NotImplemented

    def __le__(self, other: 'Date') -> bool:
        if isinstance(other, Date):
            return (self.year, self.month, self.day) <= (other.year, other.month, other.day)
        else:
            return NotImplemented

    def __gt__(self, other: 'Date') -> bool:
        if isinstance(other, Date):
            return (self.year, self.month, self.day) > (other.year, other.month, other.day)
        else:
            return NotImplemented

    def __ge__(self, other: 'Date') -> bool:
        if isinstance(other, Date):
            return (self.year, self.month, self.day) >= (other.year, other.month, other.day)
        else:
            return NotImplemented

    def __repr__(self):
        return "%s.%s(%d, %d, %d)" % (self.__class__.__module__,
                                      self.__class__.__qualname__,
                                      self.year,
                                      self.month,
                                      self.day)
