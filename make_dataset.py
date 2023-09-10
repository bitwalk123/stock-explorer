import datetime as dt
import os
import pickle
import time

import pandas as pd

from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dataset import (
    get_basic_dataset,
    get_valid_list_id_code,
    get_target_list_id_code, get_candidate_tickers,
)
from functions.get_elapsed import get_elapsed


def main():
    """Main
    """
    year = 365 * 24 * 60 * 60
    end_str = '2023-01-04'
    end_dt = dt.datetime.strptime(end_str, '%Y-%m-%d')
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    end = int(dt.datetime.timestamp(end_dt)) + tz_delta
    start = end - year
    print(conv_timestamp2date(start), conv_timestamp2date(end))

    count_min = 200
    volume_min = 10000
    price_min = 950
    price_max = 1050

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

    print('valid total :', len(list_id_code))
    print('elapsed', get_elapsed(time_start), 'sec')

    # Pick target id_code
    time_start = time.time()
    pkl_list_id_code_target = 'pool/list_id_code_target.pkl'
    if os.path.isfile(pkl_list_id_code_target):
        with open(pkl_list_id_code_target, 'rb') as f:
            list_id_code_target = pickle.load(f)
    else:
        list_id_code_target = get_target_list_id_code(list_id_code, price_min, price_max, start, end)
        with open(pkl_list_id_code_target, 'wb') as f:
            pickle.dump(list_id_code_target, f)

    print('target total :', len(list_id_code_target))
    print('elapsed', get_elapsed(time_start), 'sec')

    # Base dataset
    time_start = time.time()
    pkl_df_base = 'pool/list_df_base.pkl'
    if os.path.isfile(pkl_df_base):
        with open(pkl_df_base, 'rb') as f:
            df_base = pickle.load(f)
    else:
        df_base = get_basic_dataset(list_id_code, start, end)
        with open(pkl_df_base, 'wb') as f:
            pickle.dump(df_base, f)

    print(df_base)
    print('elapsed', get_elapsed(time_start), 'sec')

    # Prediction
    time_start = time.time()
    pkl_result_pls = 'pool/result_pls.csv'
    if os.path.isfile(pkl_result_pls):
        df_result = pd.read_csv(pkl_result_pls, index_col=0)
    else:
        df_result = get_candidate_tickers(list_id_code_target, df_base)

    print(df_result)
    print('elapsed', get_elapsed(time_start), 'sec')


if __name__ == "__main__":
    main()
