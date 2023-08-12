import math
from datetime import datetime

_LEAP_YEAR_CYCLE_DAYS = 1461
"""This constant represents a full leap year cycle consisting of four years of 365 days each plus one extra leap day. 
This figure can be derived from (365 * 4) + 1 or 365.25 * 4"""


def get_julian_date(ordinal_date):
    # ordinal_date = datetime.now().toordinal()
    four_year_cycle = int(365.25 * 4)  # 1461

    # offset = -(7 * 365)  # Julian day corresponding to Ethiopian date 1/1/1
    offset = 0

    a, b = divmod(ordinal_date + offset, four_year_cycle)
    print(a, b)

    year = (a * 4) + (b // 364)
    day_of_year = 365 if b == 0 else b % 364
    if day_of_year <= 360:
        month_of_year, day_of_month = divmod(day_of_year, 30)
    else:
        month_of_year = 12
        day_of_month = (day_of_year - 360)

    return day_of_year + 1, month_of_year + 1, day_of_month + 1, year


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
    # day_of_year, month_of_year, day_of_month, year = get_julian_date(1)
    # print(f'day_of_year {day_of_year}')
    # print(f'month_of_year {month_of_year}')
    # print(f'day_of_month {day_of_month}')
    # print(f'year {year}')
