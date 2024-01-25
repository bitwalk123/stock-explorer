import datetime as dt
import pandas as pd
import yfinance as yf

from PySide6.QtSql import QSqlQuery

from funcs.tbl_iticker import get_dict_index
from funcs.tide import conv_timestamp2date_next, get_original_start
from sqls.sql_itrade import (
    sql_create_tbl_itrade,
    sql_sel_id_itrade_from_itrade_with_date_id_index,
    sql_upd_itrade_values, sql_ins_into_itrade_values, sql_drop_tbl_itrade, sql_sel_max_date_from_itrade_with_id_index,
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


def drop_tbl_itrade() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_itrade()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


def init_tbl_itrade() -> bool:
    dict_index = get_dict_index()

    start = dt.date(2020, 1, 1)
    end = dt.date.today()

    con = DBInfo.get_connection()
    if con.open():
        for id_index in dict_index.keys():
            iticker = dict_index[id_index]
            print(iticker)
            df: pd.DataFrame = yf.download(iticker, start, end)
            add_rows_tbl_itrade(df, id_index)
        con.close()

        return True
    else:
        print('database can not be opened!')
        return False


def update_tbl_itrade(end: dt.date) -> bool:
    day1 = 24 * 60 * 60
    # get dictionary of code with id_code as key
    dict_index = get_dict_index()

    con = DBInfo.get_connection()
    if con.open():
        for id_index in dict_index.keys():
            iticker = dict_index[id_index]
            print(iticker)
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # get latest date of the trade table with specified id_code
            query = QSqlQuery()
            sql = sql_sel_max_date_from_itrade_with_id_index(id_index)
            query.exec(sql)
            while query.next():
                date_latest = query.value(0)
                if type(date_latest) is int:
                    start = conv_timestamp2date_next(date_latest - 7 * day1)
                else:
                    start = get_original_start()
                if start == end:
                    print('Skipped due to start and end are the same!')
                    continue
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # get data from Yahoo finance
                df: pd.DataFrame = yf.download(iticker, start, end)
                size_row = len(df)
                if size_row == 0:
                    print('Skipped due to no data is obtained!')
                    continue
                print('data size: %d.' % size_row)
                add_rows_tbl_itrade(df, id_index)
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False
