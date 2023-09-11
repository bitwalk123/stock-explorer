import datetime as dt
import os
import pickle
import time

import pandas as pd
from PySide6.QtSql import QSqlQuery
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler

from database.sqls import get_sql_select_open_from_trade_with_id_code_date, \
    get_sql_select_min_date_from_trade_with_id_code_end
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dataset import (
    get_basic_dataset,
    get_valid_list_id_code,
    get_target_list_id_code, get_candidate_tickers,
)
from functions.get_dict_code import get_dict_code
from functions.get_elapsed import get_elapsed
from functions.resources import get_connection


def main():
    """Make ticker selection with specified condition
    """
    year = 365 * 24 * 60 * 60
    end_str = '2023-01-04'
    end_dt = dt.datetime.strptime(end_str, '%Y-%m-%d')
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    end = int(dt.datetime.timestamp(end_dt)) + tz_delta
    start = end - year
    print(conv_timestamp2date(start), conv_timestamp2date(end))

    n_best = 10  # This number of codes will be selected for prediction
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

    print('\nvalid total :', len(list_id_code))
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

    print('\ntarget total :', len(list_id_code_target))
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
    print('\nelapsed', get_elapsed(time_start), 'sec')

    # ticker selection and performance
    pkl_df_sel = 'pool/df_sel-%d.csv' % end
    df_sel = df_result.sort_values('R2 CV', ascending=False).iloc[0:n_best, :]
    with open(pkl_df_sel, 'wb') as f:
        pickle.dump(df_sel, f)
    print(df_sel)

    dict_code = dict()
    con = get_connection()
    if con.open():
        dict_code = get_dict_code()
    con.close()

    # Create empty table
    columns_summary = ['Code', 'Components', 'R2 CV', 'Date', 'Open(pred)', 'Open', 'delta']
    df_summary = pd.DataFrame(columns=columns_summary)

    for id_code in df_sel.index:
        code = dict_code[id_code]
        n_comp = int(df_sel.loc[id_code, 'Components'])
        r2_cv = df_sel.loc[id_code, 'R2 CV']

        # Open
        end_next = None
        price_open = None
        con = get_connection()
        if con.open():
            # Get next trade day
            sql1 = get_sql_select_min_date_from_trade_with_id_code_end(id_code, end)
            query1 = QSqlQuery(sql1)
            while query1.next():
                end_next = query1.value(0)
            # Get open price in next trade day
            sql2 = get_sql_select_open_from_trade_with_id_code_date(id_code, end_next)
            query2 = QSqlQuery(sql2)
            while query2.next():
                price_open = query2.value(0)
        con.close()

        # Prediction for end
        name_open = '%d_open' % id_code
        df_base_2 = df_base.drop(name_open, axis=1)
        # Preparing Training & Test datasets
        df_X_train = df_base_2.iloc[0:len(df_base_2) - 1, :]
        df_X_test = df_base_2.tail(1)

        scaler = StandardScaler()
        scaler.fit(df_X_train)
        X_train = scaler.transform(df_X_train)
        X_test = scaler.transform(df_X_test)

        y_train = df_base[name_open].iloc[1:]

        pls = PLSRegression(n_components=n_comp)
        pls.fit(X_train, y_train)
        price_open_pred = pls.predict(X_test)[0][0]

        # create 1 row in series
        series_id_code = pd.Series(
            data=[code, n_comp,
                  '{:.3f}'.format(r2_cv),
                  conv_timestamp2date(end_next),
                  '{:.1f}'.format(price_open_pred),
                  price_open,
                  '{:.1f}'.format(price_open_pred - price_open)],
            index=columns_summary,
            name=id_code
        )
        # add row
        df_summary.loc[id_code] = series_id_code

    print('\n### PREDICTION SUMMARY ###')
    print(df_summary)


if __name__ == "__main__":
    main()
