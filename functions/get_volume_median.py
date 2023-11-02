import statistics

from PySide6.QtSql import QSqlQuery

from database.sqls import (
    select_id_code_from_ticker_with_code,
    select_date_volume_from_trade_with_id_code_start,
)
from functions.resources import get_connection


def get_volume_median_with_code_start(code: int, start: int) -> tuple:
    date_min = 0
    date_max = 0
    volume_median = 0
    num = 0

    con = get_connection()
    if con.open():
        query1 = QSqlQuery()

        sql1 = select_id_code_from_ticker_with_code(code)
        query1.exec(sql1)
        while query1.next():
            id_code = query1.value(0)

            list_date = list()
            list_volume = list()
            sql2 = select_date_volume_from_trade_with_id_code_start(id_code, start)
            query2 = QSqlQuery(sql2)
            while query2.next():
                date = query2.value(0)
                volume = query2.value(1)
                list_date.append(date)
                list_volume.append(volume)

            date_min = min(list_date)
            date_max = max(list_date)
            volume_median = int(statistics.median(list_volume))
            num = len(list_volume)

        con.close()

    return date_min, date_max, volume_median, num
