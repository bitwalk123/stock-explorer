from PySide6.QtSql import QSqlQuery

from database.sqls_trade import select_max_date_from_trade, select_max_date_from_trade_less_date
from functions.resources import get_connection


def get_latest_2dates() -> list:
    date_latest_before = 0
    date_latest = 0
    con = get_connection()
    if con.open():
        sql = select_max_date_from_trade()
        query = QSqlQuery(sql)
        if query.next():
            date_latest = query.value(0)

        if date_latest > 0:
            sql = select_max_date_from_trade_less_date(date_latest)
            query = QSqlQuery(sql)
            if query.next():
                date_latest_before = query.value(0)

        con.close()

    return [date_latest_before, date_latest]
