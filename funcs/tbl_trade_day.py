from PySide6.QtSql import QSqlQuery

from sqls.sql_trade_day import (
    sql_create_tbl_trade5m,
    sql_drop_tbl_trade5m,
    sql_create_tbl_trade1m,
    sql_drop_tbl_trade1m,
    sql_create_tbl_tradert,
    sql_drop_tbl_tradert,
)
from structs.db_info import DBInfo


# _____________________________________________________________________________
# for 5 minutes chart
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


# _____________________________________________________________________________
# for 1 minute chart
def create_tbl_trade1m():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_trade1m_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_trade1m_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_trade1m()
    if not query.exec(sql):
        print(query.lastError())


def drop_tbl_trade1m() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_trade1m()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


# _____________________________________________________________________________
# for realtime chart
def create_tbl_tradert():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_tradert_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_tradert_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_tradert()
    if not query.exec(sql):
        print(query.lastError())


def drop_tbl_tradert() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_tradert()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False
