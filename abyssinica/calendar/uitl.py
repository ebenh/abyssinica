"""
- The Julian epoch is November 24, 4713 BC (GC) and is assigned Julian day number 0
- The year 1 is preceded by hte year 0 for mathematical convenience
"""
from typing import Dict

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
def to_julian_day_number(Y: int, M: int, D: int, calendar_type: str) -> int:
    if calendar_type == 'GREGORIAN':
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
    if calendar_type == 'GREGORIAN':
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
