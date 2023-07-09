import os

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
        print(filename)
    con.close()
