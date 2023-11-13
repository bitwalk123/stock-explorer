import datetime
import re


def get_date_str(m: re.Match) -> str:
    month = int(m.group(1))
    day = int(m.group(2))
    dt_now = datetime.datetime.now()
    year = dt_now.year
    value_date = '%4d/%02d/%02d' % (year, month, day)
    return value_date


def get_today_str():
    dt_now = datetime.datetime.now()
    year = dt_now.year
    month = dt_now.month
    day = dt_now.day
    value_date = '%4d/%02d/%02d' % (year, month, day)
    return value_date
