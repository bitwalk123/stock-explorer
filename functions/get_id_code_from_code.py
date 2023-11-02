from PySide6.QtSql import QSqlQuery

from database.sqls import select_id_code_from_ticker_with_code
from functions.resources import get_connection


def get_id_code_from_code(code: int) -> int:
    con = get_connection()
    if con.open():
        sql = select_id_code_from_ticker_with_code(code)
        query = QSqlQuery(sql)
        if query.next():
            return query.value(0)
        else:
            return 0
    else:
        return 0
