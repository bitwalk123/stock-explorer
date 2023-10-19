import yfinance as yf
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_insert_into_trade_values,
    get_sql_select_id_code_code_from_ticker,
    get_sql_select_id_trade_from_trade_with_date_id_code,
    get_sql_select_max_date_from_trade_with_id_code,
    get_sql_update_trade_values,
)
from functions.conv_timestamp2date import conv_timestamp2date_next
from functions.resources import get_connection


def update_ticker(end, queries: list):
    query1: QSqlQuery = queries[0]
    query2: QSqlQuery = queries[1]
    query3: QSqlQuery = queries[2]
    query4: QSqlQuery = queries[3]

    con = get_connection()
    if con.open():
        # get list of id_code, code from the ticker table
        sql1 = get_sql_select_id_code_code_from_ticker()
        query1.exec(sql1)
        while query1.next():
            id_code = query1.value(0)
            code = '%d.T' % query1.value(1)

            # get latest date of the trade table with specified id_code
            sql2 = get_sql_select_max_date_from_trade_with_id_code(id_code)
            query2.exec(sql2)
            while query2.next():
                date_max = query2.value(0)
                if type(date_max) is not int:
                    continue
                # start day is next to the latest date
                start = conv_timestamp2date_next(date_max)
                print('\n', code)

                # get data from Yahoo finance
                df = yf.download(code, start, end)
                if len(df) == 0:
                    continue
                for row in df.index:
                    timestamp = row.timestamp()
                    series = df.loc[row].copy()
                    date = series['Date'] = timestamp

                    # get id_trade from the trade table with specified date and id_code
                    sql3 = get_sql_select_id_trade_from_trade_with_date_id_code(date, id_code)
                    query3.exec(sql3)
                    if query3.next():
                        # if data exists, update the trade table
                        id_trade = query3.value(0)
                        sql4 = get_sql_update_trade_values(id_trade, series)
                    else:
                        # if not, append data to the trade table
                        sql4 = get_sql_insert_into_trade_values(id_code, series)
                    # execute query
                    query4.exec(sql4)
        con.close()
