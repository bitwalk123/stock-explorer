from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_create_table_ticker
from functions.resources import get_connection


def initialize_db():
    con = get_connection(flag_delete=True)
    if not con.open():
        return

    sql = get_sql_create_table_ticker()
    query = QSqlQuery()
    query.exec(sql)
    con.close()
