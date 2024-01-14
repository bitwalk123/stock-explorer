from PySide6.QtSql import QSqlQuery

from sqls.sql_iticker import (
    sql_create_tbl_iticker,
    sql_ins_into_iticker_vals,
    sql_sel_id_index_from_iticker_with_iticker,
    sql_upd_iticker_vals, sql_drop_tbl_iticker,
)
from structs.db_info import DBInfo

list_iticker = [
    ['^N225', '日経平均株価'],
    ['^DJI', 'NYダウ'],
    ['^IXIC', 'ナスダック総合'],
    ['^GSPC', 'S＆P 500'],
]


def create_tbl_iticker():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_iticker_procs_1()
        create_tbl_iticker_procs_2()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False

def drop_tbl_iticker() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_iticker()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False

def create_tbl_iticker_procs_1():
    query = QSqlQuery()
    sql = sql_create_tbl_iticker()
    result = query.exec(sql)
    if result:
        print('query has been successfully executed.')


def create_tbl_iticker_procs_2():
    query = QSqlQuery()
    for row in list_iticker:
        sql = sql_sel_id_index_from_iticker_with_iticker(row[0])
        query.exec(sql)
        if query.next():
            id_index = query.value(0)
            sql = sql_upd_iticker_vals(id_index, row)
        else:
            sql = sql_ins_into_iticker_vals(row)
        result = query.exec(sql)
        if result:
            print('query has been successfully executed.')
