import statistics

from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_id_code_from_ticker_with_code,
    get_sql_select_date_volume_from_trade_with_id_code_start,
)
from functions.resources import get_connection


def get_volume_median_with_code_start(code: int, start: int) -> tuple:
    date_min = 0
    date_max = 0
    volume_median = 0
    num = 0
    con = get_connection()
    if con.open():
        query = QSqlQuery()

        sql1 = get_sql_select_id_code_from_ticker_with_code(code)
        query.exec(sql1)
        while query.next():
            id_code = query.value(0)

            sql2 = get_sql_select_date_volume_from_trade_with_id_code_start(id_code, start)
            query.exec(sql2)
            list_date = list()
            list_volume = list()
            while query.next():
                date = query.value(0)
                volume = query.value(1)
                list_date.append(date)
                list_volume.append(volume)
        con.close()

        date_min = min(list_date)
        date_max = max(list_date)
        volume_median = int(statistics.median(list_volume))
        num = len(list_volume)

    return date_min, date_max, volume_median, num
