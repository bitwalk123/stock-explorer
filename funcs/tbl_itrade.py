import datetime as dt
import pandas as pd
import yfinance as yf

from PySide6.QtSql import QSqlQuery

from funcs.tbl_iticker import get_dict_index
from sqls.sql_itrade import (
    sql_create_tbl_itrade,
    sql_sel_id_itrade_from_itrade_with_date_id_index,
    sql_upd_itrade_values, sql_ins_into_itrade_values,
)
from structs.db_info import DBInfo


def add_rows_tbl_itrade(df: pd.DataFrame, id_index: int):
    for row in df.index:
        timestamp = int(row.timestamp())
        series = df.loc[row].copy()
        series['Date'] = timestamp

        query = QSqlQuery()
        sql = sql_sel_id_itrade_from_itrade_with_date_id_index(id_index, timestamp)
        query.exec(sql)
        if query.next():
            id_itrade = query.value(0)
            sql = sql_upd_itrade_values(id_itrade, series)
        else:
            sql = sql_ins_into_itrade_values(id_index, series)
        if not query.exec(sql):
            print(query.lastError())


def create_tbl_itrade():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_itrade_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_itrade_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_itrade()
    if not query.exec(sql):
        print(query.lastError())


def init_tbl_itrade() -> bool:
    dict_index = get_dict_index()

    start = dt.date(2020, 1, 1)
    end = dt.date.today()

    con = DBInfo.get_connection()
    if con.open():
        for id_index in list(dict_index.keys()):
            iticker = dict_index[id_index]
            print(iticker)
            df: pd.DataFrame = yf.download(iticker, start, end)
            add_rows_tbl_itrade(df, id_index)
        con.close()

        return True
    else:
        print('database can not be opened!')
        return False
