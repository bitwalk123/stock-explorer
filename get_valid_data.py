import datetime as dt
import os
import pickle

import pandas as pd
import time

from functions.get_dataset import get_basic_dataset
from functions.get_elapsed import get_elapsed
from functions.get_valid_code import get_valid_code
from functions.resources import get_connection

DAY1 = 24 * 60 * 60
TZ_DELTA = 9 * 60 * 60  # Asia/Tokyo timezone


def get_valid_dataset(start, end) -> pd.DataFrame:
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # get list of valid code and target
    pkl_list_valid_id_code = 'pool/list_valid_id_code_%d.pkl' % end
    pkl_list_target_id_code = 'pool/list_target_id_code_%d.pkl' % end
    if os.path.isfile(pkl_list_valid_id_code) and os.path.isfile(pkl_list_target_id_code):
        with open(pkl_list_valid_id_code, 'rb') as f:
            list_valid_id_code = pickle.load(f)
        with open(pkl_list_target_id_code, 'rb') as f:
            list_target_id_code = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        list_valid_id_code, list_target_id_code = get_valid_code(start, end)
        with open(pkl_list_valid_id_code, 'wb') as f:
            pickle.dump(list_valid_id_code, f)
        with open(pkl_list_target_id_code, 'wb') as f:
            pickle.dump(list_target_id_code, f)

    print('number of valid id_code : %d' % len(list_valid_id_code))
    print('number of target id_code : %d' % len(list_target_id_code))

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # get base dataframe
    pkl_df_base = 'pool/df_base_%d.pkl' % end
    if os.path.isfile(pkl_df_base):
        with open(pkl_df_base, 'rb') as f:
            df_base = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        df_base: pd.DataFrame = get_basic_dataset(list_valid_id_code, start, end)
        with open(pkl_df_base, 'wb') as f:
            pickle.dump(df_base, f)

    print(df_base)
    print(df_base.shape)

    return df_base


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
        # Generate base dataframe
        df_base = get_valid_dataset(start, end)
        con.close()
    else:
        print('fail to open db.')


if __name__ == "__main__":
    time_start = time.time()
    main()
    print('elapsed %.3f sec' % get_elapsed(time_start))
