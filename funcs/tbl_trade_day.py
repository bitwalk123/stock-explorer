import pandas as pd
import yfinance as yf
from PySide6.QtSql import QSqlQuery

from funcs.tbl_ticker import get_id_code_from_code
from sqls.sql_trade_day import (
    sql_create_tbl_trade5m,
    sql_drop_tbl_trade5m,
)
from structs.db_info import DBInfo


def create_tbl_trade5m():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_trade5m_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_trade5m_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_trade5m()
    if not query.exec(sql):
        print(query.lastError())


def drop_tbl_trade5m() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_trade5m()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


def get_day_trade(code: str, start: str, end: str, interval: str) -> pd.DataFrame:
    ticker = '%s.T' % code
    df = yf.download(ticker, start, end, interval=interval)
    # id_code = get_id_code_from_code(code)
    return df
