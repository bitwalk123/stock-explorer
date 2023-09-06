import datetime as dt
import os
import pickle
import time

import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_max_date_from_trade_with_id_code,
    get_sql_select_open_from_trade_with_id_code_date,
)
from functions.get_dataset import get_valid_list_id_code
from functions.get_elapsed import get_elapsed
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
    price_min = 500
    price_max = 1000

    # List valid id_code
    time_start = time.time()
    pkl_list_id_code = 'pool/list_id_code.pkl'
    if os.path.isfile(pkl_list_id_code):
        with open(pkl_list_id_code, 'rb') as f:
            list_id_code = pickle.load(f)
    else:
        list_id_code = get_valid_list_id_code(start, count_min, volume_min)
        with open(pkl_list_id_code, 'wb') as f:
            pickle.dump(list_id_code, f)

    print('total :', len(list_id_code))
    print('elapsed', get_elapsed(time_start), 'sec')

    # pick target id_code
    time_start = time.time()
    list_id_code_target = list()
    con = get_connection()
    if con.open():
        for id_code in list_id_code:
            sql1 = get_sql_select_max_date_from_trade_with_id_code(id_code)
            query1 = QSqlQuery(sql1)
            while query1.next():
                date = query1.value(0)
                sql2 = get_sql_select_open_from_trade_with_id_code_date(id_code, date)
                query2 = QSqlQuery(sql2)
                while query2.next():
                    price_open = query2.value(0)
                    if price_min < price_open < price_max:
                        list_id_code_target.append(id_code)

        con.close()

    print('total :', len(list_id_code_target))
    print('elapsed', get_elapsed(time_start), 'sec')

if __name__ == "__main__":
    main()
