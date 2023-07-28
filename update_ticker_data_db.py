import datetime as dt
import yfinance as yf

from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_insert_into_trade_values,
    get_sql_select_id_code_code_from_ticker,
    get_sql_select_max_date_from_trade_with_id_code,
)
from functions.conv_timestamp2date import conv_timestamp2date_next
from functions.resources import get_connection

end = dt.date.today()

con = get_connection()
if con.open():
    sql1 = get_sql_select_id_code_code_from_ticker()
    query1 = QSqlQuery(sql1)
    while query1.next():
        id_code = query1.value(0)
        code = '%d.T' % query1.value(1)

        sql2 = get_sql_select_max_date_from_trade_with_id_code(id_code)
        query2 = QSqlQuery(sql2)
        while query2.next():
            date_max = query2.value(0)
            if type(date_max) is not int:
                continue
            start = conv_timestamp2date_next(date_max)
            print('\n', code)

            df = yf.download(code, start, end)
            if len(df) == 0:
                continue
            for row in df.index:
                timestamp = row.timestamp()
                series = df.loc[row].copy()
                series['Date'] = timestamp
                sql3 = get_sql_insert_into_trade_values(id_code, series)
                query3 = QSqlQuery()
                query3.exec(sql3)
    con.close()
