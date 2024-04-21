"""
- The Julian epoch is January 1, 4713 BC (JC) or November 24, 4714 BC (GC) and is assigned Julian day number 0
- The year 1 is preceded by the year 0 for mathematical convenience
"""
from typing import Dict

_JULIAN_CONSTANTS = {
    'y': 4716,
    'j': 1401,
    'm': 2,
    'n': 12,
    'r': 4,
    'p': 1461,
    'q': 0,
    'v': 3,
    'u': 5,
    's': 153,
    't': 2,
    'w': 2,
    'A': None,
    'B': None,
    'C': None,
}

_GREGORIAN_CONSTANTS = {
    'y': 4716,
    'j': 1401,
    'm': 2,
    'n': 12,
    'r': 4,
    'p': 1461,
    'q': 0,
    'v': 3,
    'u': 5,
    's': 153,
    't': 2,
    'w': 2,
    'A': 184,
    'B': 274277,
    'C': -38,
}

_ETHIOPIC_CONSTANTS = {
    'y': 4720,
    'j': 124,
    'm': 0,
    'n': 13,
    'r': 4,
    'p': 1461,
    'q': 0,
    'v': 3,
    'u': 1,
    's': 30,
    't': 0,
    'w': 0,
    'A': None,
    'B': None,
    'C': None,
}


# noinspection PyPep8Naming
def to_julian_day(Y: int, M: int, D: int, calendar_type: str) -> int:
    if calendar_type == 'JULIAN':
        c = _JULIAN_CONSTANTS
    elif calendar_type == 'GREGORIAN':
        c = _GREGORIAN_CONSTANTS
    elif calendar_type == 'ETHIOPIC':
        c = _ETHIOPIC_CONSTANTS
    else:
        assert False, 'Unknown calendar type'

    h = M - c['m']
    g = Y + c['y'] - (c['n'] - h) // c['n']
    f = (h - 1 + c['n']) % c['n']
    e = (c['p'] * g + c['q']) // c['r'] + D - 1 - c['j']
    J = e + (c['s'] * f + c['t']) // c['u']
    if calendar_type == 'GREGORIAN':
        J = J - (3 * ((g + c['A']) // 100)) // 4 - c['C']

    return J


# noinspection PyPep8Naming
def to_calendar(J: int, calendar_type: str) -> (int, int, int):
    if calendar_type == 'JULIAN':
        c = _JULIAN_CONSTANTS
    elif calendar_type == 'GREGORIAN':
        c = _GREGORIAN_CONSTANTS
    elif calendar_type == 'ETHIOPIC':
        c = _ETHIOPIC_CONSTANTS
    else:
        assert False, 'Unknown calendar type'

    f = J + c['j']
    if calendar_type == 'GREGORIAN':
        f = f + (((4 * J + c['B']) // 146097) * 3) // 4 + c['C']
    e = c['r'] * f + c['v']
    g = (e % c['p']) // c['r']
    h = c['u'] * g + c['w']
    D = (h % c['s']) // c['u'] + 1
    M = (h // c['s'] + c['m']) % c['n'] + 1
    Y = e // c['p'] - c['y'] + (c['n'] + c['m'] - M) // c['n']

    return Y, M, D


def my_test():
    from abyssinica.calendar.date import Date as EthoipicDate
    import math

    # Julian day number 0 corresponds to Monday, January 1, 4713 B.C. of the proleptic Julian calendar
    # The four year leap year cycle starts on August 30, 4714 BC (This corresponds to Meskerem 1)
    # There is a difference of 124 days between these two dates
    #
    # YEAR 0 is 1 BC!
    # -1   0    1
    # 2BC 1BC  1AD
    # To get the real year B.C. subtract one and take the absolute value
    jdn = to_julian_day(1, 1, 1, 'ETHIOPIC')
    print('JULIAN', to_calendar(jdn, 'JULIAN'))
    print('ETHIOPIC', to_calendar(jdn, 'ETHIOPIC'))
    # August 2 days
    # September 30 days
    # October 31 days
    # November 30 days
    # December 31 days
    # = 124 days
    edn = jdn + 124 + 1  # add one because all our math is one based!
    print('edn', edn)

    full_leap_year_cycle_count, remainder_days = divmod(edn, 1461)
    print('full_leap_year_cycle_count', full_leap_year_cycle_count, 'remainder_days', remainder_days)
    ethiopic_year_number = (full_leap_year_cycle_count * 4) + math.ceil(remainder_days / 365)

    # Julian day 1 is January 1, 4713 BC of proleptic julian calendar
    # There is an 8 year gap between Gregorian and Ethiopic between [Jan 1 and September 11]
    ethiopic_year = ethiopic_year_number - 4721
    # ethiopic_year = ethiopic_year - 1 if ethiopic_year <= 0 else ethiopic_year

    day_of_year = 366 if remainder_days == 0 else EthoipicDate._circular_index(remainder_days, 365)
    ethiopic_month = math.ceil(day_of_year / 30) if day_of_year <= 360 else 13
    ethopic_day_of_month = EthoipicDate._circular_index(day_of_year, 30)

    print(ethiopic_year, ethiopic_month, ethopic_day_of_month)

    """
    converter: https://aa.usno.navy.mil/data/JulianDate
    leap years: https://www.howtocreate.co.uk/php/leapyear.php
    
    01/01/4713 B.C. J.C. Julian day 0
    30/08/4714 B.C. J.C.
    01/01/4721 B.C. E.C. (subtract 7 years from previous)
    
            30/08/4714 B.C. J.C.         01/01/4713 B.C. J.C.
                  ^                             ^ 
                 -|-----------------------------+-----------------------
            01/01/4721 B.C. E.C.           Julian Day 0              
            
            
       Year No.     1  2  3  4  5  6  7  8
                   -6 -6 -6 -6 -6 -6 -6 -6
         Year       5  4  3  2  1  0  1  2      
    """
