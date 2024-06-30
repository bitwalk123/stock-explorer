import datetime
import datetime as dt
import re
import time

import pandas as pd
from PySide6.QtSql import QSqlQuery

from sqls.sql_trade import (
    sql_sel_max_date_from_trade,
    sql_sel_max_date_from_trade_less_date,
)
from structs.db_info import DBInfo

day1 = 86400


def conv_date_string(ts: pd.Timestamp) -> str:
    ts_int = int(ts.timestamp())
    date_str = str(conv_timestamp2date(ts_int))
    return date_str


def conv_pandas_timestamp(timestamp: int):
    datetime = pd.to_datetime(timestamp, unit='s')
    return datetime


def conv_timestamp2date(timestamp: int):
    """Convert timestamp to date
    """
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


def conv_timestamp2date_next(timestamp: int):
    """Convert timestamp to date of 1 day advance
    """
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


def conv_timestamp2year(timestamp: int) -> int:
    """Convert timestamp to year
    """
    date = str(pd.to_datetime(timestamp, unit='s'))
    pattern = re.compile(r'(\d{4})-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')
    m = pattern.match(date)
    if m:
        yyyy = int(m.group(1))
        return yyyy
    else:
        return 0


def get_day_timestamp(qdate) -> int:
    date_str = '%s-%s-%s 00:00:00+09:00' % (qdate.year(), qdate.month(), qdate.day())
    ts = pd.to_datetime(date_str)
    return (int(ts.timestamp()))


def get_elapsed(time_start: float) -> float:
    """Get elapsed time in second.

    Args:
        time_start (float): start time

    Returns:
        float: elapsed time in seconds
    """
    time_end = time.time()
    # elapsed seconds
    elapsed = (time_end - time_start)
    return elapsed


def get_latest_2dates() -> list:
    date_latest_before = 0
    date_latest = 0

    con = DBInfo.get_connection()
    if con.open():
        sql = sql_sel_max_date_from_trade()
        query = QSqlQuery(sql)
        if query.next():
            date_latest = query.value(0)

        if date_latest > 0:
            sql = sql_sel_max_date_from_trade_less_date(date_latest)
            query = QSqlQuery(sql)
            if query.next():
                date_latest_before = query.value(0)
        con.close()

    return [date_latest_before, date_latest]


def get_latest_date() -> int:
    date_latest = 0

    con = DBInfo.get_connection()
    if con.open():
        sql = sql_sel_max_date_from_trade()
        query = QSqlQuery(sql)
        if query.next():
            date_latest = query.value(0)
        con.close()

    return date_latest


def get_original_start() -> int:
    return int(dt.datetime(2020, 1, 1, 0, 0).timestamp())


def get_past_date(past):
    # today = int(pd.to_datetime(str(dt.date.today())).timestamp())
    now = int(time.time())
    today = now - now % day1

    year = 365.25 * day1
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


def get_past_month_day(num: int) -> int:
    month = 30 * day1
    now = int(time.time())
    today = now - now % day1
    past_month_day = today - num * month
    return past_month_day


def get_timestamp() -> pd.Timestamp:
    dt_now = datetime.datetime.now()
    return pd.to_datetime(dt_now)


def get_ymd() -> (int, int, int):
    now = dt.datetime.now()
    y = now.year
    m = now.month
    d = now.day
    return y, m, d
