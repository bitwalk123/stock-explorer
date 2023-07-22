import datetime as dt
import re

import pandas as pd


def conv_timestamp2date(timestamp: int):
    date = str(pd.to_datetime(timestamp, unit='s'))
    pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})\s\d{2}:\d{2}:\d{2}')
    m = pattern.match(date)
    if m:
        yyyy = int(m.group(1))
        mm = int(m.group(2))
        dd = int(m.group(3))
        return dt.date(yyyy, mm, dd)
    else:
        return None
