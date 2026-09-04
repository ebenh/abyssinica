from datetime import date


class Date:
    """
    Ethiopian calendar date using a simplified algorithm based on
    Julian Day Numbers.

    A Julian Day Number (JDN) is a continuous count of days, starting
    from zero, since the beginning of the Julian period: January 1,
    4713 BC (Julian calendar). It provides a single integer for any
    calendar date, making it a convenient intermediary for converting
    between calendar systems.

    This implementation uses astronomical year numbering, where 1 AD
    corresponds to 1, 1 BC corresponds to 0, 2 BC corresponds to -1,
    and so on. This avoids the discontinuity of historical year
    numbering (which has no year zero) and simplifies arithmetic.

    The algorithm works by converting between JDN and an "Ethiopian
    Day Number" (EDN), where we chose EDN 0 to be Meskerem 1,
    -4720 EC, the 4-year leap cycle boundary in the Ethiopian
    calendar closest to JDN 0. The offset between JDN and EDN is
    124 days.

        EDN:    0                        EDN: 124
        JDN: -124                        JDN:   0
           |----------- 124 days -----------|
           |                                |
       EDN epoch                        JDN epoch
    (Aug 30, 4714 BC Julian)     (Jan 1, 4713 BC Julian)

    """

    _JDN_OFFSET = 124
    """
    The offset between Julian Day Numbers and Ethiopian Day Numbers.
    124 days separate JDN 0 (Jan 1, 4713 BC Julian) from the Ethiopian cycle
    start (Aug 30, 4714 BC Julian = Meskerem 1, -4720 EC).
    """

    _LEAP_YEAR_CYCLE_DAYS = 1_461
    """
    Days in a full 4-year leap cycle: 365 * 4 + 1 = 1,461.
    """

    _YEAR_OFFSET = 4_720
    """
    The offset to convert from a zero-based year count to an Ethiopian year
    in astronomical numbering. Year 0 in the count corresponds to Ethiopian year -4720.
    """

    _MIN_YEAR = -4_720
    """
    The earliest supported Ethiopian year (astronomical numbering).
    """

    _GREGORIAN_EPOCH_JDN = 1_721_426
    """
    The Julian Day Number of January 1, 1 A.D., the day Python numbers as
    ordinal 1.
    """

    _ORDINAL_OFFSET = _GREGORIAN_EPOCH_JDN - 1
    """
    The offset between Julian Day Numbers and Python's proleptic Gregorian
    ordinals, which count days from 1 at January 1, 1 A.D. Proleptic means the
    calendar is extended backwards before its creation in 1582 A.D.

    Ordinals are one based rather than zero based, so the epoch's own Julian
    Day Number is one too many to convert with. The offset is instead the
    Julian Day Number of ordinal day zero, the day before the epoch:

        ordinal:           0           1           2
        JDN:       1,721,425   1,721,426   1,721,427
                           |           |
                           |           +-- January 1, 1 A.D., the epoch,
                           |               returned by date.fromordinal(1)
                           +-- December 31, year 0, which datetime
                               cannot represent

        JDN = ordinal + 1,721,425

    Python's `date` class already knows the Gregorian leap year rules, so this
    single constant is all that is needed to hand a JDN over to the standard
    library. No Gregorian date arithmetic is performed here.
    """

    def __init__(self, year: int, month: int, day: int):
        assert year >= self._MIN_YEAR, f'Dates before year {self._MIN_YEAR} are not supported'
        assert 1 <= month <= 13

        if month <= 12:
            assert 1 <= day <= 30
        elif self.is_leap_year(year):
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
    def from_jdn(cls, jdn: int) -> 'Date':
        """
        Create a Date from a Julian Day Number.
        """
        edn = jdn + cls._JDN_OFFSET
        assert edn >= 0, 'Julian Day Number is before the earliest supported date'

        full_cycles, remainder_days = divmod(edn, cls._LEAP_YEAR_CYCLE_DAYS)

        year_in_cycle = min(remainder_days // 365, 3)
        year_number = full_cycles * 4 + year_in_cycle
        year = year_number - cls._YEAR_OFFSET

        day_of_year = remainder_days - year_in_cycle * 365

        month = day_of_year // 30 + 1 if day_of_year < 360 else 13
        day = day_of_year % 30 + 1

        return cls(year, month, day)

    def to_jdn(self) -> int:
        """
        Convert this date to a Julian Day Number.
        """
        year_number = self.year + self._YEAR_OFFSET
        full_cycles, cycle_year = divmod(year_number, 4)
        day_of_year = (self.month - 1) * 30 + (self.day - 1)
        edn = full_cycles * self._LEAP_YEAR_CYCLE_DAYS + cycle_year * 365 + day_of_year
        return edn - self._JDN_OFFSET

    @classmethod
    def from_gregorian(cls, gregorian_date: date) -> 'Date':
        """
        Create a Date from a `datetime.date`.
        """
        return cls.from_jdn(gregorian_date.toordinal() + cls._ORDINAL_OFFSET)

    def to_gregorian(self) -> date:
        """
        Convert this date to a `datetime.date`.

        Raises `ValueError` for dates outside the range `datetime.date` can
        represent, which is January 1, 1 A.D. through December 31, 9999 A.D.
        """
        ordinal = self.to_jdn() - self._ORDINAL_OFFSET
        if not date.min.toordinal() <= ordinal <= date.max.toordinal():
            raise ValueError(f'{self} E.C. is outside the range of datetime.date '
                             f'({date.min.isoformat()} to {date.max.isoformat()})')
        return date.fromordinal(ordinal)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Whether the given year has Pagume 6 (366 days).

        In the Ethiopian calendar, the extra day falls in years where year % 4 == 3
        (astronomical numbering). For example, years 3, 7, 11, ... and -1, -5, -9, ...
        """
        return year % 4 == 3

    def weekday(self) -> int:
        """
        Return day of the week, where Monday == 0 ... Sunday == 6.
        """
        return self.to_jdn() % 7

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
