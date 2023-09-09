import datetime as dt
import os
import pickle
import time

from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_select_id_code_code_from_ticker, get_sql_insert_into_split_values
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dataset import get_valid_list_id_code
from functions.get_elapsed import get_elapsed
from functions.get_info_ticker import get_info_ticker
from functions.resources import get_connection


def main():
    """Main
    """
    year = 365 * 24 * 60 * 60
    start_str = '2022-01-04'
    start_dt = dt.datetime.strptime(start_str, "%Y-%m-%d")
    start = int(dt.datetime.timestamp(start_dt))
    end = start + year
    print(start, end)

    count_min = 200
    volume_min = 10000
    price_min = 500
    price_max = 600

    # List valid id_code
    time_start = time.time()
    pkl_list_id_code = 'pool/list_id_code.pkl'
    if os.path.isfile(pkl_list_id_code):
        with open(pkl_list_id_code, 'rb') as f:
            list_id_code = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        list_id_code = get_valid_list_id_code(start, end, count_min, volume_min)
        with open(pkl_list_id_code, 'wb') as f:
            pickle.dump(list_id_code, f)

    print('total :', len(list_id_code))
    print('elapsed', get_elapsed(time_start), 'sec')


if __name__ == "__main__":
    main()
