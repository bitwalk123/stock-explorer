import datetime as dt
import pandas as pd
import time

from functions.get_dataset import get_basic_dataset
from functions.get_elapsed import get_elapsed
from functions.get_valid_code import get_valid_code
from functions.resources import get_connection

DAY1 = 24 * 60 * 60
TZ_DELTA = 9 * 60 * 60  # Asia/Tokyo timezone


def get_dataset(start, end) -> pd.DataFrame:
    # get list of valid code and target
    list_valid_id_code, list_target_id_code = get_valid_code(start, end)
    print('number of valid id_code : %d' % len(list_valid_id_code))
    print('number of target id_code : %d' % len(list_target_id_code))
    df: pd.DataFrame = get_basic_dataset(list_valid_id_code, start, end)
    return df


def main():
    now_dt = dt.datetime.now()
    now = int(dt.datetime.timestamp(now_dt)) + TZ_DELTA
    end = (now // DAY1 - 1) * DAY1
    start = end - 365 * DAY1
    print(
        'date scope :',
        dt.datetime.fromtimestamp(start),
        '-',
        dt.datetime.fromtimestamp(end)
    )

    con = get_connection()
    if con.open():
        df_base = get_dataset(start, end)
        con.close()

        print(df_base)
        print(df_base.shape)
    else:
        print('fail to open db.')


if __name__ == "__main__":
    time_start = time.time()
    main()
    print('elapsed %.3f sec' % get_elapsed(time_start))
