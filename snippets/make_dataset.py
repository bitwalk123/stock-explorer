import datetime as dt
import statistics

import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_id_code_from_ticker,
    get_sql_select_volume_from_trade_with_id_code_start,
)
from functions.resources import get_connection


def main():
    """Main
    """
    today = int(pd.to_datetime(str(dt.date.today())).timestamp())
    year = 365 * 24 * 60 * 60
    start = today - year
    print(start)
    count_min = 200
    volume_min = 10000

    con = get_connection()
    if con.open():
        sql1 = get_sql_select_id_code_from_ticker()
        query1 = QSqlQuery(sql1)
        total = 0
        list_id_code = list()
        while query1.next():
            id_code = query1.value(0)

            sql2 = get_sql_select_volume_from_trade_with_id_code_start(id_code, start)
            query2 = QSqlQuery(sql2)
            list_volume = list()
            while query2.next():
                list_volume.append(query2.value(0))

            if len(list_volume) < count_min:
                continue
            volume_median = statistics.median(list_volume)
            if volume_median < volume_min:
                continue
            print(id_code)
            #print(list_volume)
            total += 1
        print('total :', total)


if __name__ == "__main__":
    main()
