from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_date_open_from_trade_with_id_code,
    get_sql_select_date_open_from_trade_with_id_code_start,
    get_sql_select_id_code_cname_from_ticker_with_code,
)
from functions.conv_timestamp2date import conv_timestamp
from functions.resources import get_connection


def get_open_with_code(code: int, start: int) -> tuple:
    """Get Date and Open data specified with code

    Args:
        code (int): ticker number
        start (int): start date in UNIX epoch sec

    Returns:
        cname (str): Company name
        list_x (list): List of Date in integer from Unix epoch date
        list_y (list): List of stock price
    """
    cname = None
    list_x = list()
    list_y = list()
    con = get_connection()
    if con.open():
        # get id_code == id_code
        id_code = 0
        sql = get_sql_select_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        while query.next():
            id_code = query.value(0)
            cname = query.value(1)
            # print(id_code)
            break
        # Get list of Date & Open specified with id_code
        if start > 0:
            sql = get_sql_select_date_open_from_trade_with_id_code_start(id_code, start)
        else:
            sql = get_sql_select_date_open_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            x = query.value(0)
            dt = conv_timestamp(x)
            list_x.append(dt)
            list_y.append(query.value(1))

        con.close()

    return cname, list_x, list_y
