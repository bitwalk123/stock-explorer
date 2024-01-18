import datetime as dt
from statistics import median
from typing import Union

import pandas as pd
import yfinance as yf

from PySide6.QtSql import QSqlQuery

from funcs.tbl_ticker import get_dict_code
from funcs.tide import (
    conv_pandas_timestamp,
    conv_timestamp2date_next,
    get_original_start,
)
from sqls.sql_ticker import (
    sql_sel_13sector_from_ticker_with_code,
    sql_sel_id_code_cname_from_ticker_with_code,
)
from sqls.sql_trade import (
    sql_create_tbl_trade,
    sql_drop_tbl_trade,
    sql_ins_into_trade_values,
    sql_sel_all_from_trade_with_id_code,
    sql_sel_all_from_trade_with_id_code_start,
    sql_sel_close_volume_from_trade_with_id_code_start,
    sql_sel_close_volume_from_trade_with_id_code,
    sql_sel_id_trade_from_trade_with_date_id_code,
    sql_sel_open_close_volume_from_trade_with_id_code_start,
    sql_sel_open_close_volume_from_trade_with_id_code,
    sql_sel_open_volume_from_trade_with_id_code_start,
    sql_sel_open_volume_from_trade_with_id_code,
    sql_sel_max_date_from_trade_with_id_code,
    sql_upd_trade_values, sql_sel_close_from_trade_with_id_code_start,
    sql_sel_max_date_from_trade_with_id_code_less_date,
)
from structs.db_info import DBInfo
from structs.trend_object import TrendObj


def add_rows_tbl_trade(df: pd.DataFrame, id_code: int):
    for row in df.index:
        timestamp = int(row.timestamp())
        series = df.loc[row].copy()
        series['Date'] = timestamp

        query = QSqlQuery()
        sql = sql_sel_id_trade_from_trade_with_date_id_code(id_code, timestamp)
        query.exec(sql)
        if query.next():
            id_trade = query.value(0)
            sql = sql_upd_trade_values(id_trade, series)
        else:
            sql = sql_ins_into_trade_values(id_code, series)
        if not query.exec(sql):
            print(query.lastError())


def create_tbl_trade():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_trade_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_trade_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_trade()
    if not query.exec(sql):
        print(query.lastError())


def drop_tbl_trade() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_trade()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


def get_date_close_with_id_code_start(id_code: int, start: int) -> pd.DataFrame:
    list_date = list()
    list_close = list()

    con = DBInfo.get_connection()
    if con.open():
        sql = sql_sel_close_from_trade_with_id_code_start(id_code, start)
        query = QSqlQuery(sql)
        while query.next():
            ds = conv_pandas_timestamp(query.value(0))
            list_date.append(ds)
            list_close.append(query.value(1))
        con.close()

        df = pd.DataFrame({
            'Date': list_date,
            'Close': list_close,
        })
        df.set_index('Date', inplace=True)

        return df
    else:
        return pd.DataFrame()


def get_max_date_from_trade_with_id_code_less_date(id_code: int, date: int) -> Union[int, None]:
    con = DBInfo.get_connection()
    if con.open():
        sql = sql_sel_max_date_from_trade_with_id_code_less_date(id_code, date)
        query = QSqlQuery(sql)
        if query.next():
            date_prev = query.value(0)
        else:
            date_prev = None
        con.close()
        return date_prev
    else:
        print('database can not be opened!')
        return None


def get_trade_with_code(code: str, start: int) -> tuple:
    cname = None
    list_date = list()
    list_open = list()
    list_high = list()
    list_low = list()
    list_close = list()
    list_volume = list()

    con = DBInfo.get_connection()
    if con.open():
        id_code = 0
        cname = ''
        sql = sql_sel_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            id_code = query.value(0)
            cname = query.value(1)

        if start > 0:
            sql = sql_sel_all_from_trade_with_id_code_start(id_code, start)
        else:
            sql = sql_sel_all_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            dt = conv_pandas_timestamp(query.value(0))
            list_date.append(dt)
            list_open.append(query.value(1))
            list_high.append(query.value(2))
            list_low.append(query.value(3))
            list_close.append(query.value(4))
            list_volume.append(query.value(5))
        con.close()

        df = pd.DataFrame(
            {
                'Date': list_date,
                'Open': list_open,
                'High': list_high,
                'Low': list_low,
                'Close': list_close,
                'Volume': list_volume,
            }
        )
        df.set_index('Date', inplace=True)
        return cname, df


def get_trend_object_candle(code: str, start: int) -> TrendObj:
    list_date = list()
    list_open = list()
    list_high = list()
    list_low = list()
    list_close = list()
    list_volume = list()

    con = DBInfo.get_connection()
    if con.open():
        id_code = 0
        cname = ''
        sql = sql_sel_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            id_code = query.value(0)
            cname = query.value(1)

        if start > 0:
            sql = sql_sel_all_from_trade_with_id_code_start(id_code, start)
        else:
            sql = sql_sel_all_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            ds = conv_pandas_timestamp(query.value(0))
            list_date.append(ds)
            list_open.append(query.value(1))
            list_high.append(query.value(2))
            list_low.append(query.value(3))
            list_close.append(query.value(4))
            list_volume.append(query.value(5))

        sql = sql_sel_13sector_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            name_13sector = query.value(0)
        else:
            name_13sector = None

        con.close()

        df = pd.DataFrame({
            'Date': list_date,
            'Open': list_open,
            'High': list_high,
            'Low': list_low,
            'Close': list_close,
            'Volume': list_volume,
        })
        df.set_index('Date', inplace=True)

        obj = TrendObj()
        obj.setCode(code)
        obj.setCname(cname)
        obj.setDataFrame(df)

        obj.set13Sector(name_13sector)

        obj.setDateFrom(min(list_date))
        obj.setDateTo(max(list_date))
        obj.setNum(len(list_date))

        obj.setVolume(int(median(list_volume)))

        return obj


def get_trend_object_open(code: str, start: int) -> TrendObj:
    list_date = list()
    list_open = list()
    list_volume = list()

    con = DBInfo.get_connection()
    if con.open():
        id_code = 0
        cname = ''
        sql = sql_sel_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            id_code = query.value(0)
            cname = query.value(1)

        if start > 0:
            sql = sql_sel_open_volume_from_trade_with_id_code_start(id_code, start)
        else:
            sql = sql_sel_open_volume_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            ds = conv_pandas_timestamp(query.value(0))
            list_date.append(ds)
            list_open.append(query.value(1))
            list_volume.append(query.value(2))

        sql = sql_sel_13sector_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            name_13sector = query.value(0)
        else:
            name_13sector = None

        con.close()

        df = pd.DataFrame({
            'Date': list_date,
            'Open': list_open,
        })
        df.set_index('Date', inplace=True)

        obj = TrendObj()
        obj.setCode(code)
        obj.setCname(cname)
        obj.setDataFrame(df)

        obj.set13Sector(name_13sector)

        obj.setDateFrom(min(list_date))
        obj.setDateTo(max(list_date))
        obj.setNum(len(list_date))

        obj.setVolume(int(median(list_volume)))

        return obj


def get_trend_object_close(code: str, start: int) -> TrendObj:
    list_date = list()
    list_close = list()
    list_volume = list()

    con = DBInfo.get_connection()
    if con.open():
        id_code = 0
        cname = ''
        sql = sql_sel_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            id_code = query.value(0)
            cname = query.value(1)

        if start > 0:
            sql = sql_sel_close_volume_from_trade_with_id_code_start(id_code, start)
        else:
            sql = sql_sel_close_volume_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            ds = conv_pandas_timestamp(query.value(0))
            list_date.append(ds)
            list_close.append(query.value(1))
            list_volume.append(query.value(2))

        sql = sql_sel_13sector_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            name_13sector = query.value(0)
        else:
            name_13sector = None

        con.close()

        df = pd.DataFrame({
            'Date': list_date,
            'Close': list_close,
        })
        df.set_index('Date', inplace=True)

        obj = TrendObj()
        obj.setCode(code)
        obj.setCname(cname)
        obj.setDataFrame(df)

        obj.set13Sector(name_13sector)

        obj.setDateFrom(min(list_date))
        obj.setDateTo(max(list_date))
        obj.setNum(len(list_date))

        obj.setVolume(int(median(list_volume)))

        return obj


def get_trend_object_close_open(code: str, start: int) -> TrendObj:
    list_date = list()
    list_open = list()
    list_close = list()
    list_volume = list()

    con = DBInfo.get_connection()
    if con.open():
        id_code = 0
        cname = ''
        sql = sql_sel_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            id_code = query.value(0)
            cname = query.value(1)

        if start > 0:
            sql = sql_sel_open_close_volume_from_trade_with_id_code_start(id_code, start)
        else:
            sql = sql_sel_open_close_volume_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            ds = conv_pandas_timestamp(query.value(0))
            list_date.append(ds)
            list_open.append(query.value(1))
            list_close.append(query.value(2))
            list_volume.append(query.value(3))

        sql = sql_sel_13sector_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            name_13sector = query.value(0)
        else:
            name_13sector = None

        con.close()

        list_close_open = [c - o for c, o in zip(list_close, list_open)]
        df = pd.DataFrame({
            'Date': list_date,
            'Open': list_open,
            'Close': list_close,
            'Delta': list_close_open,
        })
        df.set_index('Date', inplace=True)

        obj = TrendObj()
        obj.setCode(code)
        obj.setCname(cname)
        obj.setDataFrame(df)

        obj.set13Sector(name_13sector)

        obj.setDateFrom(min(list_date))
        obj.setDateTo(max(list_date))
        obj.setNum(len(list_date))

        obj.setVolume(int(median(list_volume)))

        return obj


def init_tbl_trade() -> bool:
    dict_code = get_dict_code()

    start = dt.date(2020, 1, 1)
    end = dt.date.today()

    con = DBInfo.get_connection()
    if con.open():
        for id_code in dict_code:
            ticker = '%s.T' % dict_code[id_code]
            print(ticker)
            df: pd.DataFrame = yf.download(ticker, start, end)
            add_rows_tbl_trade(df, id_code)
        con.close()

        return True
    else:
        print('database can not be opened!')
        return False


def update_tbl_trade(end: dt.date) -> bool:
    # get dictionary of code with id_code as key
    dict_code = get_dict_code()

    con = DBInfo.get_connection()
    if con.open():
        for id_code in dict_code:
            ticker = '%s.T' % dict_code[id_code]
            print(ticker)
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # get latest date of the trade table with specified id_code
            query = QSqlQuery()
            sql = sql_sel_max_date_from_trade_with_id_code(id_code)
            query.exec(sql)
            while query.next():
                date_latest = query.value(0)
                if type(date_latest) is int:
                    start = conv_timestamp2date_next(date_latest)
                else:
                    start = get_original_start()
                if start == end:
                    print('Skipped due to start and end are the same!')
                    continue
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # get data from Yahoo finance
                df: pd.DataFrame = yf.download(ticker, start, end)
                size_row = len(df)
                if size_row == 0:
                    print('Skipped due to no data is obtained!')
                    continue
                print('data size: %d.' % size_row)
                add_rows_tbl_trade(df, id_code)
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False
