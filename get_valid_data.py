import datetime as dt
import pandas as pd
import time

from functions.get_dataset import get_basic_dataset
from functions.get_elapsed import get_elapsed
from functions.get_valid_code import get_valid_code
from functions.resources import get_connection


def main():
    day1 = 24 * 60 * 60
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    now_dt = dt.datetime.now()
    now = int(dt.datetime.timestamp(now_dt)) + tz_delta
    end = (now // day1 - 1) * day1
    start = end - 365 * day1
    print(
        'date scope :',
        dt.datetime.fromtimestamp(start),
        '-',
        dt.datetime.fromtimestamp(end)
    )

    con = get_connection()
    if con.open():
        # get list of valid code and target
        list_valid_id_code, list_target_id_code = get_valid_code(start, end)
        print('number of valid id_code : %d' % len(list_valid_id_code))
        print('number of target id_code : %d' % len(list_target_id_code))

        df: pd.DataFrame = get_basic_dataset(list_valid_id_code, start, end)
        print(df)
        print(df.shape)

        con.close()
    else:
        print('fail to open db.')


if __name__ == "__main__":
    time_start = time.time()
    main()
    print('elapsed %.3f sec' % get_elapsed(time_start))
