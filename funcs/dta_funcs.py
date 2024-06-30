import datetime
import os
import re

import numpy as np
import pandas as pd
from PySide6.QtSql import QSqlQuery

from sqls.sql_trade_day import sql_sel_all_from_trade1m_with_dates_id_code_datetimes
from structs.db_info import DBInfo


def dta_get_data_from_db1m(id_code: int, start: int, end: int) -> pd.DataFrame:
    list_series = list()
    con = DBInfo.get_connection()
    if con.open():
        query = QSqlQuery()
        sql = sql_sel_all_from_trade1m_with_dates_id_code_datetimes(id_code, start, end)
        query.exec(sql)
        while query.next():
            date_time = query.value(0)  # "Datetime"
            dict_stock = dict()
            dict_stock['Open'] = query.value(1)  # "Open"
            dict_stock['High'] = query.value(2)  # "High"
            dict_stock['Low'] = query.value(3)  # "Low"
            dict_stock['Close'] = query.value(4)  # "Close"
            dict_stock['Volume'] = query.value(5)  # "Volume"
            series = pd.Series(data=dict_stock, name=date_time)
            list_series.append(series)
        con.close()

    if len(list_series) > 0:
        df = dta_prep_df_for1m(list_series)
    else:
        df = dta_prep_df_for1m_blank()

    return df


def dta_get_ref_times(date_str) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    # for morning session
    t1 = pd.to_datetime(date_str + ' 09:00:00')
    # for afternoon session
    t2 = pd.to_datetime(date_str + ' 10:00:00')
    # middle of lunchtime
    t3 = pd.to_datetime(date_str + ' 12:00:00')

    return t1, t2, t3


def dta_get_ref_times_JST(date_str) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    # for morning session
    t1_origin = pd.to_datetime(date_str + ' 09:00:00+09:00')
    t1_end = pd.to_datetime(date_str + ' 11:30:00+09:00')
    # for afternoon session
    t2_origin = pd.to_datetime(date_str + ' 09:59:00+09:00')
    t2_start = pd.to_datetime(date_str + ' 12:30:00+09:00')

    return t1_origin, t1_end, t2_origin, t2_start


def dta_get_ticker_filelist(ticker: str):
    dir_path = 'cache'
    pattern = re.compile(r'%s/%s.+\.pkl$' % (dir_path, ticker))
    # print(pattern)
    list_file = [
        os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
    ]
    # print(list_file)
    list_target = list()
    for f in list_file:
        if pattern.match(f):
            list_target.append(f)
    list_target.sort()
    # print(list_target)

    # list_target = [list_target[0]]
    return list_target


def dta_prep_candle1m(date_str: str, df: pd.DataFrame) -> tuple[np.array, np.array]:
    t1_origin, t1_end, t2_origin, t2_start = dta_get_ref_times_JST(date_str)

    df1 = df.loc[df.index[df.index <= t1_end]]
    df2 = df.loc[df.index[df.index >= t2_start]]

    df11 = df1.copy()
    df11.index = [(t - t1_origin).total_seconds() for t in df1.index]

    df21 = df2.copy()
    df21.index = [(t - t2_origin).total_seconds() for t in df2.index]

    df0 = pd.concat([df11, df21])

    array_x = np.array([x for x in df0.index])
    array_y = np.array(df0['Close'])

    return array_x, array_y


def dta_prep_df_for1m(list_series: list) -> pd.DataFrame:
    df = pd.concat(list_series, axis=1).T
    list_dt = [datetime.datetime.fromtimestamp(ts, datetime.timezone.utc) for ts in df.index]
    list_dt_jst = [dt.astimezone(datetime.timezone(datetime.timedelta(hours=9))) for dt in list_dt]
    df.index = list_dt_jst
    df.index.name = 'Datetime'

    return df


def dta_prep_df_for1m_blank() -> pd.DataFrame:
    df = pd.DataFrame({'Open': [], 'Low': [], 'High': [], 'Close': [], 'Volume': []})
    df.index.name = 'Datetime'

    return df


def dta_prep_realtime(date_str: str, df: pd.DataFrame) -> tuple[np.array, np.array]:
    t1, t2, t_mid = dta_get_ref_times(date_str)

    df1 = df.loc[df.index[df.index < t_mid]]
    df2 = df.loc[df.index[df.index > t_mid]]

    df11 = df1.copy()
    df11.index = [(t - t1).total_seconds() for t in df1.index]

    df21 = df2.copy()
    df21.index = [(t - t2).total_seconds() for t in df2.index]

    # Sometimes, same timestamp exists such as 11:30, 15:30.
    # Such duplicates are avoided here.
    df3 = pd.concat([df11, df21])
    dict_data = dict()
    n = len(df3)
    for idx in range(n):
        series = df3.iloc[idx]
        value = series.iloc[0]
        key = series.name
        dict_data[key] = value

    df0 = pd.DataFrame(
        {'Price': dict_data.values()},
        index=list(dict_data.keys())
    )

    array_x = np.array([x for x in df0.index])
    array_y = np.array(df0['Price'])

    return array_x, array_y
