from typing import Union

import pandas as pd
from PySide6.QtSql import QSqlQuery

from funcs.common import get_excel_from_url
from sqls.sql_ticker import (
    sql_create_tbl_ticker,
    sql_del_ticker_with_code,
    sql_drop_tbl_ticker,
    sql_ins_into_ticker_vals,
    sql_sel_cname_with_code_from_ticker,
    sql_sel_code_from_ticker,
    sql_sel_id_code_code_from_ticker,
    sql_sel_id_code_from_ticker_with_code,
    sql_upd_ticker_vals,
)
from structs.db_info import DBInfo


def create_tbl_ticker() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_ticker_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_ticker_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_ticker()
    result = query.exec(sql)
    if result:
        print('query has been successfully executed.')


def drop_tbl_ticker() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_ticker()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


def get_cname_with_code(code: str) -> str:
    con = DBInfo.get_connection()
    if con.open():
        query = QSqlQuery()
        sql = sql_sel_cname_with_code_from_ticker(code)
        query.exec(sql)
        if query.next():
            cname = query.value(0)
        else:
            cname = ''
        con.close()
        return cname
    else:
        print('database can not be opened!')
        return ''


def get_dict_code() -> dict:
    """
    dict_code[id_code] = code
    """
    con = DBInfo.get_connection()
    if con.open():
        dict_code = dict()
        query = QSqlQuery()
        sql = sql_sel_id_code_code_from_ticker()
        query.exec(sql)
        while query.next():
            id_code = query.value(0)
            code = query.value(1)
            dict_code[id_code] = code
        con.close()
        return dict_code
    else:
        print('database can not be opened!')
        return dict()


def get_dict_id_code() -> dict:
    """
    dict_id_code[code] = id_code
    """
    con = DBInfo.get_connection()
    if con.open():
        dict_id_code = dict()
        query = QSqlQuery()
        sql = sql_sel_id_code_code_from_ticker()
        query.exec(sql)
        while query.next():
            id_code = query.value(0)
            code = query.value(1)
            dict_id_code[code] = id_code
        con.close()
        return dict_id_code
    else:
        print('database can not be opened!')
        return dict()


def get_id_code_from_code(code: str) -> Union[int, None]:
    con = DBInfo.get_connection()
    if con.open():
        query = QSqlQuery()
        sql = sql_sel_id_code_from_ticker_with_code(code)
        query.exec(sql)
        if query.next():
            id_code = query.value(0)
        else:
            id_code = None
        con.close()
        return id_code
    else:
        print('database can not be opened!')
        return None


def update_tbl_ticker(tse: str) -> bool:
    list_market = [
        'グロース（内国株式）',
        'スタンダード（内国株式）',
        'プライム（内国株式）',
    ]
    df_all = get_excel_from_url(tse)

    df_stock0 = df_all[df_all['市場・商品区分'].isin(list_market)]
    df_stock = df_stock0[[len(str(p)) == 4 for p in df_stock0['コード']]].reset_index(drop=True)
    df_stock['コード'] = df_stock['コード'].astype(str)

    list_row = list(df_stock.index)

    con = DBInfo.get_connection()
    if con.open():
        query = QSqlQuery()
        # ____________________________________________________________________
        # get current list of ticker code
        list_code_current = update_tbl_ticker_procs_1(query)
        # ____________________________________________________________________
        # overwrite/update/insert tickers
        update_tbl_ticker_procs_2(df_stock, list_row, query)
        # ____________________________________________________________________
        # check code already de-listed
        update_tbl_ticker_procs_3(df_stock, list_code_current, query)

        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def update_tbl_ticker_procs_1(query):
    # get current list of ticker code
    list_code_current = list()
    sql = sql_sel_code_from_ticker()
    query.exec(sql)
    while query.next():
        code = query.value(0)
        list_code_current.append(code)
    # print(list_code_current)
    return list_code_current


def update_tbl_ticker_procs_2(
        df_stock: pd.DataFrame,
        list_row: list,
        query: QSqlQuery
):
    # overwrite/update/insert tickers
    for count, row in enumerate(list_row):
        series = df_stock.loc[row]
        code = series['コード']
        sql = sql_sel_id_code_from_ticker_with_code(code)
        query.exec(sql)
        if query.next():
            # print(code, 'is updated!')
            id_code = query.value(0)
            sql = sql_upd_ticker_vals(id_code, series)
        else:
            # print(code, 'does not exist!')
            sql = sql_ins_into_ticker_vals(series)
        query.exec(sql)


def update_tbl_ticker_procs_3(
        df_stock: pd.DataFrame,
        list_code_current: list,
        query: QSqlQuery
):
    # check code already de-listed
    list_code_new = list(df_stock['コード'])
    for code in list_code_current:
        if not (code in list_code_new):
            print(code, 'should be deleted!')
            sql = sql_del_ticker_with_code(code)
            query.exec(sql)
