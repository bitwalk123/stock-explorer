from PySide6.QtSql import QSqlQuery

from sqls.sql_order import sql_create_tbl_order
from structs.db_info import DBInfo


def create_tbl_order():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_order_procs()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_order_procs():
    query = QSqlQuery()
    sql = sql_create_tbl_order()
    if not query.exec(sql):
        print(query.lastError())
