import datetime as dt

import pandas as pd


def get_past_date(past):
    today = int(pd.to_datetime(str(dt.date.today())).timestamp())
    year = 365 * 24 * 60 * 60
    if past == '３ヵ月':
        return int(today - year / 4)
    elif past == '６ヵ月':
        return int(today - year / 2)
    elif past == '１年':
        return today - year
    elif past == '２年':
        return today - 2 * year
    else:
        return -1
