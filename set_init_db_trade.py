"""Set initial data to ingest from CSV file to the trade table of the database
"""
import os
import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_insert_into_trade_values,
    get_sql_select_id_code_code_cname_from_ticker,
)
from functions.resources import get_connection

con = get_connection()
if con.open():
    sql1 = get_sql_select_id_code_code_cname_from_ticker()
    query1 = QSqlQuery(sql1)
    while query1.next():
        id = query1.value(0)
        code = '%d.T' % query1.value(1)
        filename = '%s.csv' % os.path.join('data', code)
        if os.path.isfile(filename):
            df = pd.read_csv(filename)
            if len(df) == 0:
                continue
            print(id, filename)
            df['Date'] = pd.to_datetime(df['Date'])
            df['Date'] = [df['Date'][r].timestamp() for r in range(len(df))]

            for r in range(len(df)):
                series = df.iloc[r]
                sql2 = get_sql_insert_into_trade_values(id, series)
                query2 = QSqlQuery()
                query2.exec(sql2)
    con.close()
