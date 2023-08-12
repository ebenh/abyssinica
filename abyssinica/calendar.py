import math
from datetime import datetime, date

_LEAP_YEAR_CYCLE_DAYS = 1461
"""This constant represents a full leap year cycle consisting of four years of 365 days each plus one extra leap day. 
This figure can be derived from (365 * 4) + 1 or 365.25 * 4"""

_GREGORIAN_OFFSET_DAYS = 2795


def _get_leap_year_cycles(ordinal_date):
    """For a given ordinal date, this method returns the following two-tuple:\n
    - An integer representing the count of full leap year cycles that have occurred, and
    - An integer representing the remaining fraction of a leap year cycle expressed in days.
    """
    return divmod(ordinal_date, _LEAP_YEAR_CYCLE_DAYS)


def _get_year(ordinal_date):
    full_leap_year_cycle_count, remainder_days = _get_leap_year_cycles(ordinal_date)
    return (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365)


def _get_day_of_year(ordinal_date):
    _, remainder_days = _get_leap_year_cycles(ordinal_date)
    return 366 if remainder_days == 0 else _my_mod(remainder_days, 365)


def _get_month(ordinal_date):
    day_of_year = _get_day_of_year(ordinal_date)
    return math.ceil(day_of_year/30) if day_of_year <= 360 else 13


def _get_day_of_month(ordinal_date):
    day_of_year = _get_day_of_year(ordinal_date)
    return _my_mod(day_of_year, 30)


def _my_mod(x, k):
    return ((x - 1) % k) + 1


def gregorian_to_ethiopic(date):
    ordinal_date = date.toordinal() - _GREGORIAN_OFFSET_DAYS
    return f'{_get_month(ordinal_date)}/{_get_day_of_month(ordinal_date)}/{_get_year(ordinal_date)}'


if __name__ == '__main__':
    print(gregorian_to_ethiopic(date(2023, 8, 12)))  # 12/6/2015
    print(gregorian_to_ethiopic(date(2023, 7, 11)))  # 11/4/2015
    print(gregorian_to_ethiopic(date(2023, 3, 12)))  # 7/3/2015
    print(gregorian_to_ethiopic(date(2019, 11, 3)))  # 2/23/2012 !this is off by one day!
    print(gregorian_to_ethiopic(date(2018, 7, 19)))  # 11/12/2010
    print(gregorian_to_ethiopic(date(2017, 2, 16)))  # 6/9/2009

