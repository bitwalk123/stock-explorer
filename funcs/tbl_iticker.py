from PySide6.QtSql import QSqlQuery

from sqls.sql_iticker import (
    sql_create_tbl_iticker,
    sql_drop_tbl_iticker,
    sql_ins_into_iticker_vals,
    sql_sel_id_index_index_from_iticker,
    sql_sel_id_index_from_iticker_with_iticker,
    sql_upd_iticker_vals,
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


def get_dict_id_index() -> dict:
    """
    dict_id_index[iticker] = id_index
    """
    con = DBInfo.get_connection()
    if con.open():
        dict_id_index = dict()
        query = QSqlQuery()
        sql = sql_sel_id_index_index_from_iticker()
        query.exec(sql)
        while query.next():
            id_index = query.value(0)
            iticker = query.value(1)
            dict_id_index[iticker] = id_index
        con.close()
        return dict_id_index
    else:
        print('database can not be opened!')
        return dict()


def get_dict_index() -> dict:
    """
    dict_index[id_index] = iticker
    """
    con = DBInfo.get_connection()
    if con.open():
        dict_index = dict()
        query = QSqlQuery()
        sql = sql_sel_id_index_index_from_iticker()
        query.exec(sql)
        while query.next():
            id_index = query.value(0)
            iticker = query.value(1)
            dict_index[id_index] = iticker
        con.close()
        return dict_index
    else:
        print('database can not be opened!')
        return dict()
