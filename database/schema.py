from PySide6.QtSql import QSqlQuery

from database.sqls import (
    create_table_ticker,
    create_table_split,
    create_table_trade,
)
from functions.resources import get_connection


def initialize_db():
    """
    initialize database
    """
    con = get_connection(flag_delete=True)
    if not con.open():
        return

    sql = create_table_ticker()
    query = QSqlQuery()
    query.exec(sql)

    sql = create_table_trade()
    query = QSqlQuery()
    query.exec(sql)

    sql = create_table_split()
    query = QSqlQuery()
    query.exec(sql)

    con.close()
