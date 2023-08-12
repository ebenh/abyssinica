import math
from datetime import datetime

_LEAP_YEAR_CYCLE_DAYS = 1461
"""This constant represents a full leap year cycle consisting of four years of 365 days each plus one extra leap day. 
This figure can be derived from (365 * 4) + 1 or 365.25 * 4"""


def get_leap_year_cycles(ordinal_date):
    """For a given ordinal date, this method returns the following two-tuple:\n
    - An integer representing the count of full leap year cycles that have occurred, and
    - An integer representing the remaining fraction of a leap year cycle expressed in days.
    """
    return divmod(ordinal_date, _LEAP_YEAR_CYCLE_DAYS)


def get_year(ordinal_date):
    full_leap_year_cycle_count, remainder_days = get_leap_year_cycles(ordinal_date)
    return (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365)


def get_day_of_year(ordinal_date):
    _, remainder_days = get_leap_year_cycles(ordinal_date)
    return my_mod(remainder_days, 366) if remainder_days == 0 else my_mod(remainder_days, 365)


def get_month(ordinal_date):
    day_of_year = get_day_of_year(ordinal_date)
    return math.ceil(day_of_year/30) if day_of_year <= 360 else 13


def get_day_of_month(ordinal_date):
    day_of_year = get_day_of_year(ordinal_date)
    return my_mod(day_of_year, 30)


def my_mod(x, k):
    return ((x - 1) % k) + 1


if __name__ == '__main__':
    print(get_month(1461-5))
