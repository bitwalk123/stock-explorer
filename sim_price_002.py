import datetime as dt
import os
import pickle

import pandas as pd
import time

from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dataset import combine_ticker_data
from functions.get_dict_code import get_dict_code
from functions.get_elapsed import get_elapsed
from functions.get_valid_code import get_valid_code
from functions.resources import get_connection

DAY1 = 24 * 60 * 60
TZ_DELTA = 9 * 60 * 60  # Asia/Tokyo timezone


def get_valid_dataset(start, end) -> tuple:
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # Get list of valid code and target
    pkl_list_valid_id_code = 'pool/list_valid_id_code_%d.pkl' % end
    pkl_list_target_id_code = 'pool/list_target_id_code_%d.pkl' % end
    if os.path.isfile(pkl_list_valid_id_code) and os.path.isfile(pkl_list_target_id_code):
        dict_code: dict = get_dict_code()
        with open(pkl_list_valid_id_code, 'rb') as f:
            list_valid_id_code = pickle.load(f)
        with open(pkl_list_target_id_code, 'rb') as f:
            list_target_id_code = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        dict_code, list_valid_id_code, list_target_id_code = get_valid_code(start, end)
        with open(pkl_list_valid_id_code, 'wb') as f:
            pickle.dump(list_valid_id_code, f)
        with open(pkl_list_target_id_code, 'wb') as f:
            pickle.dump(list_target_id_code, f)

    print('number of valid id_code : %d' % len(list_valid_id_code))
    print('number of target id_code : %d' % len(list_target_id_code))

    return dict_code, list_valid_id_code, list_target_id_code


def get_base_dataframe(list_valid_id_code, start, end) -> pd.DataFrame:
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # Get base dataframe
    pkl_df_base = 'pool/df_base_%d.pkl' % end
    if os.path.isfile(pkl_df_base):
        with open(pkl_df_base, 'rb') as f:
            df_base = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        df_base: pd.DataFrame = combine_ticker_data(list_valid_id_code, start, end)
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
        # Get list of valid code and target
        dict_code, list_valid_id_code, list_target_id_code = get_valid_dataset(start, end)
        # Generate base dataframe
        df_base = get_base_dataframe(list_valid_id_code, start, end)
        con.close()
        # Prediction for next Open price
        for target_id_code in list_target_id_code:
            name_open = '%d_open' % target_id_code
            df_base_2 = df_base.drop(name_open, axis=1)
            # Preparing Training & Test datasets
            df_X_train = df_base_2.iloc[0:len(df_base_2) - 1, :]
            df_X_test = df_base_2.tail(1)
            # Standardization
            scaler = StandardScaler()
            scaler.fit(df_X_train)
            X_train = scaler.transform(df_X_train)
            X_test = scaler.transform(df_X_test)
            # Pas data for Training
            y_train = df_base[name_open].iloc[1:]
            # PLS model
            n_comp = 20
            pls = PLSRegression(n_components=n_comp)
            pls.fit(X_train, y_train)
            # Prediction and Correlation score (R square)
            y_pred = pls.predict(X_train)
            r2 = r2_score(y_train, y_pred)
            # Predict Open price for tomorrow
            price_open_pred = pls.predict(X_test)[0]
            print(
                '%d.T: R2 = %.2f %%, Prediction = %.1f JPY' % (
                    dict_code[target_id_code], r2 * 100, price_open_pred
                )
            )
    else:
        print('fail to open db.')


if __name__ == "__main__":
    time_start = time.time()
    main()
    print('elapsed %.3f sec' % get_elapsed(time_start))
