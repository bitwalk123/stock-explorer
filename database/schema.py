from PySide6.QtSql import QSqlQuery

from database.sqls_trade import (
    create_table_trade,
)
from database.sqls_ticker import create_table_ticker
from database.sqls_split import create_table_split
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
