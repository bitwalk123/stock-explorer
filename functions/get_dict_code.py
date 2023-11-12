from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import (
    select_code_cname_from_ticker,
    select_id_code_code_from_ticker,
)
from functions.resources import get_connection


def get_dict_it_code_code() -> dict:
    dict_code = dict()

    sql = select_id_code_code_from_ticker()
    query = QSqlQuery(sql)
    while query.next():
        id_code = query.value(0)
        code = query.value(1)
        dict_code[id_code] = code
    return dict_code


def get_dict_code_id_code() -> dict:
    dict_id_code = dict()

    sql = select_id_code_code_from_ticker()
    query = QSqlQuery(sql)
    while query.next():
        id_code = query.value(0)
        code = query.value(1)
        dict_id_code[code] = id_code
    return dict_id_code


def get_dict_code_cname() -> dict:
    dict_cname = dict()
    con = get_connection()
    if con.open():
        sql = select_code_cname_from_ticker()
        query = QSqlQuery(sql)
        while query.next():
            code = str(query.value(0))
            cname = query.value(1)
            dict_cname[code] = cname
        con.close()
    return dict_cname
