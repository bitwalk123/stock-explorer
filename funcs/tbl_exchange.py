import datetime as dt

import pandas as pd
import yfinance as yf
from PySide6.QtSql import QSqlQuery

from funcs.tbl_currency import get_dict_currency
from funcs.tide import conv_pandas_timestamp
from sqls.sql_currency import sql_sel_id_currency_from_currency_with_currency
from sqls.sql_exchange import (
    sql_create_tbl_exchange,
    sql_drop_tbl_exchange,
    sql_ins_into_exchange_values,
    sql_sel_id_exchange_from_exchange_with_date_id_currency,
    sql_upd_exchange_values, sql_sel_all_from_exchange_with_id_currency_start,
    sql_sel_all_from_exchange_with_id_currency,
)
from structs.db_info import DBInfo
from structs.trend_object import TrendObj


def add_rows_tbl_exchange(df: pd.DataFrame, id_currency: int):
    for row in df.index:
        timestamp = int(row.timestamp())
        series = df.loc[row].copy()
        series['Date'] = timestamp

        query = QSqlQuery()
        sql = sql_sel_id_exchange_from_exchange_with_date_id_currency(id_currency, timestamp)
        query.exec(sql)
        if query.next():
            id_exchange = query.value(0)
            sql = sql_upd_exchange_values(id_exchange, series)
        else:
            sql = sql_ins_into_exchange_values(id_currency, series)
        if not query.exec(sql):
            print(query.lastError())


def create_tbl_exchange():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_exchange_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_exchange_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_exchange()
    result = query.exec(sql)
    if result:
        print('query has been successfully executed.')


def drop_tbl_exchange() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_exchange()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


def get_trend_object_exchange(currency: str, start: int) -> TrendObj:
    list_date = list()
    list_open = list()
    list_high = list()
    list_low = list()
    list_close = list()

    con = DBInfo.get_connection()
    if con.open():
        id_currency = 0
        sql = sql_sel_id_currency_from_currency_with_currency(currency)
        query = QSqlQuery(sql)
        if query.next():
            id_currency = query.value(0)

        if start > 0:
            sql = sql_sel_all_from_exchange_with_id_currency_start(id_currency, start)
        else:
            sql = sql_sel_all_from_exchange_with_id_currency(id_currency)

        query = QSqlQuery(sql)
        while query.next():
            ds = conv_pandas_timestamp(query.value(0))
            list_date.append(ds)
            list_open.append(query.value(1))
            list_high.append(query.value(2))
            list_low.append(query.value(3))
            list_close.append(query.value(4))
        con.close()

        df = pd.DataFrame({
            'Date': list_date,
            'Open': list_open,
            'High': list_high,
            'Low': list_low,
            'Close': list_close,
        })
        df.set_index('Date', inplace=True)

        obj = TrendObj()
        obj.setCode(currency)
        obj.setCname('')
        obj.setDataFrame(df)

        obj.set13Sector('')

        obj.setDateFrom(min(list_date))
        obj.setDateTo(max(list_date))
        obj.setNum(len(list_date))

        obj.setVolume(0)

        return obj


def init_tbl_exchange():
    dict_currency = get_dict_currency()

    start = dt.date(2020, 1, 1)
    end = dt.date.today()

    con = DBInfo.get_connection()
    if con.open():
        for id_currency in dict_currency:
            currency = '%s=X' % dict_currency[id_currency]
            print(currency, start, end)
            df: pd.DataFrame = yf.download(currency, start, end)
            add_rows_tbl_exchange(df, id_currency)
        con.close()

        return True
    else:
        print('database can not be opened!')
        return False
