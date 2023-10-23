import datetime as dt

import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_select_max_date_from_trade


def get_last_trading_date() -> int:
    end = 0
    sql = get_sql_select_max_date_from_trade()
    query = QSqlQuery(sql)
    while query.next():
        end = query.value(0)
    return end


def get_next_trading_date(end: int) -> int:
    day1 = 24 * 60 * 60
    day_last = dt.datetime.fromtimestamp(end)
    weekday = day_last.weekday()
    if weekday == 4:
        end_next = end + day1 * 3
    else:
        end_next = end + day1
    list_holiday = get_holiday_list()
    while end_next in list_holiday:
        end_next += day1
    return end_next


def get_holiday_list() -> list:
    tz_delta = 9 * 60 * 60
    file_holiday = 'holiday.csv'
    df = pd.read_csv(file_holiday)
    list_holiday = list()
    for date_str in df['DATE']:
        date_dt = dt.datetime.strptime(date_str, '%Y-%m-%d')
        date_int = int(date_dt.timestamp()) + tz_delta
        list_holiday.append(date_int)
    return list_holiday
