import datetime as dt
import os
import pickle
import time

import pandas as pd
from sklearn.preprocessing import StandardScaler

from functions.get_dataset import (
    get_valid_list_id_code,
    get_target_list_id_code, get_basic_dataset,
)
from functions.get_elapsed import get_elapsed
from functions.prediction import search_minimal_component_number, minimal_scores


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
    columns_result = ['Components', 'R2 calib', 'R2 CV', 'MSE calib', 'MSE CV']
    df_result = pd.DataFrame(columns=columns_result)
    for id_code_target in list_id_code_target:
        name = '%d_open' % id_code_target
        series_y = df_base[name].iloc[1:]
        df_X = df_base.iloc[0:len(df_base) - 1, :]

        scaler = StandardScaler()
        scaler.fit(df_X)
        X = scaler.transform(df_X)
        y = series_y

        mse_min = search_minimal_component_number(X, y)

        n_comp = mse_min + 1
        result = minimal_scores(X, y, n_comp)
        series_target = pd.Series(
            data=[n_comp, result['R2 calib'], result['R2 CV'], result['MSE calib'], result['MSE CV']],
            index=columns_result,
            name=id_code_target
        )
        df_result.loc[id_code_target] = series_target
        # save result every time
        df_result.to_csv('pool/result_pls.csv')

    print(df_result)


if __name__ == "__main__":
    main()
