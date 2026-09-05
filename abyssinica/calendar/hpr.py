"""
HPR is short for Hatcher, Parisot and Richards, the three authors behind
the equations in this file. It is our shorthand, since the method carries
no name of its own.

The equations convert between calendar dates and Julian day numbers, in
either direction, for the Julian, Gregorian and Ethiopic calendars.

Why the package does not use it
-------------------------------
The equations are general but cryptic. One set of steps serves a dozen
calendars, and everything that distinguishes one calendar from another
is hidden in a letter of the table. `date.py` works the Ethiopian
calendar out longhand instead, so that the arithmetic can be followed.
This module stays behind as a second implementation to test that one
against.

Where the equations come from
-----------------------------
D. A. Hatcher set them out in "Generalised Equations for Julian Day
Numbers and Calendar Dates", Quarterly Journal of the Royal Astronomical
Society 26 (1985), 151-155. J. P. Parisot added to them the following
year, and E. G. Richards elaborated them into the form used here.

That form is chapter 15, "Calendars", by Richards, in the Explanatory
Supplement to the Astronomical Almanac, 3rd edition, edited by Sean E.
Urban and P. Kenneth Seidelmann (University Science Books, 2013). The
chapter is online at
https://aa.usno.navy.mil/downloads/c15_usb_online.pdf

Conventions
-----------
The convention here is to take names straight from the chapter, so the
code can be read against it. The single letter variables are its own, and
the two functions are named for what its algorithms do.

The constants below are its Table 15.14, "Selected arithmetic calendars,
with parameters for algorithms". `to_julian_day` is its Algorithm 3 and
`to_calendar` its Algorithm 4, both from section 15.11.3, "Interconverting
Dates and Julian Day Numbers", on pages 618 and 619.
"""
from typing import Tuple

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
def to_calendar(J: int, calendar_type: str) -> Tuple[int, int, int]:
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
