from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import select_13sector_from_ticker_with_code
from functions.resources import get_connection


def get_13sector_with_code(code: int) -> str:
    name_13sector = ''
    con = get_connection()
    if con.open():
        query = QSqlQuery()

        sql = select_13sector_from_ticker_with_code(code)
        query.exec(sql)
        if query.next():
            name_13sector = query.value(0)
        con.close()

    return name_13sector
