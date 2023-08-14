import math
from datetime import datetime, date

_LEAP_YEAR_CYCLE_DAYS = 1461
"""
This constant represents a full leap year cycle consisting of four years of 365 days each plus one extra leap day. 
This figure can be derived from (365 * 4) + 1 or 365.25 * 4
"""

_GREGORIAN_OFFSET_DAYS = 2795


def _get_leap_year_cycles(ethiopic_day_number):
    """
    :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC of
                                the Ethiopic calendar.
    :return: A two-tuple consisting of (1) An integer representing the count of full leap year cycles that have
             occurred, and (2) An integer representing the remaining fraction of a leap year cycle expressed in days.
    """
    assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
    return divmod(ethiopic_day_number, _LEAP_YEAR_CYCLE_DAYS)


def _get_year(ethiopic_day_number: int) -> int:
    """
    :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC of the
                                Ethiopic calendar.
    :return: An integer representing the year
    """
    assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
    full_leap_year_cycle_count, remainder_days = _get_leap_year_cycles(ethiopic_day_number)
    return (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365) - 1


def _get_day_of_year(ethiopic_day_number: int) -> int:
    """
    :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC of
                                the Ethiopic calendar.
    :return: The cumulative count of days since the start of the year in the range [1, 365] for non-leap years, and
             [1, 366] for leap years.
    """
    assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
    _, remainder_days = _get_leap_year_cycles(ethiopic_day_number)
    return 366 if remainder_days == 0 else _my_mod(remainder_days, 365)


def _get_month(ethiopic_day_number: int) -> int:
    """
    :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC of
                                the Ethiopic calendar.
    :return: An integer representing the month of the year in the range [1, 13].
    """
    assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
    day_of_year = _get_day_of_year(ethiopic_day_number)
    return math.ceil(day_of_year / 30) if day_of_year <= 360 else 13


def _get_day_of_month(ethiopic_day_number: int) -> int:
    """
    :param ethiopic_day_number: The cumulative count of days since the first day of the first month of the year 1 BC of
                                the Ethiopic calendar.
    :return: An integer representing the day of the month in the range [1, 30].
    """
    assert ethiopic_day_number > 365, 'Dates before 1 AD of the Ethiopic calendar are not supported'
    day_of_year = _get_day_of_year(ethiopic_day_number)
    return _my_mod(day_of_year, 30)


def _my_mod(x, k):
    return ((x - 1) % k) + 1


def gregorian_to_ethiopic(gregorian_date: date) -> str:
    """
    :param gregorian_date:
    :return:
    """
    assert gregorian_date >= date(8, 8, 27), 'Dates before 1 AD of the Ethiopic calendar are not supported'
    ethiopic_day_number = gregorian_date.toordinal() - _GREGORIAN_OFFSET_DAYS + 365
    return f'{_get_month(ethiopic_day_number)}/{_get_day_of_month(ethiopic_day_number)}/{_get_year(ethiopic_day_number)}'


if __name__ == '__main__':
    # print(gregorian_to_ethiopic(date(2023, 8, 12)))  # 12/6/2015
    # print(gregorian_to_ethiopic(date(2023, 7, 11)))  # 11/4/2015
    # print(gregorian_to_ethiopic(date(2023, 3, 12)))  # 7/3/2015
    # print(gregorian_to_ethiopic(date(2019, 11, 3)))  # 2/23/2012 !this is off by one day!
    # print(gregorian_to_ethiopic(date(2018, 7, 19)))  # 11/12/2010
    # print(gregorian_to_ethiopic(date(2017, 2, 16)))  # 6/9/2009
    # print(gregorian_to_ethiopic(date(2002, 5, 22)))  # 9/14/1994
    # print(gregorian_to_ethiopic(date(1998, 9, 14)))  # 1/4/1991

    # print(gregorian_to_ethiopic(date(2019, 2, 28)))  # 6/21/2012
    # print(gregorian_to_ethiopic(date(2020, 2, 28)))  # 6/20/2012 !this is off by one day!
    # print(gregorian_to_ethiopic(date(2021, 2, 28)))  # 6/21/2013

    print(gregorian_to_ethiopic(date(2019, 9, 10)))  # Got 13/5/2011 Expected 13/5/2011
    print(gregorian_to_ethiopic(date(2019, 9, 11)))  # Got  1/1/2012 Expected 13/6/2011
    print(gregorian_to_ethiopic(date(1, 1, 1)))  # Got  1/1/2012 Expected 13/6/2011

    print(gregorian_to_ethiopic(date(8, 8, 27)))  # Got  1/1/2012 Expected 13/6/2011
