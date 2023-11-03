import datetime as dt

import yfinance as yf
from PySide6.QtSql import QSqlQuery

from database.sqls_trade import (
    insert_into_trade_values,
    select_id_trade_from_trade_with_date_id_code,
    select_max_date_from_trade_with_id_code,
    update_trade_values,
)
from database.sqls_ticker import select_id_code_code_from_ticker
from functions.conv_timestamp2date import conv_timestamp2date_next
from functions.predict_price import (
    get_base_dataframe,
    get_prediction_by_pls,
    get_valid_dataset,
)
from functions.resources import get_connection
from functions.trading_date import (
    get_last_trading_date,
    get_next_trading_date,
)


def update_prediction():
    day1 = 24 * 60 * 60
    con = get_connection()
    if con.open():
        end: int = get_last_trading_date()
        start = end - 365 * day1
        print(
            'date scope :',
            dt.datetime.fromtimestamp(start),
            '-',
            dt.datetime.fromtimestamp(end)
        )
        end_next = get_next_trading_date(end)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Get list of valid code and target
        dict_code, list_valid_id_code, list_target_id_code = get_valid_dataset(start, end)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Generate base dataframe
        df_base = get_base_dataframe(list_valid_id_code, start, end)
        con.close()

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Prediction for next Open price
        get_prediction_by_pls(df_base, dict_code, end_next, list_target_id_code)
    else:
        print('fail to open db.')


def update_ticker(end):
    con = get_connection()
    if con.open():
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # get list of id_code, code from the ticker table
        query1 = QSqlQuery()
        sql1 = select_id_code_code_from_ticker()
        query1.exec(sql1)
        while query1.next():
            id_code = query1.value(0)
            code = '%d.T' % query1.value(1)
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # get latest date of the trade table with specified id_code
            query2 = QSqlQuery()
            sql2 = select_max_date_from_trade_with_id_code(id_code)
            query2.exec(sql2)
            while query2.next():
                date_max = query2.value(0)
                if type(date_max) is not int:
                    continue
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # start day is next to the latest date
                start = conv_timestamp2date_next(date_max)
                print('\n', code)
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # get data from Yahoo finance
                df = yf.download(code, start, end)
                if len(df) == 0:
                    continue
                for row in df.index:
                    timestamp = row.timestamp()
                    series = df.loc[row].copy()
                    date = series['Date'] = timestamp
                    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                    # get id_trade from the trade table with date and id_code
                    query3 = QSqlQuery()
                    sql3 = select_id_trade_from_trade_with_date_id_code(date, id_code)
                    query3.exec(sql3)
                    if query3.next():
                        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                        # if data exists, update the trade table
                        id_trade = query3.value(0)
                        sql4 = update_trade_values(id_trade, series)
                    else:
                        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                        # if not, append data to the trade table
                        sql4 = insert_into_trade_values(id_code, series)
                    # execute query
                    query4 = QSqlQuery()
                    query4.exec(sql4)
        con.close()
