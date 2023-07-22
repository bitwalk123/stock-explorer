import datetime as dt
import re

import pandas as pd

day1 = 86400


def conv_timestamp2date_next(timestamp: int):
    # print('timestamp =', timestamp, type(timestamp))
    date = str(pd.to_datetime(timestamp + day1, unit='s'))
    pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})\s\d{2}:\d{2}:\d{2}')
    m = pattern.match(date)
    if m:
        yyyy = int(m.group(1))
        mm = int(m.group(2))
        dd = int(m.group(3))
        return dt.date(yyyy, mm, dd)
    else:
        return None


def conv_timestamp(timestamp: int):
    date = pd.to_datetime(timestamp, unit='s')
    return date
