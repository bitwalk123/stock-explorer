import os
import pandas as pd
from PySide6.QtSql import QSqlQuery

from functions.resources import get_connection

con = get_connection()
if con.open():
    sql = 'select id_ticker, コード, 銘柄名 from ticker;'
    query = QSqlQuery(sql)
    while query.next():
        id = query.value(0)
        code = '%d.T' % query.value(1)
        filename = '%s.csv' % os.path.join('data', code)
        if os.path.isfile(filename):
            df = pd.read_csv(filename)
            if len(df) == 0:
                continue
            print(id, filename)
            df['Date'] = pd.to_datetime(df['Date'])
            df['Date'] = [int(df['Date'][r].timestamp()) for r in range(len(df))]
            print(df.head())
    con.close()
