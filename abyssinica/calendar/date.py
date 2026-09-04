from datetime import date


class Date:
    """
    Ethiopian calendar date using a simplified algorithm based on
    Julian Day Numbers.

    **All years here are astronomical**, where 1 AD corresponds to 1,
    1 BC corresponds to 0, 2 BC corresponds to -1, and so on. This avoids
    the discontinuity of historical year numbering, which has no year
    zero, and simplifies arithmetic. Years BC carry a minus sign rather
    than an era; drop the sign and add one to convert, so -4712 is
    4713 BC.

    **Dates are written mm/dd/yyyy**, with the calendar in parentheses:
    01/01/-4712 (Julian). Months are numbered rather than named, since
    the three calendars here name them differently.

    A Julian Day Number (JDN) is a continuous count of days, starting from
    zero, since the beginning of the Julian period: 01/01/-4712 (Julian).
    It provides a single integer for any calendar date, making it a
    convenient intermediary for converting between calendar systems.

    The algorithm converts between an "Ethiopian Day Number" (EDN) and a
    "Gregorian Day Number" (GDN), using JDN as the intermediary. Each
    count starts from zero on its own epoch: JDN 0, EDN 0, GDN 0.
    """

    _EDN_OFFSET = 124
    """
    The offset between Julian Day Numbers and Ethiopian Day Numbers.

    We chose EDN 0 to be 01/01/-4720 (Ethiopic) because it is the 4-year
    leap cycle boundary in the Ethiopian calendar closest to JDN 0.

        JDN: -124                          JDN:   0
        EDN:    0                          EDN: 124
           |------------- 124 days -------------|
           |                                    |
    08/30/-4713 (Julian)               01/01/-4712 (Julian)
    01/01/-4720 (Ethiopic)             05/05/-4720 (Ethiopic)
    """

    _ETHIOPIC_LEAP_CYCLE_DAYS = 1_461
    """
    Days in one Ethiopian leap cycle: 365 * 4 + 1 = 1,461.

    The Ethiopian calendar adds a leap day every fourth year without
    exception, so every cycle is exactly this long.
    """

    _ETHIOPIC_YEAR_AT_EDN_0 = -4_720
    """
    The Ethiopian year that starts on EDN 0. Our algorithm counts years
    from 0, then adds this constant to turn that count into a real year.

    It is also the earliest year this class supports, since `from_jdn`
    requires an EDN of at least zero and so the count never goes negative.
    """

    _ETHIOPIC_YEAR_COUNT_BEFORE_INCARNATION = 5_500
    """
    The number of years the Ethiopian church attests existed before the
    Incarnation (the conception of Christ).
    """

    _GDN_OFFSET = 1_721_426
    """
    The offset between Julian Day Numbers and Gregorian Day Numbers.

    We chose GDN 0 to be 01/01/0001 (Gregorian) because it is the epoch
    of the proleptic Gregorian calendar. Proleptic means the calendar is
    extended backwards before its creation in 1582.

        JDN:           0                 JDN: 1,721,426
        GDN:  -1,721,426                 GDN:         0
                   |------- 1,721,426 days -------|
                   |                              |
        01/01/-4712 (Julian)            01/03/0001 (Julian)
        11/24/-4713 (Gregorian)         01/01/0001 (Gregorian)

    Python's `date` class counts the same days from one rather than zero,
    the established convention known as Rata Die, so a GDN is Python's
    number less one. That count is the interchange `date` expects for
    converting dates; it has no notion of Julian Day Numbers.
    """

    def __init__(self, year: int, month: int, day: int):
        assert year >= self._ETHIOPIC_YEAR_AT_EDN_0, \
            f'Dates before year {self._ETHIOPIC_YEAR_AT_EDN_0} are not supported'
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

    @property
    def is_incarnation_era(self) -> bool:
        """
        Ethiopian years are reckoned from the year Christ was conceived,
        an event called the Incarnation, which falls on 07/29/0001
        (Ethiopic). Every year from 1 onwards is in the Incarnation Era.
        """
        return self.year >= 1

    @property
    def creation_year(self) -> int:
        """
        The Ethiopian calendar only counts years forwards, never backwards
        as we do with years BC.

        Years are reckoned from two dates, the Incarnation (the conception
        of Christ) and the Creation (the creation of the world). Years
        before the Incarnation can only be expressed by counting forwards
        from the Creation, which starts at year 1.

        The church places the Incarnation 5,500 years after the Creation,
        so Ethiopian year 1 counts as 5,501.
        """
        return self._ETHIOPIC_YEAR_COUNT_BEFORE_INCARNATION + self.year

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
        edn = jdn + cls._EDN_OFFSET
        assert edn >= 0, 'Julian Day Number is before the earliest supported date'

        full_cycles, remainder_days = divmod(edn, cls._ETHIOPIC_LEAP_CYCLE_DAYS)

        year_in_cycle = min(remainder_days // 365, 3)
        year_number = full_cycles * 4 + year_in_cycle
        year = year_number + cls._ETHIOPIC_YEAR_AT_EDN_0

        day_of_year = remainder_days - year_in_cycle * 365

        month = day_of_year // 30 + 1 if day_of_year < 360 else 13
        day = day_of_year % 30 + 1

        return cls(year, month, day)

    def to_jdn(self) -> int:
        """
        Convert this date to a Julian Day Number.
        """
        year_number = self.year - self._ETHIOPIC_YEAR_AT_EDN_0
        full_cycles, cycle_year = divmod(year_number, 4)
        day_of_year = (self.month - 1) * 30 + (self.day - 1)
        edn = full_cycles * self._ETHIOPIC_LEAP_CYCLE_DAYS + cycle_year * 365 + day_of_year
        return edn - self._EDN_OFFSET

    @classmethod
    def from_gregorian(cls, gregorian_date: date) -> 'Date':
        """
        Create a Date from a `datetime.date`.
        """
        gdn = gregorian_date.toordinal() - 1
        return cls.from_jdn(gdn + cls._GDN_OFFSET)

    def to_gregorian(self) -> date:
        """
        Convert this date to a `datetime.date`.

        Raises `ValueError` for dates outside the range `datetime.date` can
        represent, which is 01/01/0001 (Gregorian) through 12/31/9999
        (Gregorian).
        """
        gdn = self.to_jdn() - self._GDN_OFFSET
        ordinal = gdn + 1
        if not date.min.toordinal() <= ordinal <= date.max.toordinal():
            raise ValueError(f'{self} (Ethiopic) is outside the range of datetime.date '
                             f'({date.min.isoformat()} to {date.max.isoformat()})')
        return date.fromordinal(ordinal)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Whether the given year has 366 days: a sixth day in the
        thirteenth month, Pagume, which otherwise has five.

        The extra day falls in years where year % 4 == 3, so years
        3, 7, 11, ... and -1, -5, -9, ...
        """
        return year % 4 == 3

    def weekday(self) -> int:
        """
        Return day of the week, where Monday == 0 ... Sunday == 6.
        """
        return self.to_jdn() % 7

    def isoformat(self):
        """Return the date formatted according to ISO.

        This is 'YYYY-MM-DD', and '-YYYY-MM-DD' for years before 1, whose
        minus sign precedes the four digits rather than counting as one
        of them.

        References:
        - http://www.w3.org/TR/NOTE-datetime
        - http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        """
        sign = '-' if self.year < 0 else ''
        return "%s%04d-%02d-%02d" % (sign, abs(self.year), self.month, self.day)

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
