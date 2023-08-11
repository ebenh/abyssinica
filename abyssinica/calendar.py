import math
from datetime import datetime

'''
|----|----|----|----|-|
0   365  730  1095 1460
D   M
00
01
02
03
04
05
06
07
08
09
10
11
12
13
14
'''


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


def get_year(ordinal_date):
    four_year_cycle = int(365.25 * 4)  # 1461
    a, b = divmod(ordinal_date, four_year_cycle)
    print(a, b)
    return (a * 4) + math.ceil(b / 365)


if __name__ == '__main__':
    print(get_year(365*4+2))
    # day_of_year, month_of_year, day_of_month, year = get_julian_date(1)
    # print(f'day_of_year {day_of_year}')
    # print(f'month_of_year {month_of_year}')
    # print(f'day_of_month {day_of_month}')
    # print(f'year {year}')
