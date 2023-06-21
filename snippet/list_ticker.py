from PySide6.QtSql import QSqlQuery

from functions.resources import get_connection

con = get_connection()
if con.open():
    sql = 'select コード, 銘柄名 from ticker;'
    query = QSqlQuery(sql)
    while query.next():
        code = str(query.value(0))
        desc = str(query.value(1))
        print(code, desc)
    con.close()
