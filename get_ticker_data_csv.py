"""Dataset preparation in CSV format for ingesting new data to the database
"""
import os
import datetime as dt
import yfinance as yf

from PySide6.QtSql import QSqlQuery

from database.sqls import select_code_cname_from_ticker
from functions.resources import get_connection

#start = dt.date(2000, 1, 1)
start = dt.date(2021, 1, 1)
end = dt.date.today()

con = get_connection()
if con.open():
    sql = select_code_cname_from_ticker()
    query = QSqlQuery(sql)
    while query.next():
        code = '%d.T' % query.value(0)
        print(code)
        desc = str(query.value(1))
        df = yf.download(code, start, end)
        filename = '%s.csv' % os.path.join('data', code)
        df.to_csv(filename)
    con.close()
