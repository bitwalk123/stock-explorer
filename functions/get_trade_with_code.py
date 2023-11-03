import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls_trade import (
    select_all_from_trade_with_id_code,
    select_all_from_trade_with_id_code_start,
)
from database.sqls_ticker import select_id_code_cname_from_ticker_with_code
from functions.conv_timestamp2date import conv_timestamp
from functions.resources import get_connection


def get_trade_with_code(code: int, start: int) -> tuple:
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
    list_date = list()
    list_open = list()
    list_high = list()
    list_low = list()
    list_close = list()
    list_volume = list()
    con = get_connection()
    if con.open():
        # get id_code == id_code
        id_code = 0
        sql = select_id_code_cname_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        while query.next():
            id_code = query.value(0)
            cname = query.value(1)
            break

        # Get list of Date, Open, High, Low, Close and Volume specified with id_code
        if start > 0:
            sql = select_all_from_trade_with_id_code_start(id_code, start)
        else:
            sql = select_all_from_trade_with_id_code(id_code)

        query = QSqlQuery(sql)
        while query.next():
            dt = conv_timestamp(query.value(0))
            list_date.append(dt)
            list_open.append(query.value(1))
            list_high.append(query.value(2))
            list_low.append(query.value(3))
            list_close.append(query.value(4))
            list_volume.append(query.value(5))
        con.close()

        df = pd.DataFrame(
            {
                'Date': list_date,
                'Open': list_open,
                'High': list_high,
                'Low': list_low,
                'Close': list_close,
                'Volume': list_volume,
            }
        )
        df.set_index('Date', inplace=True)
        # df.insert(0, 'index', date2num(df.index))
        # print(df.head())
        return cname, df
    else:
        print('database cannot be opened!')
